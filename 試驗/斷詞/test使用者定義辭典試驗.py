import json

from django.test.testcases import TestCase


class 使用者定義辭典試驗(TestCase):
    def test_短詞翻譯(self):
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
        self.assertIn('分詞', 回應物件)
        self.assertIn('多元書寫', 回應物件)
