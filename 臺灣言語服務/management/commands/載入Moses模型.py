from django.core.management.base import BaseCommand
from 臺灣言語服務.模型載入 import 模型載入
from 臺灣言語服務.HTS服務 import HTS服務
import Pyro4


class Command(BaseCommand):
    help = '載入摩西翻譯模型'

    def handle(self, *args, **參數):
        #         摩西模型=模型載入.摩西模型()
        hts = HTS服務()
        Pyro4.Daemon.serveSimple(
            {
                hts: "HTS服務"
            },
            ns=True
        )
