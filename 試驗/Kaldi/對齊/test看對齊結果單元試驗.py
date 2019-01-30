
from tempfile import NamedTemporaryFile

from django.test.testcases import TestCase
from django.urls.base import resolve


from 臺灣言語服務.Kaldi語料對齊 import Kaldi語料對齊
from 臺灣言語工具.語音辨識.聲音檔 import 聲音檔
from 臺灣言語服務.Kaldi介面 import 看對齊結果


class 看對齊結果單元試驗(TestCase):

    def test_有對應函式(self):
        對應 = resolve('/對齊結果')
        self.assertEqual(對應.func, 看對齊結果)

    def test_無就免顯示(self):
        回應資料 = self.client.get('/對齊結果').json()
        self.assertEqual(len(回應資料['對齊結果']), 0)

    def test_對齊中(self):
        Kaldi語料對齊.匯入音檔(
            '台語', '啥人唸的',
            聲音檔.對參數轉(2, 16000, 1, b'sui2khiau2'), 'tsiang5 tsiang5',
        )

        回應資料 = self.client.get('/對齊結果').json()
        self.assertEqual(len(回應資料['對齊結果']), 1)
        self.assertIn('對齊中', 回應資料['對齊結果'][0]['狀態'])

    def test_對齊好產生壓縮檔中(self):
        Kaldi語料對齊.匯入音檔(
            '台語', '啥人唸的',
            聲音檔.對參數轉(2, 16000, 1, b'sui2khiau2'), 'tsiang5 tsiang5',
        ).對齊成功([
            {'開始': 0.30, '長度': 0.23, '分詞': 'tsiang5', },
            {'開始': 0.60, '長度': 0.23, '分詞': 'tsiang5', }
        ])

        回應資料 = self.client.get('/對齊結果').json()
        self.assertIn('佇產生壓縮檔', 回應資料['對齊結果'][0]['狀態'])

    def test_對齊失敗(self):
        Kaldi語料對齊.匯入音檔(
            '台語', '啥人唸的',
            聲音檔.對參數轉(2, 16000, 1, b'sui2khiau2'), 'tsiang5 tsiang5',
        ).對齊失敗()

        回應資料 = self.client.get('/對齊結果').json()
        self.assertEqual(回應資料['對齊結果'][0]['狀態'], '對齊出問題')

    def test_壓縮好矣(self):
        語料對齊 = Kaldi語料對齊.匯入音檔(
            '台語', '啥人唸的',
            聲音檔.對參數轉(2, 16, 1, b'sui2khiau2' * 33), 'tsiang5 tsiang5',
        )
        語料對齊.對齊成功([
            {'開始': 0.30, '長度': 0.23, '分詞': 'tsiang5', },
            {'開始': 0.60, '長度': 0.23, '分詞': 'tsiang5', }
        ])
        語料對齊.做出切音結果()

        回應資料 = self.client.get('/對齊結果').json()
        self.assertIn('成功', 回應資料['對齊結果'][0]['狀態'])
        self.assertIn('壓縮檔網址', 回應資料['對齊結果'][0])

    def test_有語言(self):
        語料對齊 = Kaldi語料對齊.匯入音檔(
            '台語', '啥人唸的',
            聲音檔.對參數轉(2, 16000, 1, b'sui2khiau2'), 'tsiang5 tsiang5',
        )
        語料對齊.對齊成功([
            {'開始': 0.30, '長度': 0.23, '分詞': 'tsiang5', },
            {'開始': 0.60, '長度': 0.23, '分詞': 'tsiang5', }
        ])
        with NamedTemporaryFile() as 凊彩檔案:
            語料對齊.存壓縮檔(凊彩檔案.name)

        回應資料 = self.client.get('/對齊結果').json()
        self.assertEqual(回應資料['對齊結果'][0]['語言'], '台語')

    def test_有原始檔案(self):
        Kaldi語料對齊.匯入音檔(
            '台語', '啥人唸的',
            聲音檔.對參數轉(2, 16000, 1, b'sui2khiau2'), 'tsiang5 tsiang5',
        )

        回應資料 = self.client.get('/對齊結果').json()
        self.assertEqual(len(回應資料['對齊結果']), 1)
        self.assertIn('原始wav檔網址', 回應資料['對齊結果'][0])

    def test_有原始文本(self):
        Kaldi語料對齊.匯入音檔(
            '台語', '啥人唸的',
            聲音檔.對參數轉(2, 16000, 1, b'sui2khiau2'), '\ntsiang5\ntsiang5',
        )

        回應資料 = self.client.get('/對齊結果').json()
        self.assertEqual(len(回應資料['對齊結果']), 1)
        self.assertIn(回應資料['對齊結果'][0]['分詞文本'], '\ntsiang5\ntsiang5')

    def test_有thang控制數量(self):
        for _ in range(5):
            Kaldi語料對齊.匯入音檔(
                '台語', '啥人唸的',
                聲音檔.對參數轉(2, 16000, 1, b'sui2khiau2'), '\ntsiang5\ntsiang5',
            )

        回應資料 = self.client.get('/對齊結果', {'數量': '3'}).json()
        self.assertEqual(len(回應資料['對齊結果']), 3)
