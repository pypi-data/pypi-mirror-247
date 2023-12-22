# coding = utf-8
import crawles


def get_request_data():
    url = 'https://cs.anjuke.com/ajax/aifang/tuangou/api/'

    cookies = {
        'aQQ_ajkguid': 'B9D6B72E-4C97-4532-9F96-6B691896FF76',
        'ajk-appVersion': '',
        'ctid': '27',
        'fzq_h': 'effdc1bb5c6f6851eefdb94f0ec03e34_1703051990971_f6f7cb0435294fce86eadb5dc049e6fc_47924970993954659798426939757860043325',
        'fzq_js_anjuke_ershoufang_pc': 'a92909c33a122a92ab0eb5561562d15d_1703051993632_24',
        'id58': 'CrIfp2WCgtkbX+5BGEAuAg==',
        'obtain_by': '2',
        'seo_source_type': '0',
        'sessid': 'BCE3493A-1323-4536-9424-D33B388220ED',
        'twe': '2',
        'xxzl_cid': 'dcd7201d2ca04ec29111772c1ef1f5fe',
        'xxzl_deviceid': 'bz8WmaqswGVKj4Fw48BH/tgx2eA1B43y0Z1PJtTA6ZM52pBusV/KQ1VHX4/d3Zlx',
    }

    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Referer': 'https://cs.anjuke.com/sale/qitacs-q-qitacs/?pi=baidu-cpc-cs-qybk1&kwid=129008680037&bd_vid=29451654284995768',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.57',
        'sec-ch-ua': '\"Microsoft Edge\";v=\"113\", \"Chromium\";v=\"113\", \"Not-A.Brand\";v=\"24\"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '\"Windows\"',
    }

    params = {
        'adCode': 'SaleListing',
        'cityId': '27',
        'city_id': '27',
        'num': '5',
    }

    # 当前时间戳: 1703052635.4982533
    response = crawles.get(url, headers=headers, params=params, cookies=cookies)
    return response


def response_parse(response):
    print(response.text)


if __name__ == '__main__':
    response_data = get_request_data()
    response_parse(response_data)
