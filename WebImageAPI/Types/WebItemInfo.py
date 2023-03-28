
from typing import Union
from .Types import DOMAIN, PARENT_CHILD
from ..Utils import UrlParser

class WebItemInfo:
    'Basic class contains Web Item Informations'
    
    def __init__(self, url:str):
        self.url:str = url
        self.url_parser = UrlParser(self.url)
        self.domain:DOMAIN = DOMAIN.FromStr(self.url_parser.domain)
        self.parent_child:PARENT_CHILD = PARENT_CHILD.EMPTY

