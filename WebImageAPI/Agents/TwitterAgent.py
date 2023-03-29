
from .BaseAgent import BaseAgent
from .Singleton import Singleton
from ..Types import TwitterItemInfo
from ..Utils import TypeChecker, TypeMatcher, Clamp, UrlParser, downloadFile
from tweepy import OAuth1UserHandler, API, Cursor
from tweepy.errors import TweepyException
from time import sleep
from typing import Union
from pathlib import Path


@Singleton
class TwitterAgent(BaseAgent):
    
    def __init__(self, consumer_key:str, consumer_secret:str, access_token:str, access_token_secret:str, max_try:int=5):
        auth = OAuth1UserHandler(
            consumer_key, consumer_secret, access_token, access_token_secret
        )
        
        exception = None
        sleeptime = 10
        for count in range(max_try):
            try:
                self.__api:API = API(auth)
                break
            except TweepyException as err:
                exception = err
                sleep(sleeptime)
        else:
            raise exception
    
    
    # interfaces
    def GetAPI(self) -> API:
        return self.__api
    
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
            raise ValueError('Input TwitterItemInfo is empty or invalid.')
        
        return item_info
    
    
    @TypeMatcher(['self', TwitterItemInfo, int])
    def FetchParentChildren(self, item_info:TwitterItemInfo, count:int=30) -> list:
        '''
        Fetch a Parent TwitterItemInfo\' Children
        Param:
            item_info  => TwitterItemInfo Parent to fetch
            count      => int count number >= 1
        Returns:
            list of TwitterItemInfo fetched, also edit original "item_info"
        '''
        
        if not item_info.IsParent():
            raise ValueError('Input TwitterItemInfo must be a parent.')
        
        count = Clamp(count, 1)
        
        details = []
        output = []
        cursor = Cursor(
            self.__api.user_timeline,
            screen_name=item_info.screen_name,
            tweet_mode='extended',
            exclude_replies=True,
            include_rts=False,
            count=count,
        ).items(count)
        for status in cursor:
            details.append(status._json)
            output.append(TwitterItemInfo.FromChildDetails(status._json))
        item_info.details = details
        
        return output
    
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
            raise ValueError('Cannot download non-child TwitterItemInfo.')
        
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
            filename = parsed.pathlist[-1]
            url = f'https://pbs.twimg.com/media/{imgid}?format={ext}&name=orig'
            downloadFile(url, output_path/filename, overwrite=replace)
    

