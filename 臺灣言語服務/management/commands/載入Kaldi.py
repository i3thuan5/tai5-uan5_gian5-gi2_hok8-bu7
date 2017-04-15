from django.core.management.base import BaseCommand


from 臺灣言語服務.Kaldi介面 import Kaldi辨識影音


class Command(BaseCommand):
    help = '辨識一个影音檔'

    def add_arguments(self, parser):
        parser.add_argument(
            '編號',
            type=int,
            help='愛辨識的影音編號'
        )

    def handle(self, *args, **參數):
        Kaldi辨識影音.delay(參數['編號'])
