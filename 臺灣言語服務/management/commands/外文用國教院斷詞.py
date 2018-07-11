import sys
from django.core.management.base import BaseCommand
from 臺灣言語服務.過渡語料 import 過渡語料處理


class Command(BaseCommand):

    def handle(self, *_args, **_參數):
        斷詞數量 = 過渡語料處理.外文用國教院斷詞()
        if 斷詞數量 == 0:
            print('無外文資料!!', file=self.stderr)
            sys.exit(1)
        print('斷詞 {} 句!!'.format(斷詞數量), file=self.stderr)
