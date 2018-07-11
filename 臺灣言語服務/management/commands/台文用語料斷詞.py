import sys
from django.core.management.base import BaseCommand
from 臺灣言語服務.過渡語料 import 過渡語料處理


class Command(BaseCommand):

    def handle(self, *_args, **參數):
        try:
            斷詞數量 = 過渡語料處理.台文語料斷詞(
                參數['參考'], 參數['欲斷詞'], 3
            )
        except ValueError as 錯誤:
            print('{}'.format(錯誤), file=self.stderr)
            sys.exit(1)
        print('斷詞 {} 句!!'.format(斷詞數量), file=self.stderr)
