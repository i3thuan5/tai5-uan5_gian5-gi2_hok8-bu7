from django.test.testcases import TestCase
from 臺灣言語服務.文本介面 import 文本介面


class 判斷閩南語羅馬字大小寫單元試驗(TestCase):
    def tearDown(self):
        self.assertEqual(文本介面.判斷羅馬字大小寫(self.羅馬字), self.預期結果)

    # 總共輸出三種判斷：
    # 全小寫 lí lÂ
    # 首字大寫 Lí
    # 全大寫 LÂ
    def test全小寫(self):
        self.羅馬字 = 'lâ'
        self.預期結果 = '全小寫'

    def test全大寫(self):
        self.羅馬字 = 'LÂ'
        self.預期結果 = '全大寫'

    def test首字大寫(self):
        self.羅馬字 = 'Lí'
        self.預期結果 = '首字大寫'

    def test首字小寫視為全小寫(self):
        self.羅馬字 = 'lÂ'
        self.預期結果 = '全小寫'

    def test孤字大寫視為全大寫(self):
        self.羅馬字 = 'M̄'
        self.預期結果 = '首字大寫'

    def test後半混雜視為首字大寫(self):
        self.羅馬字 = 'LíNG'
        self.預期結果 = '首字大寫'

    # 鼻化音不列入計算
    def test鼻化音全小寫(self):
        self.羅馬字 = 'íⁿ'
        self.預期結果 = '全小寫'

    def test鼻化音全大寫(self):
        self.羅馬字 = 'LÂⁿ'
        self.預期結果 = '全大寫'

    def test鼻化音首字大寫(self):
        self.羅馬字 = 'Líⁿ'
        self.預期結果 = '首字大寫'

    # 數字調符不列入計算
    def test數字調符不列入判斷(self):
        self.羅馬字 = 'LA5'
        self.預期結果 = '全大寫'
