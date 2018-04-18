from os.path import join
from shutil import rmtree
from unittest.mock import patch

from django.conf import settings
from django.test.testcases import TestCase
from django.test.utils import override_settings


from 臺灣言語工具.語音辨識.聲音檔 import 聲音檔
from 臺灣言語服務.Kaldi語料辨識 import Kaldi語料辨識


class 辨識指令單元試驗(TestCase):
    def setUp(self):
        self.音檔 = 聲音檔.對參數轉(2, 16, 1, b'sui2khiau2' * 333)

    @patch('臺灣言語工具.系統整合.程式腳本.程式腳本._讀檔案')
    @patch('臺灣言語工具.系統整合.程式腳本.程式腳本._換目錄')
    @patch('臺灣言語工具.系統整合.程式腳本.程式腳本._走指令')
    @override_settings(KALDI_KUE3_TING5='kaldi過程資料')
    def test_有產生語句(self, _走指令mock, _換目錄mock, 讀檔案mock):
        Kaldi辨識 = Kaldi語料辨識.匯入音檔(
            '台語', '啥人唸的',
            self.音檔, 'tsiang5 tsiang5',
        )
        讀檔案mock.return_value = ['句001 sing5-kong1']
        Kaldi辨識.辨識()
        目錄 = join(settings.BASE_DIR, settings.KALDI_KUE3_TING5)
        輸出檔名 = join(目錄, Kaldi辨識.編號名(), 'train', 'segments')
        with open(輸出檔名) as 檔案:
            self.assertGreater(len(檔案.read()), 0)
        rmtree(目錄)

    @patch('臺灣言語服務.Kaldi語料辨識.Kaldi語料辨識.辨識成功')
    @patch('臺灣言語工具.系統整合.程式腳本.程式腳本._讀檔案')
    @patch('臺灣言語工具.系統整合.程式腳本.程式腳本._換目錄')
    @patch('臺灣言語工具.系統整合.程式腳本.程式腳本._走指令')
    def test_有辨識成功(self, _走指令mock, _換目錄mock, 讀檔案mock, 辨識成功mock):
        Kaldi辨識 = Kaldi語料辨識.匯入音檔(
            '台語', '啥人唸的',
            self.音檔, 'tsiang5 tsiang5',
        )
        讀檔案mock.return_value = ['句001 sing5-kong1']
        Kaldi辨識.辨識()
        辨識成功mock.assert_called_once_with('sing5-kong1')

    @patch('臺灣言語服務.Kaldi語料辨識.Kaldi語料辨識.辨識成功')
    @patch('臺灣言語工具.系統整合.程式腳本.程式腳本._讀檔案')
    @patch('臺灣言語工具.系統整合.程式腳本.程式腳本._換目錄')
    @patch('臺灣言語工具.系統整合.程式腳本.程式腳本._走指令')
    @override_settings(KALDI_KUE3_TING5='kaldi過程資料')
    def test_有指定過程暫存資料夾(self, _走指令mock, _換目錄mock, 讀檔案mock, 辨識成功mock):
        Kaldi辨識 = Kaldi語料辨識.匯入音檔(
            '台語', '啥人唸的',
            self.音檔, 'tsiang5 tsiang5',
        )
        讀檔案mock.return_value = ['句001 sing5-kong1']
        Kaldi辨識.辨識()
        辨識成功mock.assert_called_once_with('sing5-kong1')
        rmtree(join(settings.BASE_DIR, settings.KALDI_KUE3_TING5))

    @patch('臺灣言語服務.Kaldi語料辨識.Kaldi語料辨識.辨識失敗')
    @patch('臺灣言語工具.系統整合.程式腳本.程式腳本._換目錄')
    @patch('臺灣言語工具.系統整合.程式腳本.程式腳本._走指令')
    def test_錯誤就是辨識失敗(self, 走指令mock, _換目錄mock, 辨識失敗mock):
        Kaldi辨識 = Kaldi語料辨識.匯入音檔(
            '台語', '啥人唸的',
            self.音檔, 'tsiang5 tsiang5',
        )
        走指令mock.side_effect = OSError()
        with self.assertRaises(OSError):
            Kaldi辨識.辨識()
        辨識失敗mock.assert_called_once_with()
