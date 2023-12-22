# coding = utf-8
import crawles
l = []
for page in range(1, 6):
    url = 'https://match.yuanrenxue.cn/api/match/1'

    cookies = {
        'Hm_lpvt_c99546cf032aaa5a679230de9a95c7db': '1702385100',
        'Hm_lvt_9bcbda9cbf86757998a2339a0437208e': '1702370772',
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
        'referer': 'https://match.yuanrenxue.cn/match/1',
        'sec-ch-ua': '\"Not.A/Brand\";v=\"8\", \"Chromium\";v=\"114\", \"Google Chrome\";v=\"114\"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '\"Windows\"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
    }
    js = crawles.execjs('j5.js')
    d = js.call('abc')
    print(d)
    params = {
        'page': page,
        'm': d,
        # 'm': '661ed93059d678f5d50909661b269b16丨1702485116',
    }

    # 当前时间戳: 1702385156.5112877
    response = crawles.get(url, headers=headers, params=params, cookies=cookies)
    print(response.text)
    for i in response.json()['data']:
        l.append(i['value'])

print(sum(l)/len(l))
