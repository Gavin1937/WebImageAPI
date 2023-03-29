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
