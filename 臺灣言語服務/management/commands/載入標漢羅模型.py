from time import sleep

import Pyro4
from django.conf import settings
from django.core.management.base import BaseCommand


from 臺灣言語服務.標書寫服務 import 漢羅服務


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument(
            '翻譯主機',
        )

    def handle(self, *args, **參數):
        pyro4主機 = getattr(settings, "PYRO4_TSU2_KI1", 'pyro4')
        daemon = Pyro4.Daemon(host=參數['翻譯主機'])
        ns = Pyro4.locateNS(host=pyro4主機)

        print("讀服務", file=self.stderr)
        uri = daemon.register(漢羅服務())
        while True:
            try:
                ns.register("台語標書寫", uri)
            except Pyro4.errors.NamingError:
                sleep(3)
            else:
                break
        print("標書寫服務", uri, file=self.stderr)

        daemon.requestLoop()
