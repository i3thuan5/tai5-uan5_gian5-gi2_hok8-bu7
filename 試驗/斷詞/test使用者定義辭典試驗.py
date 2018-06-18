import json
from unittest.mock import patch

from django.test.testcases import TestCase
from django.urls.base import resolve


from 臺灣言語服務.斷詞介面 import 斷詞介面
from 臺灣言語服務.Moses服務 import Moses服務
from 臺灣言語工具.辭典.現掀辭典 import 現掀辭典
from 臺灣言語工具.語言模型.實際語言模型 import 實際語言模型
from 臺灣言語工具.音標系統.台語 import 新白話字


class 使用者定義辭典試驗(TestCase):
    def test_有對應函式(self):
        對應 = resolve('/標漢羅')
        self.assertEqual(對應.func, 斷詞介面.標漢羅)

    @patch('臺灣言語服務.斷詞介面.斷詞介面.服務')
    def test_提供辭典(self, 服務Mock):
        服務Mock.return_value = Moses服務({'台語': {
            '解析拼音': 新白話字,
            '辭典': 現掀辭典(4),
            '語言模型': 實際語言模型(2),
        }})

        連線回應 = self.client.get(
            '/標漢羅', {
                '查詢腔口': '台語',
                '查詢語句': '你好',
                '使用者辭典': json.dumps(
                    [['你', 'li2'], ['你好', 'li2-ho2']]
                ),
            }
        )
        self.assertEqual(連線回應.status_code, 200)
        回應物件 = 連線回應.json()
        self.assertIn(回應物件[0]['分詞'].split(), 1)
        self.assertIn('多元書寫', 回應物件[0])

    @patch('臺灣言語服務.斷詞介面.斷詞介面.服務')
    def test_無提供使用者辭典(self,服務Mock):
        服務Mock.return_value = Moses服務({'台語': {
            '解析拼音': 新白話字,
            '辭典': 現掀辭典(4),
            '語言模型': 實際語言模型(2),
        }})

        連線回應 = self.client.get(
            '/標漢羅', {
                '查詢腔口': '台語',
                '查詢語句': '你好',
            }
        )
        self.assertEqual(連線回應.status_code, 200)
        回應物件 = 連線回應.json()
        self.assertIn(回應物件[0]['分詞'].split(), 2)

    @patch('臺灣言語服務.斷詞介面.斷詞介面.服務')
    def test_對齊失敗當作無傳(self,服務Mock):
        服務Mock.return_value = Moses服務({'台語': {
            '解析拼音': 新白話字,
            '辭典': 現掀辭典(4),
            '語言模型': 實際語言模型(2),
        }})

        連線回應 = self.client.get(
            '/標漢羅', {
                '查詢腔口': '台語',
                '查詢語句': '你好',
                '使用者辭典': json.dumps(
                    [ ['你好', 'li2-ho2-bo5']]
                ),
            }
        )
        self.assertEqual(連線回應.status_code, 200)
        回應物件 = 連線回應.json()
        self.assertIn(回應物件[0]['分詞'].split(), 2)
