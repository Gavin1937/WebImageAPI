
from .BaseAgent import BaseAgent
from .Singleton import Singleton
from ..Types import PixivItemInfo, UserInfo, DOMAIN
from ..Utils import (
    TypeChecker, TypeMatcher,
    Clamp, MergeDeDuplicate
)
from typing import Union
from pathlib import Path
from pixivpy3 import AppPixivAPI, PixivError
from time import sleep


@Singleton
class PixivAgent(BaseAgent):
    
    # def __init__(self, refresh_token:str, proxies:str=None, max_try:int=5):
    def __init__(self, refresh_token:str, max_try:int=5):
        proxy_settings = {}
        # if proxies is not None:
        #     proxy_type = 'https'
        #     ssl_verify = True
        #     if not proxies.startswith(proxy_type):
        #         proxy_type = 'http'
        #         ssl_verify = False
            
        #     proxy_settings = {
        #         'verify': ssl_verify,       # PAPI use https, an easy way is disable requests SSL verify
        #         'proxies': { proxy_type: proxies, },
        #     }
        
        self.__api:AppPixivAPI = AppPixivAPI(**proxy_settings)
        
        exception = None
        sleeptime = 10
        for count in range(max_try):
            try:
                self.__api.auth(refresh_token=refresh_token)
                break
            except PixivError as err:
                exception = err
                print(f'PixivError: {err}')
                wakeup_in = sleeptime * count
                print(f'[{count+1}/{max_try}] Sleep for {wakeup_in} sec before retry')
                sleep(sleeptime * count)
        else:
            # only enter this else branch if
            # above for-loop finished without breaking
            raise exception
        
        self.__refresh_token = refresh_token
        self.__max_try = max_try
    
    
    # interfaces
    def GetAPI(self) -> AppPixivAPI:
        'Get pixivpy3.AppPixivAPI object'
        return self.__api
    
    # 2023-04-03
    # currently, I cannot figure out how to allow proxy in pixivpy
    # this is due to following error:
    # Cannot set verify_mode to CERT_NONE when check_hostname is enabled.
    # 
    # even after I set { 'verify': False }
    # 
    # pixivpy uses cloudscraper underhood for all the http requests
    # and cloudscraper is depending on requests
    # this error probably happens in between cloudscraper or requests layer
    # pixivpy will pass your proxy setting to cloudscraper as function kwargs
    # maybe its caused by underlying requests.Session doesn't take 'verify' parameter came from function kwargs?
    # or maybe underlying requests.Session.verify is set to True all the time and overwriting my setting?
    
    # def SetProxies(self, proxies:str=None):
    #     if proxies is not None:
    #         proxy_type = 'https'
    #         ssl_verify = True
    #         if not proxies.startswith(proxy_type):
    #             ssl_verify = False
    #             proxy_type = 'http'
            
    #         proxy_settings = {
    #             'verify': ssl_verify,       # PAPI use https, an easy way is disable requests SSL verify
    #             'proxies': { proxy_type: proxies, },
    #         }
    #         self.__api:AppPixivAPI = AppPixivAPI(**proxy_settings)
            
    #         exception = None
    #         sleeptime = 10
    #         for count in range(self.__max_try):
    #             try:
    #                 self.__api.auth(refresh_token=self.__refresh_token)
    #                 break
    #             except PixivError as err:
    #                 exception = err
    #                 print(f'PixivError: {err}')
    #                 wakeup_in = sleeptime * count
    #                 print(f'[{count+1}/{self.__max_try}] Sleep for {wakeup_in} sec before retry')
    #                 sleep(sleeptime * count)
    #         else:
    #             # only enter this else branch if
    #             # above for-loop finished without breaking
    #             raise exception
    
    @TypeChecker(PixivItemInfo, (1,))
    def FetchItemInfoDetail(self, item_info:PixivItemInfo) -> PixivItemInfo:
        '''
        Fetch & Fill-In "detail" parameter for supplied PixivItemInfo.
        Param:
            item_info  => PixivItemInfo to fetch
        Returns:
            updated PixivItemInfo
        '''
        
        if item_info.IsParent():
            item_info.details = self.__api.user_detail(item_info.pid)
        elif item_info.IsChild():
            item_info.details = self.__api.illust_detail(item_info.pid)
            if len(item_info.details['illust']['meta_single_page']) > 0:
                item_info.details['illust']['meta_single_page'] = [{
                    'image_urls':{
                        'original':item_info.details['illust']['meta_single_page']['original_image_url']
                    }
                }]
        else:
            raise ValueError('Input PixivItemInfo is empty or invalid.')
        return item_info
    
    @TypeMatcher(['self', PixivItemInfo, int])
    def FetchParentChildren(self, item_info:PixivItemInfo, page:int=1) -> list:
        '''
        Fetch a Parent PixivItemInfo\'s Children
        Param:
            item_info  => PixivItemInfo Parent to fetch
            page       => int page number >= 1
        Returns:
            list of PixivItemInfo fetched, also edit original "item_info"
        '''
        
        if not item_info.IsParent():
            raise ValueError('Input PixivItemInfo must be a parent.')
        
        page = Clamp(page, 1)
        offset = (page-1) * 30
        item_info.details = self.__api.user_illusts(item_info.pid, offset=offset)
        
        output = []
        for illust in item_info.details['illusts']:
            if len(illust['meta_single_page']) > 0:
                illust['meta_single_page'] = [{
                    'image_urls':{
                        'original':illust['meta_single_page']['original_image_url']
                    }
                }]
            output.append(PixivItemInfo.FromChildDetails(illust))
        
        return output
    
    @TypeChecker(PixivItemInfo, (1,))
    def FetchUserInfo(self, item_info:PixivItemInfo, old_user_info:UserInfo=None) -> UserInfo:
        '''
        Fetch a PixivItemInfo\'s UserInfo
        Param:
            item_info        => PixivItemInfo Parent to fetch
            old_user_info    => UserInfo that already fill up by other agents,
                                this function will collect additional UserInfo from current domain,
                                and append to old_user_info and return it at the end.
                                (default None)
        Returns:
            UserInfo object
        '''
        
        if item_info.details is None:
            item_info = self.FetchItemInfoDetail(item_info)
        
        domain = DOMAIN.PIXIV
        if item_info.IsParent():
            user = item_info.details['user']
        if item_info.IsChild():
            user = item_info.details['illust']['user']
        
        name_list = [user['name']]
        url_dict = {domain:[f'https://www.pixiv.net/users/{user["id"]}']}
        if old_user_info is not None:
            old_user_info.name_list = MergeDeDuplicate(old_user_info.name_list, name_list)
            if domain in old_user_info.url_dict:
                old_user_info.url_dict[domain] += url_dict[domain]
            else:
                old_user_info.url_dict[domain] = url_dict[domain]
            old_user_info.url_dict[domain] = MergeDeDuplicate(old_user_info.url_dict[domain])
            old_user_info.details[domain] = user
            return old_user_info
        return UserInfo(name_list, url_dict, {domain:user})
    
    @TypeChecker(PixivItemInfo, (1,))
    def DownloadItem(self, item_info:PixivItemInfo, output_path:Union[str,Path], replace:bool=False):
        '''
        Download a supplied PixivItemInfo
        Param:
            item_info    => PixivItemInfo Child to download
            output_path  => str|Path of a directory for downloaded file
            replace      => bool flag, whether replace if download file already exists
        '''
        
        if not item_info.IsChild():
            raise ValueError('Cannot download non-child PixivItemInfo.')
        
        output_path = Path(output_path)
        if not output_path.is_dir():
            raise ValueError('Output path should be a directory path.')
        
        if item_info.details is None:
            item_info = self.FetchItemInfoDetail(item_info)
        
        illust_meta = []
        illust_meta += item_info.details['illust']['meta_single_page']
        illust_meta += item_info.details['illust']['meta_pages']
        for meta in illust_meta:
            self.__api.download(
                url=meta['image_urls']['original'],
                path=str(output_path.resolve()),
                replace=replace
            )
    

