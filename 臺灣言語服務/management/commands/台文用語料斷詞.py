import sys
from django.core.management.base import BaseCommand
from 臺灣言語服務.過渡語料 import 過渡語料處理


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument(
            '--欲參考',
            nargs='+',
            type=str,
            required=True,
        )
        parser.add_argument(
            '--欲斷詞',
            nargs='+',
            type=str,
            required=True,
        )
        parser.add_argument(
            '--辭典詞長',
            type=int,
            default='4',
            help='辭典的上大詞長'
        )
        parser.add_argument(
            '--連紲詞長度',
            type=int,
            default='3',
            help='語言文本的連紲詞長度(n-grams)'
        )

    def handle(self, *_args, **參數):
        try:
            斷詞數量 = 過渡語料處理.台文語料斷詞(
                參數['欲參考'], 參數['欲斷詞'],
                參數['辭典詞長'], 參數['連紲詞長度'],
            )
        except ValueError as 錯誤:
            print('{}'.format(錯誤), file=self.stderr)
            sys.exit(1)
        else:
            print('斷詞 {} 句!!'.format(斷詞數量), file=self.stderr)
