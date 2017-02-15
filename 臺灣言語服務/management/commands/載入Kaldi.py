from os.path import join

from django.core.management.base import BaseCommand


from 臺灣言語工具.系統整合.程式腳本 import 程式腳本
from django.core.management import call_command
from django.conf import settings
from 臺灣言語工具.解析整理.拆文分析器 import 拆文分析器


class Command(BaseCommand):
    help = '訓練一个語言的HTS模型'

    def add_arguments(self, parser):
        #         parser.add_argument(
        #             '語言',
        #             type=str,
        #             help='愛訓練的語言'
        #         )
        pass

    def handle(self, *args, **參數):
        #             語言 = 參數['語言']
        #             服務設定 = settings.HOK8_BU7_SIAT4_TING7[語言]
        #         Kaldi.辨識('/home/Ihc/git/kaldi/egs/taiwanese/s5c')
        kaldi_eg目錄 = '/home/Ihc/git/kaldi/egs/taiwanese/s5c'
        編號 = '1'
        暫存目錄 = join(settings.BASE_DIR, 'kaldi資料')
        call_command('匯出Kaldi格式資料', '閩南語', 暫存目錄, '--資料夾', 編號, '--輸出試驗音檔')
        模型目錄 = join(kaldi_eg目錄, 'exp/tri5.2')
        路徑目錄 = join(模型目錄, 'graph_format_lm')
        資料目錄 = join(暫存目錄, 編號, 'train')
        結果目錄 = join(模型目錄, 'decode_hok8bu7_{}'.format(編號))
        with 程式腳本._換目錄(kaldi_eg目錄):
            程式腳本._走指令([
                'bash', '-x',
                '服務來試.sh',
                路徑目錄,
                資料目錄,
                結果目錄,
            ], 愛直接顯示輸出=True)
        辨識文本檔案 = join(結果目錄, 'scoring', '15.0.0.txt')
        辨識文本 = 程式腳本._讀檔案(辨識文本檔案)
        章物件 = 拆文分析器.分詞章物件(' '.join(辨識文本[0].split(' ')[1:]))
        print(章物件.看型())
        print(章物件.看音())
