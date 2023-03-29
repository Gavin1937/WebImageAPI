
from typing import Union
from .Types import DOMAIN, PARENT_CHILD
from ..Utils import UrlParser

class WebItemInfo:
    'Base class contains Web Item Information'
    
    def __init__(self, url:str):
        self.url:str = url
        self.parsed_url = UrlParser(self.url)
        self.domain:DOMAIN = DOMAIN.FromStr(self.parsed_url.domain)
        self.parent_child:PARENT_CHILD = PARENT_CHILD.EMPTY
        self.details = None
        self._PostInitAnalyzing()
    
    def __repr__(self):
        return f'<domain="{DOMAIN.ToStr(self.domain)}", parent_children="{PARENT_CHILD.ToStr(self.parent_child)}">'
    
    def __str__(self):
        return f'<domain="{DOMAIN.ToStr(self.domain)}", parent_children="{PARENT_CHILD.ToStr(self.parent_child)}">'
    
    # interfaces
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
    
