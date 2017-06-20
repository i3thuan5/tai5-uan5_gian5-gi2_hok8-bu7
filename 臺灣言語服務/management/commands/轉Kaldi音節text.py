from os import makedirs
from os.path import join, isfile, isdir
from shutil import copyfile, rmtree

from django.conf import settings
from django.core.management.base import BaseCommand


from 臺灣言語服務.Kaldi語料處理 import Kaldi語料處理
from 臺灣言語工具.系統整合.程式腳本 import 程式腳本


class Command(BaseCommand, 程式腳本):
    help = '照kaldi格式匯出語料'

    def add_arguments(self, parser):
        parser.add_argument(
            '語言',
            type=str,
            help='選擇語料的語言'
        )
        parser.add_argument(
            '原本資料',
            type=str,
            help='原本文本的train資料夾'
        )
        parser.add_argument(
            '結果資料夾',
            type=str,
            help='新文本的train資料夾'
        )

    def handle(self, *args, **參數):
        服務設定 = settings.HOK8_BU7_SIAT4_TING7[參數['語言']]
        新文本 = Kaldi語料處理.轉音節text格式(
            服務設定['音標系統'],
            self._讀檔案(join(參數['原本資料'], 'text'))
        )
        if isdir(參數['結果資料夾']):
            rmtree(參數['結果資料夾'])
        makedirs(參數['結果資料夾'])
        self._陣列寫入檔案(
            join(參數['結果資料夾'], 'text'),
            新文本
        )
        for 檔名 in [
            'segments',
            'spk2utt',
            'utt2spk',
            'wav.scp',
            'reco2file_and_channel',
            'feats.scp',
            'cmvn.scp',
        ]:
            原檔 = join(參數['原本資料'], 檔名)
            if isfile(原檔):
                copyfile(原檔, join(參數['結果資料夾'], 檔名))
