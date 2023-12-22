# coding = utf-8
import crawles

url = 'https://pixabay.com/images/search/cat/'

cookies = {
    'OptanonConsent': 'isGpcEnabled=0&datestamp=Mon+Dec+11+2023+15%3A08%3A17+GMT%2B0800+(%E4%B8%AD%E5%9B%BD%E6%A0%87%E5%87%86%E6%97%B6%E9%97%B4)&version=6.31.0&isIABGlobal=false&hosts=&consentId=ae8b7115-9135-4654-9d11-1d6b8993ac36&interactionCount=1&landingPath=https%3A%2F%2Fpixabay.com%2Fimages%2Fsearch%2Fcat%2F&groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1%2CC0004%3A1',
    '__cf_bm': 'vom4iI9yyjSdLes01U4zMTc2BC.OYxpQ8O8A3AmwBVE-1702278496-0-Abv8jTO0K6Zoo0+t/iOSo84+ihlggWrb1v513PeMHk5TC3QSANO21sLpSGUavxjrFBWvh5BFbVHBzl6u5x7kzmg=',
    '_ga': 'GA1.2.402846587.1701935447',
    '_gat_UA-20223345-1': '1',
    '_gid': 'GA1.2.410534775.1702278495',
    'anonymous_user_id': 'ca7628d6a9844953b8735e1621535450',
    'csrftoken': 'tpDmGZGZLgSlT8QD75h8GV0KkxdGENNUC9Omk2FE76D8GNJndrOHYeYRTKgpqSmU',
    'is_human': '1',
}

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'authority': 'pixabay.com',
    'cache-control': 'no-cache',
    'pragma': 'no-cache',
    'sec-ch-ua': '\"Microsoft Edge\";v=\"113\", \"Chromium\";v=\"113\", \"Not-A.Brand\";v=\"24\"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '\"Windows\"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.57',
}

params = {
}

# 当前时间戳: 1702278529.0715356
response = crawles.get(url, headers=headers, params=params, cookies=cookies)
print(response.status_code, response.text)
response = crawles.get(url, headers=headers, params=params, cookies=cookies, impersonate='chrome110')
print(response.status_code, response.text)
