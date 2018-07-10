# -*- coding: utf-8 -*-
from unittest.mock import patch

from django.test import TestCase
from 臺灣言語服務.過渡語料 import 過渡語料處理


class test華語斷詞單元試驗(TestCase):

    公家內容 = {'來源': 'Dr. Pigu', '種類':  '語句', '年代':  '2018', }

    @patch('臺灣言語工具.斷詞.國教院斷詞用戶端.國教院斷詞用戶端.語句斷詞做陣列')
    def test_華語(self, 回應mock):
        回應mock.return_value = [
            ["我", "Nc"], ["愛", "Ncd"], ["小豬", "D"],
        ]
        過渡語料處理.objects.create(外文='我愛小豬', **self.公家內容)
        過渡語料處理.外文用國教院斷詞()
        self.assertEqual(過渡語料處理.objects.get().外文, '我 愛 小豬')
