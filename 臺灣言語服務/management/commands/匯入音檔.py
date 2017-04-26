from django.core.management.base import BaseCommand


from 臺灣言語工具.語音辨識.聲音檔 import 聲音檔
from 臺灣言語服務.Kaldi語料辨識 import Kaldi語料辨識


class Command(BaseCommand):
    help = '匯入準備愛予Kaldi辨識的音檔'

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
        parser.add_argument(
            '--分詞',
            dest='分詞',
            type=str,
            default='',
        )

    def handle(self, *args, **參數):
        for 音檔路徑 in 參數['音檔路徑']:
            影音 = Kaldi語料辨識.匯入音檔(參數['語言'], '無註明', 聲音檔.對檔案讀(音檔路徑), 參數['分詞'])
            print(影音.編號())
