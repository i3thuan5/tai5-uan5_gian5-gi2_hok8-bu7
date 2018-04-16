
from django.test.testcases import TestCase


from 臺灣言語工具.語音辨識.聲音檔 import 聲音檔
from 臺灣言語服務.Kaldi語料辨識 import Kaldi語料辨識


class Kaldi匯入音檔單元試驗(TestCase):

    def test_無就免顯示(self):
        回應資料 = self.client.get('/辦識結果').json()
        self.assertEqual(len(回應資料['辨識結果']), 0)

    def test_辨識中(self):
        Kaldi語料辨識.匯入音檔(
            '台語', '啥人唸的',
            聲音檔.對參數轉(2, 16000, 1, b'sui2khiau2'), 'tsiang5 tsiang5',
        )

        回應資料 = self.client.get('/辦識結果').json()
        self.assertEqual(len(回應資料['辨識結果']), 1)
        self.assertIn('辨識中', 回應資料['辨識結果'][0]['狀態'])

    def test_辨識成功(self):
        Kaldi語料辨識.匯入音檔(
            '台語', '啥人唸的',
            聲音檔.對參數轉(2, 16000, 1, b'sui2khiau2'), 'tsiang5 tsiang5',
        ).Kaldi辨識結果.辨識成功('sui2')

        回應資料 = self.client.get('/辦識結果').json()
        self.assertEqual(回應資料['辨識結果'][0]['狀態'], '成功')
        self.assertEqual(回應資料['辨識結果'][0]['分詞'], 'sui2')

    def test_辨識有語言(self):
        Kaldi語料辨識.匯入音檔(
            '台語', '啥人唸的',
            聲音檔.對參數轉(2, 16000, 1, b'sui2khiau2'), 'tsiang5 tsiang5',
        ).Kaldi辨識結果.辨識成功('sui2')

        回應資料 = self.client.get('/辦識結果').json()
        self.assertEqual(回應資料['辨識結果'][0]['語言'], '台語')

    def test_辨識失敗(self):
        Kaldi語料辨識.匯入音檔(
            '台語', '啥人唸的',
            聲音檔.對參數轉(2, 16000, 1, b'sui2khiau2'), 'tsiang5 tsiang5',
        ).Kaldi辨識結果.辨識失敗()

        回應資料 = self.client.get('/辦識結果').json()
        self.assertEqual(回應資料['辨識結果'][0]['狀態'], '辨識出問題')
