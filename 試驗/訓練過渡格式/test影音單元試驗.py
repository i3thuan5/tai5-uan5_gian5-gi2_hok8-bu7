from os.path import join
from shutil import rmtree
import wave

from django.core.exceptions import ValidationError
from django.test.testcases import TestCase


from 臺灣言語服務.models import 訓練過渡格式
from os import makedirs
from django.conf import settings


class 影音所在試驗(TestCase):
    公家內容 = {'來源': 'Dr. Pigu', '種類':  '字詞', '年代':  '2017', }

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

    def test_無影音無要緊(self):
        一筆 = 訓練過渡格式(**self.公家內容)
        一筆.full_clean()
        一筆.save()
        self.assertIsNone(一筆.影音所在)

    def test_有影音上好有語者(self):
        訓練過渡格式(影音所在=self.音檔所在, 影音語者='Pigu', **self.公家內容).full_clean()

    def test_有影音無一定愛有語者(self):
        訓練過渡格式(影音所在=self.音檔所在, **self.公家內容).full_clean()

    def test_無語者就是存空的(self):
        一筆 = 訓練過渡格式.objects.create(影音所在=self.音檔所在, **self.公家內容)
        self.assertEqual(一筆.影音語者, '')

    def test_有語者就一定愛有影音(self):
        with self.assertRaises(ValidationError):
            訓練過渡格式(影音語者='Pigu', **self.公家內容).full_clean()

    def test_影音所在毋是檔案(self):
        with self.assertRaises(ValidationError):
            訓練過渡格式(影音所在=self.資料夾, **self.公家內容).full_clean()

    def test_影音所在毋是wav(self):
        檔案所在 = join(self.資料夾, '別種檔案.sui')
        with open(檔案所在, 'wb') as 音檔:
            音檔.write(b'sui2' * 80000)
        with self.assertRaises(ValidationError):
            訓練過渡格式(影音所在=檔案所在, **self.公家內容).full_clean()

    def test_愛轉做絕對路徑(self):
        一筆 = 訓練過渡格式(影音所在=join('暫存', '音檔.wav'), **self.公家內容)
        一筆.full_clean()
        一筆.save()
        self.assertEqual(一筆.影音所在, self.音檔所在)

    def test_影音所在袂使是空字串(self):
        with self.assertRaises(ValidationError):
            訓練過渡格式(影音所在='', **self.公家內容).full_clean()

    def test_影音有通提出來用(self):
        一筆 = 訓練過渡格式.objects.create(影音所在=self.音檔所在, **self.公家內容)
        self.assertEqual(一筆.聲音檔().時間長度(), 10.0)
