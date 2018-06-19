import json
from time import sleep
from unittest.mock import patch

from django.test.client import RequestFactory
from django.test.testcases import TestCase


from 臺灣言語服務.Moses模型訓練 import Moses模型訓練
from 臺灣言語服務.Moses載入 import Moses載入
from 臺灣言語服務.Moses服務 import Moses服務
from 臺灣言語服務.Moses介面 import Moses介面
from 臺灣言語工具.翻譯.摩西工具.安裝摩西翻譯佮相關程式 import 安裝摩西翻譯佮相關程式


class 詔安腔翻譯整合試驗(TestCase):

    @classmethod
    def setUpClass(cls):
        super(cls, cls).setUpClass()
        安裝摩西翻譯佮相關程式.安裝gizapp()
        安裝摩西翻譯佮相關程式.安裝moses(編譯CPU數=4)
        Moses模型訓練.訓練正規化模型('詔安腔', '漢語')
        cls.服務 = Moses服務({'詔安腔': Moses載入.摩西翻譯模型('詔安腔', 8501)})
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
            '查詢腔口': '詔安腔',
            '查詢語句': '你好'
        }
        連線回應 = self.服務功能.正規化翻譯(連線要求)
        self.assertEqual(連線回應.status_code, 200)
        回應物件 = json.loads(連線回應.content.decode("utf-8"))
        self.assertIn('分詞', 回應物件)
        self.assertIn('綜合標音', 回應物件)

    def test_兩句翻譯(self):
        連線要求 = RequestFactory().get('/正規化翻譯')
        連線要求.GET = {
            '查詢腔口': '詔安腔',
            '查詢語句': '你好嗎？我很好！'
        }
        連線回應 = self.服務功能.正規化翻譯(連線要求)
        self.assertEqual(連線回應.status_code, 200)
        回應物件 = json.loads(連線回應.content.decode("utf-8"))
        self.assertIn('分詞', 回應物件)
        self.assertIn('綜合標音', 回應物件)
