from os import listdir
from os.path import join
from tempfile import TemporaryDirectory
import wave

from django.test.testcases import TestCase


from 臺灣言語服務.tacotron.輸出 import Tacotron模型訓練
from 臺灣言語服務.models import 訓練過渡格式
from 臺灣言語工具.音標系統.閩南語.臺灣閩南語羅馬字拼音 import 臺灣閩南語羅馬字拼音


class Tacotron輸出語料單元試驗(TestCase):

    def test_有文本(self):
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
            訓練過渡格式.objects.create(**self.資料內容)
            Tacotron模型訓練.輸出LJ格式(
                目錄, '豬仔', 8000, 臺灣閩南語羅馬字拼音,
            )
            self.確定檔案數量(目錄, 1)

    def test_無文本免輸出(self):
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
            self.資料內容['影音語者'] = '豬仔'
            訓練過渡格式.objects.create(**self.資料內容)

            Tacotron模型訓練.輸出LJ格式(
                目錄, '豬仔', 8000, 臺灣閩南語羅馬字拼音,
            )
            self.確定檔案數量(目錄, 0)

    def test_指定語者(self):
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
            self.資料內容['影音語者'] = '大隻豬仔'
            訓練過渡格式.objects.create(**self.資料內容)

            Tacotron模型訓練.輸出LJ格式(
                目錄, '豬仔', 8000, 臺灣閩南語羅馬字拼音,
            )
            self.確定檔案數量(目錄, 0)

    def test_有回傳數量(self):
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
            for _ in range(3):
                訓練過渡格式.objects.create(**self.資料內容)
            數量 = Tacotron模型訓練.輸出LJ格式(
                目錄, '豬仔', 8000, 臺灣閩南語羅馬字拼音,
            )
            self.assertEqual(數量, 3)

    def 確定檔案數量(self, 目錄, 數量):
        with open(join(目錄, 'taioanoe', 'metadata.csv')) as tong:
            if 數量 == 0:
                self.assertEqual(tong.read().rstrip(), '')
            else:
                self.assertEqual(len(tong.read().rstrip().split('\n')), 數量)
            self.assertEqual(
                len(listdir(join(目錄, 'taioanoe', 'wavs'))),
                數量
            )
