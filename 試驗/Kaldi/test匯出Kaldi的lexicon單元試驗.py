import io
from os.path import join
from tempfile import TemporaryDirectory

from django.core.management import call_command
from django.test.testcases import TestCase


class 匯出lexicon單元試驗(TestCase):

    def test_有結果(self):
        with TemporaryDirectory() as 資料夾路徑:
            來源 = join(資料夾路徑, 'su.txt')
            with open(來源, 'wt') as tong:
                print('sui2-sui2 e5 sui2-koo1-niu5', file=tong)
            with io.StringIO() as out:
                call_command(
                    '匯出Kaldi的lexicon', '台語', '拆做音素',
                    來源, 資料夾路徑, stdout=out
                )
            結果 = join(資料夾路徑, 'lexicon.txt')
            with open(結果) as kiatko:
                tsuan = kiatko.read()
                self.assertIn('sui2-sui2\ts-', tsuan)
                self.assertIn('e5\t', tsuan)
                self.assertIn('sui2-koo1-niu5\ts-', tsuan)

    def test_部份無羅馬字(self):
        with TemporaryDirectory() as 資料夾路徑:
            來源 = join(資料夾路徑, 'su.txt')
            with open(來源, 'wt') as tong:
                print('B-sann', file=tong)
            with io.StringIO() as out:
                call_command(
                    '匯出Kaldi的lexicon', '台語', '拆做音素',
                    來源, 資料夾路徑, stdout=out
                )
            結果 = join(資料夾路徑, 'lexicon.txt')
            with open(結果) as kiatko:
                tsuan = kiatko.read()
                self.assertIn('B-sann\t', tsuan)
                self.assertIn('e5\t', tsuan)
                self.assertIn('sui2-koo1-niu5\ts-', tsuan)

    def test_有詞的數量(self):
        with TemporaryDirectory() as 資料夾路徑:
            來源 = join(資料夾路徑, 'su.txt')
            with open(來源, 'wt') as tong:
                print('sui2-sui2 e5 sui2-koo1-niu5', file=tong)
            with io.StringIO() as out:
                call_command(
                    '匯出Kaldi的lexicon', '台語', '拆做音素',
                    來源, 資料夾路徑, stdout=out
                )
                self.assertIn('3 詞', out.getvalue())
