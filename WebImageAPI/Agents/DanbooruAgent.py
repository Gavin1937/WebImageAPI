
from .BaseAgent import BaseAgent
from .Singleton import Singleton
from ..Types import DanbooruItemInfo, UserInfo, DOMAIN
from ..Utils import (
    TypeChecker, TypeMatcher,
    Clamp, MergeDeDuplicate,
    getSrcJson, getSrcStr, downloadFile,
    PROJECT_USERAGENT, UrlParser
)
from typing import Union
from pathlib import Path
from bs4 import BeautifulSoup


@Singleton
class DanbooruAgent(BaseAgent):
    
    def __init__(self):
        # in order to use danbooru's api,
        # we need to set a custom user-agent for this project
        # instead of pretending to be a browser,
        # which will make the project get banned by cloudflare
        # details: https://github.com/mikf/gallery-dl/issues/3665
        # danbooru api: https://danbooru.donmai.us/wiki_pages/help%3Aapi
        self.__headers = { 'User-Agent': PROJECT_USERAGENT }
        super().__init__()
    
    # interfaces
    @TypeChecker(DanbooruItemInfo, (1,))
    def FetchItemInfoDetail(self, item_info:DanbooruItemInfo) -> DanbooruItemInfo:
        '''
        Fetch & Fill-In "detail" parameter for supplied DanbooruItemInfo.
        Param:
            item_info  => DanbooruItemInfo to fetch
        Returns:
            updated DanbooruItemInfo
        '''
        
        if item_info.IsParent() or item_info.IsChild():
            item_info.details = getSrcJson(self.__NormalURLToApi(item_info.url), self.__headers)
        else:
            raise ValueError('Input DanbooruItemInfo is empty or invalid.')
        
        return item_info
    
    @TypeMatcher(['self', DanbooruItemInfo, int])
    def FetchParentChildren(self, item_info:DanbooruItemInfo, page:int=1) -> list:
        '''
        Fetch a Parent DanbooruItemInfo\'s Children
        Param:
            item_info  => DanbooruItemInfo Parent to fetch
            page       => int page number >= 1
        Returns:
            list of DanbooruItemInfo fetched, also edit original "item_info"
        '''
        
        if not item_info.IsParent():
            raise ValueError('Input DanbooruItemInfo must be a parent.')
        
        page = Clamp(page, 1)
        url = self.__NormalURLToApi(item_info.url, {'page':[page]})
        item_info.details = getSrcJson(url, self.__headers)
        
        output = []
        for post in item_info.details:
            output.append(DanbooruItemInfo.FromChildDetails(post))
        
        return output
    
    @TypeChecker(DanbooruItemInfo, (1,))
    def FetchUserInfo(self, item_info:DanbooruItemInfo, old_user_info:UserInfo=None) -> UserInfo:
        '''
        Fetch a DanbooruItemInfo\'s UserInfo
        Param:
            item_info        => DanbooruItemInfo Parent to fetch
            old_user_info    => UserInfo that already fill up by other agents,
                                this function will collect additional UserInfo from current domain,
                                and append to old_user_info and return it at the end.
                                (default None)
        Returns:
            UserInfo object
        '''
        
        if item_info.details is None:
            item_info = self.FetchItemInfoDetail(item_info)
        
        if item_info.IsParent():
            artist_tag = item_info.details[0]['tag_string_artist'].split(' ')[0]
        elif item_info.IsChild():
            artist_tag = item_info.details['tag_string_artist'].split(' ')[0]
        url = f'https://danbooru.donmai.us/artists.json?only=id,name,group_name,other_names,is_banned,is_deleted,created_at,updated_at,urls&search[name]={artist_tag}'
        user = getSrcJson(url, self.__headers)[0]
        
        domain = DOMAIN.DANBOORU
        name_list = [user['name'], *user['other_names']]
        url_dict = {domain:[url['url'] for url in user['urls'] if url['is_active']]}
        if old_user_info is not None:
            old_user_info.name_list = MergeDeDuplicate(old_user_info.name_list, name_list)
            if domain in old_user_info.url_dict:
                old_user_info.url_dict[domain] += url_dict[domain]
            else:
                old_user_info.url_dict[domain] = url_dict[domain]
            old_user_info.url_dict[domain] = MergeDeDuplicate(old_user_info.url_dict[domain])
            old_user_info.details[domain] = user
            return old_user_info
        return UserInfo(name_list, url_dict, {domain:user})
    
    @TypeChecker(DanbooruItemInfo, (1,))
    def DownloadItem(self, item_info:DanbooruItemInfo, output_path:Union[str,Path], replace:bool=False):
        '''
        Download a supplied DanbooruItemInfo
        Param:
            item_info    => DanbooruItemInfo Child to download
            output_path  => str|Path of a directory for downloaded file
            replace      => bool flag, whether replace if download file already exists
        '''
        
        if not item_info.IsChild():
            raise ValueError('Cannot download non-child DanbooruItemInfo.')
        
        output_path = Path(output_path)
        if not output_path.is_dir():
            raise ValueError('Output path should be a directory path.')
        
        # get item source url from html to retrieve filename with tags
        html = getSrcStr(item_info.url, self.__headers)
        soup = BeautifulSoup(html, 'lxml')
        url = soup.select_one('#post-info-size a').get('href')
        filename = url.split('/')[-1]
        downloadFile(url, output_path/filename, overwrite=replace)
    
    
    # private helper function
    def __NormalURLToApi(self, url:str, update_qs:dict={}) -> str:
        parsed = UrlParser(url)
        parsed.pathlist[-1] += '.json'
        parsed.UpdatePathList(parsed.pathlist)
        parsed.query.update(update_qs)
        parsed.UpdateQuery(parsed.query)
        return parsed.url
    
    # danbooru's api provides a file_url with filename:
    # {filemd5}.{filext}
    # 
    # but its html posts page provides a file_url with filename:
    # __{character_tags}_{copyright_tag}_drawn_by_{artist_tag}__{filemd5}.{filext}
    # 
    # this function tries to generate tagged posts filename just like the one show up in html.
    # however, all the tags in html page filename are sorted ascending by their posts count.
    # currently, the only way we can achieve the same thing is to search tags one by one,
    # which is useless comparing to just fetch the whole html page.
    # 
    # this function's filename output is valid even with wrong tag order.
    # if you remove the filename in file_url returned by danbooru posts api,
    # and replace with this one, it's a valid file_url.
    def __GenTaggedFilename(
        self,
        character_taglist:list,
        copyright_taglist:list,
        artist_taglist:list,
        filemd5:str, fileext:str
    ) -> str:
        
        
        # tag string pre-process logic
        # danbooru source:
        # https://github.com/danbooru/danbooru/blob/master/app/presenters/tag_set_presenter.rb
        # function humanized_essential_tag_string
        
        # character tags
        # removes meta tags inside character tags (quoted in parentheses "()")
        # cause I think danbooru can get pure name tags from their database
        characters = map(lambda c:re.sub(r'_\(.*\)','',c), character_taglist[:5])
        characters = '_'+'_'.join(characters)
        characters += f'_and_{len(character_taglist)-5}_more' if len(character_taglist) > 5 else ''
        
        # copyright tags
        copyrights = '_'+'_'.join(copyright_taglist[:1])
        copyrights += f'_and_{len(copyright_taglist)-1}_more' if len(copyright_taglist) > 1 else ''
        copyrights = copyrights if characters and len(characters) > 0 and copyrights and len(copyrights) > 0 else ''
        
        # artist tags
        artists = '_'+'_'.join(filter(('banned_artist').__ne__, artist_taglist))
        artists = f'_drawn_by{artists}'
        
        # tag string combination & post-processing
        # danbooru source:
        # https://github.com/danbooru/danbooru/blob/master/app/models/post.rb
        # function seo_tags
        # danbooru uses following regex substitution to post-process tag strings
        # I modify it a bit to match the final filename
        
        import re
        
        # final regex sub
        filename = '_' + characters.strip() + copyrights.strip() + artists.strip()
        filename = re.sub(r'[^a-z0-9]+', r'_', filename)
        filename = re.sub(r'(?:^_+)|(?:_+$)', r'', filename)
        filename = re.sub(r'_{2,}', r'_', filename)
        filename = '__' + filename + '__' + filemd5 + '.' + fileext
        
        return filename
