
from .Agents import *
from .Types import *
from .Utils import TypeChecker
from typing import Union
from pathlib import Path


class WebImageAPI:
    'Handles all Agents & WebItemInfo in one place'
    
    def __init__(self):
        self.__pixiv_agent:PixivAgent             = None
        self.__twitter_agent:TwitterAgent         = None
        self.__twitter_web_agent:TwitterWebAgent  = None
        self.__danbooru_agent:DanbooruAgent       = None
        self.__yandere_agent:YandereAgent         = None
        self.__konachan_agent:KonachanAgent       = None
        self.__weibo_agent:WeiboAgent             = None
        self.__ehentai_agent:EHentaiAgent         = None
    
    
    # interfaces
    
    # agent setup 
    def SetPixivTokens(self, refresh_token:str):
        self.__InitAgent(DOMAIN.PIXIV, refresh_token=refresh_token)
    
    def SetTwitterTokens(
        self, agent_type:str,
        
        # agent_type == 'web'
        header_authorization:str=None,
        header_x_csrf_token:str=None, cookie_auth_token:str=None,
        cookie_ct0:str=None, endpoint_userbyscreenname:str=None,
        endpoint_usermedia:str=None, endpoint_tweetdetail:str=None,
        
        # agent_type == 'dev'
        consumer_key:str=None, consumer_secret:str=None,
        access_token:str=None, access_token_secret:str=None,
        bearer_token:str=None,
    ):
        '''
        Setup TwitterAgent & TwitterWebAgent
        Param:
            agent_type   => str, indicating which type of twitter agent to use.
                            Can be: 'web', 'dev', 'both'
            if agent_type == 'web', initialize a TwitterWebAgent.
            Requires Param:
                header_authorization        => str, Authorization in request header
                header_x_csrf_token         => str, X-Csrf-Token in request header
                cookie_auth_token           => str, auth_token in cookie
                cookie_ct0                  => str, ct0 in cookie
                endpoint_userbyscreenname   => str, unique id for UserByScreenName endpoint
                endpoint_usermedia          => str, unique id for UserMedia endpoint
                endpoint_tweetdetail        => str, unique id for TweetDetail endpoint
            if agent_type == 'dev', initialize a TwitterAgent.
            Requires Param:
                consumer_key                => str, consumer_key of your twitter app
                consumer_secret             => str, consumer_secret of your twitter app
                access_token                => str, access_token of your twitter app
                access_token_secret         => str, access_token_secret of your twitter app
                bearer_token                => str, bearer_token of your twitter app
            if agent_type == 'both', initialize both TwitterWebAgent and TwitterAgent.
            Require all the parameters listed above.
        WebImageAPI will prioritize TwitterWebAgent if possible.
        checkout TwitterWebAgent for detail.
        '''
        
        if agent_type == 'web':
            check = self.__CheckArgs(
                [
                'header_authorization',
                'header_x_csrf_token', 'cookie_auth_token',
                'cookie_ct0', 'endpoint_userbyscreenname',
                'endpoint_usermedia', 'endpoint_tweetdetail'
                ],
                header_authorization=header_authorization,
                header_x_csrf_token=header_x_csrf_token, cookie_auth_token=cookie_auth_token,
                cookie_ct0=cookie_ct0, endpoint_userbyscreenname=endpoint_userbyscreenname,
                endpoint_usermedia=endpoint_usermedia, endpoint_tweetdetail=endpoint_tweetdetail
            )
            if not check:
                raise ValueError('Missing required parameters.')
            self.__InitAgent(
                DOMAIN.TWITTER, special_arg='web',
                header_authorization=header_authorization,
                header_x_csrf_token=header_x_csrf_token, cookie_auth_token=cookie_auth_token,
                cookie_ct0=cookie_ct0, endpoint_userbyscreenname=endpoint_userbyscreenname,
                endpoint_usermedia=endpoint_usermedia, endpoint_tweetdetail=endpoint_tweetdetail
            )
        elif agent_type == 'dev':
            check = self.__CheckArgs(
                [
                'consumer_key', 'consumer_secret',
                'access_token', 'access_token_secret',
                'bearer_token'
                ],
                consumer_key=consumer_key, consumer_secret=consumer_secret,
                access_token=access_token, access_token_secret=access_token_secret,
                bearer_token=bearer_token
            )
            if not check:
                raise ValueError('Missing required parameters.')
            self.__InitAgent(
                DOMAIN.TWITTER, special_arg='dev',
                consumer_key=consumer_key, consumer_secret=consumer_secret,
                access_token=access_token, access_token_secret=access_token_secret,
                bearer_token=bearer_token
            )
        elif agent_type == 'both':
            check = self.__CheckArgs(
                [
                'header_authorization',
                'header_x_csrf_token', 'cookie_auth_token',
                'cookie_ct0', 'endpoint_userbyscreenname',
                'endpoint_usermedia', 'endpoint_tweetdetail',
                'consumer_key', 'consumer_secret',
                'access_token', 'access_token_secret',
                'bearer_token'
                ],
                header_authorization=header_authorization,
                header_x_csrf_token=header_x_csrf_token, cookie_auth_token=cookie_auth_token,
                cookie_ct0=cookie_ct0, endpoint_userbyscreenname=endpoint_userbyscreenname,
                endpoint_usermedia=endpoint_usermedia, endpoint_tweetdetail=endpoint_tweetdetail,
                consumer_key=consumer_key, consumer_secret=consumer_secret,
                access_token=access_token, access_token_secret=access_token_secret,
                bearer_token=bearer_token
            )
            if not check:
                raise ValueError('Missing required parameters.')
            self.__InitAgent(
                DOMAIN.TWITTER, special_arg='web',
                header_authorization=header_authorization,
                header_x_csrf_token=header_x_csrf_token, cookie_auth_token=cookie_auth_token,
                cookie_ct0=cookie_ct0, endpoint_userbyscreenname=endpoint_userbyscreenname,
                endpoint_usermedia=endpoint_usermedia, endpoint_tweetdetail=endpoint_tweetdetail
            )
            self.__InitAgent(
                DOMAIN.TWITTER, special_arg='dev',
                consumer_key=consumer_key, consumer_secret=consumer_secret,
                access_token=access_token, access_token_secret=access_token_secret,
                bearer_token=bearer_token
            )
    
    def SetEHentaiAuthInfo(self, ipb_member_id:str, ipb_pass_hash:str):
        if self.__ehentai_agent is None:
            self.__InitAgent(DOMAIN.EHENTAI, ipb_member_id=ipb_member_id, ipb_pass_hash=ipb_pass_hash)
            return
        self.__ehentai_agent.SetEHentaiAuthInfo(ipb_member_id, ipb_pass_hash)
    
    def GetEHentaiIgnorePeekHour(self) -> bool:
        if self.__ehentai_agent is None:
            self.__InitAgent(DOMAIN.EHENTAI)
        return self.__ehentai_agent.GetIgnorePeekHour()
    
    def SetEHentaiIgnorePeekHour(self, whether_ignore:bool) -> None:
        if self.__ehentai_agent is None:
            self.__InitAgent(DOMAIN.EHENTAI, ignore_peek_hour=whether_ignore)
        else:
            self.__ehentai_agent.SetIgnorePeekHour(whether_ignore)
    
    def GetEHentaiNextPeekHour(self) -> tuple:
        '''
        Get next peek hour information from EHentaiAgent
        Returns:
            tuple( whether in peek hour : bool, peek hour : datetime )
            If currently in peek hour, tuple( True, datetime obj of the end of current peek hour )
            If currently not in peek hour, tuple( False, datetime obj of the start of next peek hour )
        '''
        if self.__ehentai_agent is None:
            self.__InitAgent(DOMAIN.EHENTAI)
        return self.__ehentai_agent.GetNextPeekHour()
    
    
    # agent getters
    def GetPixivAgent(self) -> PixivAgent:
        if self.__pixiv_agent is None:
            raise ValueError('Please initialize PixivAgent through WebImageAPI.SetPixivTokens() first.')
        return self.__pixiv_agent
    
    def GetTwitterAgent(self, which_one:str='web') -> Union[TwitterAgent,TwitterWebAgent]:
        '''
        Get exiting, initialized TwitterAgent or TwitterWebAgent
        Param:
            which_one    => str, if set to 'web', return TwitterWebAgent.
                            If set to 'dev', return TwitterAgent.
                            Default 'web'
        '''
        if which_one not in ['web', 'dev']:
            raise ValueError('Invalid "which_one" value, it must be either "web" or "dev".')
        if which_one == 'web' and self.__twitter_web_agent is not None:
            return self.__twitter_web_agent
        elif which_one == 'dev' and self.__twitter_agent is not None:
            return self.__twitter_agent
        else:
            raise ValueError('Please initialize TwitterAgent through WebImageAPI.SetTwitterTokens() first.')
    
    def GetDanbooruAgent(self) -> DanbooruAgent:
        if self.__danbooru_agent is None:
            self.__InitAgent(DOMAIN.DANBOORU)
        return self.__danbooru_agent
    
    def GetYandereAgent(self) -> YandereAgent:
        if self.__yandere_agent is None:
            self.__InitAgent(DOMAIN.YANDERE)
        return self.__yandere_agent
    
    def GetKonachanAgent(self) -> KonachanAgent:
        if self.__konachan_agent is None:
            self.__InitAgent(DOMAIN.KONACHAN)
        return self.__konachan_agent
    
    def GetWeiboAgent(self) -> WeiboAgent:
        if self.__weibo_agent is None:
            self.__InitAgent(DOMAIN.WEIBO)
        return self.__weibo_agent
    
    def GetEHentaiAgent(self) -> EHentaiAgent:
        if self.__ehentai_agent is None:
            self.__InitAgent(DOMAIN.EHENTAI)
        return self.__ehentai_agent
    
    
    # agent common features
    def FetchItemInfoDetail(self, item_info:WebItemInfo) -> WebItemInfo:
        '''
        Fetch & Fill-In "detail" parameter for supplied WebItemInfo.
        Param:
            item_info  => WebItemInfo to fetch
        Returns:
            updated WebItemInfo
        '''
        
        if isinstance(item_info, PixivItemInfo):
            return self.GetPixivAgent().FetchItemInfoDetail(item_info)
        elif isinstance(item_info, TwitterItemInfo):
            return self.GetTwitterAgent().FetchItemInfoDetail(item_info)
        elif isinstance(item_info, DanbooruItemInfo):
            return self.GetDanbooruAgent().FetchItemInfoDetail(item_info)
        elif isinstance(item_info, YandereItemInfo):
            return self.GetYandereAgent().FetchItemInfoDetail(item_info)
        elif isinstance(item_info, KonachanItemInfo):
            return self.GetKonachanAgent().FetchItemInfoDetail(item_info)
        elif isinstance(item_info, WeiboItemInfo):
            return self.GetWeiboAgent().FetchItemInfoDetail(item_info)
        elif isinstance(item_info, EHentaiItemInfo):
            return self.GetEHentaiAgent().FetchItemInfoDetail(item_info)
        else:
            raise ValueError('Empty or Invalid WebItemInfo.')
    
    def FetchParentChildren(self, item_info:WebItemInfo, page:int=1) -> list:
        '''
        Fetch a Parent WebItemInfo\'s Children
        Param:
            item_info  => WebItemInfo Parent to fetch
            page       => int page number >= 1
        Returns:
            list of WebItemInfo fetched, also edit original "item_info"
        '''
        
        if isinstance(item_info, PixivItemInfo):
            return self.GetPixivAgent().FetchParentChildren(item_info, page)
        elif isinstance(item_info, TwitterItemInfo):
            return self.GetTwitterAgent().FetchParentChildren(item_info, page)
        elif isinstance(item_info, DanbooruItemInfo):
            return self.GetDanbooruAgent().FetchParentChildren(item_info, page)
        elif isinstance(item_info, YandereItemInfo):
            return self.GetYandereAgent().FetchParentChildren(item_info, page)
        elif isinstance(item_info, KonachanItemInfo):
            return self.GetKonachanAgent().FetchParentChildren(item_info, page)
        elif isinstance(item_info, WeiboItemInfo):
            return self.GetWeiboAgent().FetchParentChildren(item_info, page)
        elif isinstance(item_info, EHentaiItemInfo):
            return self.GetEHentaiAgent().FetchParentChildren(item_info, page)
        else:
            raise ValueError('Empty or Invalid WebItemInfo.')
    
    def FetchUserInfo(self, item_info:WebItemInfo, old_user_info:UserInfo=None) -> UserInfo:
        '''
        Fetch a WebItemInfo\'s UserInfo
        Param:
            item_info        => WebItemInfo Parent to fetch
            old_user_info    => UserInfo that already fill up by other agents,
                                this function will collect additional UserInfo from current domain,
                                and append to old_user_info and return it at the end.
                                (default None)
        Returns:
            UserInfo object
        '''
        
        if isinstance(item_info, PixivItemInfo):
            return self.GetPixivAgent().FetchUserInfo(item_info, old_user_info)
        elif isinstance(item_info, TwitterItemInfo):
            return self.GetTwitterAgent().FetchUserInfo(item_info, old_user_info)
        elif isinstance(item_info, DanbooruItemInfo):
            return self.GetDanbooruAgent().FetchUserInfo(item_info, old_user_info)
        elif isinstance(item_info, YandereItemInfo):
            return self.GetYandereAgent().FetchUserInfo(item_info, old_user_info)
        elif isinstance(item_info, KonachanItemInfo):
            return self.GetKonachanAgent().FetchUserInfo(item_info, old_user_info)
        elif isinstance(item_info, WeiboItemInfo):
            return self.GetWeiboAgent().FetchUserInfo(item_info, old_user_info)
        elif isinstance(item_info, EHentaiItemInfo):
            return self.GetEHentaiAgent().FetchUserInfo(item_info, old_user_info)
        else:
            raise ValueError('Empty or Invalid WebItemInfo.')
    
    def DownloadItem(self, item_info:WebItemInfo, output_path:Union[str,Path], replace:bool=False):
        '''
        Download a supplied WebItemInfo
        Param:
            item_info    => WebItemInfo Child to download
            output_path  => str|Path of a directory for downloaded file
            replace      => bool flag, whether replace if download file already exists
        '''
        
        if isinstance(item_info, PixivItemInfo):
            return self.GetPixivAgent().DownloadItem(item_info, output_path, replace)
        elif isinstance(item_info, TwitterItemInfo):
            return self.GetTwitterAgent().DownloadItem(item_info, output_path, replace)
        elif isinstance(item_info, DanbooruItemInfo):
            return self.GetDanbooruAgent().DownloadItem(item_info, output_path, replace)
        elif isinstance(item_info, YandereItemInfo):
            return self.GetYandereAgent().DownloadItem(item_info, output_path, replace)
        elif isinstance(item_info, KonachanItemInfo):
            return self.GetKonachanAgent().DownloadItem(item_info, output_path, replace)
        elif isinstance(item_info, WeiboItemInfo):
            return self.GetWeiboAgent().DownloadItem(item_info, output_path, replace)
        elif isinstance(item_info, EHentaiItemInfo):
            return self.GetEHentaiAgent().DownloadItem(item_info, output_path, replace)
        else:
            raise ValueError('Empty or Invalid WebItemInfo.')
    
    def FindSource(self, item_info:WebItemInfo, absolute:bool=False) -> Union[WebItemInfo,str]:
        '''
        Find the source of a Child WebItemInfo.
        Param:
            item_info    => WebItemInfo Child
            absolute     => bool flag
                            if True, return str url when find a not support url.
                            if False, return None in above case
        Returns:
            a valid WebItemInfo if find one source
            if find one source but not valid, return str or item_info base on "absolute"
            if not find any source, return None
        '''
        
        src = None
        if isinstance(item_info, PixivItemInfo):
            return item_info
        elif isinstance(item_info, TwitterItemInfo):
            return item_info
        elif isinstance(item_info, DanbooruItemInfo):
            src = self.GetDanbooruAgent().FindSource(item_info)
        elif isinstance(item_info, YandereItemInfo):
            src = self.GetYandereAgent().FindSource(item_info)
        elif isinstance(item_info, KonachanItemInfo):
            src = self.GetKonachanAgent().FindSource(item_info)
        elif isinstance(item_info, WeiboItemInfo):
            return item_info
        elif isinstance(item_info, EHentaiItemInfo):
            return item_info
        else:
            raise ValueError('Empty or Invalid WebItemInfo.')
        
        try:
            return self.UrlToWebItemInfo(src)
        except ValueError:
            if src is not None and len(src) > 0:
                if absolute:
                    return src
                return item_info
            return None
    
    
    # WebItemInfo generation
    @TypeChecker(str, (1,))
    def UrlToWebItemInfo(self, url:str) -> WebItemInfo:
        domain = DOMAIN.FromUrl(url)
        if domain == DOMAIN.PIXIV:
            return PixivItemInfo(url)
        elif domain == DOMAIN.TWITTER:
            return TwitterItemInfo(url)
        elif domain == DOMAIN.DANBOORU:
            return DanbooruItemInfo(url)
        elif domain == DOMAIN.YANDERE:
            return YandereItemInfo(url)
        elif domain == DOMAIN.KONACHAN:
            return KonachanItemInfo(url)
        elif domain == DOMAIN.WEIBO:
            return WeiboItemInfo(url)
        elif domain == DOMAIN.EHENTAI:
            return EHentaiItemInfo(url)
        else:
            raise ValueError('Empty, Invalid, or Unsupported url domain.')
    
    @TypeChecker(DOMAIN, (1,))
    def FromChildDetails(self, domain:DOMAIN, details) -> WebItemInfo:
        if domain == DOMAIN.PIXIV:
            return PixivItemInfo.FromChildDetails(details)
        elif domain == DOMAIN.TWITTER:
            return TwitterItemInfo.FromChildDetails(details)
        elif domain == DOMAIN.DANBOORU:
            return DanbooruItemInfo.FromChildDetails(details)
        elif domain == DOMAIN.YANDERE:
            return YandereItemInfo.FromChildDetails(details)
        elif domain == DOMAIN.KONACHAN:
            return KonachanItemInfo.FromChildDetails(details)
        elif domain == DOMAIN.WEIBO:
            return WeiboItemInfo.FromChildDetails(details)
        elif domain == DOMAIN.EHENTAI:
            return EHentaiItemInfo.FromChildDetails(details)
        else:
            raise ValueError('Empty, Invalid, or Unsupported domain.')
    
    
    # private helper functions
    def __InitAgent(self, agent_domain:DOMAIN, special_arg=None, **init_args):
        if agent_domain == DOMAIN.PIXIV:
            self.__pixiv_agent = PixivAgent.instance(**init_args)
        elif agent_domain == DOMAIN.TWITTER and special_arg == 'dev':
            self.__twitter_agent = TwitterAgent.instance(**init_args)
        elif agent_domain == DOMAIN.TWITTER and special_arg == 'web':
            self.__twitter_web_agent = TwitterWebAgent.instance(**init_args)
        elif agent_domain == DOMAIN.DANBOORU:
            self.__danbooru_agent = DanbooruAgent.instance(**init_args)
        elif agent_domain == DOMAIN.YANDERE:
            self.__yandere_agent = YandereAgent.instance(**init_args)
        elif agent_domain == DOMAIN.KONACHAN:
            self.__konachan_agent = KonachanAgent.instance(**init_args)
        elif agent_domain == DOMAIN.WEIBO:
            self.__weibo_agent = WeiboAgent.instance(**init_args)
        elif agent_domain == DOMAIN.EHENTAI:
            self.__ehentai_agent = EHentaiAgent.instance(**init_args)
    
    def __CheckArgs(self, requirements:list, **kwargs):
        for req in requirements:
            if req not in kwargs or kwargs[req] is None:
                return False
        return True
