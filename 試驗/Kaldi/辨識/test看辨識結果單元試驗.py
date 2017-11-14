import io

from django.test.testcases import TestCase


from 臺灣言語工具.語音辨識.聲音檔 import 聲音檔
from 臺灣言語服務.Kaldi語料辨識 import Kaldi語料辨識
from 臺灣言語資料庫.資料模型 import 來源表
from 臺灣言語資料庫.資料模型 import 版權表
from 臺灣言語資料庫.資料模型 import 影音表


class Kaldi匯入音檔單元試驗(TestCase):

    def test_無佇辨識的莫顯示(self):
        公家內容 = {
            '收錄者': 來源表.objects.get_or_create(名='系統管理員')[0].編號(),
            '來源': 來源表.objects.get_or_create(名='系統管理員')[0].編號(),
            '版權': 版權表.objects.get_or_create(版權='會使公開')[0].pk,
            '種類': '語句',
            '語言腔口': '語言',
            '著作所在地': '臺灣',
            '著作年': '2017',
        }
        音檔 = io.BytesIO(b'sui2khiau2')
        影音內容 = {'影音資料': 音檔}
        影音內容.update(公家內容)
        影音表.加資料(影音內容)
#         Kaldi語料辨識.匯入音檔(
#             '閩南語', '啥人唸的',
#             聲音檔.對參數轉(2, 16000, 1, b'sui2khiau2'), 'tsiang5 tsiang5',
#         )

        回應資料 = self.client.get('/辦識結果').json()
        self.assertEqual(len(回應資料['辨識結果']), 0)

    def test_辨識中(self):
        Kaldi語料辨識.匯入音檔(
            '閩南語', '啥人唸的',
            聲音檔.對參數轉(2, 16000, 1, b'sui2khiau2'), 'tsiang5 tsiang5',
        )

        回應資料 = self.client.get('/辦識結果').json()
        self.assertEqual(len(回應資料['辨識結果']), 1)
        self.assertIn('辨識中', 回應資料['辨識結果'][0]['狀態'])

    def test_辨識成功(self):
        Kaldi語料辨識.匯入音檔(
            '閩南語', '啥人唸的',
            聲音檔.對參數轉(2, 16000, 1, b'sui2khiau2'), 'tsiang5 tsiang5',
        ).Kaldi辨識結果.辨識成功('sui2')

        回應資料 = self.client.get('/辦識結果').json()
        self.assertEqual(回應資料['辨識結果'][0]['狀態'], '成功')
        self.assertEqual(回應資料['辨識結果'][0]['分詞'], 'sui2')

    def test_辨識失敗(self):
        Kaldi語料辨識.匯入音檔(
            '閩南語', '啥人唸的',
            聲音檔.對參數轉(2, 16000, 1, b'sui2khiau2'), 'tsiang5 tsiang5',
        ).Kaldi辨識結果.辨識失敗()

        回應資料 = self.client.get('/辦識結果').json()
        self.assertEqual(回應資料['辨識結果'][0]['狀態'], '辨識出問題')
