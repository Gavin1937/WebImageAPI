
from .BaseAgent import BaseAgent
from .Singleton import Singleton
from ..Types import YandereItemInfo, UserInfo, DOMAIN, PARENT_CHILD
from ..Types.Exceptions import WrongParentChildException
from ..Utils import (
    TypeChecker, TypeMatcher,
    Clamp, MergeDeDuplicate,
    UrlParser, HTTPClient
)
from typing import Union
from pathlib import Path


@Singleton
class YandereAgent(BaseAgent):
    
    def __init__(self, proxies:str=None):
        # similar to DanbooruAgent,
        # in order to use yande.re's api,
        # we need to set a custom user-agent for this project
        # instead of pretending to be a browser,
        # which will make the project get banned by cloudflare
        # details: https://github.com/mikf/gallery-dl/issues/3665
        # yande.re api: https://yande.re/help/api
        self.__http = HTTPClient(default_proxies=proxies)
        super().__init__()
    
    # interfaces
    def SetProxies(self, proxies:str=None):
        self.__http = HTTPClient(default_proxies=proxies)
    
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
            item_info.details = self.__http.GetJson(
                self.__NormalURLToApi(item_info.url, item_info.parent_child)
            )
        else:
            raise ValueError('Input YandereItemInfo is empty or invalid.')
        
        return item_info
    
    @TypeMatcher(['self', YandereItemInfo, int])
    def FetchParentChildren(self, item_info:YandereItemInfo, page:int=1) -> list:
        '''
        Fetch a Parent YandereItemInfo\'s Children
        Param:
            item_info  => YandereItemInfo Parent to fetch
            page       => int page number >= 1
        Returns:
            list of YandereItemInfo fetched, also edit original "item_info"
        '''
        
        if not item_info.IsParent():
            raise WrongParentChildException(item_info.parent_child, 'Input YandereItemInfo must be a parent.')
        
        page = Clamp(page, 1)
        new_query = {**item_info.parsed_url.query}
        new_query['page'] = [page]
        url = self.__NormalURLToApi(item_info.url, item_info.parent_child, new_query)
        item_info.details = self.__http.GetJson(url)
        
        output = []
        for post in item_info.details['posts']:
            output.append(YandereItemInfo.FromChildDetails({'posts':[post]}))
        
        return output
    
    @TypeChecker(YandereItemInfo, (1,))
    def FetchUserInfo(self, item_info:YandereItemInfo, old_user_info:UserInfo=None) -> UserInfo:
        '''
        Fetch a YandereItemInfo\'s UserInfo
        Param:
            item_info        => YandereItemInfo Parent to fetch
            old_user_info    => UserInfo that already fill up by other agents,
                                this function will collect additional UserInfo from current domain,
                                and append to old_user_info and return it at the end.
                                (default None)
        Returns:
            UserInfo object
        '''
        
        if item_info.details is None:
            item_info = self.FetchItemInfoDetail(item_info)
        
        tags = item_info.details['tags']
        artist_tag = None
        for tag,type in tags.items():
            if type == 'artist':
                artist_tag = tag
                break
        url = f'https://yande.re/artist.json?name={artist_tag}'
        user = self.__http.GetJson(url)
        if len(user) <= 0:
            return UserInfo([artist_tag], {DOMAIN.YANDERE:[]}, {DOMAIN.YANDERE:user})
        user = user[0]
        
        domain = DOMAIN.YANDERE
        name_list = [user['name']]
        url_dict = {domain:user['urls']}
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
            raise WrongParentChildException(item_info.parent_child, 'Cannot download non-child YandereItemInfo.')
        
        output_path = Path(output_path)
        if not output_path.is_dir():
            raise ValueError('Output path should be a directory path.')
        
        if item_info.details is None:
            item_info = self.FetchItemInfoDetail(item_info)
        
        url = item_info.details['posts'][0]['file_url']
        filename = url.split('/')[-1]
        self.__http.DownloadUrl(url, output_path/filename, overwrite=replace)
    
    
    # private helper function
    def __NormalURLToApi(self, url:str, parent_child:PARENT_CHILD, update_qs:dict={}) -> str:
        parsed = UrlParser(url)
        if parent_child == PARENT_CHILD.CHILD:
            if 'tags' not in parsed.query:
                parsed.query['tags'] = [f'id:{parsed.pathlist[2]}']
            else:
                parsed.query['tags'] += [f'id:{parsed.pathlist[2]}']
        parsed.query.update({
            **update_qs, 'api_version':[2],
            'include_tags':[1], 'include_pools':[1]
        })
        parsed.UpdatePath('post.json')
        parsed.UpdateQuery(parsed.query)
        return parsed.url

