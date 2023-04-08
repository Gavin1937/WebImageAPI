
from __future__ import annotations
from .WebItemInfo import WebItemInfo
from .Types import DOMAIN, PARENT_CHILD


class PixivItemInfo(WebItemInfo):
    def __init__(self, url) -> None:
        self.pid:int = None
        super().__init__(url)
    
    def _PostInitAnalyzing(self) -> None:
        if self.domain != DOMAIN.PIXIV:
            raise ValueError('Invalid url, you must supply a pixiv url.')
        
        pathlist = self.parsed_url.pathlist
        if 'users' in pathlist:
            self.parent_child = PARENT_CHILD.PARENT
            self.pid = int(pathlist[pathlist.index('users')+1])
        elif 'artworks' in pathlist:
            self.parent_child = PARENT_CHILD.CHILD
            self.pid = int(pathlist[pathlist.index('artworks')+1])
        elif 'member.php' == pathlist[-1]:
            self.parent_child = PARENT_CHILD.PARENT
            self.pid = int(self.parsed_url.query['id'][0])
        elif 'member_illust.php' == pathlist[-1]:
            self.parent_child = PARENT_CHILD.CHILD
            self.pid = int(self.parsed_url.query['id'][0])
        elif 'pximg.net' in self.parsed_url.domain:
            self.parent_child = PARENT_CHILD.CHILD
            self.pid = int(pathlist[-1].split('_')[0])
    
    def FromChildDetails(details) -> PixivItemInfo:
        output = PixivItemInfo(
            f'https://www.pixiv.net/artworks/{details["id"]}'
        )
        output.details = details
        return output


class TwitterItemInfo(WebItemInfo):
    def __init__(self, url) -> None:
        self.screen_name:str = None
        self.status_id:str = None
        super().__init__(url)
    
    def _PostInitAnalyzing(self) -> None:
        if self.domain != DOMAIN.TWITTER:
            raise ValueError('Invalid url, you must supply a twitter url.')
        
        pathlist = self.parsed_url.pathlist
        if 'status' in pathlist:
            self.parent_child = PARENT_CHILD.CHILD
            self.screen_name = pathlist[0]
            self.status_id = pathlist[2]
        else: # 'status' not in pathlist
            self.parent_child = PARENT_CHILD.PARENT
            self.screen_name = pathlist[0]
    
    def FromChildDetails(details) -> TwitterItemInfo:
        output = TwitterItemInfo(
            f'https://twitter.com/{details["user"]["screen_name"]}/status/{details["id_str"]}'
        )
        output.details = details
        return output


class DanbooruItemInfo(WebItemInfo):
    def _PostInitAnalyzing(self) -> None:
        if self.domain != DOMAIN.DANBOORU:
            raise ValueError('Invalid url, you must supply a danbooru url.')
        
        pathlist = self.parsed_url.pathlist
        if 'posts' == pathlist[-1]:
            self.parent_child = PARENT_CHILD.PARENT
        elif 'posts' == pathlist[-2]:
            self.parent_child = PARENT_CHILD.CHILD
    
    def FromChildDetails(details) -> DanbooruItemInfo:
        output = DanbooruItemInfo(
            f'https://danbooru.donmai.us/posts/{details["id"]}'
        )
        output.details = details
        return output


class YandereItemInfo(WebItemInfo):
    def _PostInitAnalyzing(self) -> None:
        if self.domain != DOMAIN.YANDERE:
            raise ValueError('Invalid url, you must supply a yande.re url.')
        
        pathlist = self.parsed_url.pathlist
        if 'post' == pathlist[0] and len(pathlist) == 1:
            self.parent_child = PARENT_CHILD.PARENT
        elif 'post' == pathlist[0] and 'show' == pathlist[1]:
            self.parent_child = PARENT_CHILD.CHILD
    
    def FromChildDetails(details) -> YandereItemInfo:
        output = YandereItemInfo(
            f'https://yande.re/post/show/{details["posts"][0]["id"]}'
        )
        output.details = details
        return output


class KonachanItemInfo(WebItemInfo):
    def _PostInitAnalyzing(self) -> None:
        if self.domain != DOMAIN.KONACHAN:
            raise ValueError('Invalid url, you must supply a konachan.com url.')
        
        pathlist = self.parsed_url.pathlist
        if 'post' == pathlist[0] and len(pathlist) == 1:
            self.parent_child = PARENT_CHILD.PARENT
        elif 'post' == pathlist[0] and 'show' == pathlist[1]:
            self.parent_child = PARENT_CHILD.CHILD
    
    def FromChildDetails(details) -> KonachanItemInfo:
        output = KonachanItemInfo(
            f'https://konachan.com/post/show/{details["posts"][0]["id"]}'
        )
        output.details = details
        return output


class WeiboItemInfo(WebItemInfo):
    def __init__(self, url) -> None:
        self.weibo_id:str = None
        super().__init__(url)
    
    def _PostInitAnalyzing(self) -> None:
        if self.domain != DOMAIN.WEIBO:
            raise ValueError('Invalid url, you must supply a m.weibo.cn url.')
        
        pathlist = self.parsed_url.pathlist
        if 'u' == pathlist[0]:
            self.parent_child = PARENT_CHILD.PARENT
        elif 'detail' == pathlist[0]:
            self.parent_child = PARENT_CHILD.CHILD
        self.weibo_id = pathlist[1]
    
    def FromChildDetails(details) -> WeiboItemInfo:
        if 'id' in details:
            output = WeiboItemInfo(
                f'https://m.weibo.cn/detail/{details["id"]}'
            )
        elif 'mblog' in details and 'id' in details['mblog']:
            output = WeiboItemInfo(
                f'https://m.weibo.cn/detail/{details["mblog"]["id"]}'
            )
        output.details = details
        return output


class EHentaiItemInfo(WebItemInfo):
    def __init__(self, url) -> None:
        self.gallery_id:str = None
        self.other:dict = None
        super().__init__(url)
    
    def _PostInitAnalyzing(self) -> None:
        if self.domain != DOMAIN.EHENTAI:
            raise ValueError('Invalid url, you must supply a m.weibo.cn url.')
        
        pathlist = self.parsed_url.pathlist
        if 'g' == pathlist[0]:
            self.parent_child = PARENT_CHILD.PARENT
            self.gallery_id = pathlist[1]
            self.other = {'gallery_token':pathlist[2]}
        elif 's' == pathlist[0]:
            self.parent_child = PARENT_CHILD.CHILD
            tmp = pathlist[2].split('-')
            self.gallery_id = tmp[0]
            self.other = {'page_token':pathlist[1], 'pagenumber':tmp[1]}
    
    def FromChildDetails(details) -> EHentaiItemInfo:
        if 'gmetadata' in details:
            gallery_id = details['gmetadata']['gid']
            gallery_token = details['gmetadata']['token']
            output = EHentaiItemInfo(
                f'https://e-hentai.org/g/{gallery_id}/{gallery_token}/'
            )
        elif 'tokenlist' in details and 'page_token' in details:
            gallery_id = details['tokenlist'][0]['gid']
            output = EHentaiItemInfo(
                f'https://e-hentai.org/s/{details["page_token"]}/{gallery_id}-1'
            )
        else:
            return None
        output.details = details
        return output
