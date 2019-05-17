import gzip
import io
from os.path import join, isfile, isdir, exists
from shutil import rmtree
from unittest.mock import patch
import wave

from django.test.testcases import TestCase


from 臺灣言語資料庫.資料模型 import 版權表
from 臺灣言語資料庫.欄位資訊 import 會使公開
from 臺灣言語資料庫.欄位資訊 import 字詞
from 臺灣言語資料庫.資料模型 import 來源表
from 臺灣言語資料庫.資料模型 import 外語表
from 臺灣言語資料庫.資料模型 import 文本表
from 臺灣言語資料庫.資料模型 import 影音表
from 臺灣言語服務.輸出 import 資料輸出工具
from 臺灣言語服務.資料模型路徑 import 翻譯語料資料夾


class 輸出文本單元試驗(TestCase):

    def setUp(self):
        版權表.objects.create(版權=會使公開)
        Pigu = 來源表.objects.create(名='Dr. Pigu')
        self.資料內容 = {
            '收錄者': Pigu.編號(),
            '來源': Pigu.編號(),
            '版權': '會使公開',
            '種類': '語句',
            '語言腔口': '臺灣話',
            '著作所在地': '花蓮',
            '著作年': '2015',
        }

        self.語料 = 資料輸出工具()
        self.目錄 = 翻譯語料資料夾('臺灣話')

    def tearDown(self):
        if isdir(翻譯語料資料夾('臺灣話')):
            rmtree(翻譯語料資料夾('臺灣話'))
        if isdir(翻譯語料資料夾('臺語')):
            rmtree(翻譯語料資料夾('臺語'))

    def test_無語料就啥物攏無(self):
        self.語料.輸出文本語料()
        self.assertFalse(exists(self.目錄))

    def test_愛有一筆無語料就啥物攏無(self):
        self.加一筆外語你好嗎()
        self.語料.輸出文本語料()
        self.assertFalse(exists(self.目錄))

    def test_有做語言模型的文本(self):
        外語 = self.加一筆外語你好嗎()
        self.外語加一筆母語食飽未(外語)
        self.語料.輸出文本語料()
        self.assertTrue(isfile(join(翻譯語料資料夾('臺灣話'), '語句文本.txt.gz')))
        self.assertTrue(isfile(join(翻譯語料資料夾('臺灣話'), '字詞文本.txt.gz')))

    def test_外語母語語句對應檢查文本(self):
        外語 = self.加一筆外語你好嗎()
        self.外語加一筆母語食飽未(外語)
        self.語料.輸出文本語料()
        self.assertEqual(
            self.得著檔案資料(join(翻譯語料資料夾('臺灣話'), '語句文本.txt.gz')),
            ['食-飽-未 ？']
        )
        self.assertEqual(
            self.得著檔案資料(join(翻譯語料資料夾('臺灣話'), '字詞文本.txt.gz')),
            []
        )

    def test_外語母語字詞對應檢查文本(self):
        self.資料內容['種類'] = 字詞
        外語 = self.加一筆外語你好嗎()
        self.外語加一筆母語食飽未(外語)
        self.語料.輸出文本語料()
        self.assertEqual(
            self.得著檔案資料(join(翻譯語料資料夾('臺灣話'), '語句文本.txt.gz')),
            []
        )
        self.assertEqual(
            self.得著檔案資料(join(翻譯語料資料夾('臺灣話'), '字詞文本.txt.gz')),
            ['食-飽-未 ？'])

    def test_外語雙母語對應(self):
        外語 = self.加一筆外語你好嗎()
        self.外語加一筆母語食飽未(外語)
        self.外語加一筆母語食飽未(外語)
        self.語料.輸出文本語料()
        self.assertEqual(
            self.得著檔案資料(join(翻譯語料資料夾('臺灣話'), '語句文本.txt.gz')),
            ['食-飽-未 ？', '食-飽-未 ？']
        )

    def test_外語影音母語對應(self):
        外語 = self.加一筆外語你好嗎()
        影音 = self.外語加一筆母語影音(外語)
        self.影音加一筆母語食飽未(影音)
        self.語料.輸出文本語料()
        self.assertEqual(
            self.得著檔案資料(join(翻譯語料資料夾('臺灣話'), '語句文本.txt.gz')),
            ['食-飽-未 ？']
        )

    def test_影音母語對應(self):
        影音 = self.加一筆影音食飽未()
        self.影音加一筆母語食飽未(影音)
        self.語料.輸出文本語料()
        self.assertEqual(
            self.得著檔案資料(join(翻譯語料資料夾('臺灣話'), '語句文本.txt.gz')),
            ['食-飽-未 ？']
        )

    def test_外語母語文本兩層對應檢查文本(self):
        外語 = self.加一筆外語你好嗎()
        第一層文本 = self.外語加一筆母語食飽未(外語)
        self.母語文本加一筆食飽未矣(第一層文本)
        self.語料.輸出文本語料()
        self.assertEqual(
            self.得著檔案資料(join(翻譯語料資料夾('臺灣話'), '語句文本.txt.gz')),
            ['食-飽-未 矣 ！ ？']
        )

    def test_一個文本(self):
        self.加一筆母語食飽未()
        self.語料.輸出文本語料()
        self.assertEqual(
            self.得著檔案資料(join(翻譯語料資料夾('臺灣話'), '語句文本.txt.gz')),
            ['食-飽-未 ？']
        )

    def test_無仝語言袂使出現(self):
        self.加一筆母語食飽未()
        self.資料內容['語言腔口'] = '臺語'
        self.加一筆母語食飽未()
        資料輸出工具('臺語').輸出文本語料()
        self.assertFalse(
            isfile(join(翻譯語料資料夾('臺灣話'), '語句文本.txt.gz'))
        )

    @patch('臺灣言語資料庫.資料模型.文本表.分詞資料')
    def test_用格式化輸出(self, 分詞資料mocka):
        分詞資料mocka.return_value = ''
        self.加一筆母語食飽未()
        self.語料.輸出文本語料()
        分詞資料mocka.assert_called_once_with()

    def test_無翻譯檔案(self):
        self.加一筆母語食飽未()
        self.語料.輸出文本語料()
        self.assertFalse(exists(join(翻譯語料資料夾('臺灣話'), '對齊母語語句.txt.gz')))

    def 加一筆外語你好嗎(self):
        外語內容 = {'外語語言': '華語', '外語資料': '你好嗎？'}
        外語內容.update(self.資料內容)
        return 外語表.加資料(外語內容)

    def 外語加一筆母語食飽未(self, 外語):
        文本內容 = {'文本資料': '食飽未？'}
        文本內容.update(self.資料內容)
        return 外語.翻母語(文本內容)

    def 外語加一筆母語影音(self, 外語):
        影音資料 = io.BytesIO()
        with wave.open(影音資料, 'wb') as 音檔:
            音檔.setnchannels(1)
            音檔.setframerate(16000)
            音檔.setsampwidth(2)
            音檔.writeframesraw(b'0' * 100)
        影音內容 = {'影音資料': 影音資料}
        影音內容.update(self.資料內容)
        return 外語.錄母語(影音內容)

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

    def 影音加一筆母語食飽未(self, 影音):
        文本內容 = {'文本資料': '食飽未？'}
        文本內容.update(self.資料內容)
        return 影音.寫文本(文本內容)

    def 加一筆母語食飽未(self):
        文本內容 = {'文本資料': '食飽未？'}
        文本內容.update(self.資料內容)
        return 文本表.加資料(文本內容)

    def 母語文本加一筆食飽未矣(self, 文本):
        文本內容 = {'文本資料': '食飽未 矣 ！ ？'}
        文本內容.update(self.資料內容)
        return 文本.校對做(文本內容)

    def 得著檔案資料(self, 檔名):
        with gzip.open(檔名, 'rt') as 檔案:
            return [逝.strip() for 逝 in 檔案.readlines()]
