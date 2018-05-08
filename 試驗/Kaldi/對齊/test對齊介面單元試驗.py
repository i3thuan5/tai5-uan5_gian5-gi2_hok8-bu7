from base64 import b64encode
import io
import json

from django.test.testcases import TestCase
from django.urls.base import resolve


from 臺灣言語服務.Kaldi介面 import Kaldi對齊
from 臺灣言語服務.KaldiModels import Kaldi對齊結果
from 臺灣言語工具.語音辨識.聲音檔 import 聲音檔


class 對齊介面單元試驗(TestCase):
    def setUp(self):
        self.音檔 = 聲音檔.對參數轉(2, 16000, 1, b'sui2')
        self.blob = b64encode(
            json.dumps(list(self.音檔.wav格式資料()))[1:-1].encode('utf-8')
        ).decode('utf-8')

    def test_有對應函式(self):
        對應 = resolve('/對齊音檔')
        self.assertEqual(對應.func, Kaldi對齊)

    def test_成功(self):
        回應 = self.client.post('/對齊音檔', {
            '語言': '台語',
            'blob': self.blob,
            '文本': 'sannh4',
        })
        self.assertEqual(回應.status_code, 200)

    def test_blob有音檔(self):
        self.client.post('/對齊音檔', {
            '語言': '台語',
            'blob': self.blob,
            '文本': 'sannh4',
        })
        self.assertEqual(
            Kaldi對齊結果.objects.get().聲音檔().wav格式資料(),
            self.音檔.wav格式資料()
        )

    def test_file有音檔(self):
        with io.BytesIO(self.音檔.wav格式資料()) as 音檔:
            self.client.post('/對齊音檔', {
                '語言': '台語',
                '音檔': 音檔,
                '文本': 'sannh4',
            })
        self.assertEqual(
            Kaldi對齊結果.objects.get().聲音檔().wav格式資料(),
            self.音檔.wav格式資料()
        )

    def test_音檔佮blob攏無傳(self):
        回應 = self.client.post('/對齊音檔', {
            '語言': '台語',
            '文本': 'sannh4',
        })
        self.assertEqual(回應.status_code, 400)

    def test_文本無傳(self):
        回應 = self.client.post('/對齊音檔', {
            '語言': '台語',
            'blob': self.blob,
        })
        self.assertEqual(回應.status_code, 400)
