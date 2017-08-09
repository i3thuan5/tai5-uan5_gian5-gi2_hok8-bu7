from django.test.testcases import TestCase
from 臺灣言語資料庫.資料模型 import 來源表
from 臺灣言語資料庫.資料模型 import 版權表
from 臺灣言語資料庫.資料模型 import 外語表
from 臺灣言語服務.Kaldi語料處理 import Kaldi語料處理
from unittest.mock import patch
from tempfile import TemporaryDirectory
from os.path import join
from django.core.management import call_command


#   /\      /\
#  /  \—-—/  \
# |            |
# \   ( () ()) /
#  ------------
class 資料庫匯出外語辭典試驗(TestCase):

    def test匯出一個詞(self):
        self._在外語表塞一個例()
        fst = Kaldi語料處理.資料庫匯出外語辭典檔()
        self.assertEqual(
            fst,
            [
                '母親\tʔ- a1 b- ə2',
            ]
        )

    def test不匯出重複的詞(self):
        self._在外語表塞一個例()
        self._在外語表塞一個例()
        fst = Kaldi語料處理.資料庫匯出外語辭典檔()
        self.assertEqual(
            fst,
            [
                '母親\tʔ- a1 b- ə2',
            ]
        )

    def test不合法的音標(self):
        self._在外語表塞一個例('隨', '便', 'min2')
        fst = Kaldi語料處理.資料庫匯出外語辭典檔()
        self.assertEqual(fst, [])

    def test不合法的文本(self):
        # 6397,chhiah-chang,,赤&#399,;赤&#39918;;,,472,
        self._在外語表塞一個例('隨便', '赤&#39918', 'chhiah-chang')
        fst = Kaldi語料處理.資料庫匯出外語辭典檔()
        self.assertEqual(fst, [])

    @patch('臺灣言語服務.Kaldi語料處理.Kaldi語料處理.資料庫匯出外語辭典檔')
    def test指令匯出辭典檔(self, 資料庫匯出外語辭典檔mock):
        資料庫匯出外語辭典檔mock.return_value = [
            '母親\tʔ- a1 b- ə2',
        ]
        with TemporaryDirectory() as 資料夾路徑:
            call_command('匯出華台辭典', 資料夾路徑)

            self.比較檔案(
                join(資料夾路徑, 'lexicon.txt'),
                資料庫匯出外語辭典檔mock.return_value
            )

    def _在外語表塞一個例(self, 外語資料='母親', 文本資料='阿母', 音標資料='a-bo2'):
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
            '外語資料': 外語資料.strip(),
            '屬性': {'詞性': 'Na'},
        }
        外語內容.update(公家)
        外語 = 外語表.加資料(外語內容)
        文本內容 = {
            '文本資料': 文本資料,
            '音標資料': 音標資料,
        }
        文本內容.update(公家)
        外語.翻母語(文本內容)

    def 比較檔案(self, 檔名, 資料):
        with open(檔名) as 檔案:
            self.assertEqual(檔案.read(), '\n'.join(資料) + '\n')

    def 檔案內底有(self, 檔名, 資料):
        with open(檔名) as 檔案:
            self.assertIn(資料, 檔案.read())
