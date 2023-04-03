

<details>

<summary><strong style="font-size:large;">
Table Of Content
</strong></summary>

* [1. class WebImageAPI](#1-class-webimageapi)
  * [Methods](#methods)
      * [\_\_init\_\_(WebImageAPI):](#__init__webimageapi)
    * [**Agent Setup**](#agent-setup)
      * [SetPixivTokens(WebImageAPI, refresh\_token:str):](#setpixivtokenswebimageapi-refresh_tokenstr)
      * [SetTwitterTokens(WebImageAPI, consumer\_key:str, consumer\_secret:str, access\_token:str, access\_token\_secret:str):](#settwittertokenswebimageapi-consumer_keystr-consumer_secretstr-access_tokenstr-access_token_secretstr)
    * [**Agent Getters**](#agent-getters)
      * [GetPixivAgent(WebImageAPI) -\> PixivAgent:](#getpixivagentwebimageapi---pixivagent)
      * [GetTwitterAgent(WebImageAPI) -\> TwitterAgent:](#gettwitteragentwebimageapi---twitteragent)
      * [GetDanbooruAgent(WebImageAPI) -\> DanbooruAgent:](#getdanbooruagentwebimageapi---danbooruagent)
      * [GetYandereAgent(WebImageAPI) -\> YandereAgent:](#getyandereagentwebimageapi---yandereagent)
    * [**Agent Common Features**](#agent-common-features)
      * [FetchItemInfoDetail(WebImageAPI, item\_info:WebItemInfo) -\> WebItemInfo:](#fetchiteminfodetailwebimageapi-item_infowebiteminfo---webiteminfo)
      * [FetchParentChildren(WebImageAPI, item\_info:WebItemInfo, page:int=1) -\> list:](#fetchparentchildrenwebimageapi-item_infowebiteminfo-pageint1---list)
      * [FetchUserInfo(WebImageAPI, item\_info:WebItemInfo, old\_user\_info:UserInfo=None) -\> UserInfo:](#fetchuserinfowebimageapi-item_infowebiteminfo-old_user_infouserinfonone---userinfo)
      * [DownloadItem(WebImageAPI, item\_info:WebItemInfo, output\_path:Union\[str,Path\], replace:bool=False):](#downloaditemwebimageapi-item_infowebiteminfo-output_pathunionstrpath-replaceboolfalse)
    * [**WebItemInfo Generation**](#webiteminfo-generation)
      * [UrlToWebItemInfo(WebImageAPI, url:str) -\> WebItemInfo:](#urltowebiteminfowebimageapi-urlstr---webiteminfo)
      * [FromChildDetails(self, domain:DOMAIN, details) -\> WebItemInfo:](#fromchilddetailsself-domaindomain-details---webiteminfo)

</details>

<br>



# 1. class WebImageAPI

This class is an abstraction class that handles all API features of the package.

I highly recommend you to stick with this class and let it to handle everything in the background.

## Methods

#### \_\_init\_\_(WebImageAPI):

* Class constructor

### **Agent Setup**

#### SetPixivTokens(WebImageAPI, refresh_token:str):

* Setup PixivAgent with supplied parameters
* Parameters:
  * **refresh_token**:  string, pixiv refresh_token
* You need to call this function before using any of the `PixivAgent` features

#### SetTwitterTokens(WebImageAPI, consumer_key:str, consumer_secret:str, access_token:str, access_token_secret:str):

* Setup TwitterAgent with supplied parameters
* Parameters:
  * **consumer_key**:         string, twitter cunsumer api key
  * **consumer_secret**:      string, twitter consumer api secret
  * **access_token**:         string, twitter access token
  * **access_token_secret**:  string, twitter access token secret

### **Agent Getters**

#### GetPixivAgent(WebImageAPI) -> PixivAgent:

* Get existing, initialized `PixivAgent`

#### GetTwitterAgent(WebImageAPI) -> TwitterAgent:

* Get existing, initialized `TwitterAgent`

#### GetDanbooruAgent(WebImageAPI) -> DanbooruAgent:

* Get existing, initialized `DanbooruAgent`

#### GetYandereAgent(WebImageAPI) -> YandereAgent:

* Get existing, initialized `YandereAgent`

### **Agent Common Features**

#### FetchItemInfoDetail(WebImageAPI, item_info:WebItemInfo) -> WebItemInfo:

* An abstraction function for all Agents, you can pass in any child `WebItemInfo` into this function and let it to handle agents for you.
* Fetch & Fill-In `detail` member for supplied WebItemInfo.
* Paremters
  * **item_info**:   WebItemInfo to fetch
* Returns:
  * updated WebItemInfo

#### FetchParentChildren(WebImageAPI, item_info:WebItemInfo, page:int=1) -> list:

* An abstraction function for all Agents, you can pass in any child `WebItemInfo` into this function and let it to handle agents for you.
* Fetch a Parent WebItemInfo's Children
* Parameters:
  * **item_info**:   WebItemInfo Parent to fetch
  * **page**:        int page number >= 1
* Returns:
  * list of WebItemInfo fetched, also edit original `item_info`

#### FetchUserInfo(WebImageAPI, item_info:WebItemInfo, old_user_info:UserInfo=None) -> UserInfo:

* An abstraction function for all Agents, you can pass in any child `WebItemInfo` into this function and let it to handle agents for you.
* Fetch a WebItemInfo's UserInfo
* Parameters:
  * **item_info**:         PixivItemInfo Parent to fetch
  * **old_user_info**:     UserInfo that already fill up by  agents.
    * this function will collect additional UserInfo from current domain, and append to old_user_info and return it at the end.
    * (default None)
* Returns:
  * [UserInfo object](../index.md#class-userinfo)

#### DownloadItem(WebImageAPI, item_info:WebItemInfo, output_path:Union[str,Path], replace:bool=False):

* An abstraction function for all Agents, you can pass in any child `WebItemInfo` into this function and let it to handle agents for you.
* Download supplied WebItemInfo
* Parameters:
  * **item_info**:     WebItemInfo Child to download
  * **output_path**:   string | pathlib.Path of a directory for downloaded file
  * **replace**:       boolean flag, whether replace if download file already exists

### **WebItemInfo Generation**

#### UrlToWebItemInfo(WebImageAPI, url:str) -> WebItemInfo:

* An abstraction function that converts any string url into their dedicated `WebItemInfo` child class and return to you
* You can use this function handle your urls and not worry about choose which `WebItemInfo` child class to use.
* Parameters:
  * **url**:        string, url string
* Returns:
  * If url is supported, url's dedicated `WebItemInfo` child object.
  * Else, raise ValueError

#### FromChildDetails(self, domain:DOMAIN, details) -> WebItemInfo:

* An abstraction function that converts any child details dictionary into a child `WebItemInfo` with specified DOMAIN
* Parameters:
  * **domain**:        DOMAIN, domain of details
  * **details**:       any (usually dict|list), details to set
* Returns:
  * If domain is valid, return `WebItemInfo` specified by domain
  * Else, raise ValueError

