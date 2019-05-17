# -*- coding: utf-8 -*-
import io
from unittest.mock import patch

from django.core.management import call_command
from django.test import TestCase


from 臺灣言語服務.過渡語料 import 過渡語料處理
from django.core.management.base import CommandError


class test台文斷詞單元試驗(TestCase):
    公家內容 = {'種類':  '語句', '年代':  '2018', }

    @patch('臺灣言語服務.過渡語料.過渡語料處理.台文語料斷詞')
    def test_指令的參數愛運作正常(self, 台文語料斷詞mock):
        with io.StringIO() as err:
            call_command(
                '台文用語料斷詞',
                '--欲參考', 'su-tian', 'su-lui',
                '--欲斷詞', 'ti-a',
                '--辭典詞長', '4', '--連紲詞長度', '3',
                stderr=err
            )
        台文語料斷詞mock.assert_called_once_with(
            ['su-tian', 'su-lui'],
            ['ti-a'],
            4, 3,
        )

    @patch('臺灣言語服務.過渡語料.過渡語料處理.台文語料斷詞')
    def test_指令顯示數量(self, 台文語料斷詞mock):
        台文語料斷詞mock.return_value = 333
        with io.StringIO() as err:
            call_command(
                '台文用語料斷詞',
                '--欲參考', 'su-tian',  'su-lui',
                '--欲斷詞', 'ti-a',
                stderr=err
            )
            self.assertIn('斷詞 333 句', err.getvalue())

    @patch('sys.exit')
    @patch('臺灣言語服務.過渡語料.過渡語料處理.台文語料斷詞')
    def test_無語料愛錯誤(self, 台文語料斷詞mock, exitMock):
        台文語料斷詞mock.side_effect = ValueError()
        with io.StringIO() as err:
            call_command(
                '台文用語料斷詞',
                '--欲參考', 'su-tian', 'su-lui',
                '--欲斷詞', 'ti-a',
                stderr=err,
            )
        exitMock.assert_called_once_with(1)

    def test_無參數愛錯誤(self):
        with self.assertRaises(CommandError):
            call_command(
                '台文用語料斷詞'
            )

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
