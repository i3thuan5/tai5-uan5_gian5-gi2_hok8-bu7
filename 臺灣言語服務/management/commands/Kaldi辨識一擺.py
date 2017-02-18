from django.core.management.base import BaseCommand


from 臺灣言語服務.Kaldi介面 import 無辨識過的重訓練一擺


class Command(BaseCommand):
    help = '無辨識過的音檔重訓練一擺'

    def handle(self, *args, **參數):
        無辨識過的重訓練一擺()
