import json
from time import sleep

from django.test.client import RequestFactory
from django.test.testcases import TestCase


from 臺灣言語服務.模型訓練 import 模型訓練
from 臺灣言語服務.資料模型路徑 import 翻譯語料資料夾
from 臺灣言語服務.資料模型路徑 import 翻譯模型資料夾
from 臺灣言語服務.模型載入 import 模型載入
from 臺灣言語服務.Moses載入 import Moses載入
from 臺灣言語服務.Moses服務 import Moses服務


class 詔安腔翻譯整合試驗(TestCase):

    @classmethod
    def setUpClass(cls):
        super(cls, cls).setUpClass()
        try:
            cls.母語模型 = Moses載入.摩西翻譯模型(翻譯模型資料夾, '詔安腔', 8501)
        except Exception as 錯誤:
            print(錯誤)
            模型訓練.訓練摩西翻譯模型(翻譯語料資料夾, 翻譯模型資料夾, '詔安腔')
            cls.母語模型 = Moses載入.摩西翻譯模型(翻譯模型資料夾, '詔安腔', 8501)
        sleep(30)

    @classmethod
    def tearDownClass(cls):
        cls.母語模型['摩西服務'].停()

    def setUp(self):
        self.assertIn('摩西用戶端', self.母語模型)
        self.assertIn('辭典', self.母語模型)
        self.assertIn('語言模型', self.母語模型)
        self.assertIn('拼音', self.母語模型)
        self.assertIn('字綜合標音', self.母語模型)
        self.服務功能 = Moses服務(全部翻譯母語模型={'詔安腔': self.母語模型})

    def test_短詞翻譯(self):
        連線要求 = RequestFactory().get('/正規化翻譯')
        連線要求.GET = {
            '查詢腔口': '詔安腔',
            '查詢語句': '你好'
        }
        連線回應 = self.服務功能.正規化翻譯(連線要求)
        self.assertEqual(連線回應.status_code, 200)
        回應物件 = json.loads(連線回應.content.decode("utf-8"))
        self.assertIn('翻譯正規化結果', 回應物件)
        self.assertIn('綜合標音', 回應物件)

    def test_兩句翻譯(self):
        連線要求 = RequestFactory().get('/正規化翻譯')
        連線要求.GET = {
            '查詢腔口': '詔安腔',
            '查詢語句': '你好嗎？我很好！'
        }
        連線回應 = self.服務功能.正規化翻譯(連線要求)
        self.assertEqual(連線回應.status_code, 200)
        回應物件 = json.loads(連線回應.content.decode("utf-8"))
        self.assertIn('翻譯正規化結果', 回應物件)
        self.assertIn('綜合標音', 回應物件)
