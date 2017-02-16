from django.db import models
from 臺灣言語資料庫.資料模型 import 影音表


class Kaldi辨識結果(models.Model):
    影音 = models.OneToOneField(影音表,related_name='Kaldi辨識結果')
    辨識出問題 = models.BooleanField()
    分詞 = models.TextField(blank=True)
