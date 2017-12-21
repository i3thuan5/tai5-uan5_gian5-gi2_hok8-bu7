from os.path import abspath

from django.core.exceptions import ValidationError
from django.db import models

from jsonfield.fields import JSONField


from 臺灣言語資料庫.資料模型 import 影音表
from 臺灣言語資料庫.資料模型 import 聽拍表
from 臺灣言語服務.models檢查 import 檢查敢是分詞
from 臺灣言語服務.models檢查 import 檢查敢是影音檔案
from 臺灣言語服務.models檢查 import 檢查聽拍內底欄位敢有夠
from 臺灣言語服務.models檢查 import 檢查敢是wav
from 臺灣言語工具.語音辨識.聲音檔 import 聲音檔
from 臺灣言語服務.models檢查 import 檢查聽拍結束時間有超過音檔無


class 訓練過渡格式(models.Model):
    來源 = models.CharField(max_length=100, db_index=True)
    年代 = models.CharField(max_length=30, db_index=True)
    種類 = models.CharField(
        max_length=100, db_index=True,
        choices=[('字詞', '字詞'), ('語句', '語句'), ],
    )

    影音所在 = models.FilePathField(
        null=True, blank=True,
        max_length=200, validators=[檢查敢是影音檔案, 檢查敢是wav]
    )
    影音語者 = models.CharField(blank=True, max_length=100)
    文本 = models.TextField(null=True, blank=True, validators=[檢查敢是分詞])
    聽拍 = JSONField(null=True, blank=True, validators=[檢查聽拍內底欄位敢有夠])
    外文 = models.TextField(null=True, blank=True, validators=[檢查敢是分詞])

    def 編號(self):
        return self.pk

    @classmethod
    def 資料數量(cls):
        return cls.objects.all().count()

    def 聲音檔(self):
        return 聲音檔.對檔案讀(self.影音所在)

    def clean(self):
        super().clean()
        if self.影音所在 is not None:
            self.影音所在 = abspath(self.影音所在)
            檢查敢是影音檔案(self.影音所在)
            if self.聽拍:
                檢查聽拍結束時間有超過音檔無(self.聲音檔().時間長度(), self.聽拍)
        else:
            if self.影音語者:
                raise ValidationError('有指定語者，煞無影音')
            if self.聽拍:
                raise ValidationError('有聽拍，煞無影音')


class Kaldi辨識結果(models.Model):
    影音 = models.OneToOneField(影音表, related_name='Kaldi辨識結果')
    辨識好猶未 = models.BooleanField(default=False)
    辨識出問題 = models.BooleanField(default=False)
    分詞 = models.TextField(blank=True)

    @classmethod
    def 準備辨識(cls, 影音):
        return cls.objects.create(影音=影音)

    def 辨識成功(self, 分詞):
        self.辨識好猶未 = True
        self.辨識出問題 = False
        self.分詞 = 分詞
        self.save()

    def 辨識失敗(self):
        self.辨識好猶未 = True
        self.辨識出問題 = True
        self.save()


class Kaldi對齊結果(models.Model):
    影音 = models.OneToOneField(影音表, related_name='Kaldi對齊結果')
    對齊好猶未 = models.BooleanField(default=False)
    對齊出問題 = models.BooleanField(default=False)
    欲切開的聽拍 = models.OneToOneField(聽拍表, related_name='+')
    切好的聽拍 = models.OneToOneField(聽拍表, null=True, related_name='+')
    壓縮檔 = models.FileField(blank=True)
