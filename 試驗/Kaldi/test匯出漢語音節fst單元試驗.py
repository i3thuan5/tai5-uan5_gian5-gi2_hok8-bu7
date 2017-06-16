from os.path import join
from tempfile import TemporaryDirectory
from unittest.mock import patch

from django.core.management import call_command
from django.test.testcases import TestCase


from 臺灣言語服務.Kaldi語料處理 import Kaldi語料處理
from 臺灣言語工具.音標系統.閩南語.臺灣閩南語羅馬字拼音 import 臺灣閩南語羅馬字拼音


class 匯出漢語音節fst單元試驗(TestCase):

    def test_函式(self):
        音節 = Kaldi語料處理.揣出漢語音節種類(
            ['敢-若｜kan2-na2 散-步｜san3-poo7 咧｜leh4']
        )
        self.assertEqual(
            音節,
            {'kan2', 'na2', 'san3', 'poo7', 'leh4'}
        )

    def test_轉fst(self):
        fst = Kaldi語料處理.轉fst格式(
            {'kan2', 'na2', 'san3', 'poo7', 'leh4'}
        )
        self.assertEqual(
            fst,
            [
                '0\t0\tkan2｜kan2\t0',
                '0\t0\tleh4｜leh4\t0',
                '0\t0\tna2｜na2\t0',
                '0\t0\tpoo7｜poo7\t0',
                '0\t0\tsan3｜san3\t0',
                '0\t1',
            ]
        )

    def test_轉辭典檔(self):
        fst = Kaldi語料處理.轉辭典檔(
            臺灣閩南語羅馬字拼音,
            {'kan2', 'na2', 'san3', 'poo7', 'leh4'}
        )
        self.assertEqual(
            fst,
            [
                'kan2｜kan2\tk- a2 n2',
                'leh4｜leh4\tl- e4 ʔ4',
                'na2｜na2\tn- a2',
                'poo7｜poo7\tp- o7',
                'san3｜san3\ts- a3 n3'
            ]
        )

    @patch('臺灣言語服務.Kaldi語料處理.Kaldi語料處理.揣出漢語音節種類')
    def test_指令有讀(self, 揣出漢語音節種類mock):
        揣出漢語音節種類mock.return_value = {'kan2', 'na2', 'san3', 'poo7', 'leh4'}
        with TemporaryDirectory() as 資料夾路徑:
            語言文本 = join(資料夾路徑, '語言文本.txt')
            with open(語言文本, 'w') as 檔案:
                print('敢-若｜kan2-na2 散-步｜san3-poo7 咧｜leh4', file=檔案)

            call_command('轉Kaldi音節fst',  '閩南語', 語言文本, 資料夾路徑)

            揣出漢語音節種類mock.assert_called_once_with(
                ['敢-若｜kan2-na2 散-步｜san3-poo7 咧｜leh4']
            )

    @patch('臺灣言語服務.Kaldi語料處理.Kaldi語料處理.轉fst格式')
    def test_指令有輸出fst(self, 轉fst格式mock):
        轉fst格式mock.return_value = [
            '0 0 leh4｜leh4 0',
            '0 0 kan2｜kan2 0',
            '0 0 na2｜na2 0',
            '0 0 poo7｜poo7 0',
            '0 0 san3｜san3 0',
            '0 1',
        ]
        with TemporaryDirectory() as 資料夾路徑:
            語言文本 = join(資料夾路徑, '語言文本.txt')
            with open(語言文本, 'w') as 檔案:
                print('敢-若｜kan2-na2 散-步｜san3-poo7 咧｜leh4', file=檔案)

            call_command('轉Kaldi音節fst',  '閩南語', 語言文本, 資料夾路徑)

            self.比較檔案(
                join(資料夾路徑, 'data', 'local', 'free-syllable', 'uniform.fst'),
                [
                    '0 0 leh4｜leh4 0',
                    '0 0 kan2｜kan2 0',
                    '0 0 na2｜na2 0',
                    '0 0 poo7｜poo7 0',
                    '0 0 san3｜san3 0',
                    '0 1',
                ]
            )

    @patch('臺灣言語服務.Kaldi語料處理.Kaldi語料處理.轉辭典檔')
    def test_指令有輸出辭典檔(self, 轉辭典檔mock):
        轉辭典檔mock.return_value = [
            'sui2 s- u2 i2',
        ]
        with TemporaryDirectory() as 資料夾路徑:
            語言文本 = join(資料夾路徑, '語言文本.txt')
            with open(語言文本, 'w') as 檔案:
                print('敢-若｜kan2-na2 散-步｜san3-poo7 咧｜leh4', file=檔案)

            call_command('轉Kaldi音節fst',  '閩南語', 語言文本, 資料夾路徑)

            self.比較檔案(
                join(資料夾路徑, 'data', 'local', 'free-syllable', 'lexicon.txt'),
                [
                    'sui2 s- u2 i2',
                ]
            )

    def 比較檔案(self, 檔名, 資料):
        with open(檔名) as 檔案:
            self.assertEqual(檔案.read(), '\n'.join(資料) + '\n')
