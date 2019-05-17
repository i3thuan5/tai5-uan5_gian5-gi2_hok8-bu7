from django.test.testcases import TestCase


from 臺灣言語服務.Kaldi語料匯出 import Kaldi語料匯出
from 臺灣言語工具.音標系統.閩南語.臺灣閩南語羅馬字拼音 import 臺灣閩南語羅馬字拼音
from 臺灣言語服務.kaldi.lexicon import 辭典輸出


class 資料加到辭典單元試驗(TestCase):

    def setUp(self):
        self.輸出單位 = 辭典輸出(臺灣閩南語羅馬字拼音, '拆做音素')

    def test_合法拼音(self):
        全部詞 = set()
        全部句 = []
        聲類 = set()
        韻類 = {}
        調類 = {}
        Kaldi語料匯出._資料加到辭典(
            聲類, 韻類, 調類, 全部詞, 全部句, '媠｜sui2', self.輸出單位,
            加語料=True,
        )
        self.assertGreater(len(聲類), 0)
        self.assertGreater(len(韻類), 0)
        self.assertGreater(len(調類), 0)
        self.assertEqual(len(全部詞), 1)

    def test_拆做音素(self):
        全部詞 = set()
        全部句 = []
        聲類 = set()
        韻類 = {}
        調類 = {}
        Kaldi語料匯出._資料加到辭典(
            聲類, 韻類, 調類, 全部詞, 全部句, '媠｜sui2', self.輸出單位,
            加語料=True,
        )
        self.assertEqual(聲類, {'s-'})
        self.assertEqual(韻類,  {'i': {'i2'}, 'u': {'u2'}})
        self.assertEqual(調類,  {'2': {'i2', 'u2'}, })

    def test_拆做聲韻(self):
        全部詞 = set()
        全部句 = []
        聲類 = set()
        韻類 = {}
        調類 = {}
        Kaldi語料匯出._資料加到辭典(
            聲類, 韻類, 調類, 全部詞, 全部句, '媠｜sui2', 辭典輸出(臺灣閩南語羅馬字拼音, '拆做聲韻'),
            加語料=True,
        )
        self.assertEqual(聲類, {'s-'})
        self.assertEqual(韻類,  {'ui': {'ui2'}})
        self.assertEqual(調類,  {'2': {'ui2'}, })

    def test_拆做音節(self):
        全部詞 = set()
        全部句 = []
        聲類 = set()
        韻類 = {}
        調類 = {}
        Kaldi語料匯出._資料加到辭典(
            聲類, 韻類, 調類, 全部詞, 全部句, '媠｜sui2', 辭典輸出(臺灣閩南語羅馬字拼音, '拆做音節'),
            加語料=True,
        )
        self.assertEqual(聲類, set())
        self.assertEqual(韻類,  {'sui': {'sui2'}, })
        self.assertEqual(調類,  {'2': {'sui2'}, })

    def test_語料有就會當加入辭典(self):
        全部詞 = set()
        全部句 = []
        聲類 = set()
        韻類 = {}
        調類 = {}
        Kaldi語料匯出._資料加到辭典(
            聲類, 韻類, 調類, 全部詞, 全部句, '我｜gua2 是｜si7 你｜li2', self.輸出單位,
            加語料=True,
        )
        詞數量 = len(全部詞)
        Kaldi語料匯出._資料加到辭典(
            聲類, 韻類, 調類, 全部詞, 全部句, '媠｜sui2', self.輸出單位,
            加語料=False,
        )
        self.assertEqual(len(全部詞), 詞數量 + 1)

    def test_聲無就袂當加入辭典(self):
        全部詞 = set()
        全部句 = []
        聲類 = set()
        韻類 = {}
        調類 = {}
        Kaldi語料匯出._資料加到辭典(
            聲類, 韻類, 調類, 全部詞, 全部句, '是｜si7', self.輸出單位,
            加語料=True,
        )
        Kaldi語料匯出._資料加到辭典(
            聲類, 韻類, 調類, 全部詞, 全部句, '莉｜li7', self.輸出單位,
            加語料=False,
        )
        self.assertEqual(len(聲類), 1)
        self.assertEqual(len(韻類), 1)
        self.assertEqual(len(調類), 1)
        self.assertEqual(len(全部詞), 1)

    def test_韻無就袂當加入辭典(self):
        全部詞 = set()
        全部句 = []
        聲類 = set()
        韻類 = {}
        調類 = {}
        Kaldi語料匯出._資料加到辭典(
            聲類, 韻類, 調類, 全部詞, 全部句, '豬｜ti1', self.輸出單位,
            加語料=True,
        )
        Kaldi語料匯出._資料加到辭典(
            聲類, 韻類, 調類, 全部詞, 全部句, '豬｜tu1', self.輸出單位,
            加語料=False,
        )
        self.assertEqual(len(聲類), 1)
        self.assertEqual(len(韻類), 1)
        self.assertEqual(len(調類), 1)
        self.assertEqual(len(全部詞), 1)

    def test_調無仝就袂使加入辭典(self):
        全部詞 = set()
        全部句 = []
        聲類 = set()
        韻類 = {}
        調類 = {}
        Kaldi語料匯出._資料加到辭典(
            聲類, 韻類, 調類, 全部詞, 全部句, '滇｜tinn7', self.輸出單位,
            加語料=True,
        )
        self.assertEqual(len(韻類['iⁿ']), 1, 韻類)
        self.assertEqual(len(全部詞), 1)
        Kaldi語料匯出._資料加到辭典(
            聲類, 韻類, 調類, 全部詞, 全部句, '甜｜tinn1', self.輸出單位,
            加語料=False,
        )
        self.assertEqual(len(韻類['iⁿ']), 1)
        self.assertEqual(len(全部詞), 1)

    def test_音素無仝就袂使加入辭典(self):
        全部詞 = set()
        全部句 = []
        聲類 = set()
        韻類 = {}
        調類 = {}
        Kaldi語料匯出._資料加到辭典(
            聲類, 韻類, 調類, 全部詞, 全部句, '被｜pi7 所-有｜soo2-u6', self.輸出單位,
            加語料=True,
        )
        self.assertEqual(len(韻類['i']), 1)
        self.assertEqual(len(全部詞), 2)
        Kaldi語料匯出._資料加到辭典(
            聲類, 韻類, 調類, 全部詞, 全部句, '是｜si6', self.輸出單位,
            加語料=False,
        )
        self.assertEqual(len(韻類['i']), 1)
        self.assertEqual(len(全部詞), 2)

    def test_有換逝無要緊(self):
        全部詞 = set()
        全部句 = []
        聲類 = set()
        韻類 = {}
        調類 = {}
        Kaldi語料匯出._資料加到辭典(
            聲類, 韻類, 調類, 全部詞, 全部句, '\n我｜gua2\n是｜si7\n你｜li2', self.輸出單位,
            加語料=True,
        )
        self.assertEqual(len(全部詞), 3)

    def test_無合法拼音就莫愛(self):
        分詞 = 'la0123006｜la0123006'

        全部詞 = set()
        全部句 = []
        聲類 = set()
        韻類 = {}
        調類 = {}
        Kaldi語料匯出._資料加到辭典(
            聲類, 韻類, 調類, 全部詞, 全部句, 分詞, self.輸出單位,
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
            聲類, 韻類, 調類, 全部詞, 全部句, 分詞, self.輸出單位,
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
            聲類, 韻類, 調類, 全部詞, 全部句, 分詞, self.輸出單位,
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
            聲類, 韻類, 調類, 全部詞, 全部句, 分詞, self.輸出單位,
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
            聲類, 韻類, 調類, 全部詞, [], 分詞, self.輸出單位,
            加語料=True,
        )
        self.assertEqual(len(聲類), 0)
        self.assertEqual(len(韻類), 0)
        self.assertEqual(len(調類), 0)
        self.assertIn("NSN\tNSN", 全部詞)
