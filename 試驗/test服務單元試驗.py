from django.test.testcases import TestCase


from 臺灣言語服務.服務 import 服務


class 服務單元試驗(TestCase):

    def test_會當無傳模型(self):
        服務()

    def test_會當無半個模型(self):
        服務(全部翻譯母語模型={}, 全部合成母語模型={})
