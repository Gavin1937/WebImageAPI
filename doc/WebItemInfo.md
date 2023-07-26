
<details>

<summary><strong style="font-size:large;">
Table Of Content
</strong></summary>

* [1. class WebItemInfo](#1-class-webiteminfo)
  * [Members](#members)
    * [**WebItemInfo.url:str**](#webiteminfourlstr)
    * [**WebItemInfo.parsed\_url:UrlParser**](#webiteminfoparsed_urlurlparser)
    * [**WebItemInfo.domain:DOMAIN**](#webiteminfodomaindomain)
    * [**WebItemInfo.parent\_child:PARENT\_CHILD**](#webiteminfoparent_childparent_child)
    * [**WebItemInfo.details:Any**](#webiteminfodetailsany)
  * [Methods](#methods)
    * [**WebItemInfo.\_\_init\_\_(self, url:str):**](#webiteminfo__init__self-urlstr)
    * [**WebItemInfo.IsParent(self) -\> bool:**](#webiteminfoisparentself---bool)
    * [**WebItemInfo.IsChild(self) -\> bool:**](#webiteminfoischildself---bool)
    * [**WebItemInfo.IsEmpty(self) -\> bool:**](#webiteminfoisemptyself---bool)
    * [**WebItemInfo.UpdateUrl(self, url:str) -\> WebItemInfo:**](#webiteminfoupdateurlself-urlstr---webiteminfo)
    * [**WebItemInfo.UpdateParsedUrl(self, parsed\_url:UrlParser) -\> WebItemInfo:**](#webiteminfoupdateparsedurlself-parsed_urlurlparser---webiteminfo)
    * [**FromChildDetails(details) -\> WebItemInfo:**](#fromchilddetailsdetails---webiteminfo)
* [2. class PixivItemInfo](#2-class-pixiviteminfo)
  * [Additional Members](#additional-members)
    * [**PixivItemInfo.pid**](#pixiviteminfopid)
    * [**\_\_init\_\_(PixivItemInfo, url:str=None, \*\*kwargs) -\> None:**](#__init__pixiviteminfo-urlstrnone-kwargs---none)
* [3. class TwitterItemInfo](#3-class-twitteriteminfo)
  * [Additional Members](#additional-members-1)
    * [**TwitterItemInfo.screen\_name**](#twitteriteminfoscreen_name)
    * [**TwitterItemInfo.status\_id**](#twitteriteminfostatus_id)
    * [**\_\_init\_\_(TwitterItemInfo, url:str=None, \*\*kwargs) -\> None:**](#__init__twitteriteminfo-urlstrnone-kwargs---none)
* [4. class DanbooruItemInfo](#4-class-danbooruiteminfo)
* [5. class YandereItemInfo](#5-class-yandereiteminfo)
* [6. class KonachanItemInfo](#6-class-konachaniteminfo)
* [7. class WeiboItemInfo](#7-class-weiboiteminfo)
  * [Additional Members](#additional-members-2)
    * [**WeiboItemInfo.weibo\_id**](#weiboiteminfoweibo_id)
    * [**\_\_init\_\_(WeiboItemInfo, url:str=None, \*\*kwargs) -\> None:**](#__init__weiboiteminfo-urlstrnone-kwargs---none)
* [8. class EHentaiItemInfo](#8-class-ehentaiiteminfo)
  * [Additional Members](#additional-members-3)
    * [**EHentaiItemInfo.gallery\_id**](#ehentaiiteminfogallery_id)
    * [**EHentaiItemInfo.other**](#ehentaiiteminfoother)

</details>

<br>


# 1. class WebItemInfo

Base class for other `ItemInfo` classes.

This class contains all the common class members and methods that shared by other `ItemInfo` classes.

The documentation of other `ItemInfo` classes will not repeat common interfaces that `WebItemInfo` has, and focus on the differences of interfaces comparing to this base class.

## Members

Although members `WebItemInfo.url` and `WebItemInfo.parsed_url` are public and you can modify them freely, I recommend using `WebItemInfo.UpdateUrl` and `WebItemInfo.UpdateParsedUrl` functions to update them.

### **WebItemInfo.url:str**

* url string

### **WebItemInfo.parsed_url:UrlParser**

* [UrlParser object](../index.md#class-urlparser)

### **WebItemInfo.domain:DOMAIN**

* [DOMAIN object](../index.md#enum-class-domain)

### **WebItemInfo.parent_child:PARENT_CHILD**

* [PARENT_CHILD object](../index.md#enum-class-parent_child)

### **WebItemInfo.details:Any**

* stores WebItemInfo details fetched by [BaseAgent.FetchItemInfoDetail()](./Agents.md#fetchiteminfodetailbaseagent-item_infowebiteminfo---webiteminfo) function
* set to default value before Agent.FetchItemInfoDetail() function is called
* default value None
* this class member can be any type (usually a dictionary or list)

## Methods

### **WebItemInfo.\_\_init\_\_(self, url:str):**

* WebItemInfo constructor
* Parameters:
  * **url**: string url

### **WebItemInfo.IsParent(self) -> bool:**

* Whether current WebItemInfo is a Parent page
* Returns:
  * boolean: True if is parent, otherwise False

### **WebItemInfo.IsChild(self) -> bool:**

* Whether current WebItemInfo is a Child page
* Returns:
  * boolean: True if is child, otherwise False

### **WebItemInfo.IsEmpty(self) -> bool:**

* Whether current WebItemInfo is Empty
* Returns:
  * boolean: True if `WebItemInfo.domain` is `DOMAIN.EMPTY` or `DOMAIN.INVALID` or `WebItemInfo.parent_child` is `PARENT_CHILD.EMPTY` or `PARENT_CHILD.INVALID`, otherwise False

### **WebItemInfo.UpdateUrl(self, url:str) -> WebItemInfo:**

* Update url by input string
* also update WebItemInfo.parsed_url automatically

### **WebItemInfo.UpdateParsedUrl(self, parsed_url:UrlParser) -> WebItemInfo:**

* Update parsed_url by input UrlParser
* also update WebItemInfo.url automatically

### **FromChildDetails(details) -> WebItemInfo:**

* Construct a new Child WebItemInfo with input `details`
* This method can only be called from child classes of WebItemInfo
* If called from WebItemInfo base class, raise NotImplementedError

# 2. class PixivItemInfo

Child class of [WebItemInfo](#1-class-webiteminfo) to store items in [pixiv](https://www.pixiv.net/)

Sharing all the common members and methods from base class.

## Additional Members

### **PixivItemInfo.pid**

integer member stores the id for a pixiv user or artworks.

### **\_\_init\_\_(PixivItemInfo, url:str=None, \*\*kwargs) -> None:**

* constructor of PixivItemInfo
* Parameters:
  * **url:** string url, can be None
  * If **url** is None, you must supply parent_child & pid as kwargs
    * **parent_child:** PARENT_CHILD state
    * **pid:** string | int pixiv id

# 3. class TwitterItemInfo

Child class of [WebItemInfo](#1-class-webiteminfo) to store items in [twitter](https://twitter.com/)

Sharing all the common members and methods from base class.

## Additional Members

### **TwitterItemInfo.screen_name**

string  twitter user screen name

### **TwitterItemInfo.status_id**

string tweet status id

### **\_\_init\_\_(TwitterItemInfo, url:str=None, \*\*kwargs) -> None:**

* constructor of TwitterItemInfo
* Parameters:
  * **url:** string url, can be None
  * If **url** is None, you must input parent_child & screen_name & status_id
    * **parent_child:** PARENT_CHILD state
    * **screen_name:** string twitter screen name, this is mandatory
    * **status_id:** string twitter status id, this is mandatory for child


# 4. class DanbooruItemInfo

Child class of [WebItemInfo](#1-class-webiteminfo) to store items in [danbooru](https://danbooru.donmai.us/)

Sharing all the common members and methods from base class.


# 5. class YandereItemInfo

Child class of [WebItemInfo](#1-class-webiteminfo) to store items in [yande.re](https://yande.re/)

Sharing all the common members and methods from base class.


# 6. class KonachanItemInfo

Child class of [WebItemInfo](#1-class-webiteminfo) to store items in [konachan](https://konachan.com/)

Sharing all the common members and methods from base class.

# 7. class WeiboItemInfo

Child class of [WebItemInfo](#1-class-webiteminfo) to store items in [weibo](https://m.weibo.cn/)

Sharing all the common members and methods from base class.

## Additional Members

### **WeiboItemInfo.weibo_id**

string weibo user id or status id

### **\_\_init\_\_(WeiboItemInfo, url:str=None, \*\*kwargs) -> None:**

* constructor of WeiboItemInfo
* Parameters:
  * **url:** string url, can be None
  * If **url** is None, you must input parent_child & weibo_id
    * **parent_child:** PARENT_CHILD state
    * **weibo_id:** string weibo user id or status id

# 8. class EHentaiItemInfo

Child class of [WebItemInfo](#1-class-webiteminfo) to store items in [e-hentai](https://e-hentai.org/)

Sharing all the common members and methods from base class.

## Additional Members

### **EHentaiItemInfo.gallery_id**

string E-Hentai gallery_id

### **EHentaiItemInfo.other**

dict E-Hentai parent or child information

If this is a parent

```py
{
  'gallery_token': 'hex gallery token'
}
```

If this is a child

```py
{
  'page_token': 'hex page token',
  'pagenumber': 'int page number'
}
```

