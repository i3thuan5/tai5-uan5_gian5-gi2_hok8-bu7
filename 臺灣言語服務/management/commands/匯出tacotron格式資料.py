import csv
from os.path import join

from django.core.management.base import BaseCommand


from 臺灣言語服務.資料模型路徑 import 資料路徑
from 臺灣言語資料庫.資料模型 import 影音表
from 臺灣言語資料庫.資料模型 import 資料屬性表
from os import makedirs


class Command(BaseCommand):
    help = '照kaldi格式匯出語料'

    def add_arguments(self, parser):
        parser.add_argument(
            '語言',
            type=str,
            help='愛訓練的語言'
        )
        parser.add_argument(
            '語者',
            type=str,
            help='發音人'
        )

    def handle(self, *args, **參數):
        語言 = 參數['語言']
        語者 = 參數['語者']
        資料夾 = join(資料路徑, 語言)
        幾段音檔 = self.輸出一種語言語料(
            資料夾, 語言, 語者
        )
        self.stdout.write('輸出 {} 段音檔'.format(幾段音檔))

    def 輸出一種語言語料(self, 合成語料資料夾, 語言, 語者):
        makedirs(合成語料資料夾, exist_ok=True)
        with open(join(合成語料資料夾, 'tacotron.csv'), 'wt') as tacotron檔案:
            tacotron資料 = csv.writer(tacotron檔案)
            for 第幾个, 影音 in enumerate(
                影音表.objects
                .distinct()
                .filter(影音文本__isnull=False)
                .filter(語言腔口__語言腔口=語言)
                .filter(屬性=資料屬性表.揣屬性('語者', 語者))
            ):
                文本 = self._揣上尾的文本(影音.影音文本.first().文本)
                tacotron資料.writerow([
                    影音.影音所在(), 文本.文本資料, 影音.聲音檔().時間長度()
                ])
            return 第幾个

    def _揣上尾的文本(self, 文本):
        try:
            while True:
                文本 = 文本.文本校對.first().新文本
        except:
            return 文本
