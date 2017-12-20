import json

from django.db import models


from 臺灣言語資料庫.資料模型 import 影音表
from 臺灣言語資料庫.資料模型 import 聽拍表
from 臺灣言語服務.models檢查 import 檢查敢是分詞
from 臺灣言語服務.models檢查 import 檢查敢是影音檔案
from os.path import abspath
from django.core.exceptions import ValidationError


class 訓練過渡格式(models.Model):
    來源 = models.CharField(max_length=100, db_index=True)
    年代 = models.CharField(max_length=30, db_index=True)
    種類 = models.CharField(
        max_length=100, db_index=True,
        choices=[('字詞', '字詞'), ('語句', '語句'), ],
    )

    影音所在 = models.FilePathField(
        null=True, blank=True,
        max_length=200, validators=[檢查敢是影音檔案]
    )
    影音語者 = models.CharField(blank=True, max_length=100)
    文本 = models.TextField(blank=True, validators=[檢查敢是分詞])
    聽拍 = models.TextField(blank=True)
    外語 = models.TextField(blank=True, validators=[檢查敢是分詞])

    def 編號(self):
        return self.pk

    @classmethod
    def 資料數量(cls):
        return cls.objects.all().count()

    def 聽拍內容(self):
        return json.loads(self.聽拍資料)

    def clean(self):
        super().clean()
        if self.影音所在 != None:
            self.影音所在 = abspath(self.影音所在)
            檢查敢是影音檔案(self.影音所在)
        if self.影音語者 and not self.影音所在:
            raise ValidationError('有指令語者，煞無影音')


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
