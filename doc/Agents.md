
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
    * [**instance(self, \*\*args):**](#instanceself-args)
* [4. class PixivAgent](#4-class-pixivagent)
  * [Additional Methods](#additional-methods)
    * [**\_\_init\_\_(PixivAgent, refresh\_token:str, max\_try:int=5):**](#__init__pixivagent-refresh_tokenstr-max_tryint5)
    * [**GetAPI(PixivAgent) -\> AppPixivAPI:**](#getapipixivagent---apppixivapi)
* [5. class TwitterAgent](#5-class-twitteragent)
  * [Additional Methods](#additional-methods-1)
    * [**\_\_init\_\_(TwitterAgent, consumer\_key:str, consumer\_secret:str, access\_token:str, access\_token\_secret:str, max\_try:int=5):**](#__init__twitteragent-consumer_keystr-consumer_secretstr-access_tokenstr-access_token_secretstr-max_tryint5)
    * [**GetAPI(TwitterAgent) -\> tweepy.API:**](#getapitwitteragent---tweepyapi)
    * [**SetProxies(TwitterAgent, proxies:str=None):**](#setproxiestwitteragent-proxiesstrnone)
* [6. class DanbooruAgent](#6-class-danbooruagent)
  * [Additional Methods](#additional-methods-2)
    * [**\_\_init\_\_(DanbooruAgent, proxies:str=None):**](#__init__danbooruagent-proxiesstrnone)
    * [**SetProxies(DanbooruAgent, proxies:str=None):**](#setproxiesdanbooruagent-proxiesstrnone)
* [7. class YandereAgent](#7-class-yandereagent)
  * [Additional Methods](#additional-methods-3)
    * [**\_\_init\_\_(YandereAgent, proxies:str=None):**](#__init__yandereagent-proxiesstrnone)
    * [**SetProxies(YandereAgent, proxies:str=None):**](#setproxiesyandereagent-proxiesstrnone)
* [8. class KonachanAgent](#8-class-konachanagent)
  * [Additional Methods](#additional-methods-4)
    * [**\_\_init\_\_(KonachanAgent, proxies:str=None):**](#__init__konachanagent-proxiesstrnone)
    * [**SetProxies(KonachanAgent, proxies:str=None):**](#setproxieskonachanagent-proxiesstrnone)
* [9. class WeiboAgent](#9-class-weiboagent)
  * [Additional Methods](#additional-methods-5)
    * [**\_\_init\_\_(WeiboAgent, proxies:str=None):**](#__init__weiboagent-proxiesstrnone)
    * [**SetProxies(WeiboAgent, proxies:str=None):**](#setproxiesweiboagent-proxiesstrnone)
* [10. class EHentaiAgent](#10-class-ehentaiagent)
  * [E-Hentai Peek Hour](#e-hentai-peek-hour)
  * [Additional Methods](#additional-methods-6)
    * [**\_\_init\_\_(EHentaiAgent, proxies:str=None):**](#__init__ehentaiagent-proxiesstrnone)
    * [**SetProxies(EHentaiAgent, proxies:str=None):**](#setproxiesehentaiagent-proxiesstrnone)
    * [**GetIgnorePeekHour(EHentaiAgent) -\> bool:**](#getignorepeekhourehentaiagent---bool)
    * [**SetIgnorePeekHour(EHentaiAgent, whether\_ignore:bool):**](#setignorepeekhourehentaiagent-whether_ignorebool)
    * [**InPeekHour(self) -\> bool:**](#inpeekhourself---bool)

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

This design decision is because I don't want to initialize the same `Agent` class multiple times during the run time, so I uses singleton to avoid re-initialize and authenticated session copying.

## Methods

### **instance(self, \*\*args):**

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

# 5. class TwitterAgent

Child class of [BaseAgent](#2-class-baseagent) for handling requests to [twitter](https://twitter.com/)

Sharing all the common members and methods from base class.

This Agent only accept [TwitterItemInfo](./WebItemInfo.md#3-class-twitteriteminfo)

## Additional Methods

### **\_\_init\_\_(TwitterAgent, consumer_key:str, consumer_secret:str, access_token:str, access_token_secret:str, max_try:int=5):**

* Constructor for TwitterAgent class
* You need to pass in required/optional parameters for authentication in [TwitterAgent.instance() function](#instanceself-args)
* Parameters:
  * **consumer_key**:         string, twitter cunsumer api key
  * **consumer_secret**:      string, twitter consumer api secret
  * **access_token**:         string, twitter access token
  * **access_token_secret**:  string, twitter access token secret
  * **proxies**:              string, a proxy server url string, default None, disabled
  * **max_try**:              integer, max retry number
* This Agent uses tweepy.OAuth1UserHandler() and tweepy.API() to authenticate with twitter.
* [2023-04-01]: Twitter will change their api policy within 30 days. Therefore, this Agent may be affect by the api policy changes.

### **GetAPI(TwitterAgent) -> tweepy.API:**

* Get tweepy.API object created in the background

### **SetProxies(TwitterAgent, proxies:str=None):**

* Set proxy for TwitterAgent
* This function will perform a re-authentication with Twitter
* Parameters
  * **proxies**:              string, a proxy server url string, default None, disabled

# 6. class DanbooruAgent

Child class of [BaseAgent](#2-class-baseagent) for handling requests to [danbooru](https://danbooru.donmai.us/)

Sharing all the common members and methods from base class.

This Agent only accept [DanbooruItemInfo](./WebItemInfo.md#4-class-danbooruiteminfo)

## Additional Methods

### **\_\_init\_\_(DanbooruAgent, proxies:str=None):**

* Constructor for DanbooruAgent class
* You can pass in optional parameters via [DanbooruAgent.instance() function](#instanceself-args)
* Parameters:
  * **proxies**:              string, a proxy server url string, default None, disabled

### **SetProxies(DanbooruAgent, proxies:str=None):**

* Set proxy for DanbooruAgent
* Parameters
  * **proxies**:              string, a proxy server url string, default None, disabled

# 7. class YandereAgent

Child class of [BaseAgent](#2-class-baseagent) for handling requests to [yande.re](https://yande.re/)

Sharing all the common members and methods from base class.

This Agent only accept [YandereItemInfo](./WebItemInfo.md#5-class-yandereiteminfo)

## Additional Methods

### **\_\_init\_\_(YandereAgent, proxies:str=None):**

* Constructor for YandereAgent class
* You can pass in optional parameters via [YandereAgent.instance() function](#instanceself-args)
* Parameters:
  * **proxies**:              string, a proxy server url string, default None, disabled

### **SetProxies(YandereAgent, proxies:str=None):**

* Set proxy for DanbooruAgent
* Parameters
  * **proxies**:              string, a proxy server url string, default None, disabled

# 8. class KonachanAgent

Child class of [BaseAgent](#2-class-baseagent) for handling requests to [konachan](https://konachan.com/)

Sharing all the common members and methods from base class.

This Agent only accept [KonachanItemInfo](./WebItemInfo.md#6-class-konachaniteminfo)

## Additional Methods

### **\_\_init\_\_(KonachanAgent, proxies:str=None):**

* Constructor for KonachanAgent class
* You can pass in optional parameters via [KonachanAgent.instance() function](#instanceself-args)
* Parameters:
  * **proxies**:              string, a proxy server url string, default None, disabled

### **SetProxies(KonachanAgent, proxies:str=None):**

* Set proxy for DanbooruAgent
* Parameters
  * **proxies**:              string, a proxy server url string, default None, disabled

# 9. class WeiboAgent

Child class of [BaseAgent](#2-class-baseagent) for handling requests to [weibo](https://m.weibo.cn/)

Sharing all the common members and methods from base class.

This Agent only accept [WeiboItemInfo](./WebItemInfo.md#7-class-weiboiteminfo)

## Additional Methods

### **\_\_init\_\_(WeiboAgent, proxies:str=None):**

* Constructor for WeiboAgent class
* You can pass in optional parameters via [WeiboAgent.instance() function](#instanceself-args)
* Parameters:
  * **proxies**:              string, a proxy server url string, default None, disabled

### **SetProxies(WeiboAgent, proxies:str=None):**

* Set proxy for DanbooruAgent
* Parameters
  * **proxies**:              string, a proxy server url string, default None, disabled

# 10. class EHentaiAgent

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

### **\_\_init\_\_(EHentaiAgent, proxies:str=None):**

* Constructor for EHentaiAgent class
* You can pass in optional parameters via [EHentaiAgent.instance() function](#instanceself-args)
* Parameters:
  * **proxies**:              string, a proxy server url string, default None, disabled

### **SetProxies(EHentaiAgent, proxies:str=None):**

* Set proxy for DanbooruAgent
* Parameters
  * **proxies**:              string, a proxy server url string, default None, disabled

### **GetIgnorePeekHour(EHentaiAgent) -> bool:**

* Get ignore peek hour flag

### **SetIgnorePeekHour(EHentaiAgent, whether_ignore:bool):**

* Set ignore peek hour flag
* Parameters
  * **whether_ignore**:              bool, whether to ignore peek hour exception

### **InPeekHour(self) -> bool:**

* Whether E-Hentai is in Peek Hour now
