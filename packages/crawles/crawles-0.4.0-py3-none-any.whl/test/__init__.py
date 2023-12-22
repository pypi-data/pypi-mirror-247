# coding = utf-8
import crawles

url = 'https://h5api.m.taobao.com/h5/mtop.alimama.union.xt.en.api.entry/1.0/'

cookies = { 
    '_cc_': 'V32FPkk%2Fhw%3D%3D',
    '_l_g_': 'Ug%3D%3D',
    '_m_h5_tk': 'b69961affd4f8da420eefbed3d4b5f4b_1702458870316',
    '_m_h5_tk_enc': '4eabebdc644fc0dfcb5bc34d53c7d930',
    '_nk_': 'kjk1431',
    '_samesite_flag_': 'true',
    '_tb_token_': 'e8ae7e73fb858',
    'cancelledSubSites': 'empty',
    'cna': '9n1XHXcZrwICAXb6t4sStF0r',
    'cookie1': 'VvlyVbjZTXmvd4eQ2n2Qy9g1iRqnXrhtODb1IFCVIQE%3D',
    'cookie17': 'UUphw2LzTK2r3Ai5FQ%3D%3D',
    'cookie2': '1a8787eb06c9e21eed0c2dbec899f680',
    'csg': 'e8870131',
    'dnk': 'kjk1431',
    'existShop': 'MTcwMjQ0OTU0OQ%3D%3D',
    'isg': 'BLy8yqVS9TbD3ccfjNiF3ogPjVputWDfnIVXCpY9yKeKYVzrvsUwbzLXQYkZKZg3',
    'l': 'fBI34Q7rTgLYuJ-wBOfwPurza77OSIRAguPzaNbMi9fPOq1p5fQdW1UsXAT9C3GVFsFvR3lDK4dwBeYBqI2jPGKnNSVsr4DmnmOk-Wf..',
    'lgc': 'kjk1431',
    'sg': '165',
    'sgcookie': 'E100IdDsFyQufwDx5PgaZbRyYBcNyT51RDWZBh2UvRLycfh3hyb8Q7%2BNAwx4mKGSmxHCGjgYaQ18AawLmOlLk3U1WgLgNF1slO66eY3yWUyu%2FbA%3D',
    'skt': 'c02de76fdf0c226c',
    't': 'e482c7bee3d194c73e6e312b981e7cca',
    'tfstk': 'eSD2AO99LKpVG8sIg72aLnKK-awYCJLIiAa_jcmgcr40cVwZ_2U5CneX6RuazVUbG-4fQAzoxhBXDIFg7qe06ja_lPyZX2-WRp9IDmeTneTBd9DOfe2GAB2o6mnYBgI5SBGoDOoj_9SQT2jPPmR4om8w7vQZPb4nmzmjcYqVRym0zOXguoP2Gm4PIODP4-bTqrOZBj7G_Sq84yty4fr8DBg1sxt561FxwuzBDnCO6Sq84yty41CTM8EzRnKA.',
    'tracknick': 'kjk1431',
    'uc1': 'cookie21=WqG3DMC9Eman&cookie15=URm48syIIVrSKA%3D%3D&pas=0&cookie14=UoYelzjpjyD9nw%3D%3D&existShop=false&cookie16=Vq8l%2BKCLySLZMFWHxqs8fwqnEw%3D%3D',
    'uc3': 'vt3=F8dD3CV6JWqgXpl4BvA%3D&lg2=URm48syIIVrSKA%3D%3D&id2=UUphw2LzTK2r3Ai5FQ%3D%3D&nk2=CN1CLfLV3g%3D%3D',
    'uc4': 'id4=0%40U2grGN2A6MrBpgscJYaz7ZwlrwoonyPX&nk4=0%40CrhDS628o%2B9Kg%2B5%2FM8kSMv3Z',
    'unb': '2209757102136',
    'x5sec': '7b22733b32223a2263306362633430333765363334366361222c22617365727665723b33223a22307c434f4b69356173474549764c6d4e51464d4c5046383458382f2f2f2f2f77453d227d',
    'xlly_s': '1',
}

headers = { 
    'accept': '*/*',
    'accept-language': 'zh-CN,zh;q=0.9',
    'authority': 'h5api.m.taobao.com',
    'cache-control': 'no-cache',
    'pragma': 'no-cache',
    'referer': 'https://uland.taobao.com/',
    'sec-ch-ua': '\"Not.A/Brand\";v=\"8\", \"Chromium\";v=\"114\", \"Google Chrome\";v=\"114\"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '\"Windows\"',
    'sec-fetch-dest': 'script',
    'sec-fetch-mode': 'no-cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
}

params = { 
    'AntiCreep': 'true',
    'AntiFlood': 'true',
    'api': 'mtop.alimama.union.xt.en.api.entry',
    'appKey': '12574478',
    'callback': 'mtopjsonp2',
    'data': '{"pNum":0,"pSize":"60","refpid":"mm_26632258_3504122_32538762","variableMap":"{\"q\":\"cos\",\"navigator\":false,\"clk1\":\"3c5fe1276dcd835014a03cab96b23965\",\"union_lens\":\"recoveryid:201_33.51.94.81_7164953_1702449505634;prepvid:201_33.51.94.81_7164953_1702449505634\",\"recoveryId\":\"201_33.61.246.115_7164192_1702449556237\"}","qieId":"36308","spm":"a2e0b.20350158.31919782","app_pvid":"201_33.61.246.115_7164192_1702449556237","ctm":"spm-url:a2e0b.20350158.search.1;page_url:https://uland.taobao.com/sem/tbsearch?refpid=mm_26632258_3504122_32538762&keyword=cos&clk1=3c5fe1276dcd835014a03cab96b23965&upsId=3c5fe1276dcd835014a03cab96b23965&spm=a2e0b.20350158.search.1&pid=mm_26632258_3504122_32538762&union_lens=recoveryid%3A201_33.51.94.81_7164953_1702449505634%3Bprepvid%3A201_33.51.94.81_7164953_1702449505634"}',
    'dataType': 'jsonp',
    'jsv': '2.5.1',
    'sign': '8543e6fa772e7885f43bf8ed8da131a6',
    't': '1702449556632',
    'timeout': '20000',
    'type': 'jsonp',
    'v': '1.0',
}


# 当前时间戳: 1702449674.1595664
response = crawles.get(url, headers=headers, params=params, cookies=cookies,impersonate='chrome110')
print(response.text)

crawles.unicode_toc()