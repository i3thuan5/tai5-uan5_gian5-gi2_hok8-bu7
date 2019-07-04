import os
from os.path import join

from django.conf import settings
from django.core.management.base import BaseCommand


from 臺灣言語服務.Kaldi語料匯出 import Kaldi語料匯出
from 臺灣言語服務.kaldi.lexicon import 辭典輸出


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            '語言',
            type=str,
            help='選擇語料的語言'
        )
        parser.add_argument(
            '辭典輸出函式',
            type=str,
            choices=[
                mia
                for mia in dir(辭典輸出)
                if (
                    callable(getattr(辭典輸出, mia)) and
                    not mia.startswith("_") and
                    mia != '漢字聲韻'
                )
            ],
            help='選擇lexicon佮聲學單位格式'
        )
        parser.add_argument(
            '語言文本',
            type=str,
            help='選擇語料的語言文本，產生lexicon辭典'
        )
        parser.add_argument(
            '匯出路徑',
            type=str,
            help='kaldi的egs內底的s5資料夾'
        )

    def handle(self, *args, **參數):
        辭典資料 = Kaldi語料匯出.初使化辭典資料()
        非語言音數 = len(辭典資料['全部詞'])
        語言 = 參數['語言']
        服務設定 = settings.HOK8_BU7_SIAT4_TING7[語言]
        辭典輸出物件 = 辭典輸出(服務設定['音標系統'], 參數['辭典輸出函式'])
        Kaldi語料匯出.辭典資料載入語句文本(參數['語言文本'], 辭典輸出物件, 辭典資料, 加語料=True)
        dict資料夾 = Kaldi語料匯出.匯出辭典資料(辭典資料, 參數['匯出路徑'], 'data')
        os.rename(
            join(dict資料夾, 'lexicon.txt'),
            join(參數['匯出路徑'], 'lexicon.txt')
        )
        self.stdout.write('辭典有 {} 詞'.format(len(辭典資料['全部詞']) - 非語言音數))
