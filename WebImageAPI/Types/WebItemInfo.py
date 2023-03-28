
from typing import Union
from .Types import DOMAIN, PARENT_CHILD
from ..Utils import UrlParser

# base class

class WebItemInfo:
    'Basic class contains Web Item Information'
    
    def __init__(self, url:str):
        self.url:str = url
        self.url_parser = UrlParser(self.url)
        self.domain:DOMAIN = DOMAIN.FromStr(self.url_parser.domain)
        self.parent_child:PARENT_CHILD = PARENT_CHILD.EMPTY
        self._PostInitAnalyzing()
    
    def IsParent(self) -> bool:
        return self.parent_child == PARENT_CHILD.PARENT
    
    def IsChild(self) -> bool:
        return self.parent_child == PARENT_CHILD.CHILD
    
    def IsEmpty(self) -> bool:
        return (
            len(self.url) <= 0 or
            self.domain == DOMAIN.EMPTY or
            self.domain == DOMAIN.INVALID or
            self.parent_child == PARENT_CHILD.EMPTY or 
            self.parent_child == PARENT_CHILD.INVALID
        )
    
    
    # protected virtual functions
    def _PostInitAnalyzing(self) -> None:
        raise NotImplementedError('Subclass must implement this method')
    


# children classes

class PixivItemInfo(WebItemInfo):
    def _PostInitAnalyzing(self) -> None:
        if self.domain != DOMAIN.PIXIV:
            raise ValueError('Invalid url, you must supply a pixiv url.')
        
        if 'users' in self.url_parser.pathlist:
            self.parent_child = PARENT_CHILD.PARENT
        elif 'artworks' in self.url_parser.pathlist:
            self.parent_child = PARENT_CHILD.CHILD
        elif 'member.php' == self.url_parser.pathlist[-1]:
            self.parent_child = PARENT_CHILD.PARENT
        elif 'member_illust.php' == self.url_parser.pathlist[-1]:
            self.parent_child = PARENT_CHILD.CHILD
        elif 'pximg.net' in self.url_parser.domain:
            self.parent_child = PARENT_CHILD.CHILD


