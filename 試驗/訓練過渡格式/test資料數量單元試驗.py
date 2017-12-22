from django.test.testcases import TestCase
from 臺灣言語服務.models import 訓練過渡格式


class 文本分詞資料(TestCase):

    def test_一開始無資料(self):
        self.assertEqual(訓練過渡格式.objects.count(), 0)

    def test_加一筆(self):
        公家內容 = {'來源': 'Dr. Pigu', '種類':  '字詞', '年代':  '2017', }
        訓練過渡格式.objects.create(文本='媠｜sui2', **公家內容)
        self.assertEqual(訓練過渡格式.objects.count(), 1)
