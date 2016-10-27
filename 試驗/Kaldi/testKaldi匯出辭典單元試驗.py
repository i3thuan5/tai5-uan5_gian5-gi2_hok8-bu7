from os import remove
from tempfile import mkstemp

from django.test.testcases import TestCase


from 臺灣言語服務.Kaldi語料匯出 import Kaldi語料匯出
from 臺灣言語工具.音標系統.閩南語.臺灣閩南語羅馬字拼音 import 臺灣閩南語羅馬字拼音


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
        Kaldi語料匯出._資料加到辭典(
            聲類, 韻類, 調類, 全部詞, 全部句, 分詞, 臺灣閩南語羅馬字拼音,
            加語料=True,
        )
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
        Kaldi語料匯出._資料加到辭典(
            聲類, 韻類, 調類, 全部詞, 全部句, 分詞, 臺灣閩南語羅馬字拼音,
            加語料=True,
        )
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
        Kaldi語料匯出._資料加到辭典(
            聲類, 韻類, 調類, 全部詞, 全部句, 分詞, 臺灣閩南語羅馬字拼音,
            加語料=True,
        )
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
        Kaldi語料匯出._資料加到辭典(
            聲類, 韻類, 調類, 全部詞, 全部句, 分詞, 臺灣閩南語羅馬字拼音,
            加語料=True,
        )
        self.assertEqual(len(聲類), 0)
        self.assertEqual(len(韻類), 0)
        self.assertEqual(len(調類), 0)
        self.assertIn("﹔｜﹔\tSIL", 全部詞)

    def test_環境噪音(self):
        分詞 = "NSN"

        全部詞 = set()
        聲類 = set()
        韻類 = {}
        調類 = {}
        Kaldi語料匯出._資料加到辭典(
            聲類, 韻類, 調類, 全部詞, [], 分詞, 臺灣閩南語羅馬字拼音,
            加語料=True,
        )
        self.assertEqual(len(聲類), 0)
        self.assertEqual(len(韻類), 0)
        self.assertEqual(len(調類), 0)
        self.assertIn("NSN\tNSN", 全部詞)

    def test_合法拼音(self):
        全部詞 = set()
        全部句 = []
        聲類 = set()
        韻類 = {}
        調類 = {}
        Kaldi語料匯出._資料加到辭典(
            聲類, 韻類, 調類, 全部詞, 全部句, '媠｜sui2', 臺灣閩南語羅馬字拼音,
            加語料=True,
        )
        self.assertGreater(len(聲類), 0)
        self.assertGreater(len(韻類), 0)
        self.assertGreater(len(調類), 0)
        self.assertEqual(len(全部詞), 1)

    def test_合法拼音語料有(self):
        全部詞 = set()
        全部句 = []
        聲類 = set()
        韻類 = {}
        調類 = {}
        Kaldi語料匯出._資料加到辭典(
            聲類, 韻類, 調類, 全部詞, 全部句, '我｜gua2 是｜si7', 臺灣閩南語羅馬字拼音,
            加語料=True,
        )
        詞數量 = len(全部詞)
        Kaldi語料匯出._資料加到辭典(
            聲類, 韻類, 調類, 全部詞, 全部句, '媠｜sui2', 臺灣閩南語羅馬字拼音,
            加語料=False,
        )
        self.assertEqual(len(全部詞), 詞數量 + 1)

    def test_合法拼音毋過語料無(self):
        全部詞 = set()
        全部句 = []
        聲類 = set()
        韻類 = {}
        調類 = {}
        Kaldi語料匯出._資料加到辭典(
            聲類, 韻類, 調類, 全部詞, 全部句, '是｜si7', 臺灣閩南語羅馬字拼音,
            加語料=True,
        )
        Kaldi語料匯出._資料加到辭典(
            聲類, 韻類, 調類, 全部詞, 全部句, '媠｜sui2', 臺灣閩南語羅馬字拼音,
            加語料=False,
        )
        self.assertEqual(len(聲類), 1)
        self.assertEqual(len(韻類), 1)
        self.assertEqual(len(調類), 1)
        self.assertEqual(len(全部詞), 1)
