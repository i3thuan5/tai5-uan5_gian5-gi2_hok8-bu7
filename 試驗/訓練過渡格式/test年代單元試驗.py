from django.core.exceptions import ValidationError
from django.test.testcases import TestCase
from 臺灣言語服務.models import 訓練過渡格式


class 年代試驗(TestCase):
    公家內容 = {'來源':  'Pigu', '種類':  '字詞', '文本': 'sui2'}

    def test_1945(self):
        訓練過渡格式(年代='1945', **self.公家內容).full_clean()

    def test_19xx(self):
        訓練過渡格式(年代='19xx', 來源='Pigu', 種類='字詞', 文本='sui2').full_clean()

    def test_無年代愛錯誤(self):
        with self.assertRaises(ValidationError):
            訓練過渡格式(**self.公家內容).full_clean()
