from django.test.testcases import TestCase


from 臺灣言語工具.語音辨識.聲音檔 import 聲音檔
from 臺灣言語服務.Kaldi語料對齊 import Kaldi語料對齊


class 對齊狀態單元試驗(TestCase):

    def test_猶未對齊狀態(self):
        語料對齊 = Kaldi語料對齊.匯入音檔(
            '台語', '啥人唸的',
            聲音檔.對參數轉(2, 16000, 1, b'sui2khiau2'), 'tsiang5 tsiang5',
        )
        self.assertFalse(語料對齊.對齊好猶未)

    def test_對齊前就有聽拍(self):
        語料對齊 = Kaldi語料對齊.匯入音檔(
            '台語', '媠媠',
            聲音檔.對參數轉(2, 16000, 1, b'sui2khiau2'), 'tsiang5 tsiang5\nkhiau2',
        )
        self.assertEqual(
            語料對齊.欲切開的聽拍,
            'tsiang5 tsiang5\nkhiau2'
        )

    def test_對齊成功(self):
        語料對齊 = Kaldi語料對齊.匯入音檔(
            '台語', '媠媠',
            聲音檔.對參數轉(2, 16000, 1, b'sui2khiau2'), 'tsiang5 tsiang5\nkhiau2',
        )
        語料對齊.對齊成功([
            {'開始': 0.30, '長度': 0.23, '分詞': 'tsiang5', },
            {'開始': 0.60, '長度': 0.23, '分詞': 'tsiang5', },
            {'開始': 0.83, '長度': 0.23, '分詞': 'khiau2', },
        ])
        self.assertTrue(語料對齊.對齊好猶未)
        self.assertFalse(語料對齊.對齊出問題)
        self.assertEqual(
            語料對齊.切好的聽拍,
            [
                {
                    '語者': '媠媠',
                    '內容': 'tsiang5 tsiang5',
                    '開始時間': 0.3,
                    '結束時間': 0.83,
                },
                {
                    '語者': '媠媠',
                    '內容': 'khiau2',
                    '開始時間': 0.83,
                    '結束時間': 1.06,
                },
            ]
        )

    def test_有換逝(self):
        語料對齊 = Kaldi語料對齊.匯入音檔(
            '台語', '媠媠',
            聲音檔.對參數轉(2, 16000, 1, b'sui2khiau2'),
            '\ntsiang5 tsiang5\n\nkhiau2\n',
        )
        語料對齊.對齊成功([
            {'開始': 0.30, '長度': 0.23, '分詞': 'tsiang5', },
            {'開始': 0.60, '長度': 0.23, '分詞': 'tsiang5', },
            {'開始': 0.83, '長度': 0.23, '分詞': 'khiau2', },
        ])
        self.assertTrue(語料對齊.對齊好猶未)
        self.assertFalse(語料對齊.對齊出問題)
        self.assertEqual(
            語料對齊.切好的聽拍,
            [
                {
                    '語者': '媠媠',
                    '內容': 'tsiang5 tsiang5',
                    '開始時間': 0.3,
                    '結束時間': 0.83,
                },
                {
                    '語者': '媠媠',
                    '內容': 'khiau2',
                    '開始時間': 0.83,
                    '結束時間': 1.06,
                },
            ]
        )

    def test_對齊失敗(self):
        語料對齊 = Kaldi語料對齊.匯入音檔(
            '台語', '啥人唸的',
            聲音檔.對參數轉(2, 16000, 1, b'sui2khiau2'), 'tsiang5 tsiang5',
        )
        語料對齊.對齊失敗()
        self.assertTrue(語料對齊.對齊好猶未)
        self.assertTrue(語料對齊.對齊出問題)
