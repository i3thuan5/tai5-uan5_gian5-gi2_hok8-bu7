from django.test.testcases import TestCase
from 臺灣言語資料庫.資料模型 import 版權表
from 臺灣言語資料庫.欄位資訊 import 會使公開
from 臺灣言語資料庫.資料模型 import 來源表
from 臺灣言語資料庫.資料模型 import 文本表


class 文本表格式化單元試驗(TestCase):

    def setUp(self):
        版權表.objects.create(版權=會使公開)
        Pigu = 來源表.objects.create(名='Dr. Pigu')
        self.資料內容 = {
            '收錄者': Pigu.編號(),
            '來源': Pigu.編號(),
            '版權': '會使公開',
            '種類': '語句',
            '語言腔口': '閩南語',
            '著作所在地': '花蓮',
            '著作年': '2015',
        }

    def test_無音標文本(self):
        文本內容 = {'文本資料': '食飽未？'}
        文本內容.update(self.資料內容)
        文本 = 文本表.加資料(文本內容)
        self.assertEqual(
            文本.文本佮音標格式化資料(),
            '食飽未？'
        )

    def test_對齊成功文本(self):
        文本內容 = {
            '文本資料': '食飽未？',
            '屬性': {'音標': 'tsiah8-pa2 0bue7 ?'}
        }
        文本內容.update(self.資料內容)
        文本 = 文本表.加資料(文本內容)
        self.assertEqual(
            文本.文本佮音標格式化資料(),
            '食-飽｜tsiah8-pa2 未｜0bue7 ？｜?'
        )

    def test_對齊失敗文本(self):
        文本內容 = {
            '文本資料': '食飽未？',
            '屬性': {'音標': 'tsiah8-pa2'}
        }
        文本內容.update(self.資料內容)
        文本 = 文本表.加資料(文本內容)
        self.assertEqual(
            文本.文本佮音標格式化資料(),
            '食飽未？'
        )

    def test_兩個文本嘛愛有法度對齊(self):
        文本內容 = {
            '文本資料': '食飯',
            '屬性': {'音標': 'tsiah8-png7'}
        }
        文本內容.update(self.資料內容)
        文本表.加資料(文本內容)
        文本內容 = {
            '文本資料': '食飽未？',
            '屬性': {'音標': 'tsiah8-pa2 0bue7 ?'}
        }
        文本內容.update(self.資料內容)
        文本 = 文本表.加資料(文本內容)
        self.assertEqual(
            文本.文本佮音標格式化資料(),
            '食-飽｜tsiah8-pa2 未｜0bue7 ？｜?'
        )
