from 臺灣言語服務.models import 訓練過渡格式
from 臺灣言語工具.解析整理.拆文分析器 import 拆文分析器
from 臺灣言語工具.斷詞.國教院斷詞用戶端 import 國教院斷詞用戶端
from itertools import chain
from os.path import join
from tempfile import TemporaryDirectory
from 臺灣言語工具.語言模型.KenLM語言模型訓練 import KenLM語言模型訓練
from 臺灣言語工具.語言模型.KenLM語言模型 import KenLM語言模型
from 臺灣言語工具.辭典.型音辭典 import 型音辭典
from 臺灣言語工具.斷詞.拄好長度辭典揣詞 import 拄好長度辭典揣詞
from 臺灣言語工具.斷詞.語言模型揀集內組 import 語言模型揀集內組
from 臺灣言語工具.基本物件.公用變數 import 無音


class 過渡語料處理(訓練過渡格式):
    class Meta:
        proxy = True

    @classmethod
    def 台文語料斷詞(cls, 會當參考的來源, 欲斷詞的來源, 辭典詞長=4, 連紲詞長度=3):
        無出現的來源 = []
        for 來源 in chain(會當參考的來源, 欲斷詞的來源):
            if not cls.objects.filter(來源=來源).exists():
                無出現的來源.append(來源)
        if len(無出現的來源) > 0:
            raise ValueError('{} 的來源無資料!!'.format('、'.join(無出現的來源)))
        全部詞 = set()
        with TemporaryDirectory() as 暫時:
            全部資料暫時所在 = join(暫時, '全部資料.txt')
            with open(全部資料暫時所在, 'w') as 全部資料暫時檔案:
                for 一逝 in cls.objects.filter(
                    來源__in=會當參考的來源, 文本__isnull=False
                ):
                    for 詞物件 in 拆文分析器.分詞句物件(一逝.文本).網出詞物件():
                        全部詞.add(詞物件)

                    print(一逝.文本, file=全部資料暫時檔案)
            語言模型檔 = KenLM語言模型訓練().訓練(
                [全部資料暫時所在], 暫存資料夾=暫時, 連紲詞長度=連紲詞長度
            )
            語言模型 = KenLM語言模型(語言模型檔)
        辭典 = 型音辭典(辭典詞長)
        for 詞物件 in 全部詞:
            辭典.加詞(詞物件)

        幾逝 = 0
        for 一逝 in cls.objects.filter(
            來源__in=欲斷詞的來源, 文本__isnull=False
        ):
            標好句物件 = (
                拆文分析器.分詞句物件(一逝.文本)
                .揣詞(拄好長度辭典揣詞, 辭典)
                .揀(語言模型揀集內組, 語言模型)
            )
            for 字物件 in 標好句物件.篩出字物件():
                if 字物件.音 == 無音:
                    字物件.音 = 字物件.型
            一逝.文本 = 標好句物件.看分詞()
            一逝.save()
            幾逝 += 1
        return 幾逝

    @classmethod
    def 外文用國教院斷詞(cls):
        幾逝 = 0
        for 一逝 in cls.objects.filter(外文__isnull=False):
            句物件 = 拆文分析器.分詞句物件(一逝.外文)
            一逝.外文 = 國教院斷詞用戶端.斷詞(句物件).看分詞()
            一逝.save()
            幾逝 += 1
        return 幾逝
