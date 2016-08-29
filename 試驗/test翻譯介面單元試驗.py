import json
from unittest.mock import patch

from django.test.client import RequestFactory
from django.test.testcases import TestCase


from 臺灣言語服務.Moses介面 import Moses介面


class 翻譯介面單元試驗(TestCase):

    def setUp(self):
        self.工具 = RequestFactory()

    @patch('Pyro4.Proxy')
    def test_正規化翻譯支援腔口(self, ProxyMock):
        ProxyMock.return_value.支援腔口.return_value = ['臺語', '客話',  'Kaxabu']
        服務功能 = Moses介面()
        要求 = self.工具.get('/正規化翻譯支援腔口')
        回應 = 服務功能.正規化翻譯支援腔口(要求)
        回應資料 = json.loads(回應.content.decode("utf-8"))
        self.assertIn('臺語', 回應資料['腔口'])
        self.assertIn('客話', 回應資料['腔口'])
        self.assertIn('Kaxabu', 回應資料['腔口'])

    @patch('Pyro4.Proxy')
    def test_正規化翻譯get(self, ProxyMock):
        服務功能 = Moses介面()

        要求 = self.工具.get('/正規化翻譯')
        要求.GET = {
            '查詢腔口': '母語',
            '查詢語句': '你好'
        }
        服務功能.正規化翻譯(要求)
        ProxyMock.return_value.正規化翻譯實作.assert_called_once_with('閩南語', '你好')

    @patch('Pyro4.Proxy')
    def test_正規化翻譯post(self, ProxyMock):
        服務功能 = Moses介面()

        要求 = self.工具.post('/正規化翻譯')
        要求.POST = {
            '查詢腔口': '母語',
            '查詢語句': '你好'
        }
        服務功能.正規化翻譯(要求)
        ProxyMock.return_value.正規化翻譯實作.assert_called_once_with('閩南語', '你好')
