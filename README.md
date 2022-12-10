# Genshin-artifacter-scoring
画像を読み取ってスコアリング


## 必須 required
- https://github.com/UB-Mannheim/tesseract/wiki/

↑ just for me

```py
import re
import io
import pyocr
import discord
import requests
from PIL import Image
from discord.ext import commands

pyocr.tesseract.TESSERACT_CMD = r'C:\\Users\\{UserName}\\AppData\\Local\\Tesseract-OCR\\tesseract.exe'
```


### これいいよ
- https://youtu.be/BqyJt1wCN_0 【Python】便利OCRツール作成！画像を一瞬でテキスト化！！業務で即役立つ！
- https://qiita.com/ku_a_i/items/93fdbd75edacb34ec610 【Tesseract】Pythonで簡単に日本語OCRimport os


## 使い方 Usage 1
![USAGE IMAGE_1](doc/ezgif-3-325a06454c.gif)

## 使い方 Usage 2
![USAGE IMAGE_2](doc/ezgif-3-926a3f520e.gif)



[option] 1 ~ 5
1. 汎用型
2. 元素チャージ型
3. 防御型
4. HP型
5. 熟知型


[計算式]
1. 攻撃力 + (会心率 * 2) + 会心ダメージ 
2. (元素チャージ効率 * 0.4) + (会心率 * 2) + 会心ダメージ
3. 防御力 + (会心率 * 2) + 会心ダメージ 
4. HP + (会心率 * 2) + 会心ダメージ 
5. (元素熟知 // 2) + 会心率 + (会心ダメージ // 2)


