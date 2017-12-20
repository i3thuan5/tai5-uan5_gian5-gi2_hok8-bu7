# -*- coding: utf-8 -*-
import json
from os import makedirs
from os.path import join
from shutil import rmtree
import wave

from django.conf import settings
from django.core.exceptions import ValidationError
from django.test import TestCase


from 臺灣言語服務.models import 訓練過渡格式


class 聽拍資料試驗(TestCase):

    公開內容 = {'來源': 'Dr. Pigu', '種類':  '字詞', '年代':  '2017', }

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.資料夾 = join(settings.BASE_DIR, '暫存')
        makedirs(cls.資料夾, exist_ok=True)
        cls.音檔所在 = join(cls.資料夾, '音檔.wav')
        with wave.open(cls.音檔所在, 'wb') as 音檔:
            音檔.setnchannels(1)
            音檔.setframerate(16000)
            音檔.setsampwidth(2)
            音檔.writeframesraw(b'sui2' * 80000)

    @classmethod
    def tearDownClass(cls):
        rmtree(cls.資料夾)

    def test_一句話(self):
        聽拍 = [
            {'語者': '阿宏', '內容': 'sui2', '開始時間': 0.0, '結束時間': 1.2},
        ]
        訓練過渡格式(影音所在=self.音檔所在, 聽拍=聽拍, **self.公開內容).full_clean()

    def test_一句一句話(self):
        聽拍 = [
            {'語者': '阿宏', '內容': 'li1', '開始時間': 0.0, '結束時間': 1.2},
            {'語者': '阿莉', '內容': 'ho2', '開始時間': 1.2, '結束時間': 2.0},
        ]
        訓練過渡格式(影音所在=self.音檔所在, 聽拍=聽拍, **self.公開內容).full_clean()

    def test_時間疊做伙無要緊(self):
        聽拍 = [
            {'語者': '阿宏', '內容': 'li1', '開始時間': 0.0, '結束時間': 1.5},
            {'語者': '阿莉', '內容': 'ho2', '開始時間': 0.5, '結束時間': 2.0},
        ]
        訓練過渡格式(影音所在=self.音檔所在, 聽拍=聽拍, **self.公開內容).full_clean()

    def test_愛有音檔才會當有聽拍(self):
        聽拍 = [
            {'語者': '阿宏', '內容': 'li1', '開始時間': 0.0, '結束時間': 1.2},
            {'語者': '阿莉', '內容': 'ho2', '開始時間': 1.2, '結束時間': 2.0},
        ]
        with self.assertRaises(ValidationError):
            訓練過渡格式(聽拍=聽拍, **self.公開內容).full_clean()

    def test_聽拍的時間袂使超過音檔(self):
        聽拍 = [
            {'語者': '阿宏', '內容': 'li1', '開始時間': 0.0, '結束時間': 10.2},
            {'語者': '阿莉', '內容': 'ho2', '開始時間': 10.2, '結束時間': 20.0},
        ]
        with self.assertRaises(ValidationError):
            訓練過渡格式(影音所在=self.音檔所在, 聽拍=聽拍, **self.公開內容).full_clean()

    def test_聽拍的時間袂使有負的(self):
        聽拍 = [
            {'語者': '阿宏', '內容': 'li1', '開始時間': -3.0, '結束時間': 1.2},
            {'語者': '阿莉', '內容': 'ho2', '開始時間': 1.2, '結束時間': 2.0},
        ]
        with self.assertRaises(ValidationError):
            訓練過渡格式(影音所在=self.音檔所在, 聽拍=聽拍, **self.公開內容).full_clean()

    def test_無聽拍資料無要緊(self):
        訓練過渡格式(**self.公開內容).full_clean()

    def test_聽拍資料無內容欄位(self):
        聽拍 = [
            {'語者': '阿宏',  '開始時間': 0.0, '結束時間': 1.2},
        ]
        with self.assertRaises(ValidationError):
            訓練過渡格式(影音所在=self.音檔所在, 聽拍=聽拍, **self.公開內容).full_clean()

    def test_無語者欄位(self):
        聽拍 = [
            {'內容': 'sui2', '開始時間': 0.0, '結束時間': 1.2},
        ]
        with self.assertRaises(ValidationError):
            訓練過渡格式(影音所在=self.音檔所在, 聽拍=聽拍, **self.公開內容).full_clean()

    def test_無開始時間欄位(self):
        聽拍 = [
            {'語者': '阿宏', '內容': 'sui2', '開始時': 0.0, '結束時間': 1.2},
        ]
        with self.assertRaises(ValidationError):
            訓練過渡格式(影音所在=self.音檔所在, 聽拍=聽拍, **self.公開內容).full_clean()

    def test_聽拍資料無結束時間欄位(self):
        聽拍 = [
            {'語者': '阿宏', '內容': 'sui2', '開始時間': 0.0, '結束': 1.2},
        ]
        with self.assertRaises(ValidationError):
            訓練過渡格式(影音所在=self.音檔所在, 聽拍=聽拍, **self.公開內容).full_clean()

    def test_聽拍資料用字串(self):
        聽拍 = [
            {'語者': '阿宏', '內容': 'sui2', '開始時間': 0.0, '結束時間': 1.2},
        ]
        with self.assertRaises(ValidationError):
            訓練過渡格式(影音所在=self.音檔所在, 聽拍=json.dumps(聽拍), **self.公開內容).full_clean()

    def test_有聽拍資料就filter揣出來(self):
        聽拍 = [
            {'語者': '阿宏', '內容': 'sui2', '開始時間': 0.0, '結束時間': 1.2},
        ]
        訓練過渡格式.objects.create(影音所在=self.音檔所在, 聽拍=聽拍, **self.公開內容)
        self.assertTrue(訓練過渡格式.objects.filter(聽拍__isnull=False).exists())

    def test_無聽拍資料就袂使用聽拍_會當filter(self):
        訓練過渡格式.objects.create(**self.公開內容)
        self.assertTrue(訓練過渡格式.objects.filter(聽拍__isnull=True).exists())
        self.assertTrue(訓練過渡格式.objects.filter(聽拍=None).exists())

    def test_無聽拍資料就袂使用聽拍_是None(self):
        一筆 = 訓練過渡格式.objects.create(**self.公開內容)
        self.assertIsNone(一筆.聽拍)

    def test_存入去愛有法度提出來用(self):
        聽拍 = [
            {'語者': '阿宏', '內容': 'sui2', '開始時間': 0.0, '結束時間': 1.2},
        ]
        一筆 = 訓練過渡格式(影音所在=self.音檔所在, 聽拍=聽拍, **self.公開內容)
        self.assertEqual(一筆.聽拍, 聽拍)

    def test_改聽拍(self):
        聽拍 = [
            {'語者': '阿宏', '內容': 'sui2', '開始時間': 0.0, '結束時間': 1.2},
        ]
        一筆 = 訓練過渡格式.objects.create(影音所在=self.音檔所在, 聽拍=聽拍, **self.公開內容)
        新聽拍 = [
            {'語者': '阿莉', '內容': 'khiau2', '開始時間': 0.0, '結束時間': 1.2},
        ]
        一筆.聽拍 = 新聽拍
        self.assertEqual(一筆.聽拍, 新聽拍)
