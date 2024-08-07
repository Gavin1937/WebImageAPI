
from .BaseAgent import BaseAgent
from .Singleton import Singleton
from ..Types import TwitterItemInfo, UserInfo, DOMAIN
from ..Types.Exceptions import (
    WrongParentChildException,
    BadWebItemInfoException
)
from ..Utils import (
    TypeChecker, TypeMatcher,
    Clamp, MergeDeDuplicate,
    UrlParser, HTTPClient,
    IsValidProxies
)
from tweepy import OAuth1UserHandler, API, Client, Cursor
from tweepy.errors import TweepyException, Unauthorized
from time import sleep
from typing import Union
from pathlib import Path


# This is a TwitterAgent implementation base on twitter's developer api.
# 
# Starting from early 2023, twitter force its free tier developer api to be write-only.
# Thus, I need to replace TwitterAgent's backend with twitter's web client api.
# 
# checkout following articles for detail:
# https://developer.twitter.com/en/docs/twitter-api

@Singleton
class TwitterAgent(BaseAgent):
    
    def __init__(self, consumer_key:str, consumer_secret:str, access_token:str, access_token_secret:str, bearer_token:str, proxies:dict=None, max_try:int=5):
        auth = OAuth1UserHandler(
            consumer_key, consumer_secret, access_token, access_token_secret
        )
        
        self.__proxies = proxies if IsValidProxies(proxies) else {}
        self.__http = HTTPClient(default_proxies=self.__proxies)
        self.__consumer_key = consumer_key
        self.__consumer_secret = consumer_secret
        self.__access_token = access_token
        self.__access_token_secret = access_token_secret
        self.__bearer_token = bearer_token
        self.__max_try = max_try
        
        exception = None
        sleeptime = 10
        for count in range(max_try):
            try:
                self.__api:API = API(auth, proxy=self.__proxies)
                break
            except TweepyException or Unauthorized as err:
                exception = err
                print(f'TweepyException or Unauthorized: {err}')
                wakeup_in = sleeptime * (count+1)
                print(f'[{count+1}/{self.__max_try}] Sleep for {wakeup_in} sec before retry')
                sleep(wakeup_in)
        else:
            raise exception
    
    
    # interfaces
    def GetAPI(self) -> API:
        'Get tweepy.API object'
        return self.__api
    
    def SetProxies(self, proxies:dict):
        if IsValidProxies(proxies):
            auth = OAuth1UserHandler(
                self.__consumer_key, self.__consumer_secret, self.__access_token, self.__access_token_secret
            )
            
            self.__proxies = proxies
            exception = None
            sleeptime = 10
            for count in range(self.__max_try):
                try:
                    self.__api:API = API(auth, proxy=self.__proxies)
                    break
                except TweepyException or Unauthorized as err:
                    exception = err
                    print(f'TweepyException or Unauthorized: {err}')
                    wakeup_in = sleeptime * (count+1)
                    print(f'[{count+1}/{self.__max_try}] Sleep for {wakeup_in} sec before retry')
                    sleep(wakeup_in)
            else:
                raise exception
        self.__http = HTTPClient(default_proxies=self.__proxies)
    
    
    @TypeChecker(TwitterItemInfo, (1,))
    def FetchItemInfoDetail(self, item_info:TwitterItemInfo) -> TwitterItemInfo:
        '''
        Fetch & Fill-In "detail" parameter for supplied TwitterItemInfo.
        Param:
            item_info  => TwitterItemInfo to fetch
        Returns:
            updated TwitterItemInfo
        '''
        
        if item_info.IsParent():
            item_info.details = self.__api.get_user(screen_name=item_info.screen_name)._json
        elif item_info.IsChild():
            item_info.details = self.__api.get_status(item_info.status_id, include_entities=True, tweet_mode='extended')._json
        else:
            raise BadWebItemInfoException(item_info.__name__)
        
        return item_info
    
    
    @TypeMatcher(['self', TwitterItemInfo, int])
    def FetchParentChildren(self, item_info:TwitterItemInfo, page:int=1) -> list:
        '''
        Fetch a Parent TwitterItemInfo\'s Children
        Param:
            item_info  => TwitterItemInfo Parent to fetch
            page       => int page number >= 1
        Returns:
            list of TwitterItemInfo fetched, also edit original "item_info"
        '''
        
        if not item_info.IsParent():
            raise WrongParentChildException(item_info.parent_child, 'Input TwitterItemInfo must be a parent.')
        
        page = Clamp(page, 1)
        
        details = []
        output = []
        cursor = Cursor(
            self.__api.user_timeline,
            screen_name=item_info.screen_name,
            tweet_mode='extended',
            exclude_replies=True,
            include_rts=False,
            count=30,
        ).page(page)
        for page in cursor:
            for status in page:
                details.append(status._json)
                output.append(TwitterItemInfo.FromChildDetails(status._json))
        item_info.details = details
        
        return output
    
    @TypeChecker(TwitterItemInfo, (1,))
    def FetchUserInfo(self, item_info:TwitterItemInfo, old_user_info:UserInfo=None) -> UserInfo:
        '''
        Fetch a TwitterItemInfo\'s UserInfo
        Param:
            item_info        => TwitterItemInfo Parent to fetch
            old_user_info    => UserInfo that already fill up by other agents,
                                this function will collect additional UserInfo from current domain,
                                and append to old_user_info and return it at the end.
                                (default None)
        Returns:
            UserInfo object
        '''
        
        if item_info.details is None:
            item_info = self.FetchItemInfoDetail(item_info)
        
        domain = DOMAIN.TWITTER
        if item_info.IsParent():
            user = item_info.details
        if item_info.IsChild():
            user = item_info.details['user']
        
        name_list = [user['name']]
        url_dict = {domain:[f'https://x.com/{user["screen_name"]}']}
        if old_user_info is not None:
            old_user_info.name_list = MergeDeDuplicate(old_user_info.name_list, name_list)
            if domain in old_user_info.url_dict:
                old_user_info.url_dict[domain] += url_dict[domain]
            else:
                old_user_info.url_dict[domain] = url_dict[domain]
            old_user_info.url_dict[domain] = MergeDeDuplicate(old_user_info.url_dict[domain])
            old_user_info.details[domain] = user
            return old_user_info
        name_list = MergeDeDuplicate(name_list)
        return UserInfo(name_list, url_dict, {domain:user})
    
    @TypeChecker(TwitterItemInfo, (1,))
    def DownloadItem(self, item_info:TwitterItemInfo, output_path:Union[str,Path], replace:bool=False):
        '''
        Download a supplied TwitterItemInfo
        Param:
            item_info    => TwitterItemInfo Child to download
            output_path  => str|Path of a directory for downloaded file
            replace      => bool flag, whether replace if download file already exists
        '''
        
        if not item_info.IsChild():
            raise WrongParentChildException(item_info.parent_child, 'Cannot download non-child TwitterItemInfo.')
        
        output_path = Path(output_path)
        if not output_path.is_dir():
            raise ValueError('Output path should be a directory path.')
        
        if item_info.details is None:
            item_info = self.FetchItemInfoDetail(item_info)
        
        medias = dict()
        tmp = []
        tmp += item_info.details['entities']['media']
        tmp += item_info.details['extended_entities']['media']
        for t in tmp:
            if t['id'] not in medias:
                medias.update({t['id']:t})
        
        for _,media in medias.items():
            parsed = UrlParser(media['media_url_https'])
            imgid,ext = parsed.pathlist[-1].split('.')
            if ext == 'jfif':
                ext = 'jpg'
            filename = f'{imgid}.{ext}'
            url = f'https://pbs.twimg.com/media/{imgid}?format={ext}&name=orig'
            self.__http.DownloadUrl(url, output_path/filename, overwrite=replace)
    
    
    # other twitter features
    
    @TypeChecker(TwitterItemInfo, (1,))
    def GetParentItemInfo(self, item_info:TwitterItemInfo) -> TwitterItemInfo:
        '''
        Get the parent TwitterItemInfo for a child TwitterItemInfo.
        Param:
            item_info    => TwitterItemInfo Child
        Returns:
            A parent TwitterItemInfo
        '''
        
        if item_info.IsParent():
            return item_info
        elif item_info.IsChild():
            user_info = self.FetchUserInfo(item_info)
            parent_url = user_info.url_dict[DOMAIN.TWITTER][0]
            return TwitterItemInfo(parent_url)
    
    @TypeChecker(TwitterItemInfo, (1,))
    def IsFollowedUser(self, item_info:TwitterItemInfo) -> bool:
        '''
        Is input TwitterItemInfo points to an user that is followed by current account.
        Param:
            item_info    => TwitterItemInfo to check
        Returns:
            True if is followed
            False if not
        '''
        
        if item_info.details is None:
            item_info = self.FetchItemInfoDetail(item_info)
        
        is_followed = False
        if not item_info.IsParent():
            is_followed = item_info.details['following']
        if not item_info.IsChild():
            is_followed = item_info.details['user']['following']
        
        return is_followed
    
    @TypeChecker(TwitterItemInfo, (1,))
    def FollowUser(self, item_info:TwitterItemInfo) -> bool:
        '''
        Follow an user that item_info points to.
        The proxy setting does not apply to this function.
        Param:
            item_info    => TwitterItemInfo Parent to check
        Returns:
            True if success
            False if failed
        '''
        
        if not item_info.IsParent():
            raise WrongParentChildException(item_info.parent_child, 'Input TwitterItemInfo must be a parent.')
        
        if self.__client is None:
            self.__client:Client = Client(
                consumer_key=self.__consumer_key, consumer_secret=self.__consumer_secret,
                access_token=self.__access_token, access_token_secret=self.__access_token_secret,
                bearer_token=self.__bearer_token,
            )
        
        if item_info.details is None:
            item_info = self.FetchItemInfoDetail(item_info)
        
        self.__client.follow_user(item_info.details['id'])
    
    @TypeChecker(TwitterItemInfo, (1,))
    def UnfollowUser(self, item_info:TwitterItemInfo) -> bool:
        '''
        Unfollow an user that item_info points to.
        The proxy setting does not apply to this function.
        Param:
            item_info    => TwitterItemInfo Parent to check
        Returns:
            True if success
            False if failed
        '''
        
        if not item_info.IsParent():
            raise WrongParentChildException(item_info.parent_child, 'Input TwitterItemInfo must be a parent.')
        
        if self.__client is None:
            self.__client:Client = Client(
                consumer_key=self.__consumer_key, consumer_secret=self.__consumer_secret,
                access_token=self.__access_token, access_token_secret=self.__access_token_secret,
                bearer_token=self.__bearer_token,
            )
        
        if item_info.details is None:
            item_info = self.FetchItemInfoDetail(item_info)
        
        self.__client.unfollow_user(item_info.details['id'])
    

