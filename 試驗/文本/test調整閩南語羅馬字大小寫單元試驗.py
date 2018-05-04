from django.test.testcases import TestCase
from 臺灣言語工具.音標系統.台語 import 新白話字
from 臺灣言語工具.音標系統.閩南語.臺灣閩南語羅馬字拼音 import 臺灣閩南語羅馬字拼音

class 調整閩南語羅馬字大小寫單元試驗(TestCase):
    #
    # 照揣著的羅馬字傳統調、數字調，
    # 維持原本的大小寫抑是調整大小寫
    #
    def tearDown(self):
        白話字物件 = 新白話字(self.原本音標)
        臺羅傳統調 = 臺灣閩南語羅馬字拼音(白話字物件.轉換到臺灣閩南語羅馬字拼音()).轉調符()
        結果 = self.調整閩南語羅馬字大小寫(self.原本音標, 臺羅傳統調)
        self.assertEqual(結果, self.預期結果)

    def test_維持全小寫(self):
        self.原本音標 = 'lí'
        self.預期結果 = 'lí'

    def test_維持全大寫(self):
        self.原本音標 = 'LÂ'
        self.預期結果 = 'LÂ'

    def test_維持首字大寫(self):
        self.原本音標 = 'Lí'
        self.預期結果 = 'Lí'

    def test_維持孤字首字大寫(self):
        self.原本音標 = 'Â'
        self.預期結果 = 'Â'

    def test_調整為首字大寫(self):
        self.原本音標 = 'LÂng'
        self.預期結果 = 'Lâng'
    
    def test_調整為全小寫(self):
        self.原本音標 = 'lÂ'
        self.預期結果 = 'lâ'

    def test_右上nn不列入判斷(self):
        self.原本音標 = 'LÂⁿ'
        self.預期結果 = 'LÂⁿ'
