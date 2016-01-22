import json
from unittest.mock import patch

from django.test.client import RequestFactory
from django.test.testcases import TestCase


from 臺灣言語服務.服務 import 服務


class 翻譯服務單元試驗(TestCase):

    def setUp(self):
        self.工具 = RequestFactory()

    def test_正規化翻譯支援腔口(self):
        服務功能 = 服務(全部翻譯母語模型={'臺語': {}, '客話': {}, 'Kaxabu': {}})
        要求 = self.工具.get('/正規化翻譯支援腔口')
        回應 = 服務功能.正規化翻譯支援腔口(要求)
        回應資料 = json.loads(回應.content.decode("utf-8"))
        self.assertIn('臺語', 回應資料['腔口'])
        self.assertIn('客話', 回應資料['腔口'])
        self.assertIn('Kaxabu', 回應資料['腔口'])

    @patch('臺灣言語服務.服務.服務._正規化翻譯實作')
    def test_正規化翻譯(self, 實作mock):
        母語模型 = {
            '摩西用戶端': None,
            '辭典': None,
            '語言模型': None,
            '拼音': None,
            '字綜合標音': None,
        }
        服務功能 = 服務(全部翻譯母語模型={'母語': 母語模型}, 全部合成母語模型={})

        要求 = self.工具.post('/正規化翻譯')
        要求.POST = {
            '查詢腔口': '母語',
            '查詢語句': '你好'
        }
        服務功能.正規化翻譯(要求)
        實作mock.assert_called_once_with(母語模型, '你好')
