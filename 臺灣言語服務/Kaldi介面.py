from base64 import b64decode
import json

from django.http.response import HttpResponse, HttpResponseServerError


from 臺灣言語服務.Kaldi語料辨識 import Kaldi語料辨識
from 臺灣言語工具.語音辨識.聲音檔 import 聲音檔
from 臺灣言語服務.models import Kaldi辨識結果


def Kaldi辨識(self, request):
    try:
        啥人唸的 = request.POST['啥人唸的'].strip()
    except:
        啥人唸的 = '無註明'
    語言 = request.POST['語言']
    資料陣列 = bytes(json.loads(
        '[' + b64decode(request.POST['blob']).decode('utf-8') + ']'
    ))

    影音 = Kaldi語料辨識.匯入音檔(語言, 啥人唸的, 聲音檔.對資料轉(資料陣列))
    try:
        章物件 = Kaldi語料辨識.辨識音檔(影音)
        影音.Kaldi辨識結果 = Kaldi辨識結果(辨識出問題=False, 辨識結果分詞=章物件.看分詞())
        影音.save()
        return HttpResponse()
    except:
        影音.Kaldi辨識結果 = Kaldi辨識結果(辨識出問題=True, 辨識結果分詞='')
        影音.save()
        return HttpResponseServerError()
