#! /bin/python3

########################################################
#                                                      #
#  Guild about new TwitterAgent for WebImageAPI        #
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


twitter_token = {
    'consumer_key': 'YOUR TWITTER consumer_key',
    'consumer_secret': 'YOUR TWITTER consumer_secret',
    'access_token': 'YOUR TWITTER access_token',
    'access_token_secret': 'YOUR TWITTER access_token_secret',
    'bearer_token': 'YOUR TWITTER bearer_token',
}

twitter_web_token = {
    'header_authorization': 'YOUR TWITTER HEADER authorization',
    'header_x_client_uuid': 'YOUR TWITTER HEADER x_client_uuid',
    'header_x_csrf_token': 'YOUR TWITTER HEADER x_csrf_token',
    'cookie_auth_token': 'YOUR TWITTER cookie auth_token',
    'cookie_ct0': 'YOUR TWITTER cookie ct0',
    'endpoint_userbyscreenname': 'YOUR TWITTER API ENDPOINT UNIQUE STR ID FOR UserByScreenName',
    'endpoint_usermedia': 'YOUR TWITTER API ENDPOINT UNIQUE STR ID FOR UserMedia',
    'endpoint_tweetdetail': 'YOUR TWITTER API ENDPOINT UNIQUE STR ID FOR TweetDetail',
}


# initialize WebImageAPI abstract class
agent = WebImageAPI()

# setup agents
agent.SetTwitterTokens('web' **twitter_web_token) # init a TwitterWebAgent
agent.SetTwitterTokens('dev', **twitter_token) # init a TwitterAgent
agent.SetTwitterTokens('both', **twitter_web_token, **twitter_token) # init both TwitterWebAgent & TwitterAgent


urls = [
'https://twitter.com/houk1se1',
'https://twitter.com/SimonCreativeTW/status/1212223385960210432',
]


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

