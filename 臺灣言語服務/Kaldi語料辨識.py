
from base64 import b64decode
import io
import json
from os.path import join

from django.conf import settings
from django.core.files.base import ContentFile
from django.db import transaction
from django.db.models.aggregates import Max
from django.db.models.query_utils import Q
from django.forms.models import model_to_dict
from django.http.response import JsonResponse
from django.utils import timezone
from django.views import View


from 臺灣言語資料庫.資料模型 import 來源表
from 臺灣言語資料庫.資料模型 import 版權表
from 臺灣言語資料庫.資料模型 import 影音表
from 臺灣言語服務.Kaldi語料匯出 import Kaldi語料匯出
from 臺灣言語工具.系統整合.程式腳本 import 程式腳本
from 臺灣言語工具.解析整理.拆文分析器 import 拆文分析器


def post(self, request):
    啥人唸的 = request.POST['啥人唸的'].strip()
    編號 = request.POST['編號']
    資料陣列 = bytes(json.loads(
        '[' + b64decode(request.POST['blob']).decode('utf-8') + ']'
    ))
    with transaction.atomic():
        例句音檔 = 例句音檔表.objects.create(
            啥人唸的=啥人唸的,
            例句=例句表.objects.get(pk=編號),
        )
        例句音檔.音檔.save(
            '錄音檔-{}-{}.wav'.format(啥人唸的, 編號),
            ContentFile(資料陣列)
        )

    return self.揣後一筆(啥人唸的)


class Kaldi語料辨識(View):

    @classmethod
    def 匯入音檔(cls, 語言, 聲音檔):
        公家內容 = {
            '收錄者': 來源表.objects.get_or_create(名='系統管理員')[0].編號(),
            '來源': 來源表.objects.get_or_create(名='系統管理員')[0].編號(),
            '版權': 版權表.objects.get_or_create(版權='會使公開')[0].pk,
            '種類': '語句',
            '語言腔口': 語言,
            '著作所在地': '臺灣',
            '著作年': str(timezone.now().year),
        }
        音檔 = io.BytesIO(聲音檔.wav格式資料())
        影音內容 = {'影音資料': 音檔}
        影音內容.update(公家內容)
        影音 = 影音表.加資料(影音內容)
        聽拍資料 = [
            {
                '語者': '無註明',
                '內容': '',
                '開始時間': 0,
                '結束時間': 聲音檔.時間長度()
            }
        ]
        聽拍內容 = {'聽拍資料': 聽拍資料}
        聽拍內容.update(公家內容)
        影音.寫聽拍(聽拍內容)
        return 影音

    @classmethod
    def 辨識音檔(cls, 影音):
        語言 = 影音.語言腔口.語言腔口
        服務設定 = settings.HOK8_BU7_SIAT4_TING7[語言]

        kaldi_eg目錄 = '/home/Ihc/git/kaldi/egs/taiwanese/s5c'
        影音編號 = 影音.編號()

        編號字串 = '{0:07}'.format(影音編號)
        暫存目錄 = join(settings.BASE_DIR, 'kaldi資料')

        Kaldi語料匯出.匯出一種語言語料(
            語言, 服務設定['音標系統'], True,
            暫存目錄, 編號字串, Kaldi語料匯出.初使化辭典資料(),
            Q(pk=影音編號)
        )
        模型目錄 = join(kaldi_eg目錄, 'exp', 'tri5.2')
        路徑目錄 = join(模型目錄, 'graph_format_lm')
        資料目錄 = join(暫存目錄, 編號字串, 'train')
        結果目錄 = join(模型目錄, 'decode_hok8bu7_{}'.format(編號字串))
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
        return 拆文分析器.分詞章物件(' '.join(辨識文本[-1].split(' ')[1:]))
