
from .BaseAgent import BaseAgent
from .Singleton import Singleton
from ..Types import DanbooruItemInfo
from ..Utils import TypeChecker, TypeMatcher, Clamp, getSrcJson, getSrcStr, downloadFile, PROJECT_USERAGENT, UrlParser
from typing import Union
from pathlib import Path
from bs4 import BeautifulSoup


@Singleton
class DanbooruAgent(BaseAgent):
    
    def __init__(self):
        # in order to use danbooru's api,
        # we need to set a custom user-agent for this project
        # instead of pretending to be a browser,
        # which will make the project get banned by cloudflare
        # details: https://github.com/mikf/gallery-dl/issues/3665
        self.__headers = { 'User-Agent': PROJECT_USERAGENT }
        super().__init__()
    
    # interfaces
    @TypeChecker(DanbooruItemInfo, (1,))
    def FetchItemInfoDetail(self, item_info:DanbooruItemInfo) -> DanbooruItemInfo:
        '''
        Fetch & Fill-In "detail" parameter for supplied DanbooruItemInfo.
        Param:
            item_info  => DanbooruItemInfo to fetch
        Returns:
            updated DanbooruItemInfo
        '''
        
        if item_info.IsParent() or item_info.IsChild():
            item_info.details = getSrcJson(self.__NormalURLToApi(item_info.url), self.__headers)
        else:
            raise ValueError('Input DanbooruItemInfo is empty or invalid.')
        
        return item_info
    
    @TypeMatcher(['self', DanbooruItemInfo, int])
    def FetchParentChildren(self, item_info:DanbooruItemInfo, page:int=1) -> list:
        '''
        Fetch a Parent DanbooruItemInfo\' Children
        Param:
            item_info  => DanbooruItemInfo Parent to fetch
            page       => int page number >= 1
        Returns:
            list of DanbooruItemInfo fetched, also edit original "item_info"
        '''
        
        if not item_info.IsParent():
            raise ValueError('Input DanbooruItemInfo must be a parent.')
        
        page = Clamp(page, 1)
        url = self.__NormalURLToApi(item_info.url, {'page':[page]})
        item_info.details = getSrcJson(url, self.__headers)
        
        output = []
        for post in item_info.details:
            output.append(DanbooruItemInfo.FromChildDetails(post))
        
        return output
    
    @TypeChecker(DanbooruItemInfo, (1,))
    def DownloadItem(self, item_info:DanbooruItemInfo, output_path:Union[str,Path], replace:bool=False):
        '''
        Download a supplied DanbooruItemInfo
        Param:
            item_info    => DanbooruItemInfo Child to download
            output_path  => str|Path of a directory for downloaded file
            replace      => bool flag, whether replace if download file already exists
        '''
        
        if not item_info.IsChild():
            raise ValueError('Cannot download non-child DanbooruItemInfo.')
        
        output_path = Path(output_path)
        if not output_path.is_dir():
            raise ValueError('Output path should be a directory path.')
        
        # get item source url from html to retrieve filename with tags
        html = getSrcStr(item_info.url, self.__headers)
        soup = BeautifulSoup(html, 'lxml')
        url = soup.select_one('#post-info-size a').get('href')
        filename = url.split('/')[-1]
        downloadFile(url, output_path/filename, overwrite=replace)
    
    
    # private helper function
    def __NormalURLToApi(self, url:str, update_qs:dict={}) -> str:
        parsed = UrlParser(url)
        parsed.pathlist[-1] += '.json'
        parsed.query.update(update_qs)
        return UrlParser.BuildUrl(
            parsed.domain,
            parsed.pathlist,
            parsed.query
        )

