from django.core.exceptions import ValidationError
from django.test.testcases import TestCase
from 臺灣言語服務.models import 訓練過渡格式


class 文本分詞資料(TestCase):
    公開內容 = {'來源': 'Dr. Pigu', '種類':  '字詞', '年代':  '2017', }

    def test_正常分詞(self):
        訓練過渡格式(文本='媠｜sui2', **self.公開內容).full_clean()

    def test_錯誤分詞(self):
        with self.assertRaises(ValidationError):
            訓練過渡格式(文本='媠｜sui2-sui2', **self.公開內容).full_clean()

    def test_無文本無要緊(self):
        訓練過渡格式(**self.公開內容).full_clean()

    def test_無文本就是愛存None才有法度filter(self):
        一筆 = 訓練過渡格式.objects.create(**self.公開內容)
        self.assertIsNone(一筆.文本)
