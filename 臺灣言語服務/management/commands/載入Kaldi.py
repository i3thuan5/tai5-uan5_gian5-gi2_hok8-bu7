from django.core.management.base import BaseCommand


from 臺灣言語服務.Kaldi語料辨識 import Kaldi語料辨識
from 臺灣言語資料庫.資料模型 import 影音表


class Command(BaseCommand):
    help = '訓練一个語言的HTS模型'

    def add_arguments(self, parser):
        parser.add_argument(
            '編號',
            type=int,
            help='愛辨識的影音編號'
        )

    def handle(self, *args, **參數):
        影音 = 影音表.objects.get(pk=參數['編號'])
        章物件 = Kaldi語料辨識.辨識音檔(影音)
        print(章物件.看型())
        print(章物件.看音())
