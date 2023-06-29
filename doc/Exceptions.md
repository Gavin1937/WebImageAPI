
<details>

<summary><strong style="font-size:large;">
Table Of Content
</strong></summary>

* [1. class WrongParentChildException](#1-class-wrongparentchildexception)
  * [Members](#members)
* [2. class BadWebItemInfoException](#2-class-badwebiteminfoexception)
  * [Members](#members-1)
* [3. class FileMD5NotMatchingException](#3-class-filemd5notmatchingexception)
  * [Members](#members-2)
* [4. class NotSupportURLException](#4-class-notsupporturlexception)
  * [Members](#members-3)
* [5. class EHentaiInPeekHourException](#5-class-ehentaiinpeekhourexception)
  * [Members](#members-4)
* [6. class EHentaiExcessViewingLimit](#6-class-ehentaiexcessviewinglimit)
  * [Members](#members-5)
* [7. class EHentaiInvalidLoginAuthentication](#7-class-ehentaiinvalidloginauthentication)
  * [Members](#members-6)

</details>

<br>


# 1. class WrongParentChildException

* User input a WebItemInfo with wrong parent_child state

## Members

* **message**: string error message
* **parent_child**: [PARENT_CHILD](./index.md#enum-class-parent_child) from input WebItemInfo

# 2. class BadWebItemInfoException

* User input an empty or invalid WebItemInfo.

## Members

* **message**: string error message
* **item_info_name**: string of item_info

# 3. class FileMD5NotMatchingException

* Downloaded file MD5 not matching

## Members

* **message**: string error message
* **md5_wanted**: string md5 wanted from downloaded file
* **md5_has**: string real md5 get from downloaded file
* **filepath**: string filepath of downloaded file

# 4. class NotSupportURLException

* Supplied url not supported

## Members

* **message**: string error message

# 5. class EHentaiInPeekHourException

* E-Hentai is in peek hour now
* you can disable this exception by enabling ignore_peek_hour in [EHentaiAgent](./Agents.md#10-class-ehentaiagent)

## Members

* **message**: string error message
* **datetime**: datetime object of current time
* **time_local**: string of current time in iso format in your local timezone
* **time_utc**: string of current time in iso format in UTC timezone

# 6. class EHentaiExcessViewingLimit

* You excess E-Hentai viewing limit

## Members

* **message**: string error message
* **url**: string WebItemInfo's url when this exception raised

# 7. class EHentaiInvalidLoginAuthentication

* Your E-Hentai Login Authentication is Invalid

## Members

* **message**: string error message
* **url**: string WebItemInfo's url when this exception raised
