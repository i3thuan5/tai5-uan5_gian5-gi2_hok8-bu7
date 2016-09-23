from tempfile import mkstemp

from django.test.testcases import TestCase


from 臺灣言語服務.Kaldi語料匯出 import Kaldi語料匯出
from os import remove


class Kaldi匯出辭典單元試驗(TestCase):

    def setUp(self):
        _資源, self.檔案路徑 = mkstemp(suffix='分詞')

    def tearDown(self):
        remove(self.檔案路徑)

    def test_無合法拼音愛當做噪音(self):
        分詞 = 'la0123006｜la0123006'
        with open(self.檔案路徑, 'w') as 檔案:
            print(分詞, file=檔案)
        聲類, 韻類, 調類, 全部詞 = Kaldi語料匯出._辭典資料(self.檔案路徑)
        self.assertEqual(len(聲類), 0)
        self.assertEqual(len(韻類), 0)
        self.assertEqual(len(調類), 0)
        self.assertEqual(len(全部詞), 3)

    def test_漢字無合法愛當做噪音(self):
        分詞 = '現｜現'
        with open(self.檔案路徑, 'w') as 檔案:
            print(分詞, file=檔案)
        聲類, 韻類, 調類, 全部詞 = Kaldi語料匯出._辭典資料(self.檔案路徑)
        self.assertEqual(len(聲類), 0)
        self.assertEqual(len(韻類), 0)
        self.assertEqual(len(調類), 0)
        self.assertEqual(len(全部詞), 3)

    def test_單引號(self):
        分詞 = "'｜'"
        with open(self.檔案路徑, 'w') as 檔案:
            print(分詞, file=檔案)
        聲類, 韻類, 調類, 全部詞 = Kaldi語料匯出._辭典資料(self.檔案路徑)
        self.assertEqual(len(聲類), 0)
        self.assertEqual(len(韻類), 0)
        self.assertEqual(len(調類), 0)
        self.assertIn("'｜'\tSIL", 全部詞)

    def test_大分號(self):
        分詞 = "﹔｜﹔"
        with open(self.檔案路徑, 'w') as 檔案:
            print(分詞, file=檔案)
        聲類, 韻類, 調類, 全部詞 = Kaldi語料匯出._辭典資料(self.檔案路徑)
        self.assertEqual(len(聲類), 0)
        self.assertEqual(len(韻類), 0)
        self.assertEqual(len(調類), 0)
        self.assertIn("﹔｜﹔\tSIL", 全部詞)
