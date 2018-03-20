from base64 import b64decode
import json

from django.conf import settings
from django.http.response import HttpResponse, JsonResponse,\
    HttpResponseBadRequest
from django.utils.datastructures import MultiValueDictKeyError
from django.views.decorators.csrf import csrf_exempt

from celery import shared_task


from 臺灣言語服務.Kaldi語料辨識 import Kaldi語料辨識
from 臺灣言語工具.語音辨識.聲音檔 import 聲音檔
from 臺灣言語資料庫.資料模型 import 影音表
from 臺灣言語工具.解析整理.拆文分析器 import 拆文分析器
from 臺灣言語服務.Kaldi語料對齊 import Kaldi語料對齊
from 臺灣言語服務.models import Kaldi對齊結果


@csrf_exempt
def 看辨識結果(request):
    結果 = []
    for 影音 in (
        影音表.objects
        .filter(Kaldi辨識結果__isnull=False)
        .select_related('Kaldi辨識結果', '語言腔口')
        .order_by('-pk')[:300]
    ):
        這筆 = {
            '編號': 影音.編號(),
            '網址': 影音.影音資料.url,
            '語言': 影音.語言腔口.語言腔口,
        }
        辨識結果 = 影音.Kaldi辨識結果
        if not 辨識結果.辨識好猶未:
            這筆['狀態'] = '辨識中…'
        elif 辨識結果.辨識出問題:
            這筆['狀態'] = '辨識出問題'
        else:
            這筆['狀態'] = '成功'
            這筆['分詞'] = 辨識結果.分詞

            語言 = 影音.語言腔口.語言腔口
            服務設定 = settings.HOK8_BU7_SIAT4_TING7[語言]
            章物件 = 拆文分析器.分詞章物件(辨識結果.分詞)
            try:
                這筆['綜合標音'] = 章物件.綜合標音(服務設定['字綜合標音'])
            except KeyError:
                pass
            try:
                這筆['多元書寫'] = 服務設定['多元書寫'].書寫章(章物件)
            except KeyError:
                pass
        結果.append(這筆)
    return JsonResponse({'辨識結果': 結果})


@csrf_exempt
def Kaldi辨識(request):
    try:
        啥人唸的 = request.POST['啥人唸的'].strip()
    except MultiValueDictKeyError:
        啥人唸的 = '無註明'
    try:
        影音 = Kaldi語料辨識.匯入音檔(request.POST['語言'], 啥人唸的, 揣音檔出來(request), '')
    except MultiValueDictKeyError:
        return HttpResponseBadRequest(
            '設定「語言」參數以外，閣愛傳「blob」抑是「音檔」！！'
        )
    Kaldi辨識影音.delay(影音.編號())
    return HttpResponse('上傳成功！！')


def 揣音檔出來(request):
    try:
        return 聲音檔.對資料轉(request.FILES['音檔'].read())
    except MultiValueDictKeyError:
        pass
    return 聲音檔.對資料轉(blob2bytes(request.POST['blob']))


def blob2bytes(blob):
    return bytes(json.loads(
        '[' + b64decode(blob).decode('utf-8') + ']'
    ))


def 無辨識過的重訓練一擺():
    for 影音 in 影音表.objects.filter(Kaldi辨識結果__辨識好猶未=False):
        _Kaldi辨識影音(影音)
    return JsonResponse({'成功': '成功'})


@shared_task
def Kaldi辨識影音(影音編號):
    _Kaldi辨識影音(影音表.objects.get(pk=影音編號))


def _Kaldi辨識影音(影音):
    try:
        章物件 = Kaldi語料辨識.辨識音檔(影音)
    except OSError:
        影音.Kaldi辨識結果.辨識失敗()
        raise
    else:
        影音.Kaldi辨識結果.辨識成功(章物件.看分詞())


@csrf_exempt
def Kaldi對齊(request):
    語言 = request.POST['語言']
    文本 = request.POST['文本']
    語料對齊 = Kaldi語料對齊.匯入音檔(
        語言, '無註明',
        聲音檔.對資料轉(request.FILES['原始wav檔'].read()),
        文本.replace('\r\n', '\n').replace('\r', '\n')
    )
    Kaldi對齊影音.delay(語料對齊.pk)
    return HttpResponse('上傳成功！！')


@csrf_exempt
def 看對齊結果(request):
    結果 = []
    for 對齊結果 in (
        Kaldi對齊結果.objects
        .filter()
        .select_related('影音__語言腔口', '欲切開的聽拍')
        .order_by('-pk')[:300]
    ):
        這筆 = {
            '編號': 對齊結果.pk,
            '原始wav檔網址': 對齊結果.影音.影音資料.url,
            '分詞文本': 對齊結果.欲切開的聽拍.聽拍內容()[0]['內容'],
            '語言': 對齊結果.影音.語言腔口.語言腔口,
        }
        if not 對齊結果.對齊好猶未:
            這筆['狀態'] = '對齊中…'
        elif 對齊結果.對齊出問題:
            這筆['狀態'] = '對齊出問題'
        elif not 對齊結果.壓縮檔.name:
            這筆['狀態'] = '佇產生壓縮檔…'
        else:
            這筆['狀態'] = '成功'
            這筆['壓縮檔網址'] = 對齊結果.壓縮檔.url

        結果.append(這筆)
    return JsonResponse({'對齊結果': 結果})


@shared_task
def Kaldi對齊影音(對齊編號):
    語料對齊 = Kaldi語料對齊.objects.get(pk=對齊編號)
    語料對齊.對齊音檔()
