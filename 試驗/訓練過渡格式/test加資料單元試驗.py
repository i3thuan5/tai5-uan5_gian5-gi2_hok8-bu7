import io

from django.test.testcases import TestCase
from 臺灣言語服務.models import 訓練過渡格式


class 加資料試驗(TestCase):
    公開內容 = {'來源': 'Dr. Pigu', '種類':  '字詞', '年代':  '2017', }

    def test_錯誤的袂加入去(self):
        with io.StringIO() as 輸出:
            訓練過渡格式.加一堆資料([
                訓練過渡格式(文本='媠｜sui2', **self.公開內容),
                訓練過渡格式(文本='媠｜sui1', **self.公開內容),
                訓練過渡格式(文本='媠｜sui2-sui2', **self.公開內容),
            ], 錯誤輸出=輸出)
        self.assertEqual(訓練過渡格式.objects.count(), 2)
