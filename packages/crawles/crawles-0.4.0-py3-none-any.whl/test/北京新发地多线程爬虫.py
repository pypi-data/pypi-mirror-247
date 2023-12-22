# coding = utf-8
import crawles
from crawles import Request


# 瑞数 3 4 5 6  app获取已经逆向  app的脱壳  小程序爬取
# 魔改加密js逆向
# https://www.cde.org.cn/main/news/listpage/3cc45b396497b598341ce3af000490e5

class SavePipeline(crawles.Pipeline):  # 数据存储类
    def __init__(self):  # 初始化文件
        self.file = open('test.txt', 'w+', encoding='utf-8')

    def save_data(self, item):  # 数据存储
        self.file.write(str(item) + '\n')

    def close(self):  # 关闭调用
        self.file.close()


class ThreadSpider(crawles.ThreadPool):
    save_class = SavePipeline
    for_index_range = (1, 2)  # 初始循环区间
    fail_request_log = True

    def start_requests(self, request, index):
        request.headers = {
            'Accept': '*/*',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Origin': 'http://www.xinfadi.com.cn',
            'Pragma': 'no-cache',
            'Referer': 'http://www.xinfadi.com.cn/priceDetail.html',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.57',
            'X-Requested-With': 'XMLHttpRequest',
        }
        request.data = {
            'current': index,
            'limit': '20',

        }
        request.url = 'http://www.xinfadi.com.cn/getPriceData.html'
        request.method = 'POST'  # GET POST JSON_POST
        request.timeout = 0.1
        request.retry.retry_request = True
        yield request

    def parse(self, item, request, response):
        item.json = response.json()

        # crawles.op(item.json)
        # print(request)
        # print(response.text)

        item['text'] = response.json()
        yield item
        # print(response.text)
        # crawles.op(request)


ThreadSpider()
