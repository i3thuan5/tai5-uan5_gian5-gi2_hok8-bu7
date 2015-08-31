from django.test.testcases import TestCase
from 臺灣言語服務.模型訓練 import 模型訓練
from 臺灣言語服務.資料模型路徑 import 翻譯語料資料夾
from 臺灣言語服務.資料模型路徑 import 翻譯模型資料夾


class 模型訓練試驗(TestCase):

    def test_閩南語混合語料(self):
        訓練 = 模型訓練()
        訓練.訓練摩西翻譯模型(翻譯語料資料夾, 翻譯模型資料夾, '閩南語')

    def test_詔安腔句無斷詞(self):
        訓練 = 模型訓練()
        訓練.訓練摩西翻譯模型(翻譯語料資料夾, 翻譯模型資料夾, '詔安腔')
