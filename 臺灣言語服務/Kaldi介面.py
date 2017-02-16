from base64 import b64decode
import json


from 臺灣言語服務.Kaldi語料辨識 import Kaldi語料辨識
from 臺灣言語工具.語音辨識.聲音檔 import 聲音檔


def post(self, request):
    try:
        啥人唸的 = request.POST['啥人唸的'].strip()
    except:
        啥人唸的 = '無註明'
    語言 = request.POST['語言']
    資料陣列 = bytes(json.loads(
        '[' + b64decode(request.POST['blob']).decode('utf-8') + ']'
    ))

    影音 = Kaldi語料辨識.匯入音檔(語言, 啥人唸的, 聲音檔.對資料轉(資料陣列))
    章物件 = Kaldi語料辨識.辨識音檔(影音)
    print(章物件)
    return
