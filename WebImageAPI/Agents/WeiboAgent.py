
from .BaseAgent import BaseAgent
from .Singleton import Singleton
from ..Types import WeiboItemInfo, UserInfo, DOMAIN
from ..Types.Exceptions import (
    WrongParentChildException,
    BadWebItemInfoException
)
from ..Utils import (
    TypeChecker, TypeMatcher,
    Clamp, MergeDeDuplicate,
    HTTPClient, BROWSER_HEADERS
)
from typing import Union
from pathlib import Path


@Singleton
class WeiboAgent(BaseAgent):
    
    def __init__(self, proxies:dict=None):
        # m.weibo.cn api research
        # 
        # older api with examples
        # https://gist.github.com/momo0v0/805e4a005225e3808626656c7ff284e5
        # newer api
        # https://cloud.tencent.com/developer/news/188614
        # 
        # weibo api url:
        # https://m.weibo.cn/api/...
        
        # header 'Referer' is required with normal browser user-agent to access the weibo api
        self.__headers = {
            'Referer': 'https://m.weibo.cn/',
            **BROWSER_HEADERS
        }
        self.__http = HTTPClient(default_headers=self.__headers, default_proxies=proxies)
        super().__init__()
    
    # interfaces
    def SetProxies(self, proxies:dict):
        self.__http.SetProxies(proxies)
    
    @TypeChecker(WeiboItemInfo, (1,))
    def FetchItemInfoDetail(self, item_info:WeiboItemInfo) -> WeiboItemInfo:
        '''
        Fetch & Fill-In "detail" parameter for supplied WeiboItemInfo.
        Param:
            item_info  => WeiboItemInfo to fetch
        Returns:
            updated WeiboItemInfo
        '''
        
        weibo_id = item_info.weibo_id
        if item_info.IsParent():
            item_info.details = self.__http.GetJson(
                f'https://m.weibo.cn/api/container/getIndex?type=uid&value={weibo_id}&containerid=107603{weibo_id}'
            )
        elif item_info.IsChild():
            item_info.details = self.__http.GetJson(
                f'https://m.weibo.cn/api/statuses/show?id={weibo_id}'
            )
        else:
            raise BadWebItemInfoException(item_info.__name__)
        
        return item_info
    
    @TypeMatcher(['self', WeiboItemInfo, int])
    def FetchParentChildren(self, item_info:WeiboItemInfo, page:int=1) -> list:
        '''
        Fetch a Parent WeiboItemInfo\'s Children
        Param:
            item_info  => WeiboItemInfo Parent to fetch
            page       => int page number >= 1
        Returns:
            list of WeiboItemInfo fetched, also edit original "item_info"
        '''
        
        if not item_info.IsParent():
            raise WrongParentChildException(item_info.parent_child, 'Input WeiboItemInfo must be a parent.')
        
        page = Clamp(page, 1)
        url = f'https://m.weibo.cn/api/container/getIndex?type=uid&value={item_info.weibo_id}&containerid=107603{item_info.weibo_id}&page={page}'
        item_info.details = self.__http.GetJson(url)
        
        output = []
        for card in item_info.details['data']['cards']:
            output.append(WeiboItemInfo.FromChildDetails(card))
        
        return output
    
    @TypeChecker(WeiboItemInfo, (1,))
    def FetchUserInfo(self, item_info:WeiboItemInfo, old_user_info:UserInfo=None) -> UserInfo:
        '''
        Fetch a WeiboItemInfo\'s UserInfo
        Param:
            item_info        => WeiboItemInfo Parent to fetch
            old_user_info    => UserInfo that already fill up by other agents,
                                this function will collect additional UserInfo from current domain,
                                and append to old_user_info and return it at the end.
                                (default None)
        Returns:
            UserInfo object
        '''
        
        if item_info.details is None:
            item_info = self.FetchItemInfoDetail(item_info)
        
        user = None
        if item_info.IsParent():
            user = item_info.details['data']['cards'][0]['mblog']['user']
        elif item_info.IsChild():
            user = item_info.details['user']
        
        domain = DOMAIN.WEIBO
        name_list = []
        if 'name' in user:
            name_list.append(user['name'])
        if 'screen_name' in user:
            name_list.append(user['screen_name'])
        url_dict = {domain:[f'https://m.weibo.cn/u/{user["id"]}']}
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
    
    @TypeChecker(WeiboItemInfo, (1,))
    def DownloadItem(self, item_info:WeiboItemInfo, output_path:Union[str,Path], replace:bool=False):
        '''
        Download a supplied WeiboItemInfo
        Param:
            item_info    => WeiboItemInfo Child to download
            output_path  => str|Path of a directory for downloaded file
            replace      => bool flag, whether replace if download file already exists
        '''
        
        if not item_info.IsChild():
            raise WrongParentChildException(item_info.parent_child, 'Cannot download non-child WeiboItemInfo.')
        
        output_path = Path(output_path)
        if not output_path.is_dir():
            raise ValueError('Output path should be a directory path.')
        
        if item_info.details is None:
            item_info = self.FetchItemInfoDetail(item_info)
        
        for pic_id in item_info.details['pic_ids']:
            url = f'https://wx1.sinaimg.cn/large/{pic_id}.jpg'
            filename = f'{pic_id}.jpg'
            self.__http.DownloadUrl(url, output_path/filename, overwrite=replace)
