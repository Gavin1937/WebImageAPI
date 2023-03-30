
from __future__ import annotations
from enum import IntEnum

class DOMAIN(IntEnum):
    'enum class to represent & handle Website domains'
    
    INVALID   = -1,
    EMPTY     = 0,
    PIXIV     = 1,
    TWITTER   = 2,
    DANBOORU  = 3,
    YANDERE   = 4,
    KONACHAN  = 5,
    WEIBO     = 6,
    EHENTAI   = 7,
    
    def FromStr(domain:str) -> DOMAIN:
        if not isinstance(domain, str):
            raise ValueError('Invalid parameter "domain", it must be a string.')
        domain = domain.lower()
        if domain in ['pixiv','pixiv.net','pximg.net']:
            return DOMAIN.PIXIV
        elif domain in ['twitter','twitter.com','m.twitter.com']:
            return DOMAIN.TWITTER
        elif domain in ['danbooru','danbooru.donmai.us']:
            return DOMAIN.DANBOORU
        elif domain in ['yandere','yande.re']:
            return DOMAIN.YANDERE
        elif domain in ['konachan','konachan.com']:
            return DOMAIN.KONACHAN
        elif domain in ['weibo','m.weibo.cn']:
            return DOMAIN.WEIBO
        elif domain in ['ehentai','e-hentai','e-hentai.org']:
            return DOMAIN.EHENTAI
        else: # Invalid
            return DOMAIN.INVALID
    
    def FromUrl(url:str) -> DOMAIN:
        if not isinstance(url, str):
            raise ValueError('Invalid parameter "url", it must be a string.')
        if 'pixiv.net' in url or 'pximg.net' in url:
            return DOMAIN.PIXIV
        elif 'twitter.com' in url:
            return DOMAIN.TWITTER
        elif 'danbooru.donmai.us' in url:
            return DOMAIN.DANBOORU
        elif 'yande.re' in url:
            return DOMAIN.YANDERE
        elif 'konachan.com' in url:
            return DOMAIN.KONACHAN
        elif 'weibo.cn' in url:
            return DOMAIN.WEIBO
        elif 'e-hentai.org' in url:
            return DOMAIN.EHENTAI
        else: # Invalid
            return DOMAIN.INVALID
    
    def FromInt(domain:int) -> DOMAIN:
        if not isinstance(domain, int):
            raise ValueError('Invalid parameter "domain", it must be an integer.')
        return DOMAIN(domain)
    
    def ToStr(domain:DOMAIN) -> str:
        if not isinstance(domain, DOMAIN):
            raise ValueError('Invalid parameter "domain", it must be a DOMAIN enum.')
        if domain == DOMAIN.PIXIV:
            return "PIXIV"
        elif domain == DOMAIN.TWITTER:
            return "TWITTER"
        elif domain == DOMAIN.DANBOORU:
            return "DANBOORU"
        elif domain == DOMAIN.YANDERE:
            return "YANDERE"
        elif domain == DOMAIN.KONACHAN:
            return "KONACHAN"
        elif domain == DOMAIN.WEIBO:
            return "WEIBO"
        elif domain == DOMAIN.EHENTAI:
            return "EHENTAI"
        elif domain == DOMAIN.INVALID or domain == DOMAIN.EMPTY:
            return None


class PARENT_CHILD(IntEnum):
    'enum class to represent a parent/child state'
    
    INVALID   = -1,
    EMPTY     = 0,
    PARENT    = 1,
    CHILD     = 2,
    
    def ToStr(parent_child:PARENT_CHILD) -> str:
        if parent_child == PARENT_CHILD.PARENT:
            return 'PARENT'
        elif parent_child == PARENT_CHILD.CHILD:
            return 'CHILD'
        elif parent_child == PARENT_CHILD.INVALID:
            return 'INVALID'
        elif parent_child == PARENT_CHILD.EMPTY:
            return 'EMPTY'


