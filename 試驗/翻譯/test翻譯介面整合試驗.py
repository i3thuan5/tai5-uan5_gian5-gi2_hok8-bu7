import json

from django.test.client import RequestFactory
from django.test.testcases import TestCase


from 臺灣言語服務.Moses介面 import Moses介面


class 翻譯介面整合試驗(TestCase):

    def setUp(self):
        self.工具 = RequestFactory()

    def test_無開服務(self):
        服務功能 = Moses介面()

        要求 = self.工具.get('/正規化翻譯')
        要求.POST = {
            '查詢腔口': '母語',
            '查詢語句': '你好'
        }

        回應 = 服務功能.正規化翻譯(要求)
        self.assertNotEqual(回應.status_code, 200)
        回應資料 = json.loads(回應.content.decode("utf-8"))
        self.assertIn('失敗', 回應資料)
