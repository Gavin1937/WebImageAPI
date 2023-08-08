
<details>

<summary><strong style="font-size:large;">
Table Of Content
</strong></summary>

* [1. Terminology](#1-terminology)
* [2. class BaseAgent](#2-class-baseagent)
  * [Methods](#methods)
    * [**FetchItemInfoDetail(BaseAgent, item\_info:WebItemInfo) -\> WebItemInfo:**](#fetchiteminfodetailbaseagent-item_infowebiteminfo---webiteminfo)
    * [**FetchParentChildren(BaseAgent, item\_info:WebItemInfo, page:int=1) -\> list:**](#fetchparentchildrenbaseagent-item_infowebiteminfo-pageint1---list)
    * [**FetchUserInfo(BaseAgent, item\_info:WebItemInfo, old\_user\_info:UserInfo=None) -\> UserInfo:**](#fetchuserinfobaseagent-item_infowebiteminfo-old_user_infouserinfonone---userinfo)
    * [**DownloadItem(BaseAgent, item\_info:WebItemInfo, output\_path:Union\[str,Path\], replace:bool=False):**](#downloaditembaseagent-item_infowebiteminfo-output_pathunionstrpath-replaceboolfalse)
* [3. About Singleton](#3-about-singleton)
  * [Methods](#methods-1)
    * [**instance(self, \*args, \*\*kwargs):**](#instanceself-args-kwargs)
* [4. class PixivAgent](#4-class-pixivagent)
  * [Additional Methods](#additional-methods)
    * [**\_\_init\_\_(PixivAgent, refresh\_token:str, max\_try:int=5):**](#__init__pixivagent-refresh_tokenstr-max_tryint5)
    * [**GetAPI(PixivAgent) -\> AppPixivAPI:**](#getapipixivagent---apppixivapi)
    * [**GetParentItemInfo(PixivAgent, item\_info:PixivItemInfo) -\> PixivItemInfo:**](#getparentiteminfopixivagent-item_infopixiviteminfo---pixiviteminfo)
    * [**IsFollowedUser(PixivAgent, item\_info:PixivItemInfo) -\> bool:**](#isfolloweduserpixivagent-item_infopixiviteminfo---bool)
    * [**FollowUser(PixivAgent, item\_info:PixivItemInfo) -\> bool:**](#followuserpixivagent-item_infopixiviteminfo---bool)
    * [**UnfollowUser(PixivAgent, item\_info:PixivItemInfo) -\> bool:**](#unfollowuserpixivagent-item_infopixiviteminfo---bool)
    * [**IsAIArtwork(PixivAgent, item\_info:PixivItemInfo) -\> bool:**](#isaiartworkpixivagent-item_infopixiviteminfo---bool)
    * [**FetchParentChildrenById(PixivAgent, item\_info:PixivItemInfo, operator:str, id:int, max\_page:int=10) -\> list:**](#fetchparentchildrenbyidpixivagent-item_infopixiviteminfo-operatorstr-idint-max_pageint10---list)
    * [**DownloadRawUrl(PixivAgent, raw\_url:str, output\_path:Union\[str,Path\], replace:bool=False):**](#downloadrawurlpixivagent-raw_urlstr-output_pathunionstrpath-replaceboolfalse)
* [5. class TwitterAgent](#5-class-twitteragent)
  * [Additional Methods](#additional-methods-1)
    * [**\_\_init\_\_(TwitterAgent, consumer\_key:str, consumer\_secret:str, access\_token:str, access\_token\_secret:str, bearer\_token:str, proxies:dict=None, max\_try:int=5):**](#__init__twitteragent-consumer_keystr-consumer_secretstr-access_tokenstr-access_token_secretstr-bearer_tokenstr-proxiesdictnone-max_tryint5)
    * [**GetAPI(TwitterAgent) -\> tweepy.API:**](#getapitwitteragent---tweepyapi)
    * [**SetProxies(TwitterAgent, proxies:dict):**](#setproxiestwitteragent-proxiesdict)
    * [**GetParentItemInfo(TwitterAgent, item\_info:TwitterItemInfo) -\> TwitterItemInfo:**](#getparentiteminfotwitteragent-item_infotwitteriteminfo---twitteriteminfo)
    * [**IsFollowedUser(TwitterAgent, item\_info:TwitterItemInfo) -\> bool:**](#isfollowedusertwitteragent-item_infotwitteriteminfo---bool)
    * [**FollowUser(TwitterAgent, item\_info:TwitterItemInfo) -\> bool:**](#followusertwitteragent-item_infotwitteriteminfo---bool)
    * [**UnfollowUser(TwitterAgent, item\_info:TwitterItemInfo) -\> bool:**](#unfollowusertwitteragent-item_infotwitteriteminfo---bool)
* [6. class TwitterWebAgent](#6-class-twitterwebagent)
  * [Additional Methods](#additional-methods-2)
    * [**\_\_init\_\_(TwitterWebAgent, ...):**](#__init__twitterwebagent-)
    * [**SetProxies(TwitterWebAgent, proxies:dict):**](#setproxiestwitterwebagent-proxiesdict)
    * [**GetParentItemInfo(TwitterWebAgent, item\_info:TwitterItemInfo) -\> TwitterItemInfo:**](#getparentiteminfotwitterwebagent-item_infotwitteriteminfo---twitteriteminfo)
    * [**IsFollowedUser(TwitterWebAgent, item\_info:TwitterItemInfo) -\> bool:**](#isfollowedusertwitterwebagent-item_infotwitteriteminfo---bool)
* [7. class DanbooruAgent](#7-class-danbooruagent)
  * [Additional Methods](#additional-methods-3)
    * [**\_\_init\_\_(DanbooruAgent, proxies:dict=None):**](#__init__danbooruagent-proxiesdictnone)
    * [**SetProxies(DanbooruAgent, proxies:dict):**](#setproxiesdanbooruagent-proxiesdict)
    * [**FindSource(DanbooruAgent, item\_info:DanbooruItemInfo) -\> str:**](#findsourcedanbooruagent-item_infodanbooruiteminfo---str)
* [8. class YandereAgent](#8-class-yandereagent)
  * [Additional Methods](#additional-methods-4)
    * [**\_\_init\_\_(YandereAgent, proxies:dict=None):**](#__init__yandereagent-proxiesdictnone)
    * [**SetProxies(YandereAgent, proxies:dict):**](#setproxiesyandereagent-proxiesdict)
    * [**FindSource(YandereAgent, item\_info:YandereItemInfo) -\> str:**](#findsourceyandereagent-item_infoyandereiteminfo---str)
* [9. class KonachanAgent](#9-class-konachanagent)
  * [Additional Methods](#additional-methods-5)
    * [**\_\_init\_\_(KonachanAgent, proxies:dict=None):**](#__init__konachanagent-proxiesdictnone)
    * [**SetProxies(KonachanAgent, proxies:dict):**](#setproxieskonachanagent-proxiesdict)
    * [**FindSource(KonachanAgent, item\_info:KonachanItemInfo) -\> str:**](#findsourcekonachanagent-item_infokonachaniteminfo---str)
* [10. class WeiboAgent](#10-class-weiboagent)
  * [Additional Methods](#additional-methods-6)
    * [**\_\_init\_\_(WeiboAgent, proxies:dict=None):**](#__init__weiboagent-proxiesdictnone)
    * [**SetProxies(WeiboAgent, proxies:dict):**](#setproxiesweiboagent-proxiesdict)
* [11. class EHentaiAgent](#11-class-ehentaiagent)
  * [E-Hentai Peek Hour](#e-hentai-peek-hour)
  * [Additional Methods](#additional-methods-7)
    * [**\_\_init\_\_(EHentaiAgent, ipb\_member\_id:str=None, ipb\_pass\_hash:str=None, proxies:dict=None):**](#__init__ehentaiagent-ipb_member_idstrnone-ipb_pass_hashstrnone-proxiesdictnone)
    * [**SetProxies(EHentaiAgent, proxies:dict):**](#setproxiesehentaiagent-proxiesdict)
    * [**SetEHentaiAuthInfo(EHentaiAgent, ipb\_member\_id:str, ipb\_pass\_hash:str):**](#setehentaiauthinfoehentaiagent-ipb_member_idstr-ipb_pass_hashstr)
    * [**GetIgnorePeekHour(EHentaiAgent) -\> bool:**](#getignorepeekhourehentaiagent---bool)
    * [**SetIgnorePeekHour(EHentaiAgent, whether\_ignore:bool):**](#setignorepeekhourehentaiagent-whether_ignorebool)
    * [**InPeekHour(self) -\> bool:**](#inpeekhourself---bool)
    * [**GetNextPeekHour(self) -\> tuple:**](#getnextpeekhourself---tuple)

</details>

<br>


# 1. Terminology

Agents in WebImageAPI are special singleton classes that handles requests to supported websites.

They usually take in a WebItemInfo and make http requests to target websites using supplied WebItemInfo.

# 2. class BaseAgent

Base class for WebImageAPI agents

This class only contains virtual protected functions for its child classes and it is not a singleton class.

You should not call any function directly from `BaseAgent` class.

If you do so, functions in `BaseAgent` will raise NotImplementedError

Note:

1. The documentation of other `Agents` classes will not repeat common interfaces that `BaseAgent` has, and focus on the differences of interfaces comparing to this base class.

2. All child class of `BaseAgent` have strict requirement about the type of `WebItemInfo` pass into their methods. For example, `PixivAgent` only accept `PixivItemInfo`. if the item info you pass in is not an instance of `PixivItemInfo`, it will fail you with a ValueError.

3. For simplicity, I recommend using wrapper methods in [class WebImageAPI](../WebImageAPI.md#1-class-webimageapi) unless you want to use special/additional methods provided by different `Agents`.

## Methods

### **FetchItemInfoDetail(BaseAgent, item_info:WebItemInfo) -> WebItemInfo:**

* Fetch & Fill-In `detail` member for supplied WebItemInfo.
* Paremters
  * **item_info**:   WebItemInfo to fetch
* Returns:
  * updated WebItemInfo

### **FetchParentChildren(BaseAgent, item_info:WebItemInfo, page:int=1) -> list:**

* Fetch a Parent WebItemInfo's Children
* Parameters:
  * **item_info**:   WebItemInfo Parent to fetch
  * **page**:        int page number >= 1
* Returns:
  * list of WebItemInfo fetched, also edit original `item_info`

### **FetchUserInfo(BaseAgent, item_info:WebItemInfo, old_user_info:UserInfo=None) -> UserInfo:**

* Fetch a WebItemInfo's UserInfo
* Parameters:
  * **item_info**:         PixivItemInfo Parent to fetch
  * **old_user_info**:     UserInfo that already fill up by  agents.
    * this function will collect additional UserInfo from current domain, and append to old_user_info and return it at the end.
    * (default None)
* Returns:
  * [UserInfo object](../index.md#class-userinfo)

### **DownloadItem(BaseAgent, item_info:WebItemInfo, output_path:Union[str,Path], replace:bool=False):**

* Download supplied WebItemInfo
* Parameters:
  * **item_info**:     WebItemInfo Child to download
  * **output_path**:   string | pathlib.Path of a directory for downloaded file
  * **replace**:       boolean flag, whether replace if download file already exists

# 3. About Singleton

All child class of `BaseAgent` are [singleton classes](https://en.wikipedia.org/wiki/Singleton_pattern).

I made this design decision because I don't want to initialize the same `Agent` class multiple times during the run time, so I use singleton to avoid re-initialization and duplicating authentication sessions.

## Methods

### **instance(self, \*args, \*\*kwargs):**

* All singleton class in WebImageAPI should be invoke through this function.
* It will create a new instance of the class when you call it the first time.
* And it will return the existing instance when you call it the second time and more.
* Note that, for some `Agents`, you need to pass in your authentication tokens at the first time calling this function in order  to authenticate the api.

# 4. class PixivAgent

Child class of [BaseAgent](#2-class-baseagent) for handling requests to [pixiv](https://www.pixiv.net/)

Sharing all the common members and methods from base class.

This Agent only accept [PixivItemInfo](./WebItemInfo.md#2-class-pixiviteminfo)

## Additional Methods

### **\_\_init\_\_(PixivAgent, refresh_token:str, max_try:int=5):**

* Constructor for PixivAgent class
* You need to pass in required/optional parameters for authentication in [PixivAgent.instance() function](#instanceself-args)
* Parameters:
  * **refresh_token**:  string, pixiv refresh_token
  * **max_try**:        integer, max retry number
* When you initialize this Agent, it will use pixivpy3.AppPixivAPI.auth() function with your `refresh_token` to retrieve a new `access_token` from pixiv, which will cause your existing `access_token` to expire.

### **GetAPI(PixivAgent) -> AppPixivAPI:**

* Get pixivpy3.AppPixivAPI object created in the background

### **GetParentItemInfo(PixivAgent, item_info:PixivItemInfo) -> PixivItemInfo:**

* Get the parent PixivItemInfo for a child PixivItemInfo.
* Parameters:
  * **item_info**: PixivItemInfo Child
* Returns:
  * A parent PixivItemInfo

### **IsFollowedUser(PixivAgent, item_info:PixivItemInfo) -> bool:**

* Is input PixivItemInfo points to an user that is followed by current account.
* Parameters:
  * **item_info**: PixivItemInfo to check
* Returns:
  * True if is followed
  * False if not

### **FollowUser(PixivAgent, item_info:PixivItemInfo) -> bool:**

* Follow an user that item_info points to.
* Parameters:
  * **item_info**: PixivItemInfo Parent to check
* Returns:
  * True if success
  * False if failed

### **UnfollowUser(PixivAgent, item_info:PixivItemInfo) -> bool:**

* Unfollow an user that item_info points to.
* Parameters:
  * **item_info**: PixivItemInfo Parent to check
* Returns:
  * True if success
  * False if failed

### **IsAIArtwork(PixivAgent, item_info:PixivItemInfo) -> bool:**

* Is input child PixivItemInfo points to an AI-Generated artwork
* Parameters:
  * **item_info**: PixivItemInfo Child to check
* Returns:
  * True if is AI-Generated artwork
  * False if not

### **FetchParentChildrenById(PixivAgent, item_info:PixivItemInfo, operator:str, id:int, max_page:int=10) -> list:**

* Fetch a Parent PixivItemInfo\'s Children by comparing with children id
* Parameters:
  * **item_info**: PixivItemInfo Parent to fetch
  * **operator**: str one comparison operators. Valid operators: <, >, <=, >=, =, ==, !=
  * **id**: int id number >= 1
  * **max_page**: maximum page to search, default 10
* Returns:
  * list of PixivItemInfo fetched, also edit original "item_info"

### **DownloadRawUrl(PixivAgent, raw_url:str, output_path:Union[str,Path], replace:bool=False):**

* Download a supplied pixiv raw url
* Raw url have domain: i.pximg.net
* Parameters:
  * **raw_url**: str raw url to download
  * **output_path**: str|Path of a directory for downloaded file
  * **replace**: bool flag, whether replace if download file already exists

# 5. class TwitterAgent

Child class of [BaseAgent](#2-class-baseagent) for handling requests to [twitter](https://twitter.com/)

Sharing all the common members and methods from base class.

This Agent only accept [TwitterItemInfo](./WebItemInfo.md#3-class-twitteriteminfo)

**This agent is backed by twitter developer api.**

* Starting from early 2023, twitter force its free tier developer api to be write-only.
* Thus, I need to replace TwitterAgent's backend with twitter's web client api.
* checkout following articles for detail:
  * [https://developer.twitter.com/en/docs/twitter-api](https://developer.twitter.com/en/docs/twitter-api)
  * [https://twittercommunity.com/t/453-you-currently-have-access-to-twitter-api-v2-endpoints-and-limited-v1-1-endpoints-only/194140](https://twittercommunity.com/t/453-you-currently-have-access-to-twitter-api-v2-endpoints-and-limited-v1-1-endpoints-only/194140)

## Additional Methods

### **\_\_init\_\_(TwitterAgent, consumer_key:str, consumer_secret:str, access_token:str, access_token_secret:str, bearer_token:str, proxies:dict=None, max_try:int=5):**

* Constructor for TwitterAgent class
* You need to pass in required/optional parameters for authentication in [TwitterAgent.instance() function](#instanceself-args)
* Parameters:
  * **consumer_key**:         string, twitter cunsumer api key
  * **consumer_secret**:      string, twitter consumer api secret
  * **access_token**:         string, twitter access token
  * **access_token_secret**:  string, twitter access token secret
  * **bearer_token**:         string, twitter bearer token
  * **proxies**:              dictionary, proxy server urls, default None, disabled. (e.g. `{'http':'http://localhost', 'https':'https://localhost'}`)
  * **max_try**:              integer, max retry number
* This Agent uses tweepy.OAuth1UserHandler() and tweepy.API() to authenticate with twitter.
* [2023-04-01]: Twitter will change their api policy within 30 days. Therefore, this Agent may be affect by the api policy changes.
* [2023-06-26]: Twitter developer api free tier is now write-only. That means TwitterAgent is pretty much unusable with a free tier twitter dev account. (maybe you still can use follow & unfollow feature?) Use TwitterWebAgent instead.

### **GetAPI(TwitterAgent) -> tweepy.API:**

* Get tweepy.API object created in the background

### **SetProxies(TwitterAgent, proxies:dict):**

* Set proxy for TwitterAgent
* This function will perform a re-authentication with Twitter
* Parameters
  * **proxies**:              dictionary, proxy server urls. (e.g.: `{'http':'http://localhost', 'https':'https://localhost'}`)

### **GetParentItemInfo(TwitterAgent, item_info:TwitterItemInfo) -> TwitterItemInfo:**

* Get the parent TwitterItemInfo for a child TwitterItemInfo.
* Parameters:
  * **item_info**: TwitterItemInfo Child
* Returns:
  * A parent TwitterItemInfo

### **IsFollowedUser(TwitterAgent, item_info:TwitterItemInfo) -> bool:**

* Is input TwitterItemInfo points to an user that is followed by current account.
* Parameters:
  * **item_info**: TwitterItemInfo to check
* Returns:
  * True if is followed
  * False if not

### **FollowUser(TwitterAgent, item_info:TwitterItemInfo) -> bool:**

* Follow an user that item_info points to.
* The proxy setting does not apply to this function.
* Parameters:
  * **item_info**: TwitterItemInfo Parent to check
* Returns:
  * True if success
  * False if failed

### **UnfollowUser(TwitterAgent, item_info:TwitterItemInfo) -> bool:**

* Unfollow an user that item_info points to.
* The proxy setting does not apply to this function.
* Parameters:
  * **item_info**: TwitterItemInfo Parent to check
* Returns:
  * True if success
  * False if failed

# 6. class TwitterWebAgent

Child class of [BaseAgent](#2-class-baseagent) for handling requests to [twitter](https://twitter.com/)

Sharing all the common members and methods from base class.

This Agent only accept [TwitterItemInfo](./WebItemInfo.md#3-class-twitteriteminfo)

**This agent is backed by twitter web client api.**

* Starting from early 2023, twitter force its free tier developer api to be write-only.
* Thus, I need to replace TwitterAgent's backend with twitter's web client api.
* checkout following articles for detail:
  * [https://developer.twitter.com/en/docs/twitter-api](https://developer.twitter.com/en/docs/twitter-api)
  * [https://twittercommunity.com/t/453-you-currently-have-access-to-twitter-api-v2-endpoints-and-limited-v1-1-endpoints-only/194140](https://twittercommunity.com/t/453-you-currently-have-access-to-twitter-api-v2-endpoints-and-limited-v1-1-endpoints-only/194140)

## Additional Methods

### **\_\_init\_\_(TwitterWebAgent, ...):**

* Constructor for TwitterWebAgent class
* You need to pass in required/optional parameters for authentication in [TwitterWebAgent.instance() function](#instanceself-args)

* To initialize this agent, you need to collect following stuff from your browser.

* From request header to twitter api:
  * **Authorization**
  * **X-Client-Uuid**
  * **X-Csrf-Token**

* From cookies:
  * **auth_token**
  * **ct0**

* twitter api endpoints:
  * Twitter's web client api endpoints are in this format:
  * `https://twitter.com/i/api/graphql/{UNIQUE_STR_ID}/{ENDPOINT_NAME}`
  * where `{UNIQUE_STR_ID}` is an unique str id for its dedicated `{ENDPOINT_NAME}`
  * We need to use 3 endpoints in this agent: `UserByScreenName`, `UserMedia`, `TweetDetail`
  * So, you need to find their dedicate `{UNIQUE_STR_ID}` from your browser's dev tool.

  * Usually, twitter web client will make a request to `UserByScreenName` endpoint when you visit an user's homepage. (e.g. [https://twitter.com/elonmusk](https://twitter.com/elonmusk))

  * And, it will make another request to 'UserMedia' endpoint when you visit a user's media page. (e.g. [https://twitter.com/elonmusk/media](https://twitter.com/elonmusk/media))

  * Finally, it will make a request to 'TweetDetail' endpoint when you visit a tweet. (e.g. [https://twitter.com/elonmusk/status/1688485935816581120](https://twitter.com/elonmusk/status/1688485935816581120))

  * For example, if you found following request when visiting a twitter user's homepage:
    * `https://twitter.com/i/api/graphql/abcdefg123456-/UserByScreenName?....`
    * you found your unique str id for UserByScreenName: `abcdefg123456-`

  * fill-in your unique str id for following parameters:
    * **endpoint_userbyscreenname**
    * **endpoint_usermedia**
    * **endpoint_tweetdetail**

* Parameters:
  * **header_authorization**: str, Authorization in request header
  * **header_x_client_uuid**: str, X-Client-Uuid in request header
  * **header_x_csrf_token**: str, X-Csrf-Token in request header
  * **cookie_auth_token**: str, auth_token in cookie
  * **cookie_ct0**: str, ct0 in cookie
  * **endpoint_userbyscreenname**: str, unique id for UserByScreenName endpoint
  * **endpoint_usermedia**: str, unique id for UserMedia endpoint
  * **endpoint_tweetdetail**: str, unique id for TweetDetail endpoint
  * **proxies**: dictionary, proxy server urls, default None, disabled. (e.g. `{'http':'http://localhost', 'https':'https://localhost'}`)
  * **delay_val**: float, seconds between each request, default 0.0

### **SetProxies(TwitterWebAgent, proxies:dict):**

* Set proxy for TwitterWebAgent
* Parameters
  * **proxies**: dictionary, proxy server urls. (e.g. `{'http':'http://localhost', 'https':'https://localhost'}`)

### **GetParentItemInfo(TwitterWebAgent, item_info:TwitterItemInfo) -> TwitterItemInfo:**

* Get the parent TwitterItemInfo for a child TwitterItemInfo.
* Parameters:
  * **item_info**: TwitterItemInfo Child
* Returns:
  * A parent TwitterItemInfo

### **IsFollowedUser(TwitterWebAgent, item_info:TwitterItemInfo) -> bool:**

* Is input TwitterItemInfo points to an user that is followed by current account.
* Parameters:
  * **item_info**: TwitterItemInfo to check
* Returns:
  * True if is followed
  * False if not

# 7. class DanbooruAgent

Child class of [BaseAgent](#2-class-baseagent) for handling requests to [danbooru](https://danbooru.donmai.us/)

Sharing all the common members and methods from base class.

This Agent only accept [DanbooruItemInfo](./WebItemInfo.md#4-class-danbooruiteminfo)

## Additional Methods

### **\_\_init\_\_(DanbooruAgent, proxies:dict=None):**

* Constructor for DanbooruAgent class
* You can pass in optional parameters via [DanbooruAgent.instance() function](#instanceself-args)
* Parameters:
  * **proxies**: dictionary, proxy server urls, default None, disabled. (e.g. `{'http':'http://localhost', 'https':'https://localhost'}`)

### **SetProxies(DanbooruAgent, proxies:dict):**

* Set proxy for DanbooruAgent
* Parameters
  * **proxies**: dictionary, proxy server urls. (e.g. `{'http':'http://localhost', 'https':'https://localhost'}`)

### **FindSource(DanbooruAgent, item_info:DanbooruItemInfo) -> str:**

* Find the source of a Child DanbooruItemInfo.
* Parameters:
  * **item_info**: DanbooruItemInfo Child
* Returns:
  * str url to the source if has one
  * otherwise, None

# 8. class YandereAgent

Child class of [BaseAgent](#2-class-baseagent) for handling requests to [yande.re](https://yande.re/)

Sharing all the common members and methods from base class.

This Agent only accept [YandereItemInfo](./WebItemInfo.md#5-class-yandereiteminfo)

## Additional Methods

### **\_\_init\_\_(YandereAgent, proxies:dict=None):**

* Constructor for YandereAgent class
* You can pass in optional parameters via [YandereAgent.instance() function](#instanceself-args)
* Parameters:
  * **proxies**: dictoinary, a proxy server url string, default None, disabled. (e.g. `{'http':'http://localhost', 'https':'https://localhost'}`)

### **SetProxies(YandereAgent, proxies:dict):**

* Set proxy for YandereAgent
* Parameters
  * **proxies**: dictionary, proxy server urls. (e.g. `{'http':'http://localhost', 'https':'https://localhost'}`)

### **FindSource(YandereAgent, item_info:YandereItemInfo) -> str:**

* Find the source of a Child YandereItemInfo.
* Parameters:
  * **item_info**: YandereItemInfo Child
* Returns:
  * str url to the source if has one
  * otherwise, None

# 9. class KonachanAgent

Child class of [BaseAgent](#2-class-baseagent) for handling requests to [konachan](https://konachan.com/)

Sharing all the common members and methods from base class.

This Agent only accept [KonachanItemInfo](./WebItemInfo.md#6-class-konachaniteminfo)

## Additional Methods

### **\_\_init\_\_(KonachanAgent, proxies:dict=None):**

* Constructor for KonachanAgent class
* You can pass in optional parameters via [KonachanAgent.instance() function](#instanceself-args)
* Parameters:
  * **proxies**: dictionary, proxy server urls, default None, disabled. (e.g. `{'http':'http://localhost', 'https':'https://localhost'}`)

### **SetProxies(KonachanAgent, proxies:dict):**

* Set proxy for KonachanAgent
* Parameters
  * **proxies**: dictionary, proxy server urls. (e.g. `{'http':'http://localhost', 'https':'https://localhost'}`)

### **FindSource(KonachanAgent, item_info:KonachanItemInfo) -> str:**

* Find the source of a Child KonachanItemInfo.
* Parameters:
  * **item_info**: KonachanItemInfo Child
* Returns:
  * str url to the source if has one
  * otherwise, None

# 10. class WeiboAgent

Child class of [BaseAgent](#2-class-baseagent) for handling requests to [weibo](https://m.weibo.cn/)

Sharing all the common members and methods from base class.

This Agent only accept [WeiboItemInfo](./WebItemInfo.md#7-class-weiboiteminfo)

## Additional Methods

### **\_\_init\_\_(WeiboAgent, proxies:dict=None):**

* Constructor for WeiboAgent class
* You can pass in optional parameters via [WeiboAgent.instance() function](#instanceself-args)
* Parameters:
  * **proxies**: dictionary, proxy server urls, default None, disabled. (e.g. `{'http':'http://localhost', 'https':'https://localhost'}`)

### **SetProxies(WeiboAgent, proxies:dict):**

* Set proxy for DanbooruAgent
* Parameters
  * **proxies**: dictoinary, proxy server urls. (e.g. `{'http':'http://localhost', 'https':'https://localhost'}`)

# 11. class EHentaiAgent

Child class of [BaseAgent](#2-class-baseagent) for handling requests to [e-hentai](https://e-hentai.org/)

Sharing all the common members and methods from base class.

This Agent only accept [EHentaiItemInfo](./WebItemInfo.md#8-class-ehentaiiteminfo)

## E-Hentai Peek Hour

EH maintainers use a set of rules to control the website's load

* [Checkout this changelog](https://forums.e-hentai.org/index.php?showtopic=244935)
* Learn more from [E-Hentai Downloader's documentation](https://github.com/ccloli/E-Hentai-Downloader/wiki/E%E2%88%92Hentai-Image-Viewing-Limits)

**Peek Hour Table (In UTC Time)**

| Date    | From Hour | To Hour |
|---------|-----------|---------|
| Mon (0) | 14        | 20      |
| Tue (1) | 14        | 20      |
| Wed (2) | 14        | 20      |
| Thu (3) | 14        | 20      |
| Fri (4) | 14        | 20      |
| Sat (5) | 14        | 20      |
| Sun (6) | 5         | 20      |

**Peek Hour Rules**

* if gallery is published within 90 days
  * Peak Hour rules won't apply to it
* otherwise
  * if current time is within Peak Hour Range
    * then "Download source image" EH feature will consume GP
* If the image viewing limit is exhausted, "Download source image" EH feature will consume GP

**About This API**

* Calling EHentaiAgent.DownloadItem during peek hour will raise EHentaiInPeekHourException
* you can disable this exception by setting EHentaiAgent.__ignore_peek_hour to False
* use EHentaiAgent.InPeekHour() to check whether you are in peek hour
* use EHentaiAgent.GetIgnorePeekHour() or EHentaiAgent.SetIgnorePeekHour() to get/set EHentaiAgent.__ignore_peek_hour flag

## Additional Methods

### **\_\_init\_\_(EHentaiAgent, ipb\_member\_id:str=None, ipb\_pass\_hash:str=None, proxies:dict=None):**

* Constructor for EHentaiAgent class
* You can pass in optional parameters via [EHentaiAgent.instance() function](#instanceself-args)
* ipb_member_id and ipb_pass_has are your EHentai account authentication token that EHentai assigned to you.
* Once you login to EHentai, the server will assign your login authentication information to your browser.
* You must login in order to download the original image source.
* WebImageAPI uses your authentication information to download the original image source like your browser.
* You can find these authentication information by:
  * visit https://e-hentai.org in your pc browser
  * open your browser's developer console
  * in the Applications tab on the console
  * under the Cookies drop down menu
  * select https://e-hentai.org
* Parameters:
  * **proxies**: dictionary, proxy server urls, default None, disabled. (e.g. `{'http':'http://localhost', 'https':'https://localhost'}`)
  * **ipb\_member\_id**: string, ipb_member_id in EHentai cookies
  * **ipb\_pass\_hash**: string, ipb_pass_has in EHentai cookies

### **SetProxies(EHentaiAgent, proxies:dict):**

* Set proxy for DanbooruAgent
* Parameters
  * **proxies**: dictionary, proxy server urls. (e.g. `{'http':'http://localhost', 'https':'https://localhost'}`)

### **SetEHentaiAuthInfo(EHentaiAgent, ipb\_member\_id:str, ipb\_pass\_hash:str):**

* Set EHentai Authentication information
* ipb_member_id and ipb_pass_has are your EHentai account authentication token that EHentai assigned to you.
* Once you login to EHentai, the server will assign your login authentication information to your browser.
* You must login in order to download the original image source.
* WebImageAPI uses your authentication information to download the original image source like your browser.
* You can find these authentication information by:
  * visit https://e-hentai.org in your pc browser
  * open your browser's developer console
  * in the Applications tab on the console
  * under the Cookies drop down menu
  * select https://e-hentai.org
* Parameters:
  * **ipb\_member\_id**:      string, ipb_member_id in EHentai cookies
  * **ipb\_pass\_hash**:      string, ipb_pass_has in EHentai cookies

### **GetIgnorePeekHour(EHentaiAgent) -> bool:**

* Get ignore peek hour flag

### **SetIgnorePeekHour(EHentaiAgent, whether_ignore:bool):**

* Set ignore peek hour flag
* Parameters
  * **whether_ignore**:              bool, whether to ignore peek hour exception

### **InPeekHour(self) -> bool:**

* Whether E-Hentai is in Peek Hour now

### **GetNextPeekHour(self) -> tuple:**

* Get next peek hour information
* Returns:
  * tuple( whether in peek hour : bool, peek hour : datetime )
  * If currently in peek hour, tuple( True, datetime obj of the end of current peek hour )
  * If currently not in peek hour, tuple( False, datetime obj of the start of next peek hour )

