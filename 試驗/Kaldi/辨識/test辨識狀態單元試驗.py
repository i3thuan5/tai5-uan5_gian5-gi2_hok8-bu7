from django.test.testcases import TestCase


from 臺灣言語工具.語音辨識.聲音檔 import 聲音檔
from 臺灣言語服務.Kaldi語料辨識 import Kaldi語料辨識


class 辨識狀態單元試驗(TestCase):

    def test_猶未辨識狀態(self):
        Kaldi辨識 = Kaldi語料辨識.匯入音檔(
            '台語', '啥人唸的',
            聲音檔.對參數轉(2, 16000, 1, b'sui2khiau2'), 'tsiang5 tsiang5',
        )
        self.assertFalse(Kaldi辨識.辨識好猶未)

    def test_辨識成功(self):
        Kaldi辨識 = Kaldi語料辨識.匯入音檔(
            '台語', '啥人唸的',
            聲音檔.對參數轉(2, 16000, 1, b'sui2khiau2'), 'tsiang5 tsiang5',
        )
        Kaldi辨識.辨識成功('sui2')
        self.assertTrue(Kaldi辨識.辨識好猶未)
        self.assertFalse(Kaldi辨識.辨識出問題)
        self.assertEqual(Kaldi辨識.分詞, 'sui2')

    def test_辨識失敗(self):
        Kaldi辨識 = Kaldi語料辨識.匯入音檔(
            '台語', '啥人唸的',
            聲音檔.對參數轉(2, 16000, 1, b'sui2khiau2'), 'tsiang5 tsiang5',
        )
        Kaldi辨識.辨識失敗()
        self.assertTrue(Kaldi辨識.辨識好猶未)
        self.assertTrue(Kaldi辨識.辨識出問題)
