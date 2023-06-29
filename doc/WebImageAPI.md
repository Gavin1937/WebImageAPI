

<details>

<summary><strong style="font-size:large;">
Table Of Content
</strong></summary>

* [1. class WebImageAPI](#1-class-webimageapi)
  * [Methods](#methods)
      * [\_\_init\_\_(WebImageAPI):](#__init__webimageapi)
    * [**Agent Setup**](#agent-setup)
      * [**SetPixivTokens(WebImageAPI, refresh\_token:str):**](#setpixivtokenswebimageapi-refresh_tokenstr)
      * [**SetTwitterTokens(WebImageAPI, agent\_type:str, ...):**](#settwittertokenswebimageapi-agent_typestr-)
      * [**SetEHentaiAuthInfo(WebImageAPI, ipb\_member\_id:str, ipb\_pass\_hash:str):**](#setehentaiauthinfowebimageapi-ipb_member_idstr-ipb_pass_hashstr)
      * [**GetEHentaiIgnorePeekHour(self) -\> bool:**](#getehentaiignorepeekhourself---bool)
      * [**SetEHentaiIgnorePeekHour(self, whether\_ignore:bool) -\> None:**](#setehentaiignorepeekhourself-whether_ignorebool---none)
      * [**GetEHentaiNextPeekHour(self) -\> tuple:**](#getehentainextpeekhourself---tuple)
    * [**Agent Getters**](#agent-getters)
      * [**GetPixivAgent(WebImageAPI) -\> PixivAgent:**](#getpixivagentwebimageapi---pixivagent)
      * [**GetTwitterAgent(WebImageAPI, which\_one:str='web') -\> Union\[TwitterAgent,TwitterWebAgent\]:**](#gettwitteragentwebimageapi-which_onestrweb---uniontwitteragenttwitterwebagent)
      * [**GetDanbooruAgent(WebImageAPI) -\> DanbooruAgent:**](#getdanbooruagentwebimageapi---danbooruagent)
      * [**GetYandereAgent(WebImageAPI) -\> YandereAgent:**](#getyandereagentwebimageapi---yandereagent)
      * [**GetKonachanAgent(WebImageAPI) -\> KonachanAgent:**](#getkonachanagentwebimageapi---konachanagent)
    * [**Agent Common Features**](#agent-common-features)
      * [**FetchItemInfoDetail(WebImageAPI, item\_info:WebItemInfo) -\> WebItemInfo:**](#fetchiteminfodetailwebimageapi-item_infowebiteminfo---webiteminfo)
      * [**FetchParentChildren(WebImageAPI, item\_info:WebItemInfo, page:int=1) -\> list:**](#fetchparentchildrenwebimageapi-item_infowebiteminfo-pageint1---list)
      * [**FetchUserInfo(WebImageAPI, item\_info:WebItemInfo, old\_user\_info:UserInfo=None) -\> UserInfo:**](#fetchuserinfowebimageapi-item_infowebiteminfo-old_user_infouserinfonone---userinfo)
      * [**DownloadItem(WebImageAPI, item\_info:WebItemInfo, output\_path:Union\[str,Path\], replace:bool=False):**](#downloaditemwebimageapi-item_infowebiteminfo-output_pathunionstrpath-replaceboolfalse)
      * [**FindSource(self, item\_info:WebItemInfo, absolute:bool=False) -\> Union\[WebItemInfo,str\]:**](#findsourceself-item_infowebiteminfo-absoluteboolfalse---unionwebiteminfostr)
    * [**WebItemInfo Generation**](#webiteminfo-generation)
      * [**UrlToWebItemInfo(WebImageAPI, url:str) -\> WebItemInfo:**](#urltowebiteminfowebimageapi-urlstr---webiteminfo)
      * [**FromChildDetails(self, domain:DOMAIN, details) -\> WebItemInfo:**](#fromchilddetailsself-domaindomain-details---webiteminfo)

</details>

<br>



# 1. class WebImageAPI

This class is an abstraction class that handles all API features of the package.

I highly recommend you to stick with this class and let it to handle everything in the background.

## Methods

#### \_\_init\_\_(WebImageAPI):

* Class constructor

### **Agent Setup**

#### **SetPixivTokens(WebImageAPI, refresh_token:str):**

* Setup PixivAgent with supplied parameters
* Parameters:
  * **refresh_token**:  string, pixiv refresh_token
* You need to call this function before using any of the `PixivAgent` features

#### **SetTwitterTokens(WebImageAPI, agent_type:str, ...):**

* Setup TwitterAgent & TwitterWebAgent
* Parameters:
  * **agent_type**: string, indicating which type of twitter agent to use. Can be: `web`, `dev`, `both`.
  * if agent_type == `web`, initialize a `TwitterWebAgent`.
    * Requires Param:
      * **header_authorization**: string, Authorization in request header
      * **header_x_client_uuid**: string, X-Client-Uuid in request header
      * **header_x_csrf_token**: string, X-Csrf-Token in request header
      * **cookie_auth_token**: string, auth_token in cookie
      * **cookie_ct0**: string, ct0 in cookie
      * **endpoint_userbyscreenname**: string, unique id for UserByScreenName endpoint
      * **endpoint_usermedia**: string, unique id for UserMedia endpoint
      * **endpoint_tweetdetail**: string, unique id for TweetDetail endpoint
  * if agent_type == `dev`, initialize a `TwitterAgent`.
    * Requires Param:
      * **consumer_key**: string, consumer_key of your twitter app
      * **consumer_secret**: string, consumer_secret of your twitter app
      * **access_token**: string, access_token of your twitter app
      * **access_token_secret**: string, access_token_secret of your twitter app
      * **bearer_token**: string, bearer_token of your twitter app
  * if agent_type == `both`, initialize both `TwitterWebAgent` and `TwitterAgent`.
    * Require all the parameters listed above.
  * WebImageAPI will prioritize `TwitterWebAgent` if possible.
  * checkout [TwitterWebAgent](./Agents.md#6-class-twitterwebagent) for detail.
  * checkout [new_twitter_agent.py](../demo/new_twitter_agent.py) for detail usage of new TwitterAgent.

#### **SetEHentaiAuthInfo(WebImageAPI, ipb\_member\_id:str, ipb\_pass\_hash:str):**

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

#### **GetEHentaiIgnorePeekHour(self) -> bool:**

* Get ignore_peek_hour flag in EHentaiAgent

#### **SetEHentaiIgnorePeekHour(self, whether_ignore:bool) -> None:**

* Set ignore_peek_hour flag in EHentaiAgent
* Parameters:
  * **whether_ignore:** boolean flag

#### **GetEHentaiNextPeekHour(self) -> tuple:**

* Get next peek hour information from EHentaiAgent
* Returns:
  * tuple( whether in peek hour : bool, peek hour : datetime )
  * If currently in peek hour, tuple( True, datetime obj of the end of current peek hour )
  * If currently not in peek hour, tuple( False, datetime obj of the start of next peek hour )

### **Agent Getters**

#### **GetPixivAgent(WebImageAPI) -> PixivAgent:**

* Get existing, initialized `PixivAgent`

#### **GetTwitterAgent(WebImageAPI, which_one:str='web') -> Union[TwitterAgent,TwitterWebAgent]:**

* Get existing, initialized `TwitterAgent` or `TwitterWebAgent`
* Parameter:
  * **which_one**: string
    * If set to `web`, return TwitterWebAgent.
    * If set to `dev`, return TwitterAgent.
    * Default `web`

#### **GetDanbooruAgent(WebImageAPI) -> DanbooruAgent:**

* Get existing, initialized `DanbooruAgent`

#### **GetYandereAgent(WebImageAPI) -> YandereAgent:**

* Get existing, initialized `YandereAgent`

#### **GetKonachanAgent(WebImageAPI) -> KonachanAgent:**

* Get existing, initialized `KonachanAgent`

### **Agent Common Features**

#### **FetchItemInfoDetail(WebImageAPI, item_info:WebItemInfo) -> WebItemInfo:**

* An abstraction function for all Agents, you can pass in any `WebItemInfo` into this function and let it to handle agents for you.
* Fetch & Fill-In `detail` member for supplied WebItemInfo.
* Paremters
  * **item_info**:   WebItemInfo to fetch
* Returns:
  * updated WebItemInfo

#### **FetchParentChildren(WebImageAPI, item_info:WebItemInfo, page:int=1) -> list:**

* An abstraction function for all Agents, you can pass in any `WebItemInfo` into this function and let it to handle agents for you.
* Fetch a Parent WebItemInfo's Children
* Parameters:
  * **item_info**:   WebItemInfo Parent to fetch
  * **page**:        int page number >= 1
* Returns:
  * list of WebItemInfo fetched, also edit original `item_info`

#### **FetchUserInfo(WebImageAPI, item_info:WebItemInfo, old_user_info:UserInfo=None) -> UserInfo:**

* An abstraction function for all Agents, you can pass in any `WebItemInfo` into this function and let it to handle agents for you.
* Fetch a WebItemInfo's UserInfo
* Parameters:
  * **item_info**:         PixivItemInfo Parent to fetch
  * **old_user_info**:     UserInfo that already fill up by  agents.
    * this function will collect additional UserInfo from current domain, and append to old_user_info and return it at the end.
    * (default None)
* Returns:
  * [UserInfo object](../index.md#class-userinfo)

#### **DownloadItem(WebImageAPI, item_info:WebItemInfo, output_path:Union[str,Path], replace:bool=False):**

* An abstraction function for all Agents, you can pass in any `WebItemInfo` into this function and let it to handle agents for you.
* Download supplied WebItemInfo
* Parameters:
  * **item_info**:     WebItemInfo Child to download
  * **output_path**:   string | pathlib.Path of a directory for downloaded file
  * **replace**:       boolean flag, whether replace if download file already exists

#### **FindSource(self, item_info:WebItemInfo, absolute:bool=False) -> Union[WebItemInfo,str]:**

* Find the source of a Child WebItemInfo.
* Param:
  * **item_info**: WebItemInfo Child
  * **absolute**: bool flag
    * if True, return str url when find a not support url.
    * if False, return None in above case
* Returns:
  * a valid WebItemInfo if find one source
  * if find one source but not valid, return str or item_info base on "absolute"
  * if not find any source, return None


### **WebItemInfo Generation**

#### **UrlToWebItemInfo(WebImageAPI, url:str) -> WebItemInfo:**

* An abstraction function that converts any string url into their dedicated `WebItemInfo` child class and return to you
* You can use this function handle your urls and not worry about choose which `WebItemInfo` child class to use.
* Parameters:
  * **url**:        string, url string
* Returns:
  * If url is supported, url's dedicated `WebItemInfo` child object.
  * Else, raise ValueError

#### **FromChildDetails(self, domain:DOMAIN, details) -> WebItemInfo:**

* An abstraction function that converts any child details dictionary into a child `WebItemInfo` with specified DOMAIN
* Parameters:
  * **domain**:        DOMAIN, domain of details
  * **details**:       any (usually dict | list), details to set
* Returns:
  * If domain is valid, return `WebItemInfo` specified by domain
  * Else, raise ValueError

