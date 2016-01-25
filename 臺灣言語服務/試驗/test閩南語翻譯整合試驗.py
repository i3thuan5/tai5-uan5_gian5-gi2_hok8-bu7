import json

from django.test.client import RequestFactory
from django.test.testcases import TestCase
from 臺灣言語服務.模型訓練 import 模型訓練
from 臺灣言語服務.資料模型路徑 import 翻譯語料資料夾
from 臺灣言語服務.資料模型路徑 import 翻譯模型資料夾
from 臺灣言語服務.模型載入 import 模型載入
from 臺灣言語服務.服務 import 服務


class 閩南語翻譯整合試驗(TestCase):

    @classmethod
    def setUpClass(cls):
        super(cls, cls).setUpClass()
        訓練 = 模型訓練()
        訓練.訓練摩西翻譯模型(翻譯語料資料夾, 翻譯模型資料夾, '閩南語')
        載入 = 模型載入()
        母語模型 = 載入.摩西翻譯模型(翻譯模型資料夾, '閩南語', 8500)
        cls.assertIn('摩西用戶端', 母語模型)
        cls.assertIn('辭典', 母語模型)
        cls.assertIn('語言模型', 母語模型)
        cls.assertIn('拼音', 母語模型)
        cls.assertIn('字綜合標音', 母語模型)
        cls.服務功能 = 服務(全部翻譯母語模型={'閩南語': 母語模型})

    def test_短詞翻譯(self):
        連線要求 = RequestFactory().get('/正規化翻譯')
        連線要求.GET = {
            '查詢腔口': '閩南語',
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
            '查詢腔口': '閩南語',
            '查詢語句': '你好嗎？我很好！'
        }
        連線回應 = self.服務功能.正規化翻譯(連線要求)
        self.assertEqual(連線回應.status_code, 200)
        回應物件 = json.loads(連線回應.content.decode("utf-8"))
        self.assertIn('翻譯正規化結果', 回應物件)
        self.assertIn('綜合標音', 回應物件)

    def test_無腔口預設閩南語(self):
        連線要求 = RequestFactory().get('/正規化翻譯')
        連線要求.GET = {
            '查詢腔口': '閩南語',
            '查詢語句': '你好嗎？我很好！'
        }
        連線回應 = self.服務功能.正規化翻譯(連線要求)
        self.assertEqual(連線回應.status_code, 200)
        閩南語回應物件 = json.loads(連線回應.content.decode("utf-8"))

        連線要求 = RequestFactory().get('/正規化翻譯')
        連線要求.GET = {
            '查詢腔口': '母語',
            '查詢語句': '你好嗎？我很好！'
        }
        連線回應 = self.服務功能.正規化翻譯(連線要求)
        self.assertEqual(連線回應.status_code, 200)
        回應物件 = json.loads(連線回應.content.decode("utf-8"))
        self.assertEqual(回應物件, 閩南語回應物件)

    def test_無參數預設閩南語(self):
        連線要求 = RequestFactory().get('/正規化翻譯')
        連線要求.GET = {
            '查詢腔口': '閩南語',
            '查詢語句': '你好嗎？我很好！'
        }
        連線回應 = self.服務功能.正規化翻譯(連線要求)
        self.assertEqual(連線回應.status_code, 200)
        閩南語回應物件 = json.loads(連線回應.content.decode("utf-8"))

        連線要求 = RequestFactory().get('/正規化翻譯')
        連線要求.GET = {}
        連線回應 = self.服務功能.正規化翻譯(連線要求)
        self.assertEqual(連線回應.status_code, 200)
        回應物件 = json.loads(連線回應.content.decode("utf-8"))
        self.assertEqual(回應物件, 閩南語回應物件)
