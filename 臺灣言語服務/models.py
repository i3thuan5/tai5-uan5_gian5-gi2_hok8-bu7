from django.db import models
from 臺灣言語資料庫.資料模型 import 影音表
from 臺灣言語資料庫.資料模型 import 聽拍表


class 訓練過渡格式(models.Model):
    來源 = models.CharField(max_length=100)
    種類 = models.CharField(max_length=100)
    年代 = models.CharField(max_length=20)

    影音所在 = models.FileField(blank=True)
    影音語者 = models.CharField(blank=True, max_length=100)
    文本 = models.TextField(blank=True)
    聽拍 = models.TextField(blank=True)
    外語 = models.TextField(blank=True)

    def 編號(self):
        return self.pk

    @classmethod
    def 資料數量(cls):
        return cls.objects.all().count()

    def 聽拍內容(self):
        return json.loads(self.聽拍資料)


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
