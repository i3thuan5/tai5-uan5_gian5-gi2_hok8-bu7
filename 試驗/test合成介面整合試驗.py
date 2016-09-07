import json
from unittest.mock import patch

from django.test.client import RequestFactory
from django.test.testcases import TestCase


from 臺灣言語服務.HTS介面 import HTS介面
from 臺灣言語服務.HTS服務 import HTS服務


class 合成介面單元試驗(TestCase):

    def setUp(self):
        self.工具 = RequestFactory()

    @patch('Pyro4.Proxy')
    def test_支援腔口(self, ProxyMock):
        ProxyMock.return_value = HTS服務()
        服務功能 = HTS介面()
        要求 = self.工具.get('/語音合成支援腔口')
        回應 = 服務功能.語音合成支援腔口(要求)
        回應資料 = json.loads(回應.content.decode("utf-8"))
        self.assertIn('閩南語', 回應資料['腔口'])
        self.assertIn('詔安腔', 回應資料['腔口'])
