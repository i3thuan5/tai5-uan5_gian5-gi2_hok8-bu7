import io
from os import listdir
from os.path import join, dirname, isdir
from shutil import rmtree
import wave

from django.test.testcases import TestCase


from 臺灣言語資料庫.資料模型 import 版權表
from 臺灣言語資料庫.欄位資訊 import 會使公開
from 臺灣言語資料庫.資料模型 import 來源表
from 臺灣言語資料庫.資料模型 import 影音表


class 輸出語料單元試驗(TestCase):

    def setUp(self):
        版權表.objects.create(版權=會使公開)
        Pigu = 來源表.objects.create(名='Dr. Pigu')
        self.資料內容 = {
            '收錄者': Pigu.編號(),
            '來源': Pigu.編號(),
            '版權': '會使公開',
            '種類': '語句',
            '語言腔口': '閩南語',
            '著作所在地': '花蓮',
            '著作年': '2015',
        }

        self.目錄 = join(dirname(__file__), '結果目錄')

    def tearDown(self):
        if isdir(self.目錄):
            rmtree(self.目錄)

    def test_影音母語對應(self):
        影音 = self.加一筆影音食飽未()
        self.母語影音加一筆食飽未(影音)
        HTK模型訓練.輸出一種語言語料(self.目錄, '閩南語')
        self.assertEqual(
            len(listdir(join(self.目錄, '標仔'))),
            1
        )
        self.assertEqual(
            len(listdir(join(self.目錄, '音檔'))),
            1
        )

    def test_兩个影音母語對應輸出其中一筆就好(self):
        影音 = self.加一筆影音食飽未()
        self.母語影音加一筆食飽未(影音)
        self.母語影音加一筆食飽未(影音)
        HTK模型訓練.輸出一種語言語料(self.目錄, '閩南語')
        self.assertEqual(
            len(listdir(join(self.目錄, '標仔'))),
            1
        )
        self.assertEqual(
            len(listdir(join(self.目錄, '音檔'))),
            1
        )

    def test_一个影音無對應(self):
        self.加一筆影音食飽未()
        HTK模型訓練.輸出一種語言語料(self.目錄, '閩南語')
        self.assertEqual(
            len(listdir(join(self.目錄, '標仔'))),
            0
        )
        self.assertEqual(
            len(listdir(join(self.目錄, '音檔'))),
            0
        )

    def test_兩層文本(self):
        影音 = self.加一筆影音食飽未()
        第一層文本 = self.母語影音加一筆食飽未(影音)
        self.母語文本加一筆斷詞食飽未(第一層文本)
        self.母語文本加一筆斷詞食飽未(第一層文本)
        HTK模型訓練.輸出一種語言語料(self.目錄, '閩南語')
        self.assertEqual(
            len(listdir(join(self.目錄, '標仔'))),
            1
        )
        self.assertEqual(
            len(listdir(join(self.目錄, '音檔'))),
            1
        )

    def test_無仝語言袂使出現(self):
        影音 = self.加一筆影音食飽未()
        self.母語影音加一筆食飽未(影音)
        self.資料內容['語言腔口'] = '臺語'
        影音 = self.加一筆影音食飽未()
        self.母語影音加一筆食飽未(影音)
        HTK模型訓練.輸出一種語言語料(self.目錄, '臺語')
        self.assertEqual(len(listdir(join(self.目錄, '標仔'))), 1)
        self.assertEqual(len(listdir(join(self.目錄, '音檔'))), 1)

    def 加一筆影音食飽未(self):
        影音資料 = io.BytesIO()
        with wave.open(影音資料, 'wb') as 音檔:
            音檔.setnchannels(1)
            音檔.setframerate(16000)
            音檔.setsampwidth(2)
            音檔.writeframesraw(b'0' * 100)
        影音內容 = {'影音資料': 影音資料}
        影音內容.update(self.資料內容)
        return 影音表.加資料(影音內容)

    def 母語影音加一筆食飽未(self, 影音):
        文本內容 = {'文本資料': '食飽未？'}
        文本內容.update(self.資料內容)
        return 影音.寫文本(文本內容)

    def 母語文本加一筆斷詞食飽未(self, 文本):
        文本內容 = {'文本資料': '食飽 未？'}
        文本內容.update(self.資料內容)
        return 文本.校對做(文本內容)
