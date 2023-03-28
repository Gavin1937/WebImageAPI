from typing import Union
from urllib.parse import urlparse

class UrlParser:
    
    def __init__(self, url:str):
        self.url = url
        self.__parser = urlparse(url)
        self.domain = self.__parser.hostname
        self.path = self.__parser.path
        self.pathlist = self.path.split('/')[1:]
        self.query = dict(map((lambda s:s.split('=')), self.__parser.query.split('&')))
    
    def __repr__(self):
        return f'<domain="{self.domain}", path="{self.path}", query="{self.query}">'
    
    def __str__(self):
        return f'<domain="{self.domain}", path="{self.path}", query="{self.query}">'
    
    def BuildUrl(domain:str, path:Union[str,list], query:Union[str,dict]) -> str:
        url = 'https://' + domain
        
        if isinstance(path, str) and path[0] == '/':
            url += path
        elif isinstance(path, str):
            url += '/' + path
        elif isinstance(path, list):
            url += '/' + '/'.join(path)
        
        if isinstance(query, str):
            url += '?' + query
        elif isinstance(query, dict):
            url += '?' + '&'.join(map(lambda i:f'{i[0]}={i[1]}',query.items()))
        
        return url
    
