from 文章.對語料庫網站掠資料落來 import 對語料庫網站掠資料落來
from 臺灣言語工具.系統整合.程式腳本 import 程式腳本

import os


from 臺灣言語工具.解析整理.拆文分析器 import 拆文分析器
from 臺灣言語工具.解析整理.物件譀鏡 import 物件譀鏡
class 臺華新聞做語料(程式腳本):
	def 做(self):
		華=[]
		閩=[]
		掠資料落來 = 對語料庫網站掠資料落來()
# 	{'文號':文章.pk, '日期':str(文章.上尾修改時間),
#         '華語':國語, '閩南語':閩南語})
		分析器=拆文分析器()
		譀鏡=物件譀鏡()
		for 資料 in 掠資料落來.掠資料():
			章物件=分析器.轉做章物件(資料['華語'])
			for 句物件 in 章物件.內底句:
				華.append(譀鏡.看分詞(句物件))
			閩.append(資料['閩南語'])
		
		self.這馬目錄 = os.path.dirname(os.path.abspath(__file__))
		資料目錄 = os.path.join(self.這馬目錄, '翻譯語料')
		self._字串寫入檔案(os.path.join(資料目錄, '華.gz'), '\n'.join(華))
		self._字串寫入檔案(os.path.join(資料目錄, '閩.gz'), '\n'.join(閩))

if __name__ == '__main__':
	臺華新聞做語料().做()