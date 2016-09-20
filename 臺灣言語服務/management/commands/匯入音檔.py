import io

from django.core.management.base import BaseCommand
from django.utils import timezone


from 臺灣言語資料庫.資料模型 import 來源表
from 臺灣言語資料庫.資料模型 import 聽拍規範表
from 臺灣言語資料庫.資料模型 import 影音表
from 臺灣言語資料庫.資料模型 import 版權表
from 臺灣言語工具.語音辨識.聲音檔 import 聲音檔


class Command(BaseCommand):
    help = '照kaldi格式匯出語料'

    def add_arguments(self, parser):
        parser.add_argument(
            '語言',
            type=str,
            help='選擇語料的語言'
        )
        parser.add_argument(
            '音檔路徑',
            nargs='+',
            type=str,
            help='要匯入的音檔'
        )

    def handle(self, *args, **參數):
        公家內容 = {
            '收錄者': 來源表.objects.get_or_create(名='系統管理員')[0].編號(),
            '來源': 來源表.objects.get_or_create(名='系統管理員')[0].編號(),
            '版權': 版權表.objects.get_or_create(版權='會使公開')[0].pk,
            '種類': '語句',
            '語言腔口': 參數['語言'],
            '著作所在地': '臺灣',
            '著作年': str(timezone.now().year),
        }
        規範 = 聽拍規範表.objects.get_or_create(規範名='無規範', 範例='無', 說明='bo5')[0]
        for 音檔路徑 in 參數['音檔路徑']:
            with io.open(音檔路徑, 'rb') as 音檔:
                音 = 聲音檔.對檔案讀(音檔路徑)
                影音內容 = {'影音資料': 音檔}
                影音內容.update(公家內容)
                影音 = 影音表.加資料(影音內容)
                聽拍資料 = [
                    {
                        '語者': '無註明',
                        '內容': '',
                        '開始時間': 0,
                        '結束時間': 音.時間長度()
                    }
                ]
                聽拍內容 = {'規範': 規範, '聽拍資料': 聽拍資料}
                聽拍內容.update(公家內容)
                影音.寫聽拍(聽拍內容)
