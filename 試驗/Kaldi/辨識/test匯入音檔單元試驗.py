from django.test.testcases import TestCase


from 臺灣言語工具.語音辨識.聲音檔 import 聲音檔
from 臺灣言語服務.Kaldi語料辨識 import Kaldi語料辨識


class 匯入音檔單元試驗(TestCase):

    def test_內容(self):
        影音 = Kaldi語料辨識.匯入音檔(
            '台語', '啥人唸的',
            聲音檔.對參數轉(2, 16000, 1, b'sui2khiau2'), 'tsiang5 tsiang5',
        )
        聽拍資料 = 影音.影音聽拍.get().聽拍.聽拍內容()
        self.assertEqual(len(聽拍資料), 1)
        self.assertEqual(聽拍資料[0]['內容'], 'tsiang5 tsiang5')

    def test_人名(self):
        影音 = Kaldi語料辨識.匯入音檔(
            '台語', '啥人唸的',
            聲音檔.對參數轉(2, 16000, 1, b'sui2khiau2'), 'tsiang5 tsiang5',
        )
        聽拍 = 影音.影音聽拍.get().聽拍
        聽拍資料 = 聽拍.聽拍內容()
        self.assertEqual(影音.來源.名, '啥人唸的')
        self.assertEqual(聽拍.來源.名, '啥人唸的')
        self.assertEqual(len(聽拍資料), 1)
        self.assertEqual(聽拍資料[0]['語者'], '啥人唸的')
