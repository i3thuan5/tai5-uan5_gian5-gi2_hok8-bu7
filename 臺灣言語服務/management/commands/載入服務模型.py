import Pyro4
from django.core.management.base import BaseCommand
from 臺灣言語服務.HTS服務 import HTS服務
from 臺灣言語服務.Moses服務 import Moses服務


class Command(BaseCommand):
    help = '載入摩西翻譯模型'

    def handle(self, *args, **參數):
        Pyro4.Daemon.serveSimple(
            {
                Moses服務(): "Moses服務",
                HTS服務(): "HTS服務",
            },
            ns=True
        )
