
<details>

<summary><strong style="font-size:large;">
Table Of Content
</strong></summary>

* [1. Terminology](#1-terminology)
  * [Supported Websites](#supported-websites)
  * [Parent Child State](#parent-child-state)
    * [Parent Page](#parent-page)
    * [Child Page](#child-page)
* [2. Types \& Utility Classes](#2-types--utility-classes)
  * [Enum Class DOMAIN](#enum-class-domain)
    * [**Values**](#values)
    * [**Methods**](#methods)
      * [DOMAIN.FromStr(domain:str) -\> DOMAIN:](#domainfromstrdomainstr---domain)
      * [DOMAIN.FromUrl(url:str) -\> DOMAIN:](#domainfromurlurlstr---domain)
      * [DOMAIN.FromInt(domain:int) -\> DOMAIN:](#domainfromintdomainint---domain)
      * [DOMAIN.ToStr(domain:DOMAIN) -\> str:](#domaintostrdomaindomain---str)
  * [Enum Class PARENT\_CHILD](#enum-class-parent_child)
    * [**Values**](#values-1)
    * [**Methods**](#methods-1)
      * [PARENT\_CHILD.ToStr(parent\_child:PARENT\_CHILD) -\> str:](#parent_childtostrparent_childparent_child---str)
      * [PARENT\_CHILD.FromInt(parent\_child:int) -\> PARENT\_CHILD:](#parent_childfromintparent_childint---parent_child)
  * [class UserInfo](#class-userinfo)
    * [**Members**](#members)
      * [UserInfo.name\_list](#userinfoname_list)
      * [UserInfo.url\_dict](#userinfourl_dict)
      * [UserInfo.details](#userinfodetails)
  * [class UrlParser](#class-urlparser)
    * [**Members**](#members-1)
      * [UrlParser.url](#urlparserurl)
      * [UrlParser.domain](#urlparserdomain)
      * [UrlParser.path](#urlparserpath)
      * [UrlParser.pathlist](#urlparserpathlist)
      * [UrlParser.querystr](#urlparserquerystr)
      * [UrlParser.query](#urlparserquery)
    * [**Methods**](#methods-2)
      * [UrlParser.UpdateUrl(self, url:str) -\> UrlParser:](#urlparserupdateurlself-urlstr---urlparser)
      * [UrlParser.UpdateDomain(self, domain:str) -\> UrlParser:](#urlparserupdatedomainself-domainstr---urlparser)
      * [UrlParser.UpdatePath(self, path:str) -\> UrlParser:](#urlparserupdatepathself-pathstr---urlparser)
      * [UrlParser.UpdatePathList(self, pathlist:list) -\> UrlParser:](#urlparserupdatepathlistself-pathlistlist---urlparser)
      * [UrlParser.UpdateQuery(self, query:dict) -\> UrlParser:](#urlparserupdatequeryself-querydict---urlparser)
      * [UrlParser.UpdateQueryStr(self, querystr:str) -\> UrlParser:](#urlparserupdatequerystrself-querystrstr---urlparser)
      * [UrlParser.BuildUrl(domain:str, path:Union\[str,list\], query:Union\[str,dict\]) -\> str:](#urlparserbuildurldomainstr-pathunionstrlist-queryunionstrdict---str)
* [3. WebItemInfo](#3-webiteminfo)
* [4. Agent](#4-agent)
* [5. class WebImageAPI](#5-class-webimageapi)
* [6. Exceptions:](#6-exceptions)
* [7. Quick Start](#7-quick-start)

</details>

<br>



# 1. Terminology

## Supported Websites

* [pixiv](https://www.pixiv.net/)
* [twitter](https://twitter.com/)
* [danbooru](https://danbooru.donmai.us/)
* [yande.re](https://yande.re/)
* [konachan](https://konachan.com/)
* [weibo](https://m.weibo.cn/)
* [e-hentai](https://e-hentai.org/)

## Parent Child State

WebImageAPI differentiate supported website's pages in two kinds.

### Parent Page

A page that contains artist/user/gallery information and links to children pages.

* Examples:
  * Pixiv:
    * Parent: https://www.pixiv.net/users/11
    * Child: https://www.pixiv.net/artworks/106725373
  * Twitter:
    * Parent: https://twitter.com/github
    * Child: https://twitter.com/github/status/1638273045587546134
  * Danbooru:
    * Parent: https://danbooru.donmai.us/posts
    * Child: https://danbooru.donmai.us/posts/1
  * yande.re:
    * Parent: https://yande.re/post
    * Child: https://yande.re/post/show/12345
  * konachan:
    * Parent: https://konachan.com/post
    * Child: https://konachan.com/post/show/1
  * weibo:
    * Parent: https://m.weibo.cn/u/1954940747
    * Child: https://m.weibo.cn/detail/4883581258435481
  * e-hentai:
    * Parent: https://e-hentai.org/g/2510385/e39a66a86e/
    * Child: https://e-hentai.org/s/9b00cf1ccc/2510385-1

### Child Page

A page that contains image.

# 2. Types & Utility Classes

## Enum Class DOMAIN

Enum Class to represent & handle supported website's domains

### **Values**

| Enum Name | Int Value |
|-----------|-----------|
| INVALID   | -1        |
| EMPTY     | 0         |
| PIXIV     | 1         |
| TWITTER   | 2         |
| DANBOORU  | 3         |
| YANDERE   | 4         |
| KONACHAN  | 5         |
| WEIBO     | 6         |
| EHENTAI   | 7         |

### **Methods**

#### DOMAIN.FromStr(domain:str) -> DOMAIN:

* Return the proper DOMAIN from **certain kind of strings**
* If `domain:str` not match any of the following strings, return `DOMAIN.INVALID`
* case insensitive
* Note: If you want to convert an url to DOMAIN, you should use [DOMAIN.FromUrl](#domainfromurlurlstr---domain)

| DOMAIN   | string                              |
|----------|-------------------------------------|
| PIXIV    | pixiv, pixiv.net, pximg.net         |
| TWITTER  | twitter, twitter.com, m.twitter.com |
| DANBOORU | danbooru, danbooru.donmai.us        |
| YANDERE  | yandere, yande.re                   |
| KONACHAN | konachan, konachan.com              |
| WEIBO    | weibo, m.weibo.cn                   |
| EHENTAI  | ehentai, e-hentai, e-hentai.org     |

#### DOMAIN.FromUrl(url:str) -> DOMAIN:

* Return the proper DOMAIN from urls
* If `url:str`'s domain not match any of the supported website, return DOMAIN.INVALID

#### DOMAIN.FromInt(domain:int) -> DOMAIN:

* Return the proper DOMAIN it's integer value
* Raise ValueError if failed

#### DOMAIN.ToStr(domain:DOMAIN) -> str:

* Return upper case string version of `domain:DOMAIN`

| DOMAIN   | string   |
|----------|----------|
| PIXIV    | PIXIV    |
| TWITTER  | TWITTER  |
| DANBOORU | DANBOORU |
| YANDERE  | YANDERE  |
| KONACHAN | KONACHAN |
| WEIBO    | WEIBO    |
| EHENTAI  | EHENTAI  |

## Enum Class PARENT_CHILD

Enum Class to represent a [parent/child state](#parent-child-state)

### **Values**

| Enum Name | Int Value |
|-----------|-----------|
| INVALID   | -1        |
| EMPTY     | 0         |
| PARENT    | 1         |
| CHILD     | 2         |

### **Methods**

#### PARENT_CHILD.ToStr(parent_child:PARENT_CHILD) -> str:

* Return upper case string version of `parent_child:PARENT_CHILD`

| DOMAIN  | string  |
|---------|---------|
| INVALID | INVALID |
| EMPTY   | EMPTY   |
| PARENT  | PARENT  |
| CHILD   | CHILD   |

#### PARENT_CHILD.FromInt(parent_child:int) -> PARENT_CHILD:

* Return the proper PARENT_CHILD it's integer value
* Raise ValueError if failed

## class UserInfo

Data class to store User Information from a [WebItemInfo](./WebItemInfo.md#1-class-webiteminfo)

### **Members**

#### UserInfo.name_list

a list of user name strings

#### UserInfo.url_dict

a dictionary of user urls, dictionary key are [Enum Class DOMAIN](#enum-class-domain)

#### UserInfo.details

a dictionary of other user details fetched by [BaseAgent.FetchUserInfo()](./Agents.md#fetchuserinfobaseagent-item_infowebiteminfo-old_user_infouserinfonone---userinfo) function

this variable can be any type, usually a dictionary or list

## class UrlParser

A simple url parser build on top of urllib.parse.urlparse()

### **Members**

Although all members are public and you can modify them freely, I recommend using `UrlParser.Update` functions to update class members.

#### UrlParser.url

* url string

#### UrlParser.domain

* url's domain string

#### UrlParser.path

* url's path string

#### UrlParser.pathlist

* url's path as a list of strings separated by "/
* format

```py
# path string: /path1/path2/path3
['path1','path2','path3',]
```

#### UrlParser.querystr

* url's query string

#### UrlParser.query

* url's query as a dictionary
* format:

```py
# query string: key=val1&key=val2&key=val3
{ 'key': ['val1', 'val2', 'val3',] }
```

### **Methods**

#### UrlParser.UpdateUrl(self, url:str) -> UrlParser:

* Update UrlParser's url from string as well as other members

#### UrlParser.UpdateDomain(self, domain:str) -> UrlParser:

* Update UrlParser's domain from string as well as other members

#### UrlParser.UpdatePath(self, path:str) -> UrlParser:

* Update UrlParser's path from string as well as other members

#### UrlParser.UpdatePathList(self, pathlist:list) -> UrlParser:

* Update UrlParser's path from list of path strings as well as other members

#### UrlParser.UpdateQuery(self, query:dict) -> UrlParser:

* Update UrlParser's query from dictionary as well as other members

#### UrlParser.UpdateQueryStr(self, querystr:str) -> UrlParser:

* Update UrlParser's query from string as well as other members

#### UrlParser.BuildUrl(domain:str, path:Union[str,list], query:Union[str,dict]) -> str:

* Static function to build a new url string from:
* Parameters:
  * **domain**: string
  * **path**: string | list
  * **query**: string | dict


# 3. WebItemInfo

Base class contains Web Item Information

[Details](./WebItemInfo.md)


# 4. Agent

Base class for WebImageAPI agents

[Details](./Agents.md)


# 5. class WebImageAPI

Abstraction class that handles all API features of the package.

I highly recommend you to stick with this class and let it to handle everything in the background.

[Details](./WebImageAPI.md)

# 6. Exceptions:

Custom Exceptions uses in WebImageAPI

[Details](./Exceptions.md)

# 7. Quick Start

Checkout [quick_start.py](../demo/quick_start.py)

Be sure to run it from `demo` directory

