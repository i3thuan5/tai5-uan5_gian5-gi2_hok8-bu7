from django.core.management.base import BaseCommand


from 臺灣言語服務.輸出 import 資料輸出工具


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument(
            '語言',
            nargs='*',
            type=str,
            help='要匯出的語言'
        )

    def handle(self, *args, **參數):
        資料輸出工具().輸出文本語料()
