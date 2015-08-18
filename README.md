# 臺灣言語服務



## 訓練模型
佇`臺灣言語資料庫`專案
```bash
pip install ...
echo "from 臺灣言語服務.模型訓練 import 模型訓練; 訓練=模型訓練(); 訓練.走()" | python manage.py shell  
```

## 使用方法
先在`settings.py`的`INSTALLED_APPS`加`'臺灣言語服務'`
```bash
python manage.py runserver
```

## 資料、模型路徑
```
資料/
├── 合成模型
│   └── 閩南語
│       └── Taiwanese.htsvoice
├── 翻譯模型
│   └── 閩南語
│       ├── model
│       │   ├── moses.ini
│       │   ├── phrase-table.gz
│       │   └── reordering-table.wbe-msd-bidirectional-fe.gz
│       ├── 母語辭典.txt.gz
│       └── 語言模型.lm
└── 翻譯語料
    └── 閩南語
        ├── 加工語料
        │   ├── 字詞文本.txt.gz
        │   ├── 對齊外語字詞.txt.gz
        │   ├── 對齊外語語句.txt.gz
        │   ├── 對齊母語字詞.txt.gz
        │   ├── 對齊母語語句.txt.gz
        │   └── 語句文本.txt.gz
        ├── 字詞文本.txt.gz
        ├── 對齊外語字詞.txt.gz
        ├── 對齊外語語句.txt.gz
        ├── 對齊母語字詞.txt.gz
        ├── 對齊母語語句.txt.gz
        ├── 語句文本.txt.gz
        └── 語言模型資料夾
            ├── 語言模型.lm
            └── 語言模型.txt
```