import json
from time import sleep
from unittest.mock import patch

from django.test.client import RequestFactory
from django.test.testcases import TestCase


from 臺灣言語服務.Moses載入 import Moses載入
from 臺灣言語服務.Moses服務 import Moses服務
from 臺灣言語服務.Moses介面 import Moses介面


class 台語正規化整合試驗(TestCase):

    @classmethod
    def setUpClass(cls):
        super(cls, cls).setUpClass()
        cls.服務 = Moses服務({'台語': Moses載入.摩西翻譯模型('台語', 8500)})
        cls.locatePatch = patch('Pyro4.locateNS')
        cls.ProxyPatch = patch('Pyro4.Proxy')
        cls.locatePatch.start()
        ProxyMock = cls.ProxyPatch.start()
        ProxyMock.return_value = cls.服務
        sleep(30)

    @classmethod
    def tearDownClass(cls):
        cls.locatePatch.stop()
        cls.ProxyPatch.stop()
        cls.服務.停()

    def setUp(self):
        self.服務功能 = Moses介面()

    def test_短詞翻譯(self):
        連線要求 = RequestFactory().get('/正規化翻譯')
        連線要求.GET = {
            '查詢腔口': '台語',
            '查詢語句': '你好'
        }
        連線回應 = self.服務功能.正規化翻譯(連線要求)
        self.assertEqual(連線回應.status_code, 200)
        回應物件 = json.loads(連線回應.content.decode("utf-8"))
        self.assertIn('分詞', 回應物件)
        self.assertIn('綜合標音', 回應物件)

    def test_有多元書寫(self):
        連線要求 = RequestFactory().get('/正規化翻譯')
        連線要求.GET = {
            '查詢腔口': '台語',
            '查詢語句': '你好'
        }
        連線回應 = self.服務功能.正規化翻譯(連線要求)
        self.assertEqual(連線回應.status_code, 200)
        回應物件 = json.loads(連線回應.content.decode("utf-8"))
        self.assertIn('多元書寫', 回應物件)

    def test_兩句翻譯(self):
        連線要求 = RequestFactory().get('/正規化翻譯')
        連線要求.GET = {
            '查詢腔口': '台語',
            '查詢語句': '你好嗎？我很好！'
        }
        連線回應 = self.服務功能.正規化翻譯(連線要求)
        self.assertEqual(連線回應.status_code, 200)
        回應物件 = json.loads(連線回應.content.decode("utf-8"))
        self.assertIn('分詞', 回應物件)
        self.assertIn('綜合標音', 回應物件)

    def test_無腔口預設台語(self):
        連線要求 = RequestFactory().get('/正規化翻譯')
        連線要求.GET = {
            '查詢腔口': '台語',
            '查詢語句': '你好嗎？我很好！'
        }
        連線回應 = self.服務功能.正規化翻譯(連線要求)
        self.assertEqual(連線回應.status_code, 200)
        台語回應物件 = json.loads(連線回應.content.decode("utf-8"))

        連線要求 = RequestFactory().get('/正規化翻譯')
        連線要求.GET = {
            '查詢腔口': '母語',
            '查詢語句': '你好嗎？我很好！'
        }
        連線回應 = self.服務功能.正規化翻譯(連線要求)
        self.assertEqual(連線回應.status_code, 200)
        回應物件 = json.loads(連線回應.content.decode("utf-8"))
        self.assertEqual(回應物件, 台語回應物件)

    def test_無參數預設台語(self):
        連線要求 = RequestFactory().get('/正規化翻譯')
        連線要求.GET = {
            '查詢腔口': '台語',
            '查詢語句': '你好嗎？我很好！'
        }
        連線回應 = self.服務功能.正規化翻譯(連線要求)
        self.assertEqual(連線回應.status_code, 200)
        台語回應物件 = json.loads(連線回應.content.decode("utf-8"))

        連線要求 = RequestFactory().get('/正規化翻譯')
        連線要求.GET = {}
        連線回應 = self.服務功能.正規化翻譯(連線要求)
        self.assertEqual(連線回應.status_code, 200)
        回應物件 = json.loads(連線回應.content.decode("utf-8"))
        self.assertEqual(回應物件, 台語回應物件)

    def test_一个空白(self):
        連線要求 = RequestFactory().get('/正規化翻譯')
        連線要求.GET = {
            '查詢腔口': '台語',
            '查詢語句': ' '
        }
        連線回應 = self.服務功能.正規化翻譯(連線要求)
        self.assertEqual(連線回應.status_code, 200)
        回應物件 = json.loads(連線回應.content.decode("utf-8"))
        self.assertIn('分詞', 回應物件)
