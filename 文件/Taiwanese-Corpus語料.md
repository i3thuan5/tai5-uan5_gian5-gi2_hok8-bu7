# Taiwanese-Corpus語料

目前專案都放在[Taiwanese-Corpus](https://github.com/Taiwanese-Corpus)。

各專案詳細內容請洽各專案README。

若對匯入細節有興趣，可以參考`臺灣語言資料庫`的[資料匯入](http://sih4sing5hong5.github.io/tai5-uan5_gian5-gi2_tsu1-liau7-khoo3/%E8%B3%87%E6%96%99%E5%8C%AF%E5%85%A5.html)。

## 全部匯入
提供一個方便匯入的指令，不過匯入相當耗時。建議可以邊匯入，邊編譯安裝環境時的moses
```bash
python manage.py migrate
python manage.py 匯入資料 \
https://Taiwanese-Corpus.github.io/moedict-data-twblg/轉到臺灣言語資料庫/資料/xls整理.yaml \
https://Taiwanese-Corpus.github.io/moedict-data-twblg/轉到臺灣言語資料庫/資料/異用字.yaml \
https://Taiwanese-Corpus.github.io/moe_minkalaok/閩南語卡拉OK正字字表.yaml \
https://Taiwanese-Corpus.github.io/icorpus_ka1_han3-ji7/臺華平行新聞語料庫.yaml \
https://Taiwanese-Corpus.github.io/Linya-Huang_2014_taiwanesecharacters/咱的字你敢捌.yaml \
https://Taiwanese-Corpus.github.io/moedict-data-hakka/臺灣客家語常用詞辭典網路版語料.yaml \
https://Taiwanese-Corpus.github.io/hakka_elearning/臺灣客話詞彙資料庫語料.yaml \
https://Taiwanese-Corpus.github.io/klokah_data_extract/族語E樂園.yaml \
https://Taiwanese-Corpus.github.io/amis-data/dict-amis.yaml
```

## 臺語/閩南語
### [臺灣閩南語常用詞辭典](https://github.com/Taiwanese-Corpus/moedict-data-twblg/tree/gh-pages/%E8%BD%89%E5%88%B0%E8%87%BA%E7%81%A3%E8%A8%80%E8%AA%9E%E8%B3%87%E6%96%99%E5%BA%AB)
```bash
python manage.py 匯入資料 https://Taiwanese-Corpus.github.io/moedict-data-twblg/轉到臺灣言語資料庫/資料/xls整理.yaml https://Taiwanese-Corpus.github.io/moedict-data-twblg/轉到臺灣言語資料庫/資料/異用字.yaml
```

### [臺灣閩南語卡拉OK正字字表](https://github.com/Taiwanese-Corpus/moe_minkalaok)
```bash
python manage.py 匯入資料 https://Taiwanese-Corpus.github.io/moe_minkalaok/閩南語卡拉OK正字字表.yaml
```

### [iCorpus臺華平行新聞語料庫漢字臺羅版](https://github.com/Taiwanese-Corpus/icorpus_ka1_han3-ji7) 
```bash
python manage.py 匯入資料 https://Taiwanese-Corpus.github.io/icorpus_ka1_han3-ji7/臺華平行新聞語料庫.yaml
```

### [咱的字你敢捌－台語漢字](https://github.com/Taiwanese-Corpus/Linya-Huang_2014_taiwanesecharacters)
```bash
python manage.py 匯入資料 https://Taiwanese-Corpus.github.io/Linya-Huang_2014_taiwanesecharacters/咱的字你敢捌.yaml
```

### 猶未整理
遮的語料攏猶未提供臺灣言語資料庫yaml格式，毋過大部份攏好處理。語料專案照處理方法排：
* [台語文數位典藏資料庫](https://github.com/Taiwanese-Corpus/nmtl_dadwt)
  * 純文字、臺灣言語工具分詞
* [台語文語料庫蒐集及語料庫為本台語書面語音節詞頻統計](https://github.com/Taiwanese-Corpus/Ungian_2005_guliau-supin)
  * 純文字
* [荷華文語類參](https://github.com/Taiwanese-Corpus/Schlegel-Gustave_1886_Nederlandsch-Chineesch-Woordenboek)
  * xls
* [厦荷詞典](https://github.com/Taiwanese-Corpus/J.-J.-C.-Francken_C.-F.-M.-de-Grijs_1882_Chineesch-Hollandsch_woordenboek-van-het-Emoi-dialekt)
  * xls
* [駱嘉鵬老師華語臺語客語文件-字典、對應表](https://github.com/Taiwanese-Corpus/Loh_2004_hanyu-document)
  * xls
* [Embree台英辭典](https://github.com/Taiwanese-Corpus/Bernard-L.M.-Embree_1973_A-Dictionary-of-Southern-Min)
  * xls
* [台文/華文線頂辭典](https://github.com/Taiwanese-Corpus/Tinn-liong-ui_2000_taihoa-dictionary)
  * xls
* [教育部臺灣閩南語字詞頻調查工作](https://github.com/Taiwanese-Corpus/Ungian_2009_KIPsupin)
  * 允言整理過的doc、json
* [臺語國校仔課本](https://github.com/Taiwanese-Corpus/kok4hau7-kho3pun2)
  * 允言整理過的doc、json
* [新約聖經語料](https://github.com/Taiwanese-Corpus/Pakhelke-1916_KoTan-1975_hiantaiekpun-2008_tailwanese-bible)
  * 允言整理過的doc、json
* [廈英大辭典](https://github.com/Taiwanese-Corpus/Carstairs-Douglas_1873_chinese-english-dictionary)
  * 未整理的doc
* [台日大辭典台語譯本](https://github.com/Taiwanese-Corpus/Ogawa-Naoyoshi_1931-1932)
  * sql
* [吳守禮《國臺對照活用辭典》電子化](https://github.com/Taiwanese-Corpus/koktai)
  * 專案內，有parser會當轉做jade格式
* [猶未整理的語料](https://github.com/Taiwanese-Corpus/unclassified_corpus)
  * csv、xls…
* [網路語料](https://github.com/Taiwanese-Corpus/internet_corpus)

## 客家話
### [教育部臺灣客家語常用詞辭典](https://github.com/Taiwanese-Corpus/moedict-data-hakka/tree/%E8%BD%89%E5%88%B0%E8%87%BA%E7%81%A3%E8%A8%80%E8%AA%9E%E8%B3%87%E6%96%99%E5%BA%AB/%E8%BD%89%E5%88%B0%E8%87%BA%E7%81%A3%E8%A8%80%E8%AA%9E%E8%B3%87%E6%96%99%E5%BA%AB)
```bash
python manage.py 匯入資料 https://Taiwanese-Corpus.github.io/moedict-data-hakka/臺灣客家語常用詞辭典網路版語料.yaml
```

### [客語能力認證資料檔](https://github.com/Taiwanese-Corpus/hakka_elearning)
```bash
python manage.py 匯入資料 https://Taiwanese-Corpus.github.io/hakka_elearning/臺灣客話詞彙資料庫語料.yaml
```

## 族語
### [族語E樂園](https://github.com/Taiwanese-Corpus/moedict-data-twblg/tree/gh-pages/%E8%BD%89%E5%88%B0%E8%87%BA%E7%81%A3%E8%A8%80%E8%AA%9E%E8%B3%87%E6%96%99%E5%BA%AB)
```bash
python manage.py 匯入資料 https://Taiwanese-Corpus.github.io/klokah_data_extract/族語E樂園.yaml
```

### [阿美語方敏英字典Virginia Fey's Amis Dictionary](https://github.com/Taiwanese-Corpus/amis-data)
```bash
python manage.py 匯入資料 https://Taiwanese-Corpus.github.io/amis-data/dict-amis.yaml
```

### 猶未整理
* [Dictionnaire Amis-Français](https://github.com/Taiwanese-Corpus/amis-francais)
* [噶哈巫語分類辭典](https://github.com/Taiwanese-Corpus/kaxabu-muwalak-misa-a-ahan-bizu)
