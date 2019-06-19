from time import sleep

import Pyro4
from django.conf import settings
from django.core.management.base import BaseCommand
from 臺灣言語服務.HTS服務 import HTS服務
from 臺灣言語服務.Moses服務 import Moses服務
from 臺灣言語服務.標書寫服務 import 標書寫服務


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument(
            '翻譯主機',
        )

    def handle(self, *args, **參數):
        pyro4主機 = getattr(settings, "PYRO4_TSU2_KI1", None)
        daemon = Pyro4.Daemon(host=參數['翻譯主機'])
        ns = Pyro4.locateNS(host=pyro4主機)

        uri = daemon.register(標書寫服務())
        while True:
            try:
                ns.register("台語標書寫", uri)
            except Pyro4.errors.NamingError:
                sleep(3)
            else:
                break
        print("標書寫服務", uri, file=self.stderr)

        daemon.requestLoop()
