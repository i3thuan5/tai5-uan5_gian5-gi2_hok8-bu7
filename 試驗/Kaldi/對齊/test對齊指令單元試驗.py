from os.path import join
from shutil import rmtree
from unittest.mock import patch

from django.conf import settings
from django.test.testcases import TestCase
from django.test.utils import override_settings


from 臺灣言語服務.Kaldi語料對齊 import Kaldi語料對齊
from 臺灣言語工具.語音辨識.聲音檔 import 聲音檔


class 對齊指令單元試驗(TestCase):
    def setUp(self):
        self.音檔 = 聲音檔.對參數轉(2, 16, 1, b'sui2khiau2' * 333)

    @patch('臺灣言語服務.Kaldi語料對齊.Kaldi語料對齊.做出切音結果')
    @patch('臺灣言語服務.Kaldi語料對齊.Kaldi語料對齊.對齊成功')
    @patch('臺灣言語工具.系統整合.程式腳本.程式腳本._讀檔案')
    @patch('臺灣言語工具.系統整合.程式腳本.程式腳本._換目錄')
    @patch('臺灣言語工具.系統整合.程式腳本.程式腳本._走指令')
    @override_settings(KALDI_KUE3_TING5='kaldi過程資料')
    def test_有產生kaldi語句(self, _走指令mock, _換目錄mock, 讀檔案mock,
                        _對齊成功mock, _做出切音結果mock):
        Kaldi對齊 = Kaldi語料對齊.匯入音檔(
            '台語', '啥人唸的',
            self.音檔, 'tsiang5 tsiang5\nkhiau2',
        )
        讀檔案mock.return_value = ['句001 A 1 1 sing5-kong1']
        Kaldi對齊.對齊()
        目錄 = join(settings.BASE_DIR, settings.KALDI_KUE3_TING5)
        輸出檔名 = join(目錄, Kaldi對齊.編號名(), 'train', 'text')
        with open(輸出檔名) as 檔案:
            self.assertIn('tsiang5 tsiang5 khiau2', 檔案.read(), 'konn5')
        rmtree(目錄)

    @patch('臺灣言語服務.Kaldi語料對齊.Kaldi語料對齊.做出切音結果')
    @patch('臺灣言語服務.Kaldi語料對齊.Kaldi語料對齊.對齊成功')
    @patch('臺灣言語工具.系統整合.程式腳本.程式腳本._讀檔案')
    @patch('臺灣言語工具.系統整合.程式腳本.程式腳本._換目錄')
    @patch('臺灣言語工具.系統整合.程式腳本.程式腳本._走指令')
    def test_有對齊成功(self, _走指令mock, _換目錄mock, 讀檔案mock, 對齊成功mock, 做出切音結果mock):
        Kaldi對齊 = Kaldi語料對齊.匯入音檔(
            '台語', '啥人唸的',
            self.音檔, 'tsiang5 tsiang5\nkhiau2',
        )
        讀檔案mock.return_value = [
            '句001 A 0.30 0.23 tsiang5',
            '句001 A 0.60 0.23 tsiang5',
            '句001 A 0.83 0.23 khiau2',
        ]
        Kaldi對齊.對齊()
        對齊成功mock.assert_called_once_with([
            {'開始': 0.30, '長度': 0.23, '分詞': 'tsiang5', },
            {'開始': 0.60, '長度': 0.23, '分詞': 'tsiang5', },
            {'開始': 0.83, '長度': 0.23, '分詞': 'khiau2', },
        ])
        做出切音結果mock.assert_called_once_with()

    @patch('臺灣言語服務.Kaldi語料對齊.Kaldi語料對齊.做出切音結果')
    @patch('臺灣言語服務.Kaldi語料對齊.Kaldi語料對齊.對齊成功')
    @patch('臺灣言語工具.系統整合.程式腳本.程式腳本._讀檔案')
    @patch('臺灣言語工具.系統整合.程式腳本.程式腳本._換目錄')
    @patch('臺灣言語工具.系統整合.程式腳本.程式腳本._走指令')
    @override_settings(KALDI_KUE3_TING5='kaldi過程資料')
    def test_有指定過程暫存資料夾(self, _走指令mock, _換目錄mock, 讀檔案mock,
                        對齊成功mock, 做出切音結果mock):
        Kaldi對齊 = Kaldi語料對齊.匯入音檔(
            '台語', '啥人唸的',
            self.音檔, 'tsiang5 tsiang5',
        )
        讀檔案mock.return_value = [
            '句001 A 0.30 0.23 tsiang5',
            '句001 A 0.60 0.23 tsiang5',
            '句001 A 0.83 0.23 khiau2',
        ]
        Kaldi對齊.對齊()
        對齊成功mock.assert_called_once_with([
            {'開始': 0.30, '長度': 0.23, '分詞': 'tsiang5', },
            {'開始': 0.60, '長度': 0.23, '分詞': 'tsiang5', },
            {'開始': 0.83, '長度': 0.23, '分詞': 'khiau2', },
        ])
        做出切音結果mock.assert_called_once_with()
        rmtree(join(settings.BASE_DIR, settings.KALDI_KUE3_TING5))

    @patch('臺灣言語服務.Kaldi語料對齊.Kaldi語料對齊.對齊失敗')
    @patch('臺灣言語工具.系統整合.程式腳本.程式腳本._換目錄')
    @patch('臺灣言語工具.系統整合.程式腳本.程式腳本._走指令')
    def test_錯誤就是對齊失敗(self, 走指令mock, _換目錄mock, 對齊失敗mock):
        Kaldi對齊 = Kaldi語料對齊.匯入音檔(
            '台語', '啥人唸的',
            self.音檔, 'tsiang5 tsiang5',
        )
        走指令mock.side_effect = OSError()
        with self.assertRaises(OSError):
            Kaldi對齊.對齊()
        對齊失敗mock.assert_called_once_with()
