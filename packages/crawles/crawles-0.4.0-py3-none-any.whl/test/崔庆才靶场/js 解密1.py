# coding = utf-8
import requests
import crawles

page = 1
js = crawles.execjs('js_1.js')
datas = (js.call('token', page))
print(datas)  # 1702282641662
# "b4fd52829b972f76f8df452a71261436"
data = {
    'now': datas['now'],
    'page': datas['page'],
    'token': datas['token'],
}

url = 'https://match2023.yuanrenxue.cn/api/match2023/1'

cookies = {
    'Hm_lpvt_2a795944b81b391f12d70da5971ba616': datas['now'],
    'Hm_lvt_2a795944b81b391f12d70da5971ba616': datas['now'],
    'no-alert3': 'true',
    'qpfccr': 'true',
}

headers = {
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'accept-language': 'zh-CN,zh;q=0.9',
    'authority': 'match2023.yuanrenxue.cn',
    'cache-control': 'no-cache',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'origin': 'https://match2023.yuanrenxue.cn',
    'pragma': 'no-cache',
    'referer': 'https://match2023.yuanrenxue.cn/topic/1',
    'sec-ch-ua': '\"Not.A/Brand\";v=\"8\", \"Chromium\";v=\"114\", \"Google Chrome\";v=\"114\"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '\"Windows\"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
}

# 当前时间戳: 1702281363.4237843
response = requests.post(url, headers=headers, data=data, cookies=cookies)
print(response.text)
