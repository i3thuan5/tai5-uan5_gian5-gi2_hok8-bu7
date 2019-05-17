from os.path import join
from tempfile import TemporaryDirectory

from django.test.testcases import TestCase


from 臺灣言語服務.Kaldi語料匯出 import Kaldi語料匯出
from 臺灣言語工具.音標系統.閩南語.臺灣閩南語羅馬字拼音 import 臺灣閩南語羅馬字拼音
from 臺灣言語服務.kaldi.lexicon import 辭典輸出


class Kaldi匯出辭典資料單元試驗(TestCase):

    def test_檢查silence_phones(self):
        辭典資料 = Kaldi語料匯出.初使化辭典資料()
        這擺參數 = {
            '辭典輸出物件': 辭典輸出(臺灣閩南語羅馬字拼音, '拆做音素'),
            '一逝': '我｜gua2 就-是｜to7-si7 你｜li2 ！｜! NSN',
            '加語料': True
        }
        這擺參數.update(辭典資料)
        Kaldi語料匯出._資料加到辭典(**這擺參數)
        with TemporaryDirectory() as 資料夾路徑:
            Kaldi語料匯出.匯出辭典資料(
                辭典資料, 資料夾路徑, '語料資料夾'
            )
            辭典路徑 = join(資料夾路徑, '語料資料夾', 'local', 'dict')
            self.檔案內底有(
                join(辭典路徑, 'silence_phones.txt'),
                'SIL'
            )
            self.檔案內底有(
                join(辭典路徑, 'silence_phones.txt'),
                'NSN'
            )

    def test_檢查nonsilence_phones(self):
        辭典資料 = Kaldi語料匯出.初使化辭典資料()
        這擺參數 = {
            '辭典輸出物件': 辭典輸出(臺灣閩南語羅馬字拼音, '拆做音素'),
            '一逝': '我｜gua2 就-是｜to7-si7 你｜li2 ！｜! NSN',
            '加語料': True
        }
        這擺參數.update(辭典資料)
        Kaldi語料匯出._資料加到辭典(**這擺參數)
        with TemporaryDirectory() as 資料夾路徑:
            Kaldi語料匯出.匯出辭典資料(
                辭典資料, 資料夾路徑, '語料資料夾'
            )
            辭典路徑 = join(資料夾路徑, '語料資料夾', 'local', 'dict')
            self.檔案內底有(
                join(辭典路徑, 'nonsilence_phones.txt'),
                'g-'
            )
            self.檔案內底有(
                join(辭典路徑, 'nonsilence_phones.txt'),
                't-'
            )
            self.檔案內底有(
                join(辭典路徑, 'nonsilence_phones.txt'),
                'i2 i7'
            )

    def test_檢查extra_questions(self):
        辭典資料 = Kaldi語料匯出.初使化辭典資料()
        這擺參數 = {
            '辭典輸出物件': 辭典輸出(臺灣閩南語羅馬字拼音, '拆做音素'),
            '一逝': '我｜gua2 就-是｜to7-si7 你｜li2 ！｜! NSN',
            '加語料': True
        }
        這擺參數.update(辭典資料)
        Kaldi語料匯出._資料加到辭典(**這擺參數)
        with TemporaryDirectory() as 資料夾路徑:
            Kaldi語料匯出.匯出辭典資料(
                辭典資料, 資料夾路徑, '語料資料夾'
            )
            辭典路徑 = join(資料夾路徑, '語料資料夾', 'local', 'dict')
            self.檔案內底有(
                join(辭典路徑, 'extra_questions.txt'),
                'a2 i2 u2'
            )
            self.檔案內底有(
                join(辭典路徑, 'extra_questions.txt'),
                'i7 ə7'
            )

    def test_檢查optional_silence(self):
        辭典資料 = Kaldi語料匯出.初使化辭典資料()
        這擺參數 = {
            '辭典輸出物件': 辭典輸出(臺灣閩南語羅馬字拼音, '拆做音素'),
            '一逝': '我｜gua2 就-是｜to7-si7 你｜li2 ！｜! NSN',
            '加語料': True
        }
        這擺參數.update(辭典資料)
        Kaldi語料匯出._資料加到辭典(**這擺參數)
        with TemporaryDirectory() as 資料夾路徑:
            Kaldi語料匯出.匯出辭典資料(
                辭典資料, 資料夾路徑, '語料資料夾'
            )
            辭典路徑 = join(資料夾路徑, '語料資料夾', 'local', 'dict')
            self.比較檔案(
                join(辭典路徑, 'optional_silence.txt'),
                ['SIL']
            )

    def test_檢查lexicon(self):
        辭典資料 = Kaldi語料匯出.初使化辭典資料()
        這擺參數 = {
            '辭典輸出物件': 辭典輸出(臺灣閩南語羅馬字拼音, '拆做音素'),
            '一逝': '我｜gua2 就-是｜to7-si7 你｜li2 ！｜! NSN',
            '加語料': True
        }
        這擺參數.update(辭典資料)
        Kaldi語料匯出._資料加到辭典(**這擺參數)
        with TemporaryDirectory() as 資料夾路徑:
            Kaldi語料匯出.匯出辭典資料(
                辭典資料, 資料夾路徑, '語料資料夾'
            )
            辭典路徑 = join(資料夾路徑, '語料資料夾', 'local', 'dict')
            self.檔案內底有(
                join(辭典路徑, 'lexicon.txt'),
                '就-是｜to7-si7\tt- ə7 s- i7'
            )

    def test_檢查lexicon_標點符號(self):
        辭典資料 = Kaldi語料匯出.初使化辭典資料()
        這擺參數 = {
            '辭典輸出物件': 辭典輸出(臺灣閩南語羅馬字拼音, '拆做音素'),
            '一逝': 'gua2 to7-si7 你 ！',
            '加語料': True
        }
        這擺參數.update(辭典資料)
        Kaldi語料匯出._資料加到辭典(**這擺參數)
        with TemporaryDirectory() as 資料夾路徑:
            Kaldi語料匯出.匯出辭典資料(
                辭典資料, 資料夾路徑, '語料資料夾'
            )
            辭典路徑 = join(資料夾路徑, '語料資料夾', 'local', 'dict')
            self.檔案內底有(
                join(辭典路徑, 'lexicon.txt'),
                '！\tSIL'
            )

    def test_檢查lexicon_全羅文(self):
        辭典資料 = Kaldi語料匯出.初使化辭典資料()
        這擺參數 = {
            '辭典輸出物件': 辭典輸出(臺灣閩南語羅馬字拼音, '拆做音素'),
            '一逝': 'gua2 to7-si7 li2 ！',
            '加語料': True
        }
        這擺參數.update(辭典資料)
        Kaldi語料匯出._資料加到辭典(**這擺參數)
        with TemporaryDirectory() as 資料夾路徑:
            Kaldi語料匯出.匯出辭典資料(
                辭典資料, 資料夾路徑, '語料資料夾'
            )
            辭典路徑 = join(資料夾路徑, '語料資料夾', 'local', 'dict')
            self.檔案內底有(
                join(辭典路徑, 'lexicon.txt'),
                'gua2\tg- u2 a2'
            )
            self.檔案內底有(
                join(辭典路徑, 'lexicon.txt'),
                'to7-si7\tt- ə7 s- i7'
            )

    def 比較檔案(self, 檔名, 資料):
        with open(檔名) as 檔案:
            self.assertEqual(檔案.read(), '\n'.join(資料) + '\n')

    def 檔案內底有(self, 檔名, 資料):
        with open(檔名) as 檔案:
            self.assertIn(資料, 檔案.read())
