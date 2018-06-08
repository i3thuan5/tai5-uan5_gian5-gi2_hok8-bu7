from base64 import b64encode
import io
import json
from os.path import abspath, dirname, join

from django.test.testcases import TestCase
from django.urls.base import resolve


from 臺灣言語服務.Kaldi介面 import Kaldi辨識
from 臺灣言語工具.語音辨識.聲音檔 import 聲音檔
from 臺灣言語服務.KaldiModels import Kaldi辨識結果


class 辨識介面單元試驗(TestCase):
    def setUp(self):
        self.音檔 = 聲音檔.對參數轉(2, 16000, 1, b'sui2')
        self.blob = b64encode(
            json.dumps(list(self.音檔.wav格式資料()))[1:-1].encode('utf-8')
        ).decode('utf-8')

    def test_有對應函式(self):
        對應 = resolve('/辨識音檔')
        self.assertEqual(對應.func, Kaldi辨識)

    def test_成功(self):
        回應 = self.client.post('/辨識音檔', {
            '語言': '台語',
            'blob': self.blob,
        })
        self.assertEqual(回應.status_code, 200)

    def test_blob有音檔(self):
        self.client.post('/辨識音檔', {
            '語言': '台語',
            'blob': self.blob,
        })
        self.assertEqual(
            Kaldi辨識結果.objects.get().聲音檔().wav格式資料(),
            self.音檔.wav格式資料()
        )

    def test_file有音檔(self):
        with io.BytesIO(self.音檔.wav格式資料()) as 音檔:
            self.client.post('/辨識音檔', {
                '語言': '台語',
                '音檔': 音檔,
            })
        self.assertEqual(
            Kaldi辨識結果.objects.get().聲音檔().wav格式資料(),
            self.音檔.wav格式資料()
        )

    def test_短檔毋是wav(self):
        with io.BytesIO(b'sui2') as 音檔:
            回應 = self.client.post('/辨識音檔', {
                '語言': '台語',
                '音檔': 音檔,
            })
        self.assertEqual(回應.status_code, 400)

    def test_長檔mp3(self):
        with open(join(dirname(abspath(__file__)), 'imtong', 'sui2.mp3'), 'rb') as mp3_tong:
            with io.BytesIO(mp3_tong.read()) as 音檔:
                self.client.post('/辨識音檔', {
                    '語言': '台語',
                    '音檔': 音檔,
                })
        Kaldi辨識結果.objects.get().聲音檔().wav格式資料()

    def test_音檔佮blob攏無傳(self):
        回應 = self.client.post('/辨識音檔', {
            '語言': '台語',
        })
        self.assertEqual(回應.status_code, 400)
