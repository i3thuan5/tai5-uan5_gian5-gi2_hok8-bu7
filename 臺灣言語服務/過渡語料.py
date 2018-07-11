from 臺灣言語服務.models import 訓練過渡格式
from 臺灣言語工具.解析整理.拆文分析器 import 拆文分析器
from 臺灣言語工具.斷詞.國教院斷詞用戶端 import 國教院斷詞用戶端


class 過渡語料處理(訓練過渡格式):
    class Meta:
        proxy = True

    @classmethod
    def 外文用國教院斷詞(cls):
        幾逝 = 0
        for 一逝 in cls.objects.filter(外文__isnull=False):
            句物件 = 拆文分析器.分詞句物件(一逝.外文)
            一逝.外文 = 國教院斷詞用戶端.斷詞(句物件).看分詞()
            一逝.save()
            幾逝 += 1
        return 幾逝
