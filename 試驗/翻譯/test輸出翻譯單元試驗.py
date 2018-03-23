import gzip
from os.path import join, isfile, isdir
from shutil import rmtree

from django.test.testcases import TestCase


from 臺灣言語服務.資料模型路徑 import 翻譯語料資料夾
from 臺灣言語服務.Moses模型訓練 import Moses模型訓練
from 臺灣言語服務.models import 訓練過渡格式
from unittest.case import expectedFailure


class 翻譯試驗(TestCase):
    公家內容 = {'來源': 'Dr. Pigu', '年代':  '2017', }

    def setUp(self):
        self.目錄 = 翻譯語料資料夾('臺灣話')

    def tearDown(self):
        if isdir(翻譯語料資料夾('臺灣話')):
            rmtree(翻譯語料資料夾('臺灣話'))
        if isdir(翻譯語料資料夾('臺語')):
            rmtree(翻譯語料資料夾('臺語'))

    def test_有語句檔案(self):
        訓練過渡格式.objects.create(
            文本='食飽未？', 外文='你好嗎？',
            種類='語句', **self.公家內容
        )
        Moses模型訓練.輸出全部語料(self.目錄)
        self.assertTrue(isfile(join(翻譯語料資料夾('臺灣話'), '對齊外語語句.txt.gz')))
        self.assertTrue(isfile(join(翻譯語料資料夾('臺灣話'), '對齊母語語句.txt.gz')))

    def test_有字詞檔案(self):
        訓練過渡格式.objects.create(
            文本='食飽未？', 外文='你好嗎？',
            種類='字詞', **self.公家內容
        )
        Moses模型訓練.輸出全部語料(self.目錄)

        self.assertTrue(isfile(join(翻譯語料資料夾('臺灣話'), '對齊外語字詞.txt.gz')))
        self.assertTrue(isfile(join(翻譯語料資料夾('臺灣話'), '對齊母語字詞.txt.gz')))

    def test_有做語言模型的文本(self):
        訓練過渡格式.objects.create(
            文本='食飽未？', 外文='你好嗎？',
            種類='語句', **self.公家內容
        )
        Moses模型訓練.輸出全部語料(self.目錄)
        self.assertTrue(isfile(join(翻譯語料資料夾('臺灣話'), '語句文本.txt.gz')))
        self.assertTrue(isfile(join(翻譯語料資料夾('臺灣話'), '字詞文本.txt.gz')))

    def test_外語母語語句對應檢查對齊語句(self):
        訓練過渡格式.objects.create(
            文本='食飽未？', 外文='你好嗎？',
            種類='語句', **self.公家內容
        )
        Moses模型訓練.輸出全部語料(self.目錄)
        self.assertEqual(
            self.得著檔案資料(join(翻譯語料資料夾('臺灣話'), '對齊外語語句.txt.gz')),
            sorted(['你好嗎？', '食飽未？'])
        )
        self.assertEqual(
            self.得著檔案資料(join(翻譯語料資料夾('臺灣話'), '對齊母語語句.txt.gz')),
            sorted(['食飽未？', '食飽未？'])
        )

    def test_外語母語語句對應檢查對齊字詞(self):
        訓練過渡格式.objects.create(
            文本='食飽未？', 外文='你好嗎？',
            種類='語句', **self.公家內容
        )
        Moses模型訓練.輸出全部語料(self.目錄)
        self.assertEqual(
            self.得著檔案資料(join(翻譯語料資料夾('臺灣話'), '對齊外語字詞.txt.gz')),
            []
        )
        self.assertEqual(
            self.得著檔案資料(join(翻譯語料資料夾('臺灣話'), '對齊母語字詞.txt.gz')),
            []
        )

    def test_外語母語語句對應檢查文本(self):
        訓練過渡格式.objects.create(
            文本='食飽未？', 外文='你好嗎？',
            種類='語句', **self.公家內容
        )
        Moses模型訓練.輸出全部語料(self.目錄)
        self.assertEqual(
            self.得著檔案資料(join(翻譯語料資料夾('臺灣話'), '語句文本.txt.gz')),
            ['食飽未？']
        )
        self.assertEqual(
            self.得著檔案資料(join(翻譯語料資料夾('臺灣話'), '字詞文本.txt.gz')),
            []
        )

    def test_一個文本(self):
        訓練過渡格式.objects.create(
            文本='食飽未？',
            種類='語句', **self.公家內容
        )
        Moses模型訓練.輸出全部語料(self.目錄)
        self.assertEqual(
            self.得著檔案資料(join(翻譯語料資料夾('臺灣話'), '對齊外語語句.txt.gz')),
            ['食飽未？']
        )
        self.assertEqual(
            self.得著檔案資料(join(翻譯語料資料夾('臺灣話'), '對齊母語語句.txt.gz')),
            ['食飽未？']
        )
        self.assertEqual(
            self.得著檔案資料(join(翻譯語料資料夾('臺灣話'), '語句文本.txt.gz')),
            ['食飽未？']
        )

    def test_檢查正規化數量(self):
        訓練過渡格式.objects.create(
            文本='食飽未？', 外文='你好嗎？',
            種類='語句', **self.公家內容
        )
        訓練過渡格式.objects.create(
            文本='食飽未 ？', 外文='你好嗎？',
            種類='語句', **self.公家內容
        )
        訓練過渡格式.objects.create(
            文本='未', 外文='嗎',
            種類='字詞', **self.公家內容
        )
        訓練過渡格式.objects.create(
            文本='食飽啦！',
            種類='語句', **self.公家內容
        )
        訓練過渡格式.objects.create(
            文本='食',
            種類='字詞', **self.公家內容
        )
        輸出數量 = Moses模型訓練.輸出全部語料(self.目錄)
        self.assertEqual(輸出數量, (2 * 2 + 1, 1 * 2 + 1, 2 + 1, 1 + 1))

    @expectedFailure
    def test_檢查翻譯數量(self):
        訓練過渡格式.objects.create(
            文本='食飽未？', 外文='你好嗎？',
            種類='語句', **self.公家內容
        )
        訓練過渡格式.objects.create(
            文本='食飽未 ？', 外文='你好嗎？',
            種類='語句', **self.公家內容
        )
        訓練過渡格式.objects.create(
            文本='未', 外文='嗎',
            種類='字詞', **self.公家內容
        )
        訓練過渡格式.objects.create(
            文本='食飽啦！',
            種類='語句', **self.公家內容
        )
        訓練過渡格式.objects.create(
            文本='食',
            種類='字詞', **self.公家內容
        )
        輸出數量 = Moses模型訓練.輸出全部語料(self.目錄)
        self.assertEqual(輸出數量, (2, 1, 3, 2))

    def 得著檔案資料(self, 檔名):
        with gzip.open(檔名, 'rt') as 檔案:
            return sorted([逝.strip() for 逝 in 檔案.readlines()])
