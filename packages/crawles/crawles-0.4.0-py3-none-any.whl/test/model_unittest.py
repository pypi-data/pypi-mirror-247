import unittest
import crawles


class TestStringMethods(unittest.TestCase):

    def test_head_format(self):
        data1 = '''
            :Accept: */*
            Accept-Encoding:zh-CN,zh;q=0.9
            X-Requested-With      :   XMLHttpRequest
            sec-ch-ua: "Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"
            sec-ch-ua-mobile: ?0
            sec-ch-ua-platform: "Windows"
            '''
        data = {'Accept': '*/*', 'Accept-Encoding': 'zh-CN,zh;q=0.9', 'X-Requested-With': 'XMLHttpRequest',
                'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
                'sec-ch-ua-mobile': '?0', 'sec-ch-ua-platform': '"Windows"'}
        self.assertEqual(crawles.head_format(data1), data)

    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')  # 是否一致
        self.assertNotEqual(11, 22)  # # 是否一致
        self.assertTrue('FOO'.isupper())  # True
        self.assertFalse('Foo'.isupper())  # False
        self.assertIn('错误', '账号错误')  # in
        self.assertNotIn('错误', '登录成功')


if __name__ == '__main__':
    unittest.main()
