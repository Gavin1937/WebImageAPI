
from .Agents import *
from .Types import *
from .Utils import TypeChecker
from typing import Union
from pathlib import Path


class WebImageAPI:
    'Handles all Agents & WebItemInfo in one place'
    
    def __init__(self):
        self.__pixiv_agent:PixivAgent          = None
        self.__twitter_agent:TwitterAgent      = None
        self.__danbooru_agent:DanbooruAgent    = None
        self.__yandere_agent:YandereAgent      = None
        self.__konachan_agent:KonachanAgent  = None
        self.__weibo_agent:WeiboAgent        = None
        self.__ehentai_agent:EHentaiAgent    = None
    
    
    # interfaces
    
    # agent setup 
    def SetPixivTokens(self, refresh_token:str):
        self.__InitAgent(DOMAIN.PIXIV, refresh_token=refresh_token)
    
    def SetTwitterTokens(self, consumer_key:str, consumer_secret:str, access_token:str, access_token_secret:str, bearer_token:str):
        self.__InitAgent(DOMAIN.TWITTER, consumer_key=consumer_key, consumer_secret=consumer_secret, access_token=access_token, access_token_secret=access_token_secret, bearer_token=bearer_token)
    
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
    
    def GetTwitterAgent(self) -> TwitterAgent:
        if self.__twitter_agent is None:
            raise ValueError('Please initialize TwitterAgent through WebImageAPI.SetTwitterTokens() first.')
        return self.__twitter_agent
    
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
    def __InitAgent(self, agent_domain:DOMAIN, **init_args):
        if agent_domain == DOMAIN.PIXIV:
            self.__pixiv_agent = PixivAgent.instance(**init_args)
        elif agent_domain == DOMAIN.TWITTER:
            self.__twitter_agent = TwitterAgent.instance(**init_args)
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
    
