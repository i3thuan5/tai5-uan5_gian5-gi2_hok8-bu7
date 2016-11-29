from django.core.management.base import BaseCommand


from 臺灣言語工具.翻譯.摩西工具.安裝摩西翻譯佮相關程式 import 安裝摩西翻譯佮相關程式


class Command(BaseCommand):
    help = '裝Moses程式。掠而且編譯，可能愛半點鐘以上'

    def add_arguments(self, parser):
        parser.add_argument(
            '--編譯核心數',
            dest='核心數',
            default=4,
            type=int,
        )

    def handle(self, *args, **參數):
        安裝摩西翻譯佮相關程式.安裝gizapp()
        安裝摩西翻譯佮相關程式.安裝moses(編譯CPU數=參數['核心數'])
