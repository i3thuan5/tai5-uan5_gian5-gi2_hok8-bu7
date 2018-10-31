from base64 import b64decode
import json
from subprocess import Popen, PIPE
import wave

from celery import shared_task
from django.conf import settings
from django.http.response import HttpResponse, JsonResponse,\
    HttpResponseBadRequest
from django.utils.datastructures import MultiValueDictKeyError
from django.views.decorators.csrf import csrf_exempt
from libavwrapper.avconv import Input, Output, AVConv
from libavwrapper.codec import AudioCodec, NO_VIDEO


from 臺灣言語服務.Kaldi語料辨識 import Kaldi語料辨識
from 臺灣言語工具.語音辨識.聲音檔 import 聲音檔
from 臺灣言語工具.解析整理.拆文分析器 import 拆文分析器
from 臺灣言語服務.Kaldi語料對齊 import Kaldi語料對齊
from 臺灣言語服務.models import Kaldi對齊結果
from 臺灣言語服務.KaldiModels import Kaldi辨識結果


def Kaldi介面處理(參數無夠):
    def 設定顯示資訊的函式(介面函式):
        def 新函式(*陣列, **辭典):
            try:
                return 介面函式(*陣列, **辭典)
            except MultiValueDictKeyError:
                return HttpResponseBadRequest(參數無夠)
            except EOFError:
                return HttpResponseBadRequest(
                    '「blob」抑是「音檔」比RIFF檔頭閣較短！！'
                )
        return 新函式
    return 設定顯示資訊的函式


@csrf_exempt
def 看辨識結果(request):
    try:
        數量 = int(request.GET['數量'])
    except MultiValueDictKeyError:
        數量 = 300
    結果 = []
    for 辨識結果 in (
        Kaldi辨識結果.objects
        .order_by('-pk')[:數量]
    ):
        這筆 = {
            '編號': 辨識結果.id,
            '網址': 辨識結果.影音.url,
            '語言': 辨識結果.語言,
        }
        if not 辨識結果.辨識好猶未:
            這筆['狀態'] = '辨識中…'
        elif 辨識結果.辨識出問題:
            這筆['狀態'] = '辨識出問題'
        else:
            這筆['狀態'] = '成功'
            這筆['分詞'] = 辨識結果.分詞

            服務設定 = settings.HOK8_BU7_SIAT4_TING7[辨識結果.語言]
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
@Kaldi介面處理(參數無夠='設定「語言」參數以外，閣愛傳「blob」抑是「音檔」！！')
def Kaldi辨識(request):
    try:
        啥人唸的 = request.POST['啥人唸的'].strip()
    except MultiValueDictKeyError:
        啥人唸的 = '無註明'
    Kaldi辨識 = Kaldi語料辨識.匯入音檔(
        request.POST['語言'], 啥人唸的, 音檔參數.揣音檔出來(request), ''
    )
    Kaldi辨識影音.delay(Kaldi辨識.id)
    return HttpResponse('上傳成功！！')


@shared_task
def Kaldi辨識影音(Kaldi辨識編號):
    Kaldi語料辨識.objects.get(pk=Kaldi辨識編號).辨識()


@csrf_exempt
def 看對齊結果(request):
    try:
        數量 = int(request.GET['數量'])
    except MultiValueDictKeyError:
        數量 = 300
    結果 = []
    for 對齊結果 in (
        Kaldi對齊結果.objects
        .order_by('-pk')[:數量]
    ):
        這筆 = {
            '編號': 對齊結果.pk,
            '原始wav檔網址': 對齊結果.影音.url,
            '分詞文本': 對齊結果.欲切開的聽拍,
            '語言': 對齊結果.語言,
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


@csrf_exempt
@Kaldi介面處理(參數無夠='設定「語言」參數以外，閣愛傳「文本」佮「blob」抑是「音檔」！！')
def Kaldi對齊(request):
    語言 = request.POST['語言']
    文本 = request.POST['文本']
    語料對齊 = Kaldi語料對齊.匯入音檔(
        語言, '無註明',
        音檔參數.揣音檔出來(request),
        文本.replace('\r\n', '\n').replace('\r', '\n')
    )
    Kaldi對齊影音.delay(語料對齊.pk)
    return HttpResponse('上傳成功！！')


@shared_task
def Kaldi對齊影音(對齊編號):
    Kaldi語料對齊.objects.get(pk=對齊編號).對齊()


class 音檔參數:
    @classmethod
    def 揣音檔出來(cls, request):
        音檔字串 = cls._揣音檔字串出來(request)
        try:
            return 聲音檔.對資料轉(音檔字串)
        except wave.Error:
            return 聲音檔.對資料轉(cls._轉做wav檔(音檔字串))

    @classmethod
    def _揣音檔字串出來(cls, request):
        try:
            return request.FILES['音檔'].read()
        except MultiValueDictKeyError:
            pass
        return cls._blob2bytes(request.POST['blob'])

    @classmethod
    def _轉做wav檔(cls, 音檔字串):
        wav聲音格式 = AudioCodec('pcm_s16le')
        輸入 = Input('pipe:')
        輸出 = Output('pipe:')
        指令 = AVConv(
            'avconv', ('-loglevel', 'panic'),
            輸入,
            ('-f', 'wav'), wav聲音格式, NO_VIDEO, 輸出
        )
        程序 = Popen(list(指令), stdin=PIPE, stdout=PIPE,)
        結果, _錯誤 = 程序.communicate(input=音檔字串)
        return 結果

    @classmethod
    def _blob2bytes(cls, blob):
        return bytes(json.loads(
            '[' + b64decode(blob).decode('utf-8') + ']'
        ))
