
from __future__ import annotations
from .Decorators import TypeChecker
from typing import Union
from urllib.parse import urlparse, parse_qs, urlencode

class UrlParser:
    'A simple url parser build on top of urllib.parse.urlparse()'
    
    def __init__(self, url:str):
        self.url = url
        self.__parser = urlparse(url)
        self.domain = self.__parser.hostname
        self.path = self.__parser.path
        self.pathlist = self.path.split('/')[1:]
        self.querystr = self.__parser.query
        self.query = parse_qs(self.__parser.query)
    
    def __repr__(self):
        return f'<domain="{self.domain}", path="{self.path}", query="{self.query}">'
    
    def __str__(self):
        return f'<domain="{self.domain}", path="{self.path}", query="{self.query}">'
    
    @TypeChecker(str, (1,))
    def UpdateUrl(self, url:str) -> UrlParser:
        self.url = url
        self.__parser = urlparse(url)
        self.domain = self.__parser.hostname
        self.path = self.__parser.path
        self.pathlist = self.path.split('/')[1:]
        self.querystr = self.__parser.query
        self.query = parse_qs(self.__parser.query)
        return self
    
    @TypeChecker(str, (1,))
    def UpdateDomain(self, domain:str) -> UrlParser:
        self.domain = domain
        self.url = UrlParser.BuildUrl(self.domain, self.path, self.querystr)
        return self
    
    @TypeChecker(str, (1,))
    def UpdatePath(self, path:str) -> UrlParser:
        if path[0] != '/':
            path = '/' + path
        self.path = path
        self.pathlist = self.path.split('/')[1:]
        self.url = UrlParser.BuildUrl(self.domain, self.path, self.querystr)
        return self
    
    @TypeChecker(list, (1,))
    def UpdatePathList(self, pathlist:list) -> UrlParser:
        self.pathlist = pathlist
        self.path = '/'+'/'.join(self.pathlist)
        self.url = UrlParser.BuildUrl(self.domain, self.path, self.querystr)
        return self
    
    @TypeChecker(dict, (1,))
    def UpdateQuery(self, query:dict) -> UrlParser:
        self.query = query
        self.querystr = urlencode([(k,v) for k,vlist in query.items() for v in vlist])
        self.url = UrlParser.BuildUrl(self.domain, self.path, self.querystr)
        return self
    
    @TypeChecker(str, (1,))
    def UpdateQueryStr(self, querystr:str) -> UrlParser:
        self.query = parse_qs(querystr)
        self.querystr = querystr
        self.url = UrlParser.BuildUrl(self.domain, self.path, self.querystr)
        return self
    
    def BuildUrl(domain:str, path:Union[str,list], query:Union[str,dict]) -> str:
        url = 'https://' + domain
        
        if isinstance(path, str) and path[0] == '/':
            url += path
        elif isinstance(path, str):
            url += '/' + path
        elif isinstance(path, list):
            url += '/' + '/'.join(path)
        
        if len(query) <= 0:
            pass
        elif isinstance(query, str):
            url += '?' + query
        elif isinstance(query, dict):
            url += '?' + urlencode([(k,v) for k,vlist in query.items() for v in vlist])
        
        return url
    
