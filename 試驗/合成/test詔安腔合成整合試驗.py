import io
from itertools import chain
from unittest.mock import patch
import wave

from django.test.client import RequestFactory
from django.test.testcases import TestCase


from 臺灣言語服務.HTS服務 import HTS服務
from 臺灣言語服務.HTS介面 import HTS介面
from django.test.utils import override_settings


class 詔安腔合成整合試驗(TestCase):

    def test_短詞合成(self):
        服務介面 = HTS介面()
        連線要求 = RequestFactory().get('/語音合成')
        連線要求.GET = {
            '查詢腔口': '詔安腔',
            '查詢語句': '你｜henˋ 好｜hoo^'
        }
        連線回應 = 服務介面.語音合成(連線要求)
        self.assertEqual(連線回應.status_code, 200)
        with io.BytesIO(bytes(chain(*連線回應.streaming_content))) as 資料:
            with wave.open(資料, 'rb') as 聲音檔:
                self.assertGreaterEqual(聲音檔.getframerate(), 16000)

    def test_兩句翻譯(self):
        服務介面 = HTS介面()
        連線要求 = RequestFactory().get('/語音合成')
        連線要求.GET = {
            '查詢腔口': '詔安腔',
            '查詢語句': '你｜henˋ 好｜hoo^ 無｜moˋ ？ 𠊎｜ngaiˋ 真｜zhinˇ 好｜hoo^ ！'
        }
        連線回應 = 服務介面.語音合成(連線要求)
        self.assertEqual(連線回應.status_code, 200)
        with io.BytesIO(bytes(chain(*連線回應.streaming_content))) as 資料:
            with wave.open(資料, 'rb') as 聲音檔:
                self.assertGreaterEqual(聲音檔.getframerate(), 16000)

    def test_空語句就下恬音(self):
        服務介面 = HTS介面()
        連線要求 = RequestFactory().get('/語音合成')
        連線要求.GET = {
            '查詢腔口': '詔安腔',
            '查詢語句': ''
        }
        連線回應 = 服務介面.語音合成(連線要求)
        self.assertEqual(連線回應.status_code, 200)
        with io.BytesIO(bytes(chain(*連線回應.streaming_content))) as 資料:
            with wave.open(資料, 'rb') as 聲音檔:
                self.assertGreaterEqual(聲音檔.getframerate(), 16000)
                self.assertGreater(聲音檔.getnframes(), 0)

    @override_settings(HTS_ING7_PYRO4=True)
    @patch('Pyro4.locateNS')
    @patch('Pyro4.Proxy')
    def test_用pyro4(self, ProxyMock, _NSmock):
        ProxyMock.return_value = HTS服務()
        服務介面 = HTS介面()
        連線要求 = RequestFactory().get('/語音合成')
        連線要求.GET = {
            '查詢腔口': '詔安腔',
            '查詢語句': '你｜henˋ 好｜hoo^'
        }
        連線回應 = 服務介面.語音合成(連線要求)
        self.assertTrue(ProxyMock.called)
        self.assertEqual(連線回應.status_code, 200)
        with io.BytesIO(bytes(chain(*連線回應.streaming_content))) as 資料:
            with wave.open(資料, 'rb') as 聲音檔:
                self.assertGreaterEqual(聲音檔.getframerate(), 16000)
