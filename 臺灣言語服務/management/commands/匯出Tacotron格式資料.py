from django.conf import settings
from django.core.management.base import BaseCommand


from 臺灣言語服務.tacotron.輸出 import Tacotron模型訓練


class Command(BaseCommand):
    help = '照kaldi格式匯出語料'

    def add_arguments(self, parser):
        parser.add_argument(
            '語言',
            type=str,
            help='選擇語料的語言'
        )
        parser.add_argument(
            '語者',
            type=str,
            help='發音人'
        )
        parser.add_argument(
            '--頻率',
            type=int,
            default=16000,
        )
        parser.add_argument(
            '匯出路徑',
            type=str,
            help='會有metadata.csv kah wavs ê taioanoe/ 所在'
        )

    def handle(self, *args, **參數):
        語言 = 參數['語言']
        語者 = 參數['語者']
        服務設定 = settings.HOK8_BU7_SIAT4_TING7[語言]
        幾段音檔 = Tacotron模型訓練.輸出LJ格式(
            參數['匯出路徑'], 語者, 參數['頻率'],
            服務設定['音標系統']
        )
        self.stdout.write('輸出 {} 段音檔'.format(幾段音檔))
