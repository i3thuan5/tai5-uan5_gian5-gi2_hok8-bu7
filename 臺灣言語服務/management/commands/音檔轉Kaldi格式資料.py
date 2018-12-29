from django.conf import settings
from django.core.management.base import BaseCommand
from django.db.models.query_utils import Q
from django.utils import timezone


from 臺灣言語服務.models import 訓練過渡格式
from 臺灣言語服務.Kaldi語料匯出 import Kaldi語料匯出
from 臺灣言語服務.kaldi.lexicon import 辭典輸出
from os.path import abspath


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
            type=str,
            help='要匯入的音檔'
        )
        parser.add_argument(
            '--分詞',
            dest='分詞',
            type=str,
            default='',
        )
        parser.add_argument(
            '匯出路徑',
            type=str,
            help='kaldi的egs內底的s5資料夾'
        )
        parser.add_argument(
            '--資料夾',
            type=str,
            dest='資料夾名',
            default='data',
            help='s5底下的資料夾名',
        )

    def handle(self, *args, **參數):
        過渡格式 = 訓練過渡格式.objects.create(
            來源='使用者',
            種類='語句',
            年代=str(timezone.now().year),
            影音所在=abspath(參數['音檔路徑']),
            文本=參數['分詞'],
        )
        服務設定 = settings.HOK8_BU7_SIAT4_TING7[參數['語言']]
        Kaldi語料匯出.匯出一種語言語料(
            參數['語言'], 辭典輸出(服務設定['音標系統'], '拆做音素'),
            參數['匯出路徑'], 參數['資料夾名'], Kaldi語料匯出.初使化辭典資料(),
            Q(pk=過渡格式.編號())
        )
        過渡格式.delete()
