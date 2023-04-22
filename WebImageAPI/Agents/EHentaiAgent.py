
from .BaseAgent import BaseAgent
from .Singleton import Singleton
from ..Types import EHentaiItemInfo, UserInfo, DOMAIN
from ..Types.Exceptions import (
    WrongParentChildException,
    EHentaiInPeekHourException,
    EHentaiExcessViewingLimit,
    FileMD5NotMatchingException
)
from ..Utils import (
    TypeChecker, TypeMatcher,
    Clamp, MergeDeDuplicate,
    UrlParser,
    HTTPClient, BROWSER_HEADERS
)
from typing import Union
from pathlib import Path
from datetime import datetime, timezone, timedelta


@Singleton
class EHentaiAgent(BaseAgent):
    
    def __init__(self, ignore_peek_hour:bool=False, ipb_member_id:str=None, ipb_pass_hash:str=None, proxies:str=None):
        self.__api_url = 'https://api.e-hentai.org/api.php'
        self.__proxies = proxies
        self.__headers = {
            'Referer': 'https://e-hentai.org/',
            **BROWSER_HEADERS
        }
        self.__ipb_member_id:str = ipb_member_id
        self.__ipb_pass_hash:str = ipb_pass_hash
        tmp_cookies = {
            'ipb_member_id':self.__ipb_member_id,
            'ipb_pass_hash':self.__ipb_pass_hash,
        }
        self.__http = HTTPClient(default_headers=self.__headers, default_cookies=tmp_cookies, default_proxies=self.__proxies)
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
    
    def SetEHentaiAuthInfo(self, ipb_member_id:str, ipb_pass_hash:str):
        self.__ipb_member_id:str = ipb_member_id
        self.__ipb_pass_hash:str = ipb_pass_hash
        tmp_cookies = {
            'ipb_member_id':self.__ipb_member_id,
            'ipb_pass_hash':self.__ipb_pass_hash,
        }
        self.__http = HTTPClient(default_headers=self.__headers, default_cookies=tmp_cookies, default_proxies=self.__proxies)
    
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
    
    def GetNextPeekHour(self) -> tuple:
        '''
        Get next peek hour information
        Returns:
            tuple( whether in peek hour : bool, peek hour : datetime )
            If currently in peek hour, tuple( True, datetime obj of the end of current peek hour )
            If currently not in peek hour, tuple( False, datetime obj of the start of next peek hour )
        '''
        
        utc_now = datetime.now(timezone.utc)
        utc_weekday = utc_now.weekday()
        start,end = self.__peek_hour_table[utc_weekday]
        next_start,_ = self.__peek_hour_table[(utc_weekday+1)%7]
        in_peek_hour = self.InPeekHour()
        next_time_point = None
        if in_peek_hour:
            next_time_point = datetime(
                year=utc_now.year, month=utc_now.month,
                day=utc_now.day, hour=end,
                tzinfo=timezone.utc,
            )
        else: # not in_peek_hour
            # before today's peek hour
            if (utc_now.hour+1) < start:
                next_time_point = datetime(
                    year=utc_now.year, month=utc_now.month,
                    day=utc_now.day, hour=start,
                    tzinfo=timezone.utc,
                )
            # after today's peek hour
            elif (utc_now.hour+1) >= end:
                next_time_point = datetime(
                    year=utc_now.year, month=utc_now.month,
                    day=utc_now.day, hour=next_start,
                    tzinfo=timezone.utc,
                ) + timedelta(days=1)
        
        return (in_peek_hour, datetime.fromtimestamp(next_time_point.timestamp()))
    
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
            raise WrongParentChildException(item_info.parent_child, 'Input EHentaiItemInfo must be a parent.')
        
        page = Clamp(page, 1) - 1
        url = UrlParser.BuildUrl(
            item_info.parsed_url.domain,
            item_info.parsed_url.path,
            {'p':[page]},
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
            raise WrongParentChildException(item_info.parent_child, 'Cannot download non-child EHentaiItemInfo.')
        
        output_path = Path(output_path)
        if not output_path.is_dir():
            raise ValueError('Output path should be a directory path.')
        
        soup = self.__http.GetHtml(item_info.url)
        filename = soup.select_one('div#i2').findChildren('div')[-1]
        filename = filename.getText().split(' :: ')[0]
        # try to find the original image download url from html (if exists)
        url = None
        orig_elem = soup.select_one('div#i7 a')
        lowres_elem = soup.select_one('div#i3 img#img')
        if orig_elem is not None and 'Download original' in orig_elem.text:
            url = orig_elem.get('href')
        elif lowres_elem is not None:
            url = lowres_elem.get('src')
        if url is None:
            raise ValueError('Cannot find download url from EHentai Child')
        
        # when you excess EH viewing limit
        # EH will send back an image with warning text on it rather than the real image
        # check for its md5
        excess_limit_md5 = '88fe16ae482faddb4cc23df15722348c'
        try:
            self.__http.DownloadUrl(url, output_path/filename, overwrite=replace, md5=excess_limit_md5)
        except FileMD5NotMatchingException:
            # downloaded file md5 not matches excess_limit_md5, good image
            pass
        else:
            # download file md5 matches excess_limit_md5, excess EH viewing limit
            (output_path/filename).unlink() # rm downloaded img
            raise EHentaiExcessViewingLimit(item_info.url)
