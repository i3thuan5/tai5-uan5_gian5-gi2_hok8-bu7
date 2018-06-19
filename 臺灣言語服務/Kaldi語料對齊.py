from os import makedirs
from os.path import join, basename
import tarfile
from tempfile import TemporaryDirectory

from django.conf import settings
from django.core.files.base import File
from django.db.models.query_utils import Q
from django.utils import timezone


from 臺灣言語服務.Kaldi語料匯出 import Kaldi語料匯出
from 臺灣言語工具.系統整合.程式腳本 import 程式腳本
from 臺灣言語服務.models import Kaldi對齊結果
from 臺灣言語服務.models import 訓練過渡格式
from 臺灣言語服務.kaldi.lexicon import 辭典輸出


class Kaldi語料對齊(Kaldi對齊結果):
    class Meta:
        proxy = True

    @classmethod
    def 匯入音檔(cls, 語言, 啥人唸的, 聲音檔, 內容):
        語料對齊 = cls.準備辨識(語言, 聲音檔)
        語料對齊.欲切開的聽拍 = 內容
        語料對齊.save()
        return 語料對齊

    def 對齊(self):
        try:
            ctm資料 = self.對齊音檔()
        except OSError:
            self.對齊失敗()
            raise
        self.對齊成功(ctm資料)
        self.做出切音結果()

    def 對齊音檔(self):
        try:
            指定目錄 = join(settings.BASE_DIR, settings.KALDI_KUE3_TING5)
            return self._對齊音檔指定資料夾(指定目錄)
        except AttributeError:
            with TemporaryDirectory() as 暫存目錄:
                return self._對齊音檔指定資料夾(暫存目錄)

    def _對齊音檔指定資料夾(self, 暫存目錄):
        服務設定 = settings.HOK8_BU7_SIAT4_TING7[self.語言]

        對齊設定 = 服務設定['辨識設定']
        kaldi_eg目錄 = 對齊設定['腳本資料夾']

        過渡格式 = 訓練過渡格式.objects.create(
            來源='使用者',
            種類='語句',
            年代=str(timezone.now().year),
            影音所在=self.影音所在(),
            文本=self.欲切開的聽拍,
        )

        辭典資料 = Kaldi語料匯出.初使化辭典資料()
        Kaldi語料匯出.匯出一種語言語料(
            self.語言, 辭典輸出(服務設定['音標系統'], '拆做音素'),  # 音素愛改
            暫存目錄, self.編號名(), 辭典資料,
            Q(pk=過渡格式.id)
        )
        Kaldi語料匯出.匯出辭典資料(辭典資料, 暫存目錄, self.編號名())

        模型目錄 = join(kaldi_eg目錄, 'exp', 對齊設定['模型資料夾'])
        資料目錄 = join(kaldi_eg目錄, 對齊設定['語料資料夾'], 'local', 'dict')
        對齊語料目錄 = join(暫存目錄, self.編號名())
        with 程式腳本._換目錄(kaldi_eg目錄):
            程式腳本._走指令([
                'bash', '-x',
                '對齊音檔.sh',
                資料目錄,
                模型目錄,
                對齊語料目錄,
            ], 愛直接顯示輸出=True)
        結果目錄 = join(對齊語料目錄, 'ali')
        對齊文本檔案 = join(結果目錄, 'ctm')
        對齊文本 = []
        for 一詞 in 程式腳本._讀檔案(對齊文本檔案):
            _檔名, _頻道, 開始時間, 長度, 分詞 = 一詞.split()
            對齊文本.append(
                {'開始': float(開始時間), '長度': float(長度), '分詞': 分詞}
            )
        return 對齊文本

    def 對齊成功(self, ctm時間):
        self.對齊好猶未 = True
        self.對齊出問題 = False

        聽拍資料 = []
        ctm所在 = 0
        for 一段 in self.欲切開的聽拍.split('\n'):
            if len(一段.strip()) == 0:
                continue
            這段長度 = len(一段.split())
            這段資訊 = ctm時間[ctm所在:ctm所在 + 這段長度]
            聽拍資料.append(
                {
                    '語者': '媠媠',
                    '內容': 一段,
                    '開始時間': 這段資訊[0]['開始'],
                    '結束時間': 這段資訊[-1]['開始'] + 這段資訊[-1]['長度'],
                }
            )
            ctm所在 += 這段長度
        self.切好的聽拍 = 聽拍資料
        self.save()

    def 對齊失敗(self):
        self.對齊好猶未 = True
        self.對齊出問題 = True
        self.save()

    def 做出切音結果(self):
        with TemporaryDirectory() as 暫存資料夾路徑:
            wav路徑 = join(暫存資料夾路徑, '切好的音檔')
            self.產生音檔(wav路徑)
            tar路徑 = join(暫存資料夾路徑, '切好的音檔.tar')
            self.壓縮音檔(wav路徑, tar路徑)
            self.存壓縮檔(tar路徑)

    def 產生音檔(self, wav資料夾路徑):
        makedirs(wav資料夾路徑, exist_ok=True)
        音檔 = self.聲音檔()
        for 第幾段, 一段 in enumerate(self.切好的聽拍, start=1):
            這段音檔 = 音檔.照秒數切出音檔(一段['開始時間'], 一段['結束時間'])
            音檔路徑 = join(wav資料夾路徑, '{}.wav'.format(第幾段))
            with open(音檔路徑, 'wb') as 檔案:
                檔案.write(這段音檔.wav格式資料())

    def 壓縮音檔(self, wav資料夾路徑, tar路徑):
        with tarfile.open(tar路徑, "w:gz") as tar檔案:
            tar檔案.add(wav資料夾路徑, arcname=basename(wav資料夾路徑))

    def 存壓縮檔(self, tar路徑):
        with open(tar路徑, 'rb') as tar檔案:
            self.壓縮檔.save(
                name='壓縮檔{0}.tar.gz'.format(self.編號名()),
                content=File(tar檔案),
                save=True
            )
