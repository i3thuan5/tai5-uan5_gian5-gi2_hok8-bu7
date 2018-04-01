import Pyro4
from django.conf import settings
from django.core.management.base import BaseCommand
from 臺灣言語服務.HTS服務 import HTS服務
from 臺灣言語服務.Moses服務 import Moses服務
from time import sleep


class Command(BaseCommand):
    help = '載入摩西翻譯模型'

    def handle(self, *args, **參數):
        pyro4主機 = getattr(settings, "PYRO4_TSU2_KI1", None)
        翻譯主機 = getattr(settings, "HUAN1_IK8_TSU2_KI1", None)
        daemon = Pyro4.Daemon(host=翻譯主機)
        ns = Pyro4.locateNS(host=pyro4主機)

        uri = daemon.register(Moses服務())
        while True:
            try:
                ns.register("Moses服務", uri)
            except Pyro4.errors.NamingError:
                sleep(3)
            else:
                break
        print("Moses服務", uri, file=self.stderr)

        if getattr(settings, "HTS_ING7_PYRO4", False):
            uri = daemon.register(HTS服務())
            ns.register("HTS服務", uri)
            print("HTS服務", uri, file=self.stderr)

        daemon.requestLoop()
