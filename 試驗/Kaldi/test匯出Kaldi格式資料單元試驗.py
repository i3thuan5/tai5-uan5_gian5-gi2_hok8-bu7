import io
from os.path import join
from tempfile import TemporaryDirectory

from django.core.management import call_command
from django.test.testcases import TestCase


from 臺灣言語工具.語音辨識.聲音檔 import 聲音檔
from 臺灣言語服務.models import 訓練過渡格式


class 匯出Kaldi格式資料單元試驗(TestCase):

    def test_有文本資料(self):
        with TemporaryDirectory() as 資料夾路徑:
            音檔所在 = join(資料夾路徑, 'siann.wav')
            with open(音檔所在, 'wb') as 檔案:
                檔案.write(聲音檔.對參數轉(2, 16, 1, b'sui2khiau2' * 160).wav格式資料())
            訓練過渡格式.objects.create(
                來源='媠巧',
                年代='2017',
                種類='語句',
                影音所在=音檔所在,
                影音語者='阿宏',
                文本='tsiang5 tsiang5',
            )
            with io.StringIO() as out:
                call_command('匯出Kaldi格式資料', '台語', '拆做音素', 資料夾路徑, stdout=out)
                self.assertIn('1 段', out.getvalue())

    def test_有聽拍資料(self):
        with TemporaryDirectory() as 資料夾路徑:
            音檔所在 = join(資料夾路徑, 'siann.wav')
            with open(音檔所在, 'wb') as 檔案:
                檔案.write(聲音檔.對參數轉(2, 16, 1, b'sui2khiau2' * 160).wav格式資料())
            訓練過渡格式.objects.create(
                來源='媠巧',
                年代='2017',
                種類='語句',
                影音所在=音檔所在,
                聽拍=[{
                    '語者': '阿宏', '內容': 'tsiang5 tsiang5',
                    '開始時間': 0.0, '結束時間': 1.2,
                }],
            )
            with io.StringIO() as out:
                call_command('匯出Kaldi格式資料', '台語', '拆做音素', 資料夾路徑, stdout=out)
                self.assertIn('1 段', out.getvalue())

    def test_無資料(self):
        with TemporaryDirectory() as 資料夾路徑:
            with io.StringIO() as out:
                call_command('匯出Kaldi格式資料', '台語', '拆做音素', 資料夾路徑, stdout=out)
                self.assertIn('0 段', out.getvalue())
