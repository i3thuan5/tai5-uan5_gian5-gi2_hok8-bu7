from os.path import join
from tempfile import TemporaryDirectory
from unittest.mock import patch

from django.core.management import call_command
from django.test.testcases import TestCase
from 臺灣言語服務.Kaldi語料處理 import Kaldi語料處理
from 臺灣言語工具.解析整理.拆文分析器 import 拆文分析器
from 臺灣言語服務.models import 訓練過渡格式


#   /\      /\
#  /  \—-—/  \
# |            |
# \   ( () ()) /
#  ------------
class 資料庫匯出外文辭典試驗(TestCase):

    def test匯出一個詞(self):
        self._在外文表塞一個例()
        fst = Kaldi語料處理.資料庫匯出外語辭典檔(set())
        self.assertEqual(
            fst,
            [
                '母親\tʔ- a1 b- ə2',
            ]
        )

    def test不匯出重複的詞(self):
        self._在外文表塞一個例()
        self._在外文表塞一個例()
        fst = Kaldi語料處理.資料庫匯出外語辭典檔(set())
        self.assertEqual(
            fst,
            [
                '母親\tʔ- a1 b- ə2',
            ]
        )

    def test外文空白愛提掉(self):
        self._在外文表塞一個例('母 親', '阿母', 'a-bo2')
        fst = Kaldi語料處理.資料庫匯出外語辭典檔(set())
        self.assertEqual(
            fst,
            [
                '母親\tʔ- a1 b- ə2',
            ]
        )

    def test不合法的音標(self):
        self._在外文表塞一個例('隨', '便', 'min2')
        fst = Kaldi語料處理.資料庫匯出外語辭典檔(set())
        self.assertEqual(fst, [])

    def test預設詞(self):
        self._在外文表塞一個例()
        fst = Kaldi語料處理.資料庫匯出外語辭典檔({'漂亮 s u i'})
        self.assertEqual(
            fst,
            sorted([
                '漂亮 s u i',
                '母親\tʔ- a1 b- ə2'
            ])
        )

    @patch('臺灣言語服務.Kaldi語料處理.Kaldi語料處理.資料庫匯出外語辭典檔')
    def test指令匯出辭典檔愛有通用的符號(self, 資料庫匯出外語辭典檔mock):
        資料庫匯出外語辭典檔mock.return_value = sorted([
            'SIL\tSIL',
            '<UNK>\tSPN',
            'SPN\tSPN',
            '母親\tʔ- a1 b- ə2',
        ])
        with TemporaryDirectory() as 資料夾路徑:
            call_command('匯出華台辭典', 資料夾路徑)

            self.比較檔案(
                join(資料夾路徑, 'lexicon.txt'),
                sorted([
                    'SIL\tSIL',
                    '<UNK>\tSPN',
                    'SPN\tSPN',
                    '母親\tʔ- a1 b- ə2',
                ])
            )

    def _在外文表塞一個例(self, 外文資料='母親', 文本資料='阿母', 音標資料='a-bo2'):
        公家內容 = {'來源': '台文華文線頂辭典', '種類':  '字詞', '年代':  '2017', }

        訓練過渡格式.objects.create(
            文本=拆文分析器.對齊句物件(文本資料, 音標資料).看分詞(),
            外文=外文資料,
            **公家內容
        )

    def 比較檔案(self, 檔名, 資料):
        with open(檔名) as 檔案:
            self.assertEqual(檔案.read(), '\n'.join(資料) + '\n')

    def 檔案內底有(self, 檔名, 資料):
        with open(檔名) as 檔案:
            self.assertIn(資料, 檔案.read())
