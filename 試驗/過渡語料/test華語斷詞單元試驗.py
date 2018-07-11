# -*- coding: utf-8 -*-
import io
from unittest.mock import patch

from django.core.management import call_command
from django.test import TestCase


from 臺灣言語服務.過渡語料 import 過渡語料處理


class test華語斷詞單元試驗(TestCase):
    公家內容 = {'來源': 'Dr. Pigu', '種類':  '語句', '年代':  '2018', }

    @patch('臺灣言語服務.過渡語料.過渡語料處理.外文用國教院斷詞')
    @patch('臺灣言語工具.斷詞.國教院斷詞用戶端.國教院斷詞用戶端.語句斷詞做陣列')
    def test_指令有叫著(self, 回應mock, 外文用國教院斷詞mock):
        外文用國教院斷詞mock.return_value = 333
        with io.StringIO() as err:
            call_command('外文用國教院斷詞', stderr=err)
            self.assertIn('斷詞 333 句', err.getvalue())

    @patch('sys.exit')
    @patch('臺灣言語服務.過渡語料.過渡語料處理.外文用國教院斷詞')
    def test_無語料愛錯誤(self,  外文用國教院斷詞mock, exitMock):
        外文用國教院斷詞mock.return_value = 0
        with io.StringIO() as err:
            call_command('外文用國教院斷詞', stderr=err)
        exitMock.assert_called_once_with(1)

    @patch('臺灣言語工具.斷詞.國教院斷詞用戶端.國教院斷詞用戶端.語句斷詞做陣列')
    def test_華語(self, 回應mock):
        回應mock.return_value = [
            ["我", "Nc"], ["愛", "Ncd"], ["小豬", "D"],
        ]
        過渡語料處理.objects.create(外文='我愛小豬', **self.公家內容)
        過渡語料處理.外文用國教院斷詞()
        self.assertEqual(過渡語料處理.objects.get().外文, '我 愛 小-豬')

    @patch('臺灣言語工具.斷詞.國教院斷詞用戶端.國教院斷詞用戶端.語句斷詞做陣列')
    def test_會回傳數量(self, 回應mock):
        回應mock.return_value = [
            ["我", "Nc"], ["愛", "Ncd"], ["小豬", "D"],
        ]
        for _ in range(333):
            過渡語料處理.objects.create(外文='我愛小豬', **self.公家內容)
        斷詞數量 = 過渡語料處理.外文用國教院斷詞()
        self.assertEqual(斷詞數量, 333)

    def test_無華語(self):
        過渡語料處理.objects.create(文本='我愛豬仔', **self.公家內容)
        斷詞數量 = 過渡語料處理.外文用國教院斷詞()
        self.assertEqual(斷詞數量, 0)
