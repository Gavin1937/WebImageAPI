#! /bin/python3

########################################################
#                                                      #
#  Quick Start guild for WebImageAPI                   #
#                                                      #
#  Make sure you run this file from "demo" directory,  #
#  so it can load the WebImageAPI package properly     #
#                                                      #
#  Author: Gavin1937                                   #
#  GitHub: https://github.com/Gavin1937/WebImageAPI    #
#                                                      #
########################################################


# set path to parent in order to import WebImageAPI
import sys
sys.path.append('..')

# start here
from WebImageAPI import WebImageAPI


pixiv_token = {
    'refresh_token':'YOUR PIXIV refresh_token'
}

twitter_token = {
    'consumer_key': 'YOUR TWITTER consumer_key',
    'consumer_secret': 'YOUR TWITTER consumer_secret',
    'access_token': 'YOUR TWITTER access_token',
    'access_token_secret': 'YOUR TWITTER access_token_secret',
    'bearer_token': 'YOUR TWITTER bearer_token',
}

ehentai_token = {
    'ipb_member_id': 'YOUR EHENTAI ipb_member_id',
    'ipb_pass_hash': 'YOUR EHENTAI ipb_pass_hash',
}


# initialize WebImageAPI abstract class
agent = WebImageAPI()

# setup agents
agent.SetPixivTokens(**pixiv_token) # required if you need to access pixiv
agent.SetTwitterTokens(**twitter_token) # required if you need to access twitter
agent.SetEHentaiAuthInfo(**ehentai_token) # optional for downloading original image from eh


urls = [
'https://www.pixiv.net/users/11764388',
'https://www.pixiv.net/artworks/76142002',
'https://twitter.com/houk1se1',
'https://twitter.com/SimonCreativeTW/status/1212223385960210432',
'https://danbooru.donmai.us/posts?tags=nagishiro_mito',
'https://danbooru.donmai.us/posts/6159304',
'https://yande.re/post?tags=nagishiro_mito&page=2',
'https://yande.re/post/show/1059321',
'https://konachan.com/post?tags=nagishiro_mito',
'https://konachan.com/post/show/355165',
'https://m.weibo.cn/u/1954940747',
'https://m.weibo.cn/detail/4883581258435481',
'https://e-hentai.org/g/2510385/e39a66a86e/',
'https://e-hentai.org/s/9b00cf1ccc/2510385-1',
]

# use additional features from specific Agents
print(agent.GetPixivAgent().GetAPI())
print(agent.GetTwitterAgent().GetAPI())


for idx, url in enumerate(urls):
    print('\n\n', idx+1, ':', url)
    
    # convert url str to dedicated WebItemInfo
    item = agent.UrlToWebItemInfo(url)
    print(item)
    
    # use common Agents methods
    res = agent.FetchItemInfoDetail(item)
    # res = agent.FetchParentChildren(item, page=2)
    # res = agent.FetchUserInfo(item)
    
    print(res)
    
    # agent.DownloadItem(item, './down')

