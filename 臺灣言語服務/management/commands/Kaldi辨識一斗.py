from django.core.management.base import BaseCommand


from 臺灣言語服務.Kaldi語料辨識 import Kaldi語料辨識


class Command(BaseCommand):
    help = '無辨識過的音檔重訓練一擺'

    def handle(self, *_args, **_參數):
        for Kaldi辨識 in Kaldi語料辨識.objects.filter(辨識好猶未=False):
            Kaldi辨識.辨識()
