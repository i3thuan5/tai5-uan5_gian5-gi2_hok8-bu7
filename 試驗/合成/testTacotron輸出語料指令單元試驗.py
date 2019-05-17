import io
from os import listdir
from os.path import join
from tempfile import TemporaryDirectory
import wave

from django.core.management import call_command
from django.test.testcases import TestCase


from 臺灣言語服務.models import 訓練過渡格式


class Tacotron輸出語料單元試驗(TestCase):

    def test_有10筆文本(self):
        with TemporaryDirectory() as 目錄:
            影音資料 = join(目錄, 'iannim.wav')
            with wave.open(影音資料, 'wb') as 音檔:
                音檔.setnchannels(1)
                音檔.setframerate(16000)
                音檔.setsampwidth(2)
                音檔.writeframesraw(b'0' * 100)
            self.資料內容 = {
                '影音所在': 影音資料,
                '種類': '語句',
                '年代': '2019',
            }
            self.資料內容['文本'] = '媠｜suí'
            self.資料內容['影音語者'] = '豬仔'
            for _ in range(10):
                訓練過渡格式.objects.create(**self.資料內容)
            with io.StringIO() as tong:
                call_command('匯出Tacotron格式資料', '台語', '豬仔', 目錄, stdout=tong)
            self.assertEqual(
                len(listdir(join(目錄, 'taioanoe', 'wavs'))),
                10
            )
