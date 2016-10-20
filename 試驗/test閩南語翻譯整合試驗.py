import json
from time import sleep
from unittest.mock import patch

from django.test.client import RequestFactory
from django.test.testcases import TestCase


from 臺灣言語服務.Moses模型訓練 import Moses模型訓練
from 臺灣言語服務.Moses載入 import Moses載入
from 臺灣言語服務.Moses服務 import Moses服務
from 臺灣言語服務.Moses介面 import Moses介面


class 閩南語翻譯整合試驗(TestCase):

    @classmethod
    def setUpClass(cls):
        super(cls, cls).setUpClass()
        try:
            cls.服務 = Moses服務({'閩南語': Moses載入.摩西翻譯模型('閩南語', 8500)})
        except:
            Moses模型訓練.訓練一个摩西翻譯模型('閩南語', '漢語')
            cls.服務 = Moses服務({'閩南語': Moses載入.摩西翻譯模型('閩南語', 8500)})
        cls.ProxyPatch = patch('Pyro4.Proxy')
        ProxyMock = cls.ProxyPatch.start()
        ProxyMock.return_value = cls.服務
        sleep(60)

    @classmethod
    def tearDownClass(cls):
        cls.服務.停()
        cls.ProxyPatch.stop()

    def setUp(self):
        self.服務功能 = Moses介面()

    def test_短詞翻譯(self):
        連線要求 = RequestFactory().get('/正規化翻譯')
        連線要求.GET = {
            '查詢腔口': '閩南語',
            '查詢語句': '你好'
        }
        連線回應 = self.服務功能.正規化翻譯(連線要求)
        self.assertEqual(連線回應.status_code, 200)
        回應物件 = json.loads(連線回應.content.decode("utf-8"))
        self.assertIn('翻譯正規化結果', 回應物件)
        self.assertIn('綜合標音', 回應物件)

    def test_兩句翻譯(self):
        連線要求 = RequestFactory().get('/正規化翻譯')
        連線要求.GET = {
            '查詢腔口': '閩南語',
            '查詢語句': '你好嗎？我很好！'
        }
        連線回應 = self.服務功能.正規化翻譯(連線要求)
        self.assertEqual(連線回應.status_code, 200)
        回應物件 = json.loads(連線回應.content.decode("utf-8"))
        self.assertIn('翻譯正規化結果', 回應物件)
        self.assertIn('綜合標音', 回應物件)

    def test_無腔口預設閩南語(self):
        連線要求 = RequestFactory().get('/正規化翻譯')
        連線要求.GET = {
            '查詢腔口': '閩南語',
            '查詢語句': '你好嗎？我很好！'
        }
        連線回應 = self.服務功能.正規化翻譯(連線要求)
        self.assertEqual(連線回應.status_code, 200)
        閩南語回應物件 = json.loads(連線回應.content.decode("utf-8"))

        連線要求 = RequestFactory().get('/正規化翻譯')
        連線要求.GET = {
            '查詢腔口': '母語',
            '查詢語句': '你好嗎？我很好！'
        }
        連線回應 = self.服務功能.正規化翻譯(連線要求)
        self.assertEqual(連線回應.status_code, 200)
        回應物件 = json.loads(連線回應.content.decode("utf-8"))
        self.assertEqual(回應物件, 閩南語回應物件)

    def test_無參數預設閩南語(self):
        連線要求 = RequestFactory().get('/正規化翻譯')
        連線要求.GET = {
            '查詢腔口': '閩南語',
            '查詢語句': '你好嗎？我很好！'
        }
        連線回應 = self.服務功能.正規化翻譯(連線要求)
        self.assertEqual(連線回應.status_code, 200)
        閩南語回應物件 = json.loads(連線回應.content.decode("utf-8"))

        連線要求 = RequestFactory().get('/正規化翻譯')
        連線要求.GET = {}
        連線回應 = self.服務功能.正規化翻譯(連線要求)
        self.assertEqual(連線回應.status_code, 200)
        回應物件 = json.loads(連線回應.content.decode("utf-8"))
        self.assertEqual(回應物件, 閩南語回應物件)
