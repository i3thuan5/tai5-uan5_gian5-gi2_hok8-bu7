import io
from time import sleep
import wave

from django.test.client import RequestFactory
from django.test.testcases import TestCase


from 臺灣言語服務.模型載入 import 模型載入
from 臺灣言語服務.資料模型路徑 import 合成模型資料夾
from 臺灣言語服務.HTS載入 import HTS載入
from 臺灣言語服務.HTS服務 import HTS服務


class 閩南語合成整合試驗(TestCase):

    @classmethod
    def setUpClass(cls):
        super(cls, cls).setUpClass()
        cls.母語模型 = HTS載入.HTS合成模型(合成模型資料夾, '閩南語')
        sleep(0.1)

    def setUp(self):
        self.assertIn('模型', self.母語模型)
        self.assertIn('拼音', self.母語模型)
        self.assertIn('變調', self.母語模型)
        self.assertIsNotNone(self.母語模型['變調'])
        self.服務功能 = HTS服務(全部合成母語模型={'閩南語': self.母語模型})

    def test_短詞合成(self):
        連線要求 = RequestFactory().get('/語音合成')
        連線要求.GET = {
            '查詢腔口': '閩南語',
            '查詢語句': '你｜li2 好｜ho2'
        }
        連線回應 = self.服務功能.語音合成(連線要求)
        self.assertEqual(連線回應.status_code, 200)
        with io.BytesIO(連線回應.content) as 資料:
            with wave.open(資料, 'rb') as 聲音檔:
                self.assertGreaterEqual(聲音檔.getframerate(), 16000)

    def test_兩句翻譯(self):
        連線要求 = RequestFactory().get('/語音合成')
        連線要求.GET = {
            '查詢腔口': '閩南語',
            '查詢語句': '你｜li2 好-無｜ho2-0bo5 ？｜? 我｜gua2 足｜tsiok4 好｜ho2 ！｜!'
        }
        連線回應 = self.服務功能.語音合成(連線要求)
        self.assertEqual(連線回應.status_code, 200)
        with io.BytesIO(連線回應.content) as 資料:
            with wave.open(資料, 'rb') as 聲音檔:
                self.assertGreaterEqual(聲音檔.getframerate(), 16000)

    def test_空語句就下恬音(self):
        連線要求 = RequestFactory().get('/語音合成')
        連線要求.GET = {
            '查詢腔口': '閩南語',
            '查詢語句': ''
        }
        連線回應 = self.服務功能.語音合成(連線要求)
        self.assertEqual(連線回應.status_code, 200)
        with io.BytesIO(連線回應.content) as 資料:
            with wave.open(資料, 'rb') as 聲音檔:
                self.assertGreaterEqual(聲音檔.getframerate(), 16000)
                self.assertGreater(聲音檔.getnframes(), 0)

    def test_無腔口預設閩南語(self):
        連線要求 = RequestFactory().get('/語音合成')
        連線要求.GET = {
            '查詢腔口': '閩南語',
            '查詢語句': '你｜li2 好-無｜ho2-0bo5 ？｜? 我｜gua2 足｜tsiok4 好｜ho2 ！｜!'
        }
        原本連線回應 = self.服務功能.語音合成(連線要求)

        連線要求 = RequestFactory().get('/語音合成')
        連線要求.GET = {
            '查詢語句': '你｜li2 好-無｜ho2-0bo5 ？｜? 我｜gua2 足｜tsiok4 好｜ho2 ！｜!'
        }
        連線回應 = self.服務功能.語音合成(連線要求)
        self.assertEqual(連線回應.status_code, 200)
        self.assertEqual(連線回應.content, 原本連線回應.content)

    def test_無參數預設閩南語(self):
        連線要求 = RequestFactory().get('/語音合成')
        連線要求.GET = {
            '查詢腔口': '閩南語',
            '查詢語句': '你｜li2 好-無｜ho2-0bo5 ？｜? 我｜gua2 足｜tsiok4 好｜ho2 ！｜!'
        }
        原本連線回應 = self.服務功能.語音合成(連線要求)

        連線要求 = RequestFactory().get('/語音合成')
        連線要求.GET = {}
        連線回應 = self.服務功能.語音合成(連線要求)
        self.assertEqual(連線回應.status_code, 200)
        self.assertEqual(連線回應.content, 原本連線回應.content)
