
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
    BROWSER_HEADERS
)
import json
from copy import deepcopy
from typing import Union
from pathlib import Path


# This is a TwitterAgent implementation base on twitter's web client api.
# 
# Starting from early 2023, twitter force its free tier developer api to be write-only.
# Thus, I need to replace TwitterAgent's backend with twitter's web client api.
# 
# checkout following articles for detail:
# https://developer.twitter.com/en/docs/twitter-api

@Singleton
class TwitterWebAgent(BaseAgent):
    
    def __init__(self,
        header_authorization:str, header_x_client_uuid:str, header_x_csrf_token:str,
        cookie_auth_token:str, cookie_ct0:str, endpoint_userbyscreenname:str,
        endpoint_usermedia:str, endpoint_tweetdetail:str,
        proxies:dict=None, delay_val:float=0.0
    ):
        '''
        To initialize this agent, you need to collect following stuff from your browser.
        
        From request header to twitter api:
            Authorization
            X-Client-Uuid
            X-Csrf-Token
        
        From cookies:
            auth_token
            ct0
        
        twitter api endpoints:
            Twitter's web client api endpoints are in this format:
            https://twitter.com/i/api/graphql/{UNIQUE_STR_ID}/{ENDPOINT_NAME}
            
            where {UNIQUE_STR_ID} is an unique str id for its dedicated {ENDPOINT_NAME}
            We need to use 3 endpoints in this agent: 'UserByScreenName', 'UserMedia', 'TweetDetail'
            So, you need to find their dedicate {UNIQUE_STR_ID} from your browser's dev tool.
            
            Usually, twitter web client will make a request to 'UserByScreenName' endpoint 
            when you visit an user's homepage. (e.g. https://twitter.com/elonmusk)
            
            And, it will make another request to 'UserMedia' endpoint when you visit a user's media page.
            (e.g. https://twitter.com/elonmusk/media)
            
            Finally, it will make a request to 'TweetDetail' endpoint when you visit a tweet.
            (e.g. https://twitter.com/elonmusk/status/1688485935816581120)
            
            For example, if you found following request when visiting a twitter user's homepage:
            https://twitter.com/i/api/graphql/abcdefg123456-/UserByScreenName?....
            
            you found your unique str id for UserByScreenName: 'abcdefg123456-'
            
            fill-in your unique str id for following parameters:
                endpoint_userbyscreenname
                endpoint_usermedia
                endpoint_tweetdetail
        '''
        
        self.__delay_val = None if delay_val is None or delay_val <= 0.0 else (0.0, Clamp(0.0, delay_val))
        self.__headers = {
            **BROWSER_HEADERS,
            'X-Twitter-Active-User': 'yes',
            'X-Twitter-Auth-Type': 'OAuth2Session',
            'X-Twitter-Client-Language': 'en',
            'Sec-Ch-Ua-Mobile': '?0',
            'Sec-Ch-Ua-Platform': '"Windows"',
            'Referer': 'https://twitter.com/',
            
            # differ for different user, must have
            'Authorization': header_authorization,
            'X-Client-Uuid': header_x_client_uuid,
            'X-Csrf-Token': header_x_csrf_token,
        }
        self.__cookies = {
            # must have
            'auth_token': cookie_auth_token,
            'ct0': cookie_ct0,
        }
        self.__proxies = proxies
        self.__http = HTTPClient(
            default_headers=self.__headers,
            default_cookies=self.__cookies,
            default_proxies=self.__proxies,
            delay_value=self.__delay_val
        )
        self.__api_base_url = 'https://twitter.com/i/api/graphql/'
        self.__endpoints = {
            'UserByScreenName': endpoint_userbyscreenname,
            'UserMedia': endpoint_usermedia,
            'TweetDetail': endpoint_tweetdetail,
        }
        self.__request_params = {
            'features': {
            'rweb_tipjar_consumption_enabled': True,
            'hidden_profile_likes_enabled': False,
            'responsive_web_graphql_exclude_directive_enabled': True,
            'verified_phone_label_enabled': False,
            'subscriptions_verification_info_verified_since_enabled': True,
            'highlights_tweets_tab_ui_enabled': True,
            'creator_subscriptions_tweet_preview_api_enabled': True,
            'responsive_web_graphql_skip_user_profile_image_extensions_enabled': False,
            'responsive_web_graphql_timeline_navigation_enabled': True,
            'rweb_lists_timeline_redesign_enabled': True,
            'tweetypie_unmention_optimization_enabled': True,
            'responsive_web_edit_tweet_api_enabled': True,
            'graphql_is_translatable_rweb_tweet_is_translatable_enabled': True,
            'view_counts_everywhere_api_enabled': True,
            'longform_notetweets_consumption_enabled': True,
            'tweet_awards_web_tipping_enabled': False,
            'freedom_of_speech_not_reach_fetch_enabled': True,
            'standardized_nudges_misinfo': True,
            'tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled': True,
            'longform_notetweets_rich_text_read_enabled': True,
            'longform_notetweets_inline_media_enabled': True,
            'responsive_web_enhance_cards_enabled': False,
            'articles_preview_enabled':True,
            'responsive_web_twitter_article_tweet_consumption_enabled':True,
            'communities_web_enable_tweet_community_results_fetch':True,
            'creator_subscriptions_quote_tweet_preview_enabled':True,
            'c9s_tweet_anatomy_moderator_badge_enabled':True,
            'rweb_video_timestamps_enabled':True,
            },
            'variables': {
            "includePromotedContent":True,
            "withQuickPromoteEligibilityTweetFields":True,
            "withVoice":True,
            "withV2Timeline":True
            }
        }
    
    
    # interfaces
    def SetProxies(self, proxies:dict):
        self.__proxies = proxies
        self.__http.SetProxies(self.__proxies)
    
    
    @TypeChecker(TwitterItemInfo, (1,))
    def FetchItemInfoDetail(self, item_info:TwitterItemInfo) -> TwitterItemInfo:
        '''
        Fetch & Fill-In "detail" parameter for supplied TwitterItemInfo.
        Param:
            item_info  => TwitterItemInfo to fetch
        Returns:
            updated TwitterItemInfo
        '''
        
        url = None
        params = None
        get_legacy = None
        if item_info.IsParent():
            url = self.__GenApiUrl('UserByScreenName')
            params = self.__GenParams(
                features={
                    'subscriptions_verification_info_is_identity_verified_enabled':True,
                    'subscriptions_feature_can_gift_premium':True,
                    'responsive_web_twitter_article_notes_tab_enabled':True,
                    'hidden_profile_subscriptions_enabled':True,
                },
                variables={'screen_name': item_info.screen_name},
            )
            def func(detail):
                return {
                    'id_str': detail['data']['user']['result']['rest_id'],
                    'id': int(detail['data']['user']['result']['rest_id']),
                    **detail['data']['user']['result']['legacy']
                }
            get_legacy = func
        elif item_info.IsChild():
            url = self.__GenApiUrl('TweetDetail')
            params = self.__GenParams(variables={
                "focalTweetId": str(item_info.status_id),
                "referrer":"profile",
                "with_rux_injections":False,
                "withCommunity":True,
                "withBirdwatchNotes":True
            })
            def func(detail):
                for entry in detail['data']['threaded_conversation_with_injections_v2']['instructions'][0]['entries']:
                    if (entry['content']['entryType'] == 'TimelineTimelineItem' and
                        entry['content']['itemContent']['itemType'] == 'TimelineTweet'):
                        return {
                            'user': {
                                ** entry['content']['itemContent']['tweet_results']['result']['core']['user_results']['result']['legacy'],
                                'id_str': entry['content']['itemContent']['tweet_results']['result']['core']['user_results']['result']['rest_id']
                            },
                            **entry['content']['itemContent']['tweet_results']['result']['legacy']
                        }
                return None
            get_legacy = func
        else:
            raise BadWebItemInfoException(item_info.__name__)
        
        try:
            res = self.__http.GetJson(url, params=params)
        except Exception as err:
            raise err
        
        item_info.details = get_legacy(res)
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
        
        if item_info.details is None:
            item_info = self.FetchItemInfoDetail(item_info)
        
        
        userid = item_info.details['id_str']
        page = Clamp(page, 1)
        url = self.__GenApiUrl('UserMedia')
        next_cursor = None
        output = []
        
        # while count > 0:
        for _ in range(page):
            # get request
            count = 30
            res = None
            try:
                params = self.__GenParams(variables={
                    'userId':userid,
                    'count':count,
                    'cursor':next_cursor,
                })
                res = self.__http.GetJson(url, params=params)
            except Exception as err:
                raise err
            
            # extract useful info & find next cursor
            entries = [i for i in res['data']['user']['result']['timeline_v2']['timeline']['instructions'] if i['type'] == 'TimelineAddEntries'][0]
            for status in entries['entries']:
                entryType = status['content']['entryType']
                if entryType == 'TimelineTimelineModule':
                    user = status['content']['items'][0]['item']['itemContent']['tweet_results']['result']['core']['user_results']['result']['legacy']
                    for item in status['content']['items']:
                        if 'legacy' not in item['item']['itemContent']['tweet_results']['result']['__typename'] == 'Tweet':
                            output.append(TwitterItemInfo.FromChildDetails({
                                'user': user,
                                **item['item']['itemContent']['tweet_results']['result']['legacy']
                            }))
                elif entryType == 'TimelineTimelineCursor' and status['content']['cursorType'] == 'Bottom':
                    next_cursor = status['content']['value']
        
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
        url_dict = {domain:[f'https://twitter.com/{user["screen_name"]}']}
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
            if t['id_str'] not in medias:
                medias.update({t['id_str']:t})
        
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
        if item_info.IsParent():
            is_followed = ('following' in item_info.details and item_info.details['following'])
        elif item_info.IsChild():
            is_followed = ('following' in item_info.details['user'] and item_info.details['user']['following'])
        
        return is_followed
    
    
    # private helper functions
    def __GenApiUrl(self, endpoint) -> str:
        if endpoint not in self.__endpoints:
            raise ValueError(f'Invalid endpoint name: {endpoint}')
        val = self.__endpoints[endpoint]
        return f'{self.__api_base_url}{val}/{endpoint}'
    
    def __GenParams(self, features:dict=dict(), variables:dict=dict()) -> dict:
        loc_fea = deepcopy(self.__request_params['features'])
        loc_fea.update(features)
        loc_var = deepcopy(self.__request_params['variables'])
        loc_var.update(variables)
        return {
            'features': json.dumps(loc_fea),
            'variables': json.dumps(loc_var)
        }
    

