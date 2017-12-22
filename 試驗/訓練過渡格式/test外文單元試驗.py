# -*- coding: utf-8 -*-
from django.core.exceptions import ValidationError
from django.test import TestCase
from 臺灣言語服務.models import 訓練過渡格式


class 外文試驗(TestCase):
    公開內容 = {'來源': 'Dr. Pigu', '種類':  '字詞', '年代':  '2017', }

    def test_正常分詞(self):
        訓練過渡格式(外文='走｜ㄗㄡˇ', **self.公開內容).full_clean()

    def test_錯誤分詞(self):
        with self.assertRaises(ValidationError):
            訓練過渡格式(外文='走走｜ㄗㄡˇ', **self.公開內容).full_clean()

    def test_無外文無要緊(self):
        訓練過渡格式(**self.公開內容).full_clean()

    def test_無外文就是愛存None才有法度filter(self):
        一筆 = 訓練過渡格式.objects.create(**self.公開內容)
        self.assertIsNone(一筆.外文)
