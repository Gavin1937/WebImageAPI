
from .BaseAgent import BaseAgent
from .Singleton import Singleton
from ..Types import PixivItemInfo
from ..Utils import TypeChecker, TypeMatcher, Clamp
from typing import Union
from pathlib import Path
from pixivpy3 import AppPixivAPI, PixivError
from time import sleep


@Singleton
class PixivAgent(BaseAgent):
    
    def __init__(self, refresh_token:str, max_try:int=5):
        __proxy_settings = {
            # 'proxies': {
            #     'https': 'http://127.0.0.1:1087',
            # },
            # 'verify': False,       # PAPI use https, an easy way is disable requests SSL verify
        }
        self.__api:AppPixivAPI = AppPixivAPI(**__proxy_settings)
        
        exception = None
        sleeptime = 10
        for count in range(max_try):
            try:
                self.__api.auth(refresh_token=refresh_token)
                break
            except PixivError as err:
                exception = err
                sleep(sleeptime * count)
        else:
            # only enter this else branch if
            # above for-loop finished without breaking
            raise exception
    
    
    # interfaces
    def GetAPI(self) -> AppPixivAPI:
        'Get pixivpy3.AppPixivAPI object'
        return self.__api
    
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
        Fetch a Parent PixivItemInfo\' Children
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
    

