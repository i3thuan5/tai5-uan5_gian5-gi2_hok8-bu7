from os import listdir
from os.path import join
import wave

from django.test.testcases import TestCase


from 臺灣言語工具.音標系統.閩南語.臺灣閩南語羅馬字拼音 import 臺灣閩南語羅馬字拼音
from 臺灣言語服務.HTS模型訓練 import HTS模型訓練
from 臺灣言語工具.語音合成.漢語語音標仔轉換 import 漢語語音標仔轉換
from tempfile import TemporaryDirectory
from 臺灣言語服務.models import 訓練過渡格式


class 輸出語料單元試驗(TestCase):

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
            HTS模型訓練.輸出語料(
                目錄, '豬仔', 8000, 臺灣閩南語羅馬字拼音, None, 漢語語音標仔轉換
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

            HTS模型訓練.輸出語料(
                目錄, '豬仔', 8000, 臺灣閩南語羅馬字拼音, None, 漢語語音標仔轉換
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

            HTS模型訓練.輸出語料(
                目錄, '豬仔', 8000, 臺灣閩南語羅馬字拼音, None, 漢語語音標仔轉換
            )
            self.確定檔案數量(目錄, 0)

    def 確定檔案數量(self, 目錄, 數量):
        for 資料夾 in ['音檔', '孤音標仔', '相依標仔']:
            self.assertEqual(
                len(listdir(join(目錄, 資料夾))),
                數量
            )
