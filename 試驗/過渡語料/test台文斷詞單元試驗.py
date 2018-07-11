# -*- coding: utf-8 -*-
from django.test import TestCase


from 臺灣言語服務.過渡語料 import 過渡語料處理


class test台文斷詞單元試驗(TestCase):
    公家內容 = {'種類':  '語句', '年代':  '2018', }

    def test_回傳處理數量(self):
        過渡語料處理.objects.create(
            來源='su-tian', 文本='我｜gua2 愛｜ai3 豬-仔｜ti1-a2', **self.公家內容
        )
        過渡語料處理.objects.create(
            來源='ti-a', 文本='豬仔愛我', **self.公家內容
        )
        斷詞數量 = 過渡語料處理.台文語料斷詞(['su-tian'], ['ti-a'])
        self.assertEqual(斷詞數量, 1)

    def test_有斷著詞(self):
        過渡語料處理.objects.create(
            來源='su-tian', 文本='我｜gua2 愛｜ai3 豬-仔｜ti1-a2', **self.公家內容
        )
        過渡語料處理.objects.create(
            來源='ti-a', 文本='豬仔愛我', **self.公家內容
        )
        過渡語料處理.台文語料斷詞(['su-tian'], ['ti-a'])
        過渡語料處理.objects.get(文本='豬-仔｜ti1-a2 愛｜ai3 我｜gua2')

    def test_來源無出現(self):
        過渡語料處理.objects.create(
            來源='ti-a', 文本='豬仔愛我', **self.公家內容
        )
        with self.assertRaises(ValueError):
            過渡語料處理.台文語料斷詞(['su-tian'], ['ti-a'])

    def test_目標無出現(self):
        過渡語料處理.objects.create(
            來源='su-tian', 文本='我｜gua2 愛｜ai3 豬-仔｜ti1-a2', **self.公家內容
        )
        with self.assertRaises(ValueError):
            過渡語料處理.台文語料斷詞(['su-tian'], ['ti-a'])