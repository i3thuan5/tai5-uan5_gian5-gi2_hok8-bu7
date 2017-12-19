# -*- coding: utf-8 -*-
import json

from django.db import models


class 資料表(models.Model):

    來源 = models.CharField(max_length=100)
    種類 = models.CharField(max_length=100)
    著作年 = models.CharField(max_length=20)  # 1952、19xx、…

    外語資料 = models.TextField(blank=True)
    影音資料 = models.FileField(blank=True)
    影音所在 = models.FileField(blank=True)
    影音語者 = models.CharField(max_length=100)

    分詞資料 = models.TextField(blank=True)

    #     語者詳細資料記佇屬性內底，逐句話記是佗一个語者
    聽拍資料 = models.TextField()  # 存json.dumps的資料

    def 編號(self):
        return self.pk

    @classmethod
    def 資料數量(cls):
        return cls.objects.all().count()

    def 聽拍內容(self):
        return json.loads(self.聽拍資料)
