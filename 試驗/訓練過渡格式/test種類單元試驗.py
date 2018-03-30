from django.core.exceptions import ValidationError
from django.test.testcases import TestCase
from 臺灣言語服務.models import 訓練過渡格式


class 種類試驗(TestCase):

    公家內容 = {'來源':  'Pigu', '年代':  '2017', '文本': 'sui2'}

    def test_字詞(self):
        訓練過渡格式(種類='字詞', **self.公家內容).full_clean()

    def test_語句(self):
        訓練過渡格式(種類='語句', **self.公家內容).full_clean()

    def test_別的無合法(self):
        with self.assertRaises(ValidationError):
            訓練過渡格式(**self.公家內容).full_clean()

    def test_無種類(self):
        with self.assertRaises(ValidationError):
            訓練過渡格式(種類='四字仔', **self.公家內容).full_clean()
