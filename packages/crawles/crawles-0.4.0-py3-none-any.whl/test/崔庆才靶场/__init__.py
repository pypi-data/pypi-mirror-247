import time
import requests
from bs4 import BeautifulSoup
from lxml import etree
import re
import csv

with open('饮品店数据爬取.csv', 'a+', encoding='utf-8', newline='') as f:
    d1 = csv.writer(f)
    for page in range(50):
        url = f'https://www.dianping.com/foshan/ch10/g34236p{page * 15}'
        headers = {
            'Cookie': 's_ViewType=10; _lxsdk_cuid=18c6842708bc8-0b36e182dcd68a-977173c-144000-18c6842708b61; _lxsdk=18c68'
                      '42708bc8-0b36e182dcd68a-977173c-144000-18c6842708b61; _hc.v=c1cf0030-d5ef-fc86-1cd6-fb451580277c.17'
                      '02556236; WEBDFPID=7uwy80wv13005u7z0x07yy57211xv33481x315721179795868z341uz-2017916236683-170255623'
                      '4030CMAEIIIfd79fef3d01d5e9aadc18ccd4d0c95072393; dper=0c075b40afcade64ebc91d28f9b3e75da09e910df1abd'
                      'c06e19f8a5055b3cfbd5bb1b70d174be77924336906bd5df8715f6dbf3c9f16887a7b8d2e553b4a01e4; qruuid=e82ba4'
                      '64-ca46-44f6-ad27-cb177adfa7d9; ll=7fd06e815b796be3df069dec7836c3df; Hm_lvt_602b80cf8079ae6591966c'
                      'c70a3940e7=1702556297; Hm_lpvt_602b80cf8079ae6591966cc70a3940e7=1702557528; _lxsdk_s=18c6842708c-d'
                      'e9-d53-bc3%7C%7C115',

            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        # print(response.text)
        # print(response.status_code)
        soup = BeautifulSoup(response.text, 'lxml')
        url_list = soup.find_all('a', onclick="LXAnalytics('moduleClick', 'shoppic')")
        # print(url_list)
        for u in url_list:
            # print(u['href'])
            response = requests.get(u['href'], headers=headers)
            # print(response.text)
            soup = BeautifulSoup(response.text, 'lxml')
            html = etree.HTML(response.text)
            area = html.xpath('//span[@class="J-current-city"]/text()')  # 解析地区信息
            shopname = html.xpath('//h1[@class="shop-name"]/text()')  # 解析店名信息
            for i in shopname:
                shopname_list = i.strip()
                # print(shopname_list)
            address_list = html.xpath('//div[@class="map_address"]/span[1]/text()')  # 解析地址信息
            tel_data = re.findall(r'(\d{11})|(\d{4})-(\d{7})', response.text, re.S)  # 解析电话信息
            for t in tel_data:
                new_t = t[0]
                # print(new_t)
            avag_list = html.xpath('//span[@id="avgPriceTitle"]/text()')  # 解析人均消费信息

            # f = open('饮品店数据爬取.csv', 'a+', encoding='utf-8', newline='')
            print([area,shopname,address_list,tel_data,avag_list])
            d1.writerow([area,shopname,address_list,tel_data,avag_list])
            time.sleep(2)
f.close()

