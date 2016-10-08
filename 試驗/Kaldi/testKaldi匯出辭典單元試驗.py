from tempfile import mkstemp

from django.test.testcases import TestCase


from 臺灣言語服務.Kaldi語料匯出 import Kaldi語料匯出
from os import remove


class Kaldi匯出辭典單元試驗(TestCase):

    def setUp(self):
        _資源, self.檔案路徑 = mkstemp(suffix='分詞')

    def tearDown(self):
        remove(self.檔案路徑)

    def test_無合法拼音就莫愛(self):
        分詞 = 'la0123006｜la0123006'

        全部詞 = set()
        全部句 = []
        聲類 = set()
        韻類 = {}
        調類 = {}
        Kaldi語料匯出._資料加到辭典(聲類, 韻類, 調類, 全部詞, 全部句, 分詞)
        self.assertEqual(len(聲類), 0)
        self.assertEqual(len(韻類), 0)
        self.assertEqual(len(調類), 0)
        self.assertEqual(len(全部詞), 0)

    def test_漢字無合法就莫愛(self):
        分詞 = '現｜現'

        全部詞 = set()
        全部句 = []
        聲類 = set()
        韻類 = {}
        調類 = {}
        Kaldi語料匯出._資料加到辭典(聲類, 韻類, 調類, 全部詞, 全部句, 分詞)
        self.assertEqual(len(聲類), 0)
        self.assertEqual(len(韻類), 0)
        self.assertEqual(len(調類), 0)
        self.assertEqual(len(全部詞), 0)

    def test_單引號(self):
        分詞 = "'｜'"

        全部詞 = set()
        全部句 = []
        聲類 = set()
        韻類 = {}
        調類 = {}
        Kaldi語料匯出._資料加到辭典(聲類, 韻類, 調類, 全部詞, 全部句, 分詞)
        self.assertEqual(len(聲類), 0)
        self.assertEqual(len(韻類), 0)
        self.assertEqual(len(調類), 0)
        self.assertIn("'｜'\tSIL", 全部詞)

    def test_大分號(self):
        分詞 = "﹔｜﹔"

        全部詞 = set()
        全部句 = []
        聲類 = set()
        韻類 = {}
        調類 = {}
        Kaldi語料匯出._資料加到辭典(聲類, 韻類, 調類, 全部詞, 全部句, 分詞)
        self.assertEqual(len(聲類), 0)
        self.assertEqual(len(韻類), 0)
        self.assertEqual(len(調類), 0)
        self.assertIn("﹔｜﹔\tSIL", 全部詞)
