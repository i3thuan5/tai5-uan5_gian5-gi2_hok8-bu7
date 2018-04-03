from os.path import join
from tempfile import TemporaryDirectory
from unittest.mock import patch

from django.core.management import call_command
from django.test.testcases import TestCase


from 臺灣言語服務.Kaldi語料處理 import Kaldi語料處理
from 臺灣言語工具.音標系統.閩南語.臺灣閩南語羅馬字拼音 import 臺灣閩南語羅馬字拼音
from 臺灣言語服務.kaldi.lexicon import 辭典輸出


class 匯出漢語音節fst單元試驗(TestCase):

    def test_揣出漢語音節(self):
        音節 = Kaldi語料處理.揣出漢語音節種類(
            辭典輸出(臺灣閩南語羅馬字拼音, '拆做音素'),
            ['敢-若｜kan2-na2 散-步｜san3-poo7 咧｜leh4']
        )
        self.assertEqual(
            音節,
            {'kan2', 'na2', 'san3', 'poo7', 'leh4'}
        )

    def test_揣出有音檔名嘛無要緊(self):
        音節 = Kaldi語料處理.揣出漢語音節種類(
            辭典輸出(臺灣閩南語羅馬字拼音, '拆做音素'),
            [
                'tong0000000-0000000無註明-ku0000000 '
                '敢-若｜kan2-na2 散-步｜san3-poo7 咧｜leh4'
            ]
        )
        self.assertEqual(
            音節,
            {'kan2', 'na2', 'san3', 'poo7', 'leh4'}
        )

    def test_無法度解析的免插(self):
        音節 = Kaldi語料處理.揣出漢語音節種類(
            辭典輸出(臺灣閩南語羅馬字拼音, '拆做音素'),
            ['敢-若｜kan2-na2 散-步｜san3-poo7 咧｜咧 !｜!']
        )
        self.assertEqual(
            音節,
            {'kan2', 'na2', 'san3', 'poo7'}
        )

    def test_轉fst(self):
        fst = Kaldi語料處理.轉fst格式(
            辭典輸出(臺灣閩南語羅馬字拼音, '拆做音素'),
            {'kan2', 'na2', 'san3', 'poo7', 'leh4'}
        )
        self.assertEqual(
            fst,
            [
                '0\t0\tkan\tkan',
                '0\t0\tleh\tleh',
                '0\t0\tna\tna',
                '0\t0\tpoo\tpoo',
                '0\t0\tsan\tsan',
                '0\t1',
            ]
        )

    def test_fst仝調一條路就好(self):
        fst = Kaldi語料處理.轉fst格式(
            辭典輸出(臺灣閩南語羅馬字拼音, '拆做音素'),
            {'sui1', 'sui2', 'sui3'}
        )
        self.assertEqual(
            fst,
            [
                '0\t0\tsui\tsui',
                '0\t1',
            ]
        )

    def test_轉辭典檔(self):
        fst = Kaldi語料處理.轉辭典檔(
            辭典輸出(臺灣閩南語羅馬字拼音, '拆做音素'),
            {'kan2', 'na2', 'san3', 'poo7', 'leh4'}
        )
        self.assertEqual(
            fst,
            [
                'kan\tk- a2 n2',
                'leh\tl- e4 ʔ4',
                'na\tn- a2',
                'poo\tp- o7',
                'san\ts- a3 n3'
            ]
        )

    def test_仝音攏出現(self):
        fst = Kaldi語料處理.轉辭典檔(
            辭典輸出(臺灣閩南語羅馬字拼音, '拆做音素'),
            {'sui1', 'sui2', 'sui3'}
        )
        self.assertEqual(
            fst,
            [
                'sui\ts- u1 i1',
                'sui\ts- u2 i2',
                'sui\ts- u3 i3',
            ]
        )

    def test_輕聲佮原本音攏仝款(self):
        fst = Kaldi語料處理.轉辭典檔(
            辭典輸出(臺灣閩南語羅馬字拼音, '拆做音素'),
            {'khiau2', '0sui2', 'sui1', 'sui2', 'sui3'}
        )
        self.assertEqual(
            fst,
            [
                'khiau\tkʰ- i2 a2 u2',
                'sui\ts- u0 i0',
                'sui\ts- u1 i1',
                'sui\ts- u2 i2',
                'sui\ts- u3 i3',
            ]
        )

    def test_外來詞佮原本音攏仝款(self):
        fst = Kaldi語料處理.轉辭典檔(
            辭典輸出(臺灣閩南語羅馬字拼音, '拆做音素'),
            {'khiau2', '1sui2', 'sui1', 'sui2', 'sui3'}
        )
        self.assertEqual(
            fst,
            [
                'khiau\tkʰ- i2 a2 u2',
                'sui\ts- u1 i1',
                'sui\ts- u2 i2',
                'sui\ts- u3 i3',
            ]
        )

    def test_單元音(self):
        fst = Kaldi語料處理.轉辭典檔(
            辭典輸出(臺灣閩南語羅馬字拼音, '拆做音素'),
            {'i1'}
        )
        self.assertEqual(
            fst,
            [
                'i\tʔ- i1',
            ]
        )

    @patch('臺灣言語服務.Kaldi語料處理.Kaldi語料處理.揣出漢語音節種類')
    def test_指令有讀(self, 揣出漢語音節種類mock):
        揣出漢語音節種類mock.return_value = {'kan2', 'na2', 'san3', 'poo7', 'leh4'}
        with TemporaryDirectory() as 資料夾路徑:
            語言文本 = join(資料夾路徑, '語言文本.txt')
            with open(語言文本, 'w') as 檔案:
                print('敢-若｜kan2-na2 散-步｜san3-poo7 咧｜leh4', file=檔案)

            call_command('轉Kaldi音節fst', '台語', '拆做音素', 語言文本, 資料夾路徑)

            self.assertEqual(揣出漢語音節種類mock.call_count, 1)

    @patch('臺灣言語服務.Kaldi語料處理.Kaldi語料處理.轉fst格式')
    def test_指令有輸出fst(self, 轉fst格式mock):
        轉fst格式mock.return_value = [
            '0 0 leh leh',
            '0 0 kan kan',
            '0 0 na na',
            '0 0 poo poo',
            '0 0 san san',
            '0 1',
        ]
        with TemporaryDirectory() as 資料夾路徑:
            語言文本 = join(資料夾路徑, '語言文本.txt')
            with open(語言文本, 'w') as 檔案:
                print('敢-若｜kan2-na2 散-步｜san3-poo7 咧｜leh4', file=檔案)

            call_command('轉Kaldi音節fst', '台語', '拆做音素', 語言文本, 資料夾路徑)

            self.比較檔案(
                join(資料夾路徑, 'data', 'local', 'free-syllable', 'uniform.fst'),
                [
                    '0 0 leh leh',
                    '0 0 kan kan',
                    '0 0 na na',
                    '0 0 poo poo',
                    '0 0 san san',
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

            call_command('轉Kaldi音節fst', '台語', '拆做音素', 語言文本, 資料夾路徑)

            self.比較檔案(
                join(資料夾路徑, 'data', 'local', 'free-syllable', 'lexicon.txt'),
                [
                    'sui2 s- u2 i2',
                ]
            )

    def 比較檔案(self, 檔名, 資料):
        with open(檔名) as 檔案:
            self.assertEqual(檔案.read(), '\n'.join(資料) + '\n')
