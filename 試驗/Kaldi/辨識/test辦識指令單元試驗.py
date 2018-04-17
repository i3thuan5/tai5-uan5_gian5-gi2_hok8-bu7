from unittest.mock import patch

from django.test.testcases import TestCase


from 臺灣言語工具.語音辨識.聲音檔 import 聲音檔
from 臺灣言語服務.Kaldi語料辨識 import Kaldi語料辨識


class 辦識指令單元試驗(TestCase):
    @patch('臺灣言語服務.Kaldi語料辨識.Kaldi語料辨識.辨識成功')
    @patch('臺灣言語工具.系統整合.程式腳本.程式腳本._讀檔案')
    @patch('臺灣言語工具.系統整合.程式腳本.程式腳本._換目錄')
    @patch('臺灣言語工具.系統整合.程式腳本.程式腳本._走指令')
    def test_有辦識成功(self, _走指令mock, _換目錄mock, 讀檔案mock, 辨識成功mock):
        Kaldi辨識 = Kaldi語料辨識.匯入音檔(
            '台語', '啥人唸的',
            聲音檔.對參數轉(2, 16000, 1, b'sui2khiau2'), 'tsiang5 tsiang5',
        )
        讀檔案mock.return_value = ['句001 sing5-kong1']
        Kaldi辨識.辨識()
        辨識成功mock.assert_called_once_with('sing5-kong1')

    @patch('臺灣言語服務.Kaldi語料辨識.Kaldi語料辨識.辨識失敗')
    @patch('臺灣言語工具.系統整合.程式腳本.程式腳本._換目錄')
    @patch('臺灣言語工具.系統整合.程式腳本.程式腳本._走指令')
    def test_錯誤就是辦識失敗(self, 走指令mock, _換目錄mock, 辨識失敗mock):
        Kaldi辨識 = Kaldi語料辨識.匯入音檔(
            '台語', '啥人唸的',
            聲音檔.對參數轉(2, 16000, 1, b'sui2khiau2'), 'tsiang5 tsiang5',
        )
        走指令mock.side_effect = OSError()
        with self.assertRaises(OSError):
            Kaldi辨識.辨識()
        辨識失敗mock.assert_called_once_with()
