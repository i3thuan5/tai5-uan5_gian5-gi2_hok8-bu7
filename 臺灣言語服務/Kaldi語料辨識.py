from os.path import join
from tempfile import TemporaryDirectory

from django.conf import settings
from django.db.models.query_utils import Q
from django.utils import timezone


from 臺灣言語服務.Kaldi語料匯出 import Kaldi語料匯出
from 臺灣言語工具.系統整合.程式腳本 import 程式腳本
from 臺灣言語工具.解析整理.拆文分析器 import 拆文分析器
from 臺灣言語服務.models import Kaldi辨識結果
from 臺灣言語服務.models import 訓練過渡格式
from 臺灣言語服務.kaldi.lexicon import 辭典輸出


class Kaldi語料辨識(Kaldi辨識結果):
    class Meta:
        proxy = True

    def 辨識成功(self, 分詞):
        self.辨識好猶未 = True
        self.辨識出問題 = False
        self.分詞 = 分詞
        self.save()

    def 辨識失敗(self):
        self.辨識好猶未 = True
        self.辨識出問題 = True
        self.save()

    @classmethod
    def 匯入音檔(cls, 語言, 啥人唸的, 聲音檔, 內容):
        return cls.準備辨識(語言, 聲音檔)

    def 辨識(self):
        try:
            章物件 = self.辨識音檔()
        except OSError:
            self.辨識失敗()
            raise
        else:
            self.辨識成功(章物件.看分詞())

    def 辨識音檔(self):
        try:
            指定目錄 = join(settings.BASE_DIR, settings.KALDI_KUE3_TING5)
            return self._辨識音檔指定資料夾(指定目錄)
        except AttributeError:
            with TemporaryDirectory() as 暫存目錄:
                return self._辨識音檔指定資料夾(暫存目錄)

    def _辨識音檔指定資料夾(self, 暫存目錄):
        服務設定 = settings.HOK8_BU7_SIAT4_TING7[self.語言]

        辨識設定 = 服務設定['辨識設定']
        kaldi_eg目錄 = 辨識設定['腳本資料夾']

        過渡格式 = 訓練過渡格式.objects.create(
            來源='使用者',
            種類='語句',
            年代=str(timezone.now().year),
            影音所在=self.影音所在(),
            文本='kaldi辨識服務',
        )

        Kaldi語料匯出.匯出一種語言語料(
            self.語言, 辭典輸出(服務設定['音標系統'], '拆做音素'),
            暫存目錄, self.編號名(), Kaldi語料匯出.初使化辭典資料(),
            Q(pk=過渡格式.編號())
        )
        模型目錄 = join(kaldi_eg目錄, 'exp', 辨識設定['模型資料夾'])
        路徑目錄 = join(模型目錄, 辨識設定['圖資料夾'])
        重估語言模型目錄 = join(kaldi_eg目錄, 辨識設定['重估語言模型資料夾'])
        資料目錄 = join(暫存目錄, self.編號名(), 'train')
        結果目錄 = join(模型目錄, 'decode_hok8bu7_{}'.format(self.編號名()))
        with 程式腳本._換目錄(kaldi_eg目錄):
            程式腳本._走指令([
                'bash', '-x',
                辨識設定['腳本'],
                路徑目錄,
                重估語言模型目錄,
                資料目錄,
                結果目錄,
            ], 愛直接顯示輸出=True)
        辨識文本檔案 = join(結果目錄, 'scoring', 辨識設定['結果檔名'])
        辨識文本 = 程式腳本._讀檔案(辨識文本檔案)
        return 拆文分析器.分詞章物件(' '.join(辨識文本[-1].split(' ')[1:]))
