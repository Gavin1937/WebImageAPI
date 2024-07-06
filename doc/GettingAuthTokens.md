
<details>

<summary><strong style="font-size:large;">
Table Of Content
</strong></summary>

* [1. Twitter Web Client Authentication Tokens](#1-twitter-web-client-authentication-tokens)
  * [Request Headers](#request-headers)
  * [In Request Cookies](#in-request-cookies)
  * [Endpoints](#endpoints)

</details>

<br>


# 1. Twitter Web Client Authentication Tokens

In order to use [TwitterWebAgent](./Agents.md#6-class-twitterwebagent), you need to collect following authentication tokens from your browser.

First open your browser and visit [https://x.com/elonmusk](https://x.com/elonmusk) while you are logged into your twitter account.

Then, open your browser's dev tool and go to `Fetch/XHR` tab under `Network` tab. (you may need to refresh the page to see stuff appear in here)

## Request Headers

In any request appears under `Fetch/XHR` tab, find following 3 things under its headers section.

* **Authorization**
* **X-Client-Uuid**
* **X-Csrf-Token**


## In Request Cookies

Go to `Application` -> `Cookies` tab of your dev tool, and find following 2 things.

* **auth_token**
* **ct0**

## Endpoints

In `Fetch/XHR` tab:

1. visit [https://x.com/elonmusk](https://x.com/elonmusk), and then find a request looks like: `https://x.com/i/api/graphql/{YOUR_STR_ID}/UserByScreenName`
   * `{YOUR_STR_ID}` is the input for `endpoint_userbyscreenname` parameter

2. visit [https://x.com/elonmusk/media](https://x.com/elonmusk/media), and then find a request looks like: `https://x.com/i/api/graphql/{YOUR_STR_ID}/UserMedia`
   * `{YOUR_STR_ID}` is the input for `endpoint_usermedia` parameter

3. visit [https://x.com/elonmusk/status/1688485935816581120](https://x.com/elonmusk/status/1688485935816581120), and then find a request looks like: `https://x.com/i/api/graphql/{YOUR_STR_ID}/TweetDetail`
   * `{YOUR_STR_ID}` is the input for `endpoint_tweetdetail` parameter

