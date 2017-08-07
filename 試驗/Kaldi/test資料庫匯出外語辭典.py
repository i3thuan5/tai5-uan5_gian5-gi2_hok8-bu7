from django.test.testcases import TestCase
from 臺灣言語資料庫.資料模型 import 來源表
from 臺灣言語資料庫.資料模型 import 版權表
from 臺灣言語資料庫.資料模型 import 外語表
from 臺灣言語服務.Kaldi語料處理 import Kaldi語料處理


#   /\      /\
#  /  \—-—/  \
# |            |
# \   ( () ()) /
#  ------------
class 資料庫匯出外語辭典試驗(TestCase):

    def setUp(self):
        self.在外語表塞一個例()

    def test匯出一個詞(self):
        fst = Kaldi語料處理.資料庫匯出外語辭典檔()
        self.assertEqual(
            fst,
            [
                '母親\tʔ- a1 b- ə2',
            ]
        )

    def test不匯出重複的詞(self):
        self.在外語表塞一個例()
        fst = Kaldi語料處理.資料庫匯出外語辭典檔()
        self.assertEqual(
            fst,
            [
                '母親\tʔ- a1 b- ə2',
            ]
        )

    def 在外語表塞一個例(self):
        公家 = {
            '收錄者': 來源表.objects.get_or_create(名='系統管理員')[0].編號(),
            '來源': 來源表.objects.get_or_create(名='台文華文線頂辭典')[0].編號(),
            '版權': 版權表.objects.get_or_create(版權='會使公開')[0].pk,
            '種類': '字詞',
            '語言腔口': '臺語',
            '著作所在地': '臺灣',
            '著作年': '2000',
        }
        外語內容 = {
            '外語語言': '華語',
            '外語資料': '母親'.strip(),
            '屬性': {'詞性': 'Na'},
        }
        外語內容.update(公家)
        外語 = 外語表.加資料(外語內容)
        文本內容 = {
            '文本資料': '阿母',
            '音標資料': 'a-bo2',
        }
        文本內容.update(公家)
        外語.翻母語(文本內容)

    def 比較檔案(self, 檔名, 資料):
        with open(檔名) as 檔案:
            self.assertEqual(檔案.read(), '\n'.join(資料) + '\n')

    def 檔案內底有(self, 檔名, 資料):
        with open(檔名) as 檔案:
            self.assertIn(資料, 檔案.read())
