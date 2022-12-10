#using pyocr
#https://github.com/UB-Mannheim/tesseract/wiki/
#for Japanese
#https://youtu.be/BqyJt1wCN_0 【Python】便利OCRツール作成！画像を一瞬でテキスト化！！業務で即役立つ！
#https://qiita.com/ku_a_i/items/93fdbd75edacb34ec610 【Tesseract】Pythonで簡単に日本語OCRimport os


import re
import io
import pyocr
import discord
import requests
from PIL import Image
from discord.ext import commands
from decimal import Decimal, ROUND_HALF_EVEN


bot = commands.Bot(command_prefix=",", intents=discord.Intents.all())   

pyocr.tesseract.TESSERACT_CMD = r'C:\\Users\\Ennui\\AppData\\Local\\Tesseract-OCR\\tesseract.exe'
tools = pyocr.get_available_tools();tool = tools[0]


"""For Japanese"""
JP_reg_CRIT  = r"(?<=会心率)\+\d+\.\d"
JP_reg_CRITD = r"(?<=会心ダメージ)\+\d+\.\d"
JP_reg_ATK = r"(?<=攻撃力)\+\d+\.\d" 
JP_reg_DEF = r"(?<=防御力)\+\d+\.\d"
JP_reg_CH = r"(?<=元素チャージ効率)\+\d+\.\d"
JP_reg_HP = r"(?<=HP)\+\d+\.\d"
JP_reg_ELE = r"(?<=元素熟知)\+\d+"


"""For English"""
EN_reg_CRIT  = r"(?<=CRIT RATE)\+\d+\.\d"
EN_reg_CRITD = r"(?<=CRIT DMG)\+\d+\.\d"
EN_reg_ATK = r"(?<=ATK)\+\d+\.\d" 
EN_reg_DEF = r"(?<=DEF)\+\d+\.\d"
EN_reg_CH = r"(?<=Energy Recharge)\+\d+\.\d"
EN_reg_HP = r"(?<=HP)\+\d+\.\d"
EN_reg_ELE = r"(?<=Elemental Burst)\+\d+"


jp_description = """
[option] 1 ~ 5
1: 汎用型
2: 元素チャージ型
3: 防御型
4: HP型
5: 熟知型

計算式
1: 攻撃力 + (会心率 * 2) + 会心ダメージ 
2: (元素チャージ効率 * 0.4) + (会心率 * 2) + 会心ダメージ
3: 防御力 + (会心率 * 2) + 会心ダメージ 
4: HP + (会心率 * 2) + 会心ダメージ 
5: (元素熟知 // 2) + 会心率 + (会心ダメージ // 2)

"""

en_description = """
[option] 1 ~ 5
1: ATK TYPE
2: RECHARGE TYPE
3: DEF TYPE
4: HP TYPE
5: ELEMENTAL TYPE

[Calculations]
1: ATK + (CRIT RATE * 2) + CRIT DMG 
2: (ENERGY RECHAGE * 0.4) + (CRIT RATE * 2) + CRIT DMG
3: DEF + (CRIT RATE * 2) + CRIT DMG 
4: HP + (CRIT RATE * 2) + CRIT DMG 
5: (ELEMENTAL BURST // 2) + CRIT RATE + (CRIT DMG // 2)
"""


@bot.command(name="jp-genshin-artifacter", aliases=["jpn"], description= jp_description)
async def re_genshin_artifacter(ctx, option=1):
    r = requests.get(ctx.message.attachments[0].url)

    msg = await ctx.reply("Please wait a moment.<a:Loading_2:1007527284753834014>")
    Image.open(io.BytesIO(r.content)).convert("L").save("image/image.png")
    builder = pyocr.builders.TextBuilder(tesseract_layout=3)
    text = tool.image_to_string(Image.open("image/image.png"), lang="jpn", builder=builder)

    if re.search(r"[\.|\*|\_|\。|]", text):
        text = str(text).translate(str.maketrans({"。":"", "*":"", "_":"", "-":"", "・":"", "廊":""}))
    search = re.search(r"[冠|杯|砂|羽|花]", text)

    if search:
        e = discord.Embed(title=f"{search.group()}", description="", color=0x9551a1)

        r1 = re.search(JP_reg_CRIT, text)#会心率
        r2 = re.search(JP_reg_CRITD, text)#会心ダメージ
        
        if r1:s1 = float(r1.group().replace("会心率", "").replace("+", ""))
        else:s1=0.0
        
        if r2:s2 = float(r2.group().replace("会心ダメージ", "").replace("+", ""))             
        else:s2 = 0.0

        if option == 1: #汎用火力
            r3= re.search(JP_reg_ATK, text) #攻撃力
            if r3:s3 = float(r3.group().replace("攻撃力", "").replace("+", ""))
            else :s3 = 0.0
            description = f"SCORE: **{Decimal(str(s3 + (s1 * 2) + s2)).quantize(Decimal('0.1'), rounding=ROUND_HALF_EVEN)}**\n"
            description += f"攻撃力 ` {str(s3)}`%\n"
            description += f"会心率 ` {str(s1)}`%\n会心ダメ ` {str(s2)}`%"
            e.description=description
            
        elif option == 2: #元素チャージ型
            r4 = re.search(JP_reg_CH, text) #元素チャージ
            if r4:s4 = float(r4.group().replace("元素チャージ効率","").replace("+",""))
            else: s4 = 0.0
            description = f"SCORE: **{Decimal(str((s4 * 0.4) + (s1 * 2) + s2)).quantize(Decimal('0.1'), rounding=ROUND_HALF_EVEN)}**\n"
            description += f"\元チャ ` {str(s4)}`%\n"
            description += f"会心率 ` {str(s1)}`%\n会心ダメ ` {str(s2)}`%"
            e.description = description

        elif option == 3: #防御型
            r5 = re.search(JP_reg_DEF, text) #防御力
            if r5:s5 = float(r5.group().replace("防御力", "").replace("+", ""))
            else: s5 = 0.0
            description = f"SCORE: **{Decimal(str(s5 + (s1 * 2) + s2)).quantize(Decimal('0.1'), rounding=ROUND_HALF_EVEN)}**\n"
            description += f"防御力 ` {str(s5)}` %\n"
            description += f"会心率 ` {str(s1)}`%\n会心ダメ ` {str(s2)}`%"
            e.description = description

        elif option == 4: #HP型
            r6 = re.search(JP_reg_HP, text) #HP
            if r6:s6 = float(r6.group().replace("HP", "").replace("+", ""))
            else:s6 = 0.0
            description = f"SCORE: **{Decimal(str(s6 + (s1 * 2) + s2)).quantize(Decimal('0.1'), rounding=ROUND_HALF_EVEN)}**\n"
            description += f"HP ` {str(s6)}`%\n"
            description += f"会心率 ` {str(s1)}`%\n会心ダメ ` {str(s2)}`%"
        elif option == 5: #熟知型
            r7 = re.search(JP_reg_ELE, text) #熟知
            if r7:s7 = int(r7.group().replace("元素熟知", "").replace("+", ""))
            else: s7 = 0
            description = f"SCORE: **{Decimal(str((s7 * 0.5) + s1 + (s2 * 0.5))).quantize(Decimal('0.1'), rounding=ROUND_HALF_EVEN)}**\n"
            description += f"熟知 ` {str(s7)}`\n"
            description += f"会心率 ` {str(s1)}`%\n会心ダメ ` {str(s2)}`%"
            e.description = description

        await msg.edit(content=None, embed=e)
    else:await msg.edit(content="Error")


"""im exhausted lol"""
@bot.command(name="en-genshin-artifacter", aliases=["eng"], description=en_description)
async def re_genshin_artifacter2(ctx, option=1):
    r = requests.get(ctx.message.attachments[0].url)

    msg = await ctx.reply("Please wait a moment.<a:Loading_2:1007527284753834014>")
    Image.open(io.BytesIO(r.content)).convert("L").save("image/image.png")

    builder = pyocr.builders.TextBuilder(tesseract_layout=3)
    text = tool.image_to_string(Image.open("image/image.png"), lang="eng", builder=builder)

    if re.search(r"[\.|\*|\_|\。|]|\}", text):
        text = str(text).translate(str.maketrans({".":"", "*":"", "_":"", "-":"", "・":"", "=":"", "}":""}))

    search = re.search(r"[Flower|Plume|Sands|Goblet|Circlet]", text)

    if search:
        e = discord.Embed(title=f"{search.group()}", description="", color=0x9551a1)
        print(text)
        print(search.group())
        print("\n\n", text)
        r1 = re.search(JP_reg_CRIT, text)#CRIT RATE
        r2 = re.search(JP_reg_CRITD, text)#CRIT DMG
        
        if r1:s1 = float(r1.group().replace("CRIT RATE", "").replace("+", ""))
        else:s1=0.0
        
        if r2:s2 = float(r2.group().replace("CRIT DMG", "").replace("+", ""))             
        else:s2 = 0.0

        if option == 1: #Default
            r3= re.search(JP_reg_ATK, text) #ATK
            if r3:s3 = float(r3.group().replace("ATK", "").replace("+", ""))
            else :s3 = 0.0

            description = f"SCORE: **{Decimal(str(s3 + (s1 * 2) + s2)).quantize(Decimal('0.1'), rounding=ROUND_HALF_EVEN)}**\n"
            description += f"ATK ` {str(s3)}`%\n"
            description += f"CRIT RATE ` {str(s1)}`%\nCRIT DMG ` {str(s2)}`%"
            e.description=description
            

        elif option == 2: #Energy Recharge
            r4 = re.search(JP_reg_CH, text) #Energy Recharge
            if r4:s4 = float(r4.group().replace("Energy Recharge","").replace("+",""))
            else: s4 = 0.0
            description = f"SCORE: **{Decimal(str((s4 * 0.4) + (s1 * 2) + s2)).quantize(Decimal('0.1'), rounding=ROUND_HALF_EVEN)}**"
            description += f"\Energy ` {str(s4)}`%"
            description += f"CRIT RATE ` {str(s1)}`%\nCRIT DMG ` {str(s2)}`%"
            e.description = description

        elif option == 3: #DEF
            r5 = re.search(JP_reg_DEF, text) #DEF
            if r5:s5 = float(r5.group().replace("DEF", "").replace("+", ""))
            else: s5 = 0.0
            description = f"SCORE: **{Decimal(str(s5 + (s1 * 2) + s2)).quantize(Decimal('0.1'), rounding=ROUND_HALF_EVEN)}**"
            description += f"DEF ` {str(s5)}` %"
            description += f"CRIT RATE ` {str(s1)}`%\nCRIT DMG ` {str(s2)}`%"
            e.description = description

        elif option == 4: #HP
            r6 = re.search(JP_reg_HP, text) #HP
            if r6:s6 = float(r6.group().replace("HP", "").replace("+", ""))
            else:s6 = 0.0
            description = f"SCORE: **{Decimal(str(s6 + (s1 * 2) + s2)).quantize(Decimal('0.1'), rounding=ROUND_HALF_EVEN)}**"
            description += f"HP ` {str(s6)}`%"
            description += f"CRIT RATE ` {str(s1)}`%\nCRIT DMG ` {str(s2)}`%"
            
        elif option==5: #Elemental-Burst
            r7 = re.search(JP_reg_ELE, text) #Elemental-Burst
            if r7:s7 = float(r7.group().replace("Elemental-Burst", "").replace("+", ""))
            else: s7 = 0.0
            description = f"SCORE: **{Decimal(str(s7 * 0.5) + s1 + (s2 * 0.5)).quantize(Decimal('0.1'), rounding=ROUND_HALF_EVEN)}**"
            description += f"EB ` {str(s7)}`%\n"
            description += f"CRIT RATE ` {str(s1)}`%\nCRIT DMG ` {str(s2)}`%"
            e.description = description

        await msg.edit(content=None, embed=e)
    else:await msg.edit(content="Error")



bot.run("MTAxOTAzMzQxMDE1NDUzMjkyOA.GDRf68.0LsijRY9gydzeYDbf8Ftx-3M5qZIaonHHs1TJY")