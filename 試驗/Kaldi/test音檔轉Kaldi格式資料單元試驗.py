from os.path import join, dirname
from tempfile import TemporaryDirectory

from django.core.management import call_command
from django.test.testcases import TestCase
from 臺灣言語工具.語音辨識.聲音檔 import 聲音檔
from 臺灣言語服務.models import 訓練過渡格式


class 音檔轉Kaldi格式資料單元試驗(TestCase):
    def test_有分詞(self):
        with TemporaryDirectory() as 資料夾路徑:
            self.音檔所在 = join(資料夾路徑, 'siann.wav')
            with open(self.音檔所在, 'wb') as 檔案:
                檔案.write(聲音檔.對參數轉(2, 16, 1, b'sui2khiau2' * 160).wav格式資料())
            self.s5 = join(資料夾路徑, 's5')
            call_command(
                '音檔轉Kaldi格式資料', '台語', self.音檔所在, self.s5,
                '--分詞', '媠巧',
            )
            with open(join(self.s5, 'data', 'train', 'text')) as tong:
                self.assertIn('媠巧', tong.read())

    def test_無新檔(self):
        with TemporaryDirectory() as 資料夾路徑:
            self.音檔所在 = join(資料夾路徑, 'siann.wav')
            with open(self.音檔所在, 'wb') as 檔案:
                檔案.write(聲音檔.對參數轉(2, 16, 1, b'sui2khiau2' * 160).wav格式資料())
            self.s5 = join(資料夾路徑, 's5')
            call_command('音檔轉Kaldi格式資料', '台語', self.音檔所在, self.s5)
        self.assertEqual(訓練過渡格式.objects.count(), 0)

    def test_mp4(self):
        with TemporaryDirectory() as 資料夾路徑:
            self.音檔所在 = join(dirname(__file__), 'iannim', '26-意傳-節氣.mp4')
            self.s5 = join(資料夾路徑, 's5')
            call_command(
                '音檔轉Kaldi格式資料', '台語', self.音檔所在, self.s5
            )
            with open(join(self.s5, 'data', 'train', 'segments')) as tong:
                self.assertIn('ku', tong.read())
