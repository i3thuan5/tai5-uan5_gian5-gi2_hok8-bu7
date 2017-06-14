import io
from tempfile import TemporaryDirectory

from django.core.management import call_command
from django.test.testcases import TestCase


from 臺灣言語工具.語音辨識.聲音檔 import 聲音檔
from 臺灣言語服務.Kaldi語料辨識 import Kaldi語料辨識


class 匯出Kaldi格式資料單元試驗(TestCase):

    def test_有資料(self):
        Kaldi語料辨識.匯入音檔(
            '閩南語', '媠巧',
            聲音檔.對參數轉(2, 16, 1, b'sui2khiau2' * 160), '\ntsiang5\ntsiang5\n',
        )
        with TemporaryDirectory() as 資料夾路徑:
            with io.StringIO() as out:
                call_command('匯出Kaldi格式資料', '閩南語', 資料夾路徑, stdout=out)
                self.assertIn('1 段', out.getvalue())

    def test_無資料(self):
        with TemporaryDirectory() as 資料夾路徑:
            with io.StringIO() as out:
                call_command('匯出Kaldi格式資料', '閩南語', 資料夾路徑, stdout=out)
                self.assertIn('0 段', out.getvalue())
