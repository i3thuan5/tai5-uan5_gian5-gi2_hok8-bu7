from django.test.testcases import TestCase


from 臺灣言語工具.音標系統.閩南語.臺灣閩南語羅馬字拼音 import 臺灣閩南語羅馬字拼音
from 臺灣言語工具.解析整理.拆文分析器 import 拆文分析器
from 臺灣言語服務.kaldi.lexicon import 辭典輸出


class 辭典輸出單元試驗(TestCase):

    def tearDown(self):
        聲類, 韻類, 調類 = self.輸出.輸出函式(
            拆文分析器.分詞字物件(self.分詞)
        )
        self.assertEqual(聲類, self.聲類結果)
        self.assertEqual(韻類, self.韻類結果)
        self.assertEqual(調類, self.調類結果)

    def test_拆做音素(self):
        self.分詞 = '媠｜sui2'
        self.輸出 = 辭典輸出(臺灣閩南語羅馬字拼音, '拆做音素')
        self.聲類結果 = ['s-']
        self.韻類結果 = [('u', 'u2'), ('i', 'i2')]
        self.調類結果 = {('2', 'i2'), ('2', 'u2')}

    def test_拆做聲韻(self):
        self.分詞 = '媠｜sui2'
        self.輸出 = 辭典輸出(臺灣閩南語羅馬字拼音, '拆做聲韻')
        self.聲類結果 = ['s-']
        self.韻類結果 = [('ui', 'ui2')]
        self.調類結果 = {('2', 'ui2')}

    def test_拆做音節(self):
        self.分詞 = '媠｜sui2'
        self.輸出 = 辭典輸出(臺灣閩南語羅馬字拼音, '拆做音節')
        self.聲類結果 = []
        self.韻類結果 = [('sui', 'sui2')]
        self.調類結果 = {('2', 'sui2')}
