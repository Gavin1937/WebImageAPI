
<details>

<summary><strong style="font-size:large;">
Table Of Content
</strong></summary>

* [1. class WrongParentChildException](#1-class-wrongparentchildexception)
  * [Members](#members)
* [2. class FileMD5NotMatchingException](#2-class-filemd5notmatchingexception)
  * [Members](#members-1)
* [3. class NotSupportURLException](#3-class-notsupporturlexception)
  * [Members](#members-2)
* [4. class EHentaiInPeekHourException](#4-class-ehentaiinpeekhourexception)
  * [Members](#members-3)
* [5. class EHentaiExcessViewingLimit](#5-class-ehentaiexcessviewinglimit)
  * [Members](#members-4)
* [6. class EHentaiInvalidLoginAuthentication](#6-class-ehentaiinvalidloginauthentication)
  * [Members](#members-5)

</details>

<br>


# 1. class WrongParentChildException

* User input a WebItemInfo with wrong parent_child state

## Members

* **message**: string error message
* **parent_child**: [PARENT_CHILD](./index.md#enum-class-parent_child) from input WebItemInfo

# 2. class FileMD5NotMatchingException

* Downloaded file MD5 not matching

## Members

* **message**: string error message
* **md5_wanted**: string md5 wanted from downloaded file
* **md5_has**: string real md5 get from downloaded file
* **filepath**: string filepath of downloaded file

# 3. class NotSupportURLException

* Supplied url not supported

## Members

* **message**: string error message

# 4. class EHentaiInPeekHourException

* E-Hentai is in peek hour now
* you can disable this exception by enabling ignore_peek_hour in [EHentaiAgent](./Agents.md#10-class-ehentaiagent)

## Members

* **message**: string error message
* **datetime**: datetime object of current time
* **time_local**: string of current time in iso format in your local timezone
* **time_utc**: string of current time in iso format in UTC timezone

# 5. class EHentaiExcessViewingLimit

* You excess E-Hentai viewing limit

## Members

* **message**: string error message
* **url**: string WebItemInfo's url when this exception raised

# 6. class EHentaiInvalidLoginAuthentication

* Your E-Hentai Login Authentication is Invalid

## Members

* **message**: string error message
* **url**: string WebItemInfo's url when this exception raised
