from os.path import abspath, join

from django.conf import settings
from django.core.files.base import ContentFile
from django.db import models
from jsonfield.fields import JSONField
from 臺灣言語服務.models檢查 import 檢查聽拍內底欄位敢有夠
from 臺灣言語工具.語音辨識.聲音檔 import 聲音檔


class 影音檔案欄位(models.Model):
    class Meta:
        abstract = True

    影音 = models.FileField(blank=True)
    語言 = models.CharField(blank=True, max_length=50)

    @classmethod
    def 準備辨識(cls, 語言, 音檔):
        return cls.objects.create(語言=語言).存影音資料(音檔)

    def 聲音檔(self):
        return 聲音檔.對檔案讀(self.影音所在())

    def 影音所在(self):
        return join(abspath(settings.MEDIA_ROOT), self.影音.name)

    def 存影音資料(self, 音檔):
        self.影音.save(
            name=self.編號名(),
            content=ContentFile(音檔.wav格式資料()),
            save=True,
        )
        return self

    def 編號名(self):
        return '{0}_{1:04}'.format(self.名, self.id)


class Kaldi辨識結果(影音檔案欄位):
    名 = 'Kaldi辨識'
    辨識好猶未 = models.BooleanField(default=False)
    辨識出問題 = models.BooleanField(default=False)
    分詞 = models.TextField(blank=True)


class Kaldi對齊結果(影音檔案欄位):
    名 = 'Kaldi對齊'
    對齊好猶未 = models.BooleanField(default=False)
    對齊出問題 = models.BooleanField(default=False)
    欲切開的聽拍 = models.TextField()
    切好的聽拍 = JSONField(null=True, blank=True, validators=[檢查聽拍內底欄位敢有夠])
    壓縮檔 = models.FileField(blank=True)
