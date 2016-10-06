from os import makedirs
from os.path import join, dirname
from shutil import copyfile
from sys import stderr

from django.conf import settings
from django.core.management.base import BaseCommand


from 臺灣言語服務.HTS模型訓練 import HTS模型訓練
from 臺灣言語服務.資料模型路徑 import 資料路徑
from 臺灣言語服務.資料模型路徑 import 合成模型路徑
from 臺灣言語工具.語音合成.HTS工具.安裝HTS語音辨識程式 import 安裝HTS語音辨識程式


class Command(BaseCommand):
    help = '訓練一个語言的HTS模型'

    def add_arguments(self, parser):
        parser.add_argument(
            '語言',
            type=str,
            help='愛訓練的語言'
        )
        parser.add_argument(
            '語者',
            type=str,
            help='發音人'
        )

    def handle(self, *args, **參數):
        安裝HTS語音辨識程式.安裝htk()
        安裝HTS語音辨識程式.安裝sptk()
        安裝HTS語音辨識程式.安裝hts()
        安裝HTS語音辨識程式.掠htsDemoScript()
        try:
            語言 = 參數['語言']
            服務設定 = settings.HOK8_BU7_SIAT4_TING7[語言]
            語者 = 參數['語者']
            模型資料夾 = join(資料路徑, 語言, '{}-HTS模型'.format(語者))
            語料資料夾 = join(模型資料夾, '語料')
            try:
                變調規則 = 服務設定['變調規則']
            except:
                變調規則 = None
            HTS模型訓練.輸出一種語言語料(
                語料資料夾, 語言, 語者,
                服務設定['音標系統'],
                變調規則
            )
            對齊聲韻結果資料夾 = HTS模型訓練.對齊聲韻(
                語料資料夾, 模型資料夾, 服務設定['文本音值表']
            )
            模型路徑 = HTS模型訓練.輸出HTS標仔問題音檔而且訓練(
                語料資料夾, 對齊聲韻結果資料夾, 模型資料夾,
                服務設定['決策樹仔']
            )
            上尾模型路徑 = 合成模型路徑(語言)
            makedirs(dirname(上尾模型路徑), exist_ok=True)
            copyfile(模型路徑, 上尾模型路徑)
        except FileNotFoundError:
            raise
            print('資料庫無「{}」的語料！！'.format(參數['語言']), file=stderr)
