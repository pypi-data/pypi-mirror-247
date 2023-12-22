# coding = utf-8
import crawles

js = crawles.execjs('j2.js')
dataa = js.call("abc")
print(dataa)
url = f'http://www.spiderbuf.cn/h05/api/{dataa["s"]}'

cookies = {
    'Hm_lpvt_ab0153f5f064a819a91a3699f63f86e3': f'1702368370',
    'Hm_lvt_ab0153f5f064a819a91a3699f63f86e3': f'1702368370',
}

headers = {
    'Accept': '*/*',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Referer': 'http://www.spiderbuf.cn/h05/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
}

params = {
}

# 当前时间戳: 1702368262.051915
response = crawles.get(url, headers=headers, params=params, cookies=cookies)
print(response.text)
