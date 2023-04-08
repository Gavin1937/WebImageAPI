
from .Variables import PROJECT_USERAGENT
from .Functions import GetMD5
from .UrlParser import UrlParser
import requests
from time import sleep
from random import uniform
from pathlib import Path
from typing import Union
from bs4 import BeautifulSoup


class HTTPClient:
    'A simple http client wrapper on top of "requests"'
    
    def __init__(
        self,
        default_headers:dict=None,
        default_cookies:dict=None,
        default_proxies:str=None,
        delay_value:tuple=None
    ) -> None:
        '''
        Construct HTTPClient
        Param:
            default_headers  => dict, default header to use inside this client (default None)
            default_cookies  => dict, default cookies to use inside this client (default None)
            default_proxies  => str, default proxy url to use inside this client (default None)
            delay_value      => tuple[number, number], a two number tuple for random delay
                                default set to None (disable)
                                if set to any valid value, HTTPClient will place a random delay
                                before every request from delay_value[0] to delay_value[1].
                                this delay will block the main thread
        '''
        self.__headers = { 'User-Agent': PROJECT_USERAGENT } if default_headers is None else default_headers
        self.__cookies = {} if default_cookies is None else default_cookies
        self.__proxies = {}
        if default_proxies is not None:
            proxy_type = 'https'
            if not default_proxies.startswith(proxy_type):
                proxy_type = 'http'
            self.__proxies = { proxy_type: default_proxies }
        self.__delay_val = delay_value
    
    
    # interfaces
    
    # getter & setter
    
    def GetHeaders(self) -> dict:
        return self.__headers
    
    def SetHeaders(self, headers:dict) -> None:
        self.__headers = headers
    
    def GetCookies(self) -> dict:
        return self.__cookies
    
    def SetCookies(self, cookies:dict) -> None:
        self.__cookies = cookies
    
    def GetProxies(self) -> dict:
        return self.__proxies
    
    def SetProxies(self, proxies:str) -> None:
        if proxies is not None:
            proxy_type = 'https'
            if not proxies.startswith(proxy_type):
                proxy_type = 'http'
            self.__proxies = { proxy_type:proxies }
    
    def GetDelayValue(self) -> tuple:
        return self.__delay_val
    
    def SetDelayValue(self, delay_value:tuple) -> None:
        if len(self.__delay_val) == 2:
            self.__delay_val = delay_value
    
    
    # request
    
    def GetBytes(self, url:str, **kwargs) -> bytes:
        return self.__Get(url, **kwargs).content
    
    def GetStr(self, url:str, encoding:str='utf-8', **kwargs) -> str:
        return self.__Get(url, **kwargs).content.decode(encoding)
    
    def GetHtml(self, url:str, encoding:str='utf-8', **kwargs) -> BeautifulSoup:
        return BeautifulSoup(self.__Get(url, **kwargs).content.decode(encoding), 'lxml')
    
    def GetJson(self, url:str, **kwargs) -> dict:
        return self.__Get(url, **kwargs).json()
    
    def DownloadUrl(
        self, url:str,
        path:Union[str,Path],
        overwrite:bool=False,
        md5:str=None
    ) -> None:
        '''
        Download specified url
        Param:
            url          => str, url to download
            path         => str|Path, output path to a file or directory
            overwrite    => bool, whether to overwrite if downloaded file already exists in output path (default False)
            md5          => str, expect md5 hash string of downloaded url
                            if set to None (default), this function will ignore any md5 checking
                            if set to a string (32 digit hex), this function will compare downloaded file's md5 with it
                            if md5 not matching, raise Exception
        '''
        
        parsed = UrlParser(url)
        path = Path(path)
        download_path = None
        
        if path.exists():
            if path.is_file() and overwrite:
                download_path = path
            elif path.is_file() and not overwrite:
                raise ValueError('Input path already exist.')
            elif path.is_dir(): # use last part of url path as filename
                download_path = path / parsed.pathlist[-1]
            else: # neither file or dir
                raise ValueError(f'Invalid path, it should be either a file or directory.')
            
        else: # path not exist
            if path.parent.exists(): # assuming path is a file to create
                download_path = path
            else: # invalid path
                raise ValueError(f'Invalid path: {path}')
        
        if download_path.exists() and not overwrite:
            raise ValueError(f'File {download_path.name} already exist in the input path.')
        
        resp = self.__Get(url)
        
        with open(download_path, 'wb') as file:
            file.write(resp.content)
        
        # check file integrity
        if md5 is not None and isinstance(md5, str) and len(md5) == 32:
            md5 = md5.lower()
            with open(download_path, 'rb') as file:
                file_md5 = GetMD5(file.read()).lower()
            if file_md5 != md5:
                raise Exception('Downloaded file MD5 not matching.')
    
    
    # private helper functions
    def __RandDelay(self):
        if self.__delay_val is not None and len(self.__delay_val) == 2:
            sleep(uniform(self.__delay_val[0], self.__delay_val[1]))
    
    def __Get(self, url, headers=None, cookies=None, proxies=None, **kwargs) -> requests.Response:
        loc_headers = self.__headers if headers is None else headers
        loc_cookies = self.__cookies if cookies is None else cookies
        loc_proxies = self.__proxies if proxies is None else proxies
        loc_kwargs = {} if kwargs is None else kwargs
        self.__RandDelay()
        return requests.get(url=url, headers=loc_headers, cookies=loc_cookies, proxies=loc_proxies, **loc_kwargs)


BROWSER_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
    'Connection': 'keep-alive',
}

