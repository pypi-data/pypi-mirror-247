# coding = utf-8
import crawles

url = 'https://match.yuanrenxue.cn/api/match/3'

cookies = { 
    'Hm_lpvt_9bcbda9cbf86757998a2339a0437208e': '1702385767',
    'Hm_lpvt_c99546cf032aaa5a679230de9a95c7db': '1702385775',
    'Hm_lvt_9bcbda9cbf86757998a2339a0437208e': '1702370772,1702385582',
    'Hm_lvt_c99546cf032aaa5a679230de9a95c7db': '1702370754,1702381757',
    'no-alert3': 'true',
    'qpfccr': 'true',
    'sessionid': 'ybwnsiiifc00tyhhzkxtdak761e45600',
}

headers = { 
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'accept-language': 'zh-CN,zh;q=0.9',
    'authority': 'match.yuanrenxue.cn',
    'cache-control': 'no-cache',
    'pragma': 'no-cache',
    'referer': 'https://match.yuanrenxue.cn/match/3',
    'sec-ch-ua': '\"Not.A/Brand\";v=\"8\", \"Chromium\";v=\"114\", \"Google Chrome\";v=\"114\"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '\"Windows\"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
}

params = { 
    'page': '2',
}


# 当前时间戳: 1702385891.155822
response = crawles.get(url, headers=headers, params=params, cookies=cookies)
print(response.text)

