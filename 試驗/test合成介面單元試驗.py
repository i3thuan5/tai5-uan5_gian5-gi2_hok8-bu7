import json
from unittest.mock import patch

from django.test.client import RequestFactory
from django.test.testcases import TestCase
from django.test.utils import override_settings


from 臺灣言語服務.HTS介面 import HTS介面

@override_settings(HTS_PYRO4=True)
class 合成介面單元試驗(TestCase):

    def setUp(self):
        self.工具 = RequestFactory()

    @patch('Pyro4.Proxy')
    def test_支援腔口(self, ProxyMock):
        ProxyMock.return_value.支援腔口.return_value = ['臺語', '客話', 'Kaxabu']
        服務功能 = HTS介面()
        要求 = self.工具.get('/語音合成支援腔口')
        回應 = 服務功能.語音合成支援腔口(要求)
        回應資料 = json.loads(回應.content.decode("utf-8"))
        self.assertIn('臺語', 回應資料['腔口'])
        self.assertIn('客話', 回應資料['腔口'])
        self.assertIn('Kaxabu', 回應資料['腔口'])

    @patch('Pyro4.Proxy')
    def test_get(self, ProxyMock):
        ProxyMock.return_value.語音合成實作.return_value = {
            'data': 'sui2', 'encoding': 'base64'
        }
        服務功能 = HTS介面()

        要求 = self.工具.get('/語音合成')
        要求.GET = {
            '查詢腔口': '母語',
            '查詢語句': '你好'
        }
        服務功能.語音合成(要求)
        ProxyMock.return_value.語音合成實作.assert_called_once_with('閩南語', '你好')

    @patch('Pyro4.Proxy')
    def test_post(self, ProxyMock):
        ProxyMock.return_value.語音合成實作.return_value = {
            'data': 'sui2', 'encoding': 'base64'
        }
        服務功能 = HTS介面()

        要求 = self.工具.post('/語音合成')
        要求.POST = {
            '查詢腔口': '母語',
            '查詢語句': '你好'
        }
        服務功能.語音合成(要求)
        ProxyMock.return_value.語音合成實作.assert_called_once_with('閩南語', '你好')
