# coding = utf-8
import crawles
from time import time

r = int(time())

js = crawles.execjs('ant09.js')
u = js.call('u', str(r))
print(u)

url = 'https://antispider9.scrape.center/api/movie/'

cookies = {
}

headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Referer': 'https://antispider9.scrape.center/page/9',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.57',
    'sec-ch-ua': '\"Microsoft Edge\";v=\"113\", \"Chromium\";v=\"113\", \"Not-A.Brand\";v=\"24\"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '\"Windows\"',
}

params = {
    'limit': '10',
    'offset': '80',
    'token': u,
}

# 当前时间戳: 1701937219.597993
response = crawles.get(url, headers=headers, params=params, cookies=cookies)
print(response.text)
print(response.status_code)
