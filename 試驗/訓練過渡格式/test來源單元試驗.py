from django.core.exceptions import ValidationError
from django.test import TestCase
from 臺灣言語服務.models import 訓練過渡格式


class 加來源試驗(TestCase):
    公開內容 = {'種類':  '字詞', '年代':  '2017', '文本': 'sui2'}

    def test_有來源(self):
        訓練過渡格式(來源='Dr. Pigu', **self.公開內容).full_clean()

    def test_一定愛有來源(self):
        with self.assertRaises(ValidationError):
            訓練過渡格式(**self.公開內容).full_clean()
