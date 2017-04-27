from os.path import isfile, join
from posix import listdir
from tempfile import TemporaryDirectory

from django.test.testcases import TestCase


from 臺灣言語工具.語音辨識.聲音檔 import 聲音檔
from 臺灣言語服務.Kaldi語料對齊 import Kaldi語料對齊


class 產生對齊音檔單元試驗(TestCase):

    def test_對齊檔案(self):
        語料對齊 = Kaldi語料對齊.匯入音檔(
            '閩南語', '媠媠',
            聲音檔.對參數轉(2, 16, 1, b'sui2khiau2' * 160), 'tsiang5 tsiang5\nkhiau2',
        )
        語料對齊.對齊成功([
            {'開始': 0.30, '長度': 0.23, '分詞': 'tsiang5', },
            {'開始': 0.60, '長度': 0.23, '分詞': 'tsiang5', },
            {'開始': 0.83, '長度': 0.23, '分詞': 'khiau2', },
        ])
        with TemporaryDirectory() as 資料夾路徑:
            語料對齊.產生音檔(資料夾路徑)
            self.assertEqual(len(listdir(資料夾路徑)), 2)

    def test_壓縮檔案(self):
        語料對齊 = Kaldi語料對齊.匯入音檔(
            '閩南語', '媠媠',
            聲音檔.對參數轉(2, 16, 1, b'sui2khiau2' * 160), 'tsiang5 tsiang5\nkhiau2',
        )
        語料對齊.對齊成功([
            {'開始': 0.30, '長度': 0.23, '分詞': 'tsiang5', },
            {'開始': 0.60, '長度': 0.23, '分詞': 'tsiang5', },
            {'開始': 0.83, '長度': 0.23, '分詞': 'khiau2', },
        ])
        with TemporaryDirectory() as 資料夾路徑:
            wav路徑 = join(資料夾路徑, 'wav')
            語料對齊.產生音檔(wav路徑)
            self.assertEqual(len(listdir(資料夾路徑)), 1)
            tar路徑 = join(資料夾路徑, 'tar')
            語料對齊.壓縮音檔(wav路徑, tar路徑)
            self.assertTrue(isfile(tar路徑))
