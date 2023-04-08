
from .BaseAgent import BaseAgent
from .Singleton import Singleton
from ..Types import EHentaiItemInfo, UserInfo, DOMAIN, EHentaiInPeekHourException
from ..Utils import (
    TypeChecker, TypeMatcher,
    Clamp, MergeDeDuplicate,
    UrlParser,
    HTTPClient, BROWSER_HEADERS
)
from typing import Union
from pathlib import Path
from datetime import datetime, timezone


@Singleton
class EHentaiAgent(BaseAgent):
    
    def __init__(self, ignore_peek_hour:bool=False, proxies:str=None):
        self.__api_url = 'https://api.e-hentai.org/api.php'
        self.__headers = {
            'Referer': 'https://e-hentai.org/',
            **BROWSER_HEADERS
        }
        self.__http = HTTPClient(default_headers=self.__headers, default_proxies=proxies)
        self.__ignore_peek_hour:bool = ignore_peek_hour
        self.__peek_hour_table:list = [
            [14, 20], # Mon (0)	
            [14, 20], # Tue (1)	
            [14, 20], # Wed (2)	
            [14, 20], # Thu (3)	
            [14, 20], # Fri (4)	
            [14, 20], # Sat (5)	
            [5,  20], # Sun (6)	
        ]
        super().__init__()
    
    # interfaces
    def SetProxies(self, proxies:str=None):
        self.__http = HTTPClient(default_proxies=proxies)
    
    def GetIgnorePeekHour(self) -> bool:
        return self.__ignore_peek_hour
    
    def SetIgnorePeekHour(self, whether_ignore:bool):
        self.__ignore_peek_hour = whether_ignore
    
    def InPeekHour(self) -> bool:
        'Whether E-Hentai is in Peek Hour now'
        utc_now = datetime.now(timezone.utc)
        start,end = self.__peek_hour_table[utc_now.weekday()]
        hour = utc_now.hour+1
        return ( hour >= start and hour < end )
    
    @TypeChecker(EHentaiItemInfo, (1,))
    def FetchItemInfoDetail(self, item_info:EHentaiItemInfo) -> EHentaiItemInfo:
        '''
        Fetch & Fill-In "detail" parameter for supplied EHentaiItemInfo.
        Param:
            item_info  => EHentaiItemInfo to fetch
        Returns:
            updated EHentaiItemInfo
        '''
        
        post_param = {}
        if item_info.IsParent():
            post_param = {
                "method": "gdata",
                "gidlist": [
                    [item_info.gallery_id, item_info.other['gallery_token']]
                ],
                "namespace": 1
            }
        elif item_info.IsChild():
            post_param = {
                "method": "gtoken",
                "pagelist": [
                    [item_info.gallery_id, item_info.other['page_token'], item_info.other['pagenumber']]
                ]
            }
        else:
            raise ValueError('Input EHentaiItemInfo is empty or invalid.')
        
        item_info.details = self.__http.PostJson(self.__api_url, json=post_param)
        
        return item_info
    
    @TypeMatcher(['self', EHentaiItemInfo, int])
    def FetchParentChildren(self, item_info:EHentaiItemInfo, page:int=1) -> list:
        '''
        Fetch a Parent EHentaiItemInfo\'s Children
        Param:
            item_info  => EHentaiItemInfo Parent to fetch
            page       => int page number >= 1
        Returns:
            list of EHentaiItemInfo fetched, also edit original "item_info"
        '''
        
        if not item_info.IsParent():
            raise ValueError('Input EHentaiItemInfo must be a parent.')
        
        page = Clamp(page, 1)
        url = UrlParser.BuildUrl(
            item_info.parsed_url.domain,
            item_info.parsed_url.path,
            {'page':[page]},
        )
        soup = self.__http.GetHtml(url)
        
        output = []
        details = {
            'gallery_id': item_info.gallery_id,
            'page': page,
            'images': []
        }
        for div in soup.select('div#gdt div.gdtm'):
            child_url = div.find('a').get('href')
            output.append(EHentaiItemInfo(child_url))
            details['images'].append(child_url)
        item_info.details = details
        
        return output
    
    @TypeChecker(EHentaiItemInfo, (1,))
    def FetchUserInfo(self, item_info:EHentaiItemInfo, old_user_info:UserInfo=None) -> UserInfo:
        '''
        Fetch a EHentaiItemInfo\'s UserInfo
        Param:
            item_info        => EHentaiItemInfo Parent to fetch
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
            user = item_info.details
        elif item_info.IsChild():
            post_param = {
                "method": "gdata",
                "gidlist": [
                    [item_info.details['tokenlist'][0]['gid'], item_info.details['tokenlist'][0]['token']]
                ],
                "namespace": 1
            }
            user = self.__http.PostJson(self.__api_url, json=post_param)
        
        domain = DOMAIN.EHENTAI
        name_list = []
        for tag in user['gmetadata'][0]['tags']:
            key,val = tag.split(':')
            if key == 'artist':
                name_list.append(val)
        url_dict = {}
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
    
    @TypeChecker(EHentaiItemInfo, (1,))
    def DownloadItem(self, item_info:EHentaiItemInfo, output_path:Union[str,Path], replace:bool=False):
        '''
        Download a supplied EHentaiItemInfo
        Param:
            item_info    => EHentaiItemInfo Child to download
            output_path  => str|Path of a directory for downloaded file
            replace      => bool flag, whether replace if download file already exists
        '''
        
        if self.InPeekHour() and not self.__ignore_peek_hour:
            raise EHentaiInPeekHourException()
        
        if not item_info.IsChild():
            raise ValueError('Cannot download non-child EHentaiItemInfo.')
        
        output_path = Path(output_path)
        if not output_path.is_dir():
            raise ValueError('Output path should be a directory path.')
        
        soup = self.__http.GetHtml(item_info.url)
        filename = soup.select_one('div#i2').findChildren('div')[-1]
        filename = filename.getText().split(' :: ')[0]
        url = soup.select_one('img#img').get('src')
        
        self.__http.DownloadUrl(url, output_path/filename, overwrite=replace)
