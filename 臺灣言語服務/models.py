from django.db import models
from django.utils import timezone
from 臺灣言語資料庫.資料模型 import 影音表
from 臺灣言語資料庫.資料模型 import 來源表
from 臺灣言語資料庫.資料模型 import 版權表


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
    欲切開的文本 = models.TextField()

    @classmethod
    def 準備對齊(cls, 影音, 欲切開的文本):
        return cls.objects.create(影音=影音, 欲切開的文本=欲切開的文本)

    def 對齊成功(self, ctm時間):
        self.對齊好猶未 = True
        self.對齊出問題 = False
        self.save()
        影音 = self.影音
        公家內容 = {
            '收錄者': 來源表.objects.get_or_create(名='系統管理員')[0].編號(),
            '來源': 來源表.objects.get_or_create(名='系統管理員')[0].編號(),
            '版權': 版權表.objects.get_or_create(版權='會使公開')[0].pk,
            '種類': '語句',
            '語言腔口': 影音.語言腔口.語言腔口,
            '著作所在地': '臺灣',
            '著作年': str(timezone.now().year),
        }

        聽拍資料 = [
        ]
        ctm所在 = 0
        for 一段 in self.欲切開的文本.split('\n'):
            這段長度 = len(一段.split())
            這段資訊=ctm時間[ctm所在:ctm所在 + 這段長度]
            聽拍資料.append(
                {
                    '語者': '媠媠',
                    '內容': 一段,
                    '開始時間': 這段資訊[0]['開始'],
                    '結束時間': 這段資訊[-1]['開始']+這段資訊[-1]['長度'],
                }
            )
            ctm所在 = +這段長度
        聽拍內容 = {'聽拍資料': 聽拍資料}
        聽拍內容.update(公家內容)
        影音.寫聽拍(聽拍內容)

    def 對齊失敗(self):
        self.對齊好猶未 = True
        self.對齊出問題 = True
        self.save()
