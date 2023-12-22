# coding = utf-8
import crawles

js = crawles.execjs('j3.js')
l = []
for page in range(1, 6):
    url = 'https://match.yuanrenxue.cn/api/match/12'

    cookies = {
        'Hm_lpvt_9bcbda9cbf86757998a2339a0437208e': '1702371162',
        'Hm_lpvt_c99546cf032aaa5a679230de9a95c7db': '1702371179',
        'Hm_lvt_9bcbda9cbf86757998a2339a0437208e': '1702279829,1702370636',
        'Hm_lvt_c99546cf032aaa5a679230de9a95c7db': '1702279800,1702370625',
        'no-alert3': 'true',
        'qpfccr': 'true',
        'sessionid': '5i6xhqrcss18vm8fm0m2dmmv9oancj99',
        'tk': '-1040984292813191015',
    }

    headers = {
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'authority': 'match.yuanrenxue.cn',
        'cache-control': 'no-cache',
        'pragma': 'no-cache',
        'referer': 'https://match.yuanrenxue.cn/match/12',
        'sec-ch-ua': '\"Microsoft Edge\";v=\"113\", \"Chromium\";v=\"113\", \"Not-A.Brand\";v=\"24\"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '\"Windows\"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.57',
        'x-requested-with': 'XMLHttpRequest',
    }

    params = {
        'm': js.call('abc', page),
        'page': page,
    }

    # 当前时间戳: 1702371380.8508484
    response = crawles.get(url, headers=headers, params=params, cookies=cookies)
    print(response.text)
    for i in response.json()['data']:
        l.append(i['value'])

print(sum(l))
