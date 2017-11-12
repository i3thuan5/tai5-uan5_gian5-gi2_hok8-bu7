import io
from os import makedirs
from os.path import join, basename
import tarfile

from django.conf import settings
from django.core.files.base import File
from django.db.models.query_utils import Q
from django.utils import timezone


from 臺灣言語資料庫.資料模型 import 來源表
from 臺灣言語資料庫.資料模型 import 版權表
from 臺灣言語資料庫.資料模型 import 影音表
from 臺灣言語服務.Kaldi語料匯出 import Kaldi語料匯出
from 臺灣言語工具.系統整合.程式腳本 import 程式腳本
from 臺灣言語服務.models import Kaldi對齊結果
from tempfile import TemporaryDirectory


class Kaldi語料對齊(Kaldi對齊結果):
    class Meta:
        proxy = True

    @classmethod
    def 匯入音檔(cls, 語言, 啥人唸的, 聲音檔, 內容):
        公家內容 = {
            '收錄者': 來源表.objects.get_or_create(名='系統管理員')[0].編號(),
            '來源': 來源表.objects.get_or_create(名=啥人唸的)[0].編號(),
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
                '語者': 啥人唸的,
                '內容': 內容,
                '開始時間': 0,
                '結束時間': 聲音檔.時間長度()
            }
        ]
        聽拍內容 = {'聽拍資料': 聽拍資料}
        聽拍內容.update(公家內容)
        聽拍 = 影音.寫聽拍(聽拍內容)

        return cls._準備對齊(影音, 聽拍)

    @classmethod
    def _準備對齊(cls, 影音, 聽拍):
        return cls.objects.create(影音=影音, 欲切開的聽拍=聽拍)

    def 對齊音檔(self):
        try:
            ctm資料 = self._對齊()
        except OSError:
            self.對齊失敗()
            raise
        self.對齊成功(ctm資料)
        with TemporaryDirectory() as 暫存資料夾路徑:
            wav路徑 = join(暫存資料夾路徑, '切好的音檔')
            self.產生音檔(wav路徑)
            tar路徑 = join(暫存資料夾路徑, '切好的音檔.tar')
            self.壓縮音檔(wav路徑, tar路徑)
            self.存壓縮檔(tar路徑)

    def _對齊(self):
        語言 = self.影音.語言腔口.語言腔口
        服務設定 = settings.HOK8_BU7_SIAT4_TING7[語言]

        對齊設定 = 服務設定['辨識設定']
        kaldi_eg目錄 = 對齊設定['腳本資料夾']
        影音編號 = self.影音.編號()

        編號字串資料夾名 = '{0:07}'.format(影音編號)
        暫存目錄 = join(settings.BASE_DIR, 'kaldi-data')

        辭典資料 = Kaldi語料匯出.初使化辭典資料()
        Kaldi語料匯出.匯出一種語言語料(
            語言, 服務設定['音標系統'],
            暫存目錄, 編號字串資料夾名, 辭典資料,
            Q(pk=影音編號)
        )
        Kaldi語料匯出.匯出辭典資料(辭典資料, 暫存目錄, 編號字串資料夾名)

        模型目錄 = join(kaldi_eg目錄, 'exp', 對齊設定['模型資料夾'])
        資料目錄 = join(kaldi_eg目錄, 對齊設定['語料資料夾'], 'local', 'dict')
        對齊語料目錄 = join(暫存目錄, 編號字串資料夾名)
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
        self.save()

        公家內容 = {
            '收錄者': 來源表.objects.get_or_create(名='系統管理員')[0].編號(),
            '來源': 來源表.objects.get_or_create(名='系統管理員')[0].編號(),
            '版權': 版權表.objects.get_or_create(版權='會使公開')[0].pk,
            '種類': '語句',
            '語言腔口': self.欲切開的聽拍.語言腔口.語言腔口,
            '著作所在地': '臺灣',
            '著作年': str(timezone.now().year),
        }

        聽拍資料 = [
        ]
        ctm所在 = 0
        for 一段 in self.欲切開的聽拍.聽拍內容()[0]['內容'].split('\n'):
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
        聽拍內容 = {'聽拍資料': 聽拍資料}
        聽拍內容.update(公家內容)
        self.切好的聽拍 = self.欲切開的聽拍.校對做(聽拍內容)
        self.save()

    def 對齊失敗(self):
        self.對齊好猶未 = True
        self.對齊出問題 = True
        self.save()

    def 產生音檔(self, wav資料夾路徑):
        makedirs(wav資料夾路徑, exist_ok=True)
        音檔 = self.影音.聲音檔()
        for 第幾段, 一段 in enumerate(self.切好的聽拍.聽拍內容(), start=1):
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
                name='壓縮檔{0:07}.tar.gz'.format(self.影音.編號()),
                content=File(tar檔案),
                save=True
            )
