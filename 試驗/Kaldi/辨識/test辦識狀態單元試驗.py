from django.test.testcases import TestCase


from 臺灣言語工具.語音辨識.聲音檔 import 聲音檔
from 臺灣言語服務.Kaldi語料辨識 import Kaldi語料辨識


class 辦識狀態單元試驗(TestCase):

    def test_猶未辦識狀態(self):
        影音 = Kaldi語料辨識.匯入音檔(
            '台語', '啥人唸的',
            聲音檔.對參數轉(2, 16000, 1, b'sui2khiau2'), 'tsiang5 tsiang5',
        )
        self.assertFalse(影音.Kaldi辨識結果.辨識好猶未)

    def test_辦識成功(self):
        影音 = Kaldi語料辨識.匯入音檔(
            '台語', '啥人唸的',
            聲音檔.對參數轉(2, 16000, 1, b'sui2khiau2'), 'tsiang5 tsiang5',
        )
        影音.Kaldi辨識結果.辨識成功('sui2')
        self.assertTrue(影音.Kaldi辨識結果.辨識好猶未)
        self.assertFalse(影音.Kaldi辨識結果.辨識出問題)
        self.assertEqual(影音.Kaldi辨識結果.分詞, 'sui2')

    def test_辦識失敗(self):
        影音 = Kaldi語料辨識.匯入音檔(
            '台語', '啥人唸的',
            聲音檔.對參數轉(2, 16000, 1, b'sui2khiau2'), 'tsiang5 tsiang5',
        )
        影音.Kaldi辨識結果.辨識失敗()
        self.assertTrue(影音.Kaldi辨識結果.辨識好猶未)
        self.assertTrue(影音.Kaldi辨識結果.辨識出問題)
