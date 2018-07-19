from os.path import abspath
from sys import stderr

from django.core.exceptions import ValidationError
from django.db import models
from jsonfield.fields import JSONField


from 臺灣言語工具.語音辨識.聲音檔 import 聲音檔
from 臺灣言語服務.KaldiModels import Kaldi對齊結果
from 臺灣言語服務.models檢查 import 檢查敢是wav
from 臺灣言語服務.models檢查 import 檢查敢是分詞
from 臺灣言語服務.models檢查 import 檢查敢是影音檔案
from 臺灣言語服務.models檢查 import 檢查聽拍內底欄位敢有夠
from 臺灣言語服務.models檢查 import 檢查聽拍結束時間有超過音檔無
from 臺灣言語服務.KaldiModels import Kaldi辨識結果


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

    @classmethod
    def 資料數量(cls):
        return cls.objects.all().count()

    @classmethod
    def 加一堆資料(cls, 資料陣列, 錯誤輸出=stderr):
        會使的資料 = []
        for 一筆 in 資料陣列:
            try:
                一筆.full_clean()
            except ValidationError as 錯誤:
                print(錯誤, file=錯誤輸出)
            else:
                會使的資料.append(一筆)
        訓練過渡格式.objects.bulk_create(會使的資料)

    def 編號(self):
        return self.pk

    def 聲音檔(self):
        return 聲音檔.對檔案讀(self.影音所在)

    def clean(self):
        super().clean()
        if self.影音所在 is not None:
            self.影音所在 = abspath(self.影音所在)
            檢查敢是影音檔案(self.影音所在)
            if self.聽拍:
                檢查聽拍結束時間有超過音檔無(self.聲音檔().時間長度(), self.聽拍)
                if self.文本 is not None:
                    raise ValidationError('有聽拍就袂使有文本')
                if self.影音語者 != '':
                    raise ValidationError('有聽拍就袂使有語者')
        else:
            if self.影音語者:
                raise ValidationError('有指定語者，煞無影音')
            if self.聽拍:
                raise ValidationError('有聽拍，煞無影音')


Kaldi辨識結果, Kaldi對齊結果
