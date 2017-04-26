from django.db import models
from 臺灣言語資料庫.資料模型 import 影音表


class Kaldi辨識結果(models.Model):
    影音 = models.OneToOneField(影音表, related_name='Kaldi辨識結果')
    辨識好矣猶未 = models.BooleanField(default=False)
    辨識出問題 = models.BooleanField(default=False)
    分詞 = models.TextField(blank=True)

    @classmethod
    def 準備辨識(cls,影音):
        return cls.objects.create(影音=影音)
    def 辨識好矣(self, 分詞):
        self.辨識好矣猶未 = True
        self.辨識出問題 = False
        self.分詞 = 分詞
        self.save()

    def 辨識失敗(self):
        self.辨識好矣猶未 = True
        self.辨識出問題 = True
        self.save()
