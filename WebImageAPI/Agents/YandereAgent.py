
from .BaseAgent import BaseAgent
from .Singleton import Singleton
from ..Types import YandereItemInfo, PARENT_CHILD
from ..Utils import (
    TypeChecker, TypeMatcher, Clamp,
    getSrcJson, downloadFile,
    PROJECT_USERAGENT, UrlParser
)
from typing import Union
from pathlib import Path


@Singleton
class YandereAgent(BaseAgent):
    
    def __init__(self):
        # similar to DanbooruAgent,
        # in order to use yande.re's api,
        # we need to set a custom user-agent for this project
        # instead of pretending to be a browser,
        # which will make the project get banned by cloudflare
        # details: https://github.com/mikf/gallery-dl/issues/3665
        # yande.re api: https://yande.re/help/api#posts
        self.__headers = { 'User-Agent': PROJECT_USERAGENT }
        super().__init__()
    
    # interfaces
    @TypeChecker(YandereItemInfo, (1,))
    def FetchItemInfoDetail(self, item_info:YandereItemInfo) -> YandereItemInfo:
        '''
        Fetch & Fill-In "detail" parameter for supplied YandereItemInfo.
        Param:
            item_info  => YandereItemInfo to fetch
        Returns:
            updated YandereItemInfo
        '''
        
        if item_info.IsParent() or item_info.IsChild():
            item_info.details = getSrcJson(
                self.__NormalURLToApi(item_info.url, item_info.parent_child),
                self.__headers
            )
        else:
            raise ValueError('Input YandereItemInfo is empty or invalid.')
        
        return item_info
    
    @TypeMatcher(['self', YandereItemInfo, int])
    def FetchParentChildren(self, item_info:YandereItemInfo, page:int=1) -> list:
        '''
        Fetch a Parent YandereItemInfo\' Children
        Param:
            item_info  => YandereItemInfo Parent to fetch
            page       => int page number >= 1
        Returns:
            list of YandereItemInfo fetched, also edit original "item_info"
        '''
        
        if not item_info.IsParent():
            raise ValueError('Input YandereItemInfo must be a parent.')
        
        page = Clamp(page, 1)
        new_query = {**item_info.parsed_url.query}
        new_query['page'] = [page]
        url = self.__NormalURLToApi(item_info.url, item_info.parent_child, new_query)
        item_info.details = getSrcJson(url, self.__headers)
        
        output = []
        for post in item_info.details:
            output.append(YandereItemInfo.FromChildDetails(post))
        
        return output
    
    @TypeChecker(YandereItemInfo, (1,))
    def DownloadItem(self, item_info:YandereItemInfo, output_path:Union[str,Path], replace:bool=False):
        '''
        Download a supplied YandereItemInfo
        Param:
            item_info    => YandereItemInfo Child to download
            output_path  => str|Path of a directory for downloaded file
            replace      => bool flag, whether replace if download file already exists
        '''
        
        if not item_info.IsChild():
            raise ValueError('Cannot download non-child YandereItemInfo.')
        
        output_path = Path(output_path)
        if not output_path.is_dir():
            raise ValueError('Output path should be a directory path.')
        
        if item_info.details is None:
            item_info = self.FetchItemInfoDetail(item_info)
        
        url = item_info.details[0]['file_url']
        filename = url.split('/')[-1]
        downloadFile(url, output_path/filename, overwrite=replace)
    
    
    # private helper function
    def __NormalURLToApi(self, url:str, parent_child:PARENT_CHILD, update_qs:dict={}) -> str:
        parsed = UrlParser(url)
        if parent_child == PARENT_CHILD.CHILD:
            if 'tags' not in parsed.query:
                parsed.query['tags'] = [f'id:{parsed.pathlist[-1]}']
            else:
                parsed.query['tags'] += [f'id:{parsed.pathlist[-1]}']
        parsed.query.update(update_qs)
        parsed.UpdatePath('post.json')
        parsed.UpdateQuery(parsed.query)
        return parsed.url

