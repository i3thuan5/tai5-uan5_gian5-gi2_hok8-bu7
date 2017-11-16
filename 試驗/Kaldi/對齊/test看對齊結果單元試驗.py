
import io
from tempfile import NamedTemporaryFile

from django.core.urlresolvers import resolve
from django.test.testcases import TestCase


from 臺灣言語服務.Kaldi語料對齊 import Kaldi語料對齊
from 臺灣言語資料庫.資料模型 import 來源表
from 臺灣言語資料庫.資料模型 import 版權表
from 臺灣言語資料庫.資料模型 import 影音表
from 臺灣言語工具.語音辨識.聲音檔 import 聲音檔
from 臺灣言語服務.Kaldi介面 import 看對齊結果


class 看對齊結果單元試驗(TestCase):

    def test_有對應函式(self):
        對應 = resolve('/對齊結果')
        self.assertEqual(對應.func, 看對齊結果)

    def test_無佇對齊的莫顯示(self):
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
        回應資料 = self.client.get('/對齊結果').json()
        self.assertEqual(len(回應資料['對齊結果']), 0)

    def test_對齊中(self):
        Kaldi語料對齊.匯入音檔(
            '閩南語', '啥人唸的',
            聲音檔.對參數轉(2, 16000, 1, b'sui2khiau2'), 'tsiang5 tsiang5',
        )

        回應資料 = self.client.get('/對齊結果').json()
        self.assertEqual(len(回應資料['對齊結果']), 1)
        self.assertIn('對齊中', 回應資料['對齊結果'][0]['狀態'])

    def test_對齊好產生壓縮檔中(self):
        Kaldi語料對齊.匯入音檔(
            '閩南語', '啥人唸的',
            聲音檔.對參數轉(2, 16000, 1, b'sui2khiau2'), 'tsiang5 tsiang5',
        ).對齊成功([
            {'開始': 0.30, '長度': 0.23, '分詞': 'tsiang5', },
            {'開始': 0.60, '長度': 0.23, '分詞': 'tsiang5', }
        ])

        回應資料 = self.client.get('/對齊結果').json()
        self.assertIn('佇產生壓縮檔', 回應資料['對齊結果'][0]['狀態'])

    def test_對齊失敗(self):
        Kaldi語料對齊.匯入音檔(
            '閩南語', '啥人唸的',
            聲音檔.對參數轉(2, 16000, 1, b'sui2khiau2'), 'tsiang5 tsiang5',
        ).對齊失敗()

        回應資料 = self.client.get('/對齊結果').json()
        self.assertEqual(回應資料['對齊結果'][0]['狀態'], '對齊出問題')

    def test_壓縮好矣(self):
        語料對齊 = Kaldi語料對齊.匯入音檔(
            '閩南語', '啥人唸的',
            聲音檔.對參數轉(2, 16000, 1, b'sui2khiau2'), 'tsiang5 tsiang5',
        )
        語料對齊.對齊成功([
            {'開始': 0.30, '長度': 0.23, '分詞': 'tsiang5', },
            {'開始': 0.60, '長度': 0.23, '分詞': 'tsiang5', }
        ])
        with NamedTemporaryFile() as 凊彩檔案:
            語料對齊.存壓縮檔(凊彩檔案.name)

        回應資料 = self.client.get('/對齊結果').json()
        self.assertIn('成功', 回應資料['對齊結果'][0]['狀態'])
        self.assertIn('壓縮檔網址', 回應資料['對齊結果'][0])

    def test_有原始檔案(self):
        Kaldi語料對齊.匯入音檔(
            '閩南語', '啥人唸的',
            聲音檔.對參數轉(2, 16000, 1, b'sui2khiau2'), 'tsiang5 tsiang5',
        )

        回應資料 = self.client.get('/對齊結果').json()
        self.assertEqual(len(回應資料['對齊結果']), 1)
        self.assertIn('原始wav檔網址', 回應資料['對齊結果'][0])

    def test_有原始文本(self):
        Kaldi語料對齊.匯入音檔(
            '閩南語', '啥人唸的',
            聲音檔.對參數轉(2, 16000, 1, b'sui2khiau2'), '\ntsiang5\ntsiang5',
        )

        回應資料 = self.client.get('/對齊結果').json()
        self.assertEqual(len(回應資料['對齊結果']), 1)
        self.assertIn(回應資料['對齊結果'][0]['分詞文本'], '\ntsiang5\ntsiang5')
