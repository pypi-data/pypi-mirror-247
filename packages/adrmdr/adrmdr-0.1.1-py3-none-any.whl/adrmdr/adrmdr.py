#!/usr/bin/env python
# coding: utf-8

# 第一部分：程序说明###################################################################################
# coding=utf-8
# 药械不良事件工作平台
# 开发人：蔡权周

# 第二部分：导入基本模块及初始化 ########################################################################

import tkinter as Tk #line:11
import os #line:12
import traceback #line:13
import ast #line:14
import re #line:15
import xlrd #line:16
import xlwt #line:17
import openpyxl #line:18
import pandas as pd #line:19
import numpy as np #line:20
import math #line:21
import scipy .stats as st #line:22
from tkinter import ttk ,Menu ,Frame ,Canvas ,StringVar ,LEFT ,RIGHT ,TOP ,BOTTOM ,BOTH ,Y ,X ,YES ,NO ,DISABLED ,END ,Button ,LabelFrame ,GROOVE ,Toplevel ,Label ,Entry ,Scrollbar ,Text ,filedialog ,dialog ,PhotoImage #line:23
import tkinter .font as tkFont #line:24
from tkinter .messagebox import showinfo #line:25
from tkinter .scrolledtext import ScrolledText #line:26
import matplotlib as plt #line:27
from matplotlib .backends .backend_tkagg import FigureCanvasTkAgg #line:28
from matplotlib .figure import Figure #line:29
from matplotlib .backends .backend_tkagg import NavigationToolbar2Tk #line:30
import collections #line:31
from collections import Counter #line:32
import datetime #line:33
from datetime import datetime ,timedelta #line:34
import xlsxwriter #line:35
import time #line:36
import threading #line:37
import warnings #line:38
from matplotlib .ticker import PercentFormatter #line:39
import sqlite3 #line:40
from sqlalchemy import create_engine #line:41
from sqlalchemy import text as sqltext #line:42
import webbrowser #line:44
global ori #line:47
ori =0 #line:48
global auto_guize #line:49
global biaozhun #line:52
global dishi #line:53
biaozhun =""#line:54
dishi =""#line:55
global ini #line:59
ini ={}#line:60
ini ["四个品种"]=1 #line:61
import random #line:64
import requests #line:65
global version_now #line:66
global usergroup #line:67
global setting_cfg #line:68
global csdir #line:69
global peizhidir #line:70
version_now ="0.1.1"#line:71
usergroup ="用户组=0"#line:72
setting_cfg =""#line:73
csdir =str (os .path .abspath (__file__ )).replace (str (__file__ ),"")#line:74
if csdir =="":#line:75
    csdir =str (os .path .dirname (__file__ ))#line:76
    csdir =csdir +csdir .split ("adrmdr")[0 ][-1 ]#line:77
title_all ="药械妆不良反应报表统计分析工作站 V"+version_now #line:80
title_all2 ="药械妆不良反应报表统计分析工作站 V"+version_now #line:81
def extract_zip_file (OO00O000O000OO00O ,OOO000O0O0O0OO0O0 ):#line:88
    import zipfile #line:90
    if OOO000O0O0O0OO0O0 =="":#line:91
        return 0 #line:92
    with zipfile .ZipFile (OO00O000O000OO00O ,'r')as O0OO00O000O0O0O0O :#line:93
        for O0OO00OO0OO0O0OO0 in O0OO00O000O0O0O0O .infolist ():#line:94
            O0OO00OO0OO0O0OO0 .filename =O0OO00OO0OO0O0OO0 .filename .encode ('cp437').decode ('gbk')#line:96
            O0OO00O000O0O0O0O .extract (O0OO00OO0OO0O0OO0 ,OOO000O0O0O0OO0O0 )#line:97
def get_directory_path (O0O00OO0O0OO00OO0 ):#line:103
    global csdir #line:105
    if not (os .path .isfile (os .path .join (O0O00OO0O0OO00OO0 ,'0（范例）比例失衡关键字库.xls'))):#line:107
        extract_zip_file (csdir +"def.py",O0O00OO0O0OO00OO0 )#line:112
    if O0O00OO0O0OO00OO0 =="":#line:114
        quit ()#line:115
    return O0O00OO0O0OO00OO0 #line:116
def convert_and_compare_dates (OOOO0000O0OOOOOOO ):#line:120
    import datetime #line:121
    O00O000OO0000O00O =datetime .datetime .now ()#line:122
    try :#line:124
       O000OO0OO0O00O000 =datetime .datetime .strptime (str (int (int (OOOO0000O0OOOOOOO )/4 )),"%Y%m%d")#line:125
    except :#line:126
        print ("fail")#line:127
        return "已过期"#line:128
    if O000OO0OO0O00O000 >O00O000OO0000O00O :#line:130
        return "未过期"#line:132
    else :#line:133
        return "已过期"#line:134
def read_setting_cfg ():#line:136
    global csdir #line:137
    if os .path .exists (csdir +'setting.cfg'):#line:139
        text .insert (END ,"已完成初始化\n")#line:140
        with open (csdir +'setting.cfg','r')as O0O0OOO0O000O0O00 :#line:141
            OO00O0OO0O00O000O =eval (O0O0OOO0O000O0O00 .read ())#line:142
    else :#line:143
        O0O00000O00O00O00 =csdir +'setting.cfg'#line:145
        with open (O0O00000O00O00O00 ,'w')as O0O0OOO0O000O0O00 :#line:146
            O0O0OOO0O000O0O00 .write ('{"settingdir": 0, "sidori": 0, "sidfinal": "11111180000808"}')#line:147
        text .insert (END ,"未初始化，正在初始化...\n")#line:148
        OO00O0OO0O00O000O =read_setting_cfg ()#line:149
    return OO00O0OO0O00O000O #line:150
def open_setting_cfg ():#line:153
    global csdir #line:154
    with open (csdir +"setting.cfg","r")as O00OOOOOO0OOOOO0O :#line:156
        O000O0OOOOO0O00OO =eval (O00OOOOOO0OOOOO0O .read ())#line:158
    return O000O0OOOOO0O00OO #line:159
def update_setting_cfg (O000O000O000OO00O ,OO0000O0OOOO000O0 ):#line:161
    global csdir #line:162
    with open (csdir +"setting.cfg","r")as OOO0O0000OOO0O0OO :#line:164
        OOO00O0O0O0OOOOO0 =eval (OOO0O0000OOO0O0OO .read ())#line:166
    if OOO00O0O0O0OOOOO0 [O000O000O000OO00O ]==0 or OOO00O0O0O0OOOOO0 [O000O000O000OO00O ]=="11111180000808":#line:168
        OOO00O0O0O0OOOOO0 [O000O000O000OO00O ]=OO0000O0OOOO000O0 #line:169
        with open (csdir +"setting.cfg","w")as OOO0O0000OOO0O0OO :#line:171
            OOO0O0000OOO0O0OO .write (str (OOO00O0O0O0OOOOO0 ))#line:172
def generate_random_file ():#line:175
    O0O0O00O0000O00O0 =random .randint (200000 ,299999 )#line:177
    update_setting_cfg ("sidori",O0O0O00O0000O00O0 )#line:179
def display_random_number ():#line:181
    global csdir #line:182
    O0O0000OOOOO0000O =Toplevel ()#line:183
    O0O0000OOOOO0000O .title ("ID")#line:184
    O0OO0O00000OOO000 =O0O0000OOOOO0000O .winfo_screenwidth ()#line:186
    O000OO0O00O0O0000 =O0O0000OOOOO0000O .winfo_screenheight ()#line:187
    OO00O0O000OO00O00 =80 #line:189
    OO0O0OOOO000OO00O =70 #line:190
    O0OOO000OO000O0OO =(O0OO0O00000OOO000 -OO00O0O000OO00O00 )/2 #line:192
    O0000O0O00O00OO0O =(O000OO0O00O0O0000 -OO0O0OOOO000OO00O )/2 #line:193
    O0O0000OOOOO0000O .geometry ("%dx%d+%d+%d"%(OO00O0O000OO00O00 ,OO0O0OOOO000OO00O ,O0OOO000OO000O0OO ,O0000O0O00O00OO0O ))#line:194
    with open (csdir +"setting.cfg","r")as O0O0O0OO00O0OO000 :#line:197
        OO000000OO0O0O000 =eval (O0O0O0OO00O0OO000 .read ())#line:199
    O0OOO0OO00OOO000O =int (OO000000OO0O0O000 ["sidori"])#line:200
    O0OO0OOOO0OOO0OOO =O0OOO0OO00OOO000O *2 +183576 #line:201
    print (O0OO0OOOO0OOO0OOO )#line:203
    O0OOOO000O0OO0O0O =ttk .Label (O0O0000OOOOO0000O ,text =f"机器码: {O0OOO0OO00OOO000O}")#line:205
    O0O00OOO000O00OOO =ttk .Entry (O0O0000OOOOO0000O )#line:206
    O0OOOO000O0OO0O0O .pack ()#line:209
    O0O00OOO000O00OOO .pack ()#line:210
    ttk .Button (O0O0000OOOOO0000O ,text ="验证",command =lambda :check_input (O0O00OOO000O00OOO .get (),O0OO0OOOO0OOO0OOO )).pack ()#line:214
def check_input (OO0000O0OO000O0O0 ,OOO0O0O0O0000OOOO ):#line:216
    try :#line:220
        OOO0O0O00000OO000 =int (str (OO0000O0OO000O0O0 )[0 :6 ])#line:221
        OOO00000000O0OOO0 =convert_and_compare_dates (str (OO0000O0OO000O0O0 )[6 :14 ])#line:222
    except :#line:223
        showinfo (title ="提示",message ="不匹配，注册失败。")#line:224
        return 0 #line:225
    if OOO0O0O00000OO000 ==OOO0O0O0O0000OOOO and OOO00000000O0OOO0 =="未过期":#line:227
        update_setting_cfg ("sidfinal",OO0000O0OO000O0O0 )#line:228
        showinfo (title ="提示",message ="注册成功,请重新启动程序。")#line:229
        quit ()#line:230
    else :#line:231
        showinfo (title ="提示",message ="不匹配，注册失败。")#line:232
def update_software (OOO0OOO00O0000OO0 ):#line:237
    global version_now #line:239
    text .insert (END ,"当前版本为："+version_now +",正在检查更新...(您可以同时执行分析任务)")#line:240
    try :#line:241
        O000OO0OOO0OOOO0O =requests .get (f"https://pypi.org/pypi/{OOO0OOO00O0000OO0}/json",timeout =2 ).json ()["info"]["version"]#line:242
    except :#line:243
        return "...更新失败。"#line:244
    if O000OO0OOO0OOOO0O >version_now :#line:245
        text .insert (END ,"\n最新版本为："+O000OO0OOO0OOOO0O +",正在尝试自动更新....")#line:246
        pip .main (['install',OOO0OOO00O0000OO0 ,'--upgrade'])#line:248
        text .insert (END ,"\n您可以开展工作。")#line:249
        return "...更新成功。"#line:250
def TOOLS_ror_mode1 (O00O0O0000O000O0O ,OO00OOO0OOOOOOO0O ):#line:267
	OO0O0O00O0OOO0O0O =[]#line:268
	for OO0OO0OO0O0OOOO00 in ("事件发生年份","性别","年龄段","报告类型-严重程度","停药减药后反应是否减轻或消失","再次使用可疑药是否出现同样反应","对原患疾病影响","不良反应结果","关联性评价"):#line:269
		O00O0O0000O000O0O [OO0OO0OO0O0OOOO00 ]=O00O0O0000O000O0O [OO0OO0OO0O0OOOO00 ].astype (str )#line:270
		O00O0O0000O000O0O [OO0OO0OO0O0OOOO00 ]=O00O0O0000O000O0O [OO0OO0OO0O0OOOO00 ].fillna ("不详")#line:271
		OOO0OOO0O0OOOOO00 =0 #line:273
		for OOO000OO0O00OO000 in O00O0O0000O000O0O [OO00OOO0OOOOOOO0O ].drop_duplicates ():#line:274
			OOO0OOO0O0OOOOO00 =OOO0OOO0O0OOOOO00 +1 #line:275
			OOOO0000OOO00OOOO =O00O0O0000O000O0O [(O00O0O0000O000O0O [OO00OOO0OOOOOOO0O ]==OOO000OO0O00OO000 )].copy ()#line:276
			O0O0O0OOOO0O0O00O =str (OOO000OO0O00OO000 )+"计数"#line:278
			OO0OOOOO00O0O0OO0 =str (OOO000OO0O00OO000 )+"构成比(%)"#line:279
			O0000O000OOO000OO =OOOO0000OOO00OOOO .groupby (OO0OO0OO0O0OOOO00 ).agg (计数 =("报告编码","nunique")).sort_values (by =OO0OO0OO0O0OOOO00 ,ascending =[True ],na_position ="last").reset_index ()#line:280
			O0000O000OOO000OO [OO0OOOOO00O0O0OO0 ]=round (100 *O0000O000OOO000OO ["计数"]/O0000O000OOO000OO ["计数"].sum (),2 )#line:281
			O0000O000OOO000OO =O0000O000OOO000OO .rename (columns ={OO0OO0OO0O0OOOO00 :"项目"})#line:282
			O0000O000OOO000OO =O0000O000OOO000OO .rename (columns ={"计数":O0O0O0OOOO0O0O00O })#line:283
			if OOO0OOO0O0OOOOO00 >1 :#line:284
				OO000O00000OO0OOO =pd .merge (OO000O00000OO0OOO ,O0000O000OOO000OO ,on =["项目"],how ="outer")#line:285
			else :#line:286
				OO000O00000OO0OOO =O0000O000OOO000OO .copy ()#line:287
		OO000O00000OO0OOO ["类别"]=OO0OO0OO0O0OOOO00 #line:289
		OO0O0O00O0OOO0O0O .append (OO000O00000OO0OOO .copy ().reset_index (drop =True ))#line:290
	OOO0OO000000O00O0 =pd .concat (OO0O0O00O0OOO0O0O ,ignore_index =True ).fillna (0 )#line:293
	OOO0OO000000O00O0 ["报表类型"]="KETI"#line:294
	TABLE_tree_Level_2 (OOO0OO000000O00O0 ,1 ,OOO0OO000000O00O0 )#line:295
def TOOLS_ror_mode2 (O0OO000O0O0O00O00 ,O00O0O00OO0000O00 ):#line:297
	OO000OO0OO0OO0O0O =Countall (O0OO000O0O0O00O00 ).df_ror (["产品类别",O00O0O00OO0000O00 ]).reset_index ()#line:298
	OO000OO0OO0OO0O0O ["四分表"]=OO000OO0OO0OO0O0O ["四分表"].str .replace ("(","")#line:299
	OO000OO0OO0OO0O0O ["四分表"]=OO000OO0OO0OO0O0O ["四分表"].str .replace (")","")#line:300
	OO000OO0OO0OO0O0O ["ROR信号（0-否，1-是）"]=0 #line:301
	OO000OO0OO0OO0O0O ["PRR信号（0-否，1-是）"]=0 #line:302
	OO000OO0OO0OO0O0O ["分母核验"]=0 #line:303
	for OO000OO0O000OOOO0 ,O00O0O000000O000O in OO000OO0OO0OO0O0O .iterrows ():#line:304
		O0OOO0O000OOO000O =tuple (O00O0O000000O000O ["四分表"].split (","))#line:305
		OO000OO0OO0OO0O0O .loc [OO000OO0O000OOOO0 ,"a"]=int (O0OOO0O000OOO000O [0 ])#line:306
		OO000OO0OO0OO0O0O .loc [OO000OO0O000OOOO0 ,"b"]=int (O0OOO0O000OOO000O [1 ])#line:307
		OO000OO0OO0OO0O0O .loc [OO000OO0O000OOOO0 ,"c"]=int (O0OOO0O000OOO000O [2 ])#line:308
		OO000OO0OO0OO0O0O .loc [OO000OO0O000OOOO0 ,"d"]=int (O0OOO0O000OOO000O [3 ])#line:309
		if int (O0OOO0O000OOO000O [1 ])*int (O0OOO0O000OOO000O [2 ])*int (O0OOO0O000OOO000O [3 ])*int (O0OOO0O000OOO000O [0 ])==0 :#line:310
			OO000OO0OO0OO0O0O .loc [OO000OO0O000OOOO0 ,"分母核验"]=1 #line:311
		if O00O0O000000O000O ['ROR值的95%CI下限']>1 and O00O0O000000O000O ['出现频次']>=3 :#line:312
			OO000OO0OO0OO0O0O .loc [OO000OO0O000OOOO0 ,"ROR信号（0-否，1-是）"]=1 #line:313
		if O00O0O000000O000O ['PRR值的95%CI下限']>1 and O00O0O000000O000O ['出现频次']>=3 :#line:314
			OO000OO0OO0OO0O0O .loc [OO000OO0O000OOOO0 ,"PRR信号（0-否，1-是）"]=1 #line:315
		OO000OO0OO0OO0O0O .loc [OO000OO0O000OOOO0 ,"事件分类"]=str (TOOLS_get_list (OO000OO0OO0OO0O0O .loc [OO000OO0O000OOOO0 ,"特定关键字"])[0 ])#line:316
	OO000OO0OO0OO0O0O =pd .pivot_table (OO000OO0OO0OO0O0O ,values =["出现频次",'ROR值',"ROR值的95%CI下限","ROR信号（0-否，1-是）",'PRR值',"PRR值的95%CI下限","PRR信号（0-否，1-是）","a","b","c","d","分母核验","风险评分"],index ='事件分类',columns =O00O0O00OO0000O00 ,aggfunc ='sum').reset_index ().fillna (0 )#line:318
	try :#line:321
		OO0OOOOOOOO0OOOO0 =peizhidir +"0（范例）比例失衡关键字库.xls"#line:322
		if "报告类型-新的"in O0OO000O0O0O00O00 .columns :#line:323
			OO00O0O0OOO00O000 ="药品"#line:324
		else :#line:325
			OO00O0O0OOO00O000 ="器械"#line:326
		OO0O00O0O0OOO00O0 =pd .read_excel (OO0OOOOOOOO0OOOO0 ,header =0 ,sheet_name =OO00O0O0OOO00O000 ).reset_index (drop =True )#line:327
	except :#line:328
		pass #line:329
	for OO000OO0O000OOOO0 ,O00O0O000000O000O in OO0O00O0O0OOO00O0 .iterrows ():#line:331
		OO000OO0OO0OO0O0O .loc [OO000OO0OO0OO0O0O ["事件分类"].str .contains (O00O0O000000O000O ["值"],na =False ),"器官系统损害"]=TOOLS_get_list (O00O0O000000O000O ["值"])[0 ]#line:332
	try :#line:335
		OO00OO0O00O0O00OO =peizhidir +""+"0（范例）标准术语"+".xlsx"#line:336
		try :#line:337
			O0OO000O0O0O000OO =pd .read_excel (OO00OO0O00O0O00OO ,sheet_name ="onept",header =0 ,index_col =0 ).reset_index ()#line:338
		except :#line:339
			showinfo (title ="错误信息",message ="标准术语集无法加载。")#line:340
		try :#line:342
			O0O0O000O0OOO0OO0 =pd .read_excel (OO00OO0O00O0O00OO ,sheet_name ="my",header =0 ,index_col =0 ).reset_index ()#line:343
		except :#line:344
			showinfo (title ="错误信息",message ="自定义术语集无法加载。")#line:345
		O0OO000O0O0O000OO =pd .concat ([O0O0O000O0OOO0OO0 ,O0OO000O0O0O000OO ],ignore_index =True ).drop_duplicates ("code")#line:347
		O0OO000O0O0O000OO ["code"]=O0OO000O0O0O000OO ["code"].astype (str )#line:348
		OO000OO0OO0OO0O0O ["事件分类"]=OO000OO0OO0OO0O0O ["事件分类"].astype (str )#line:349
		O0OO000O0O0O000OO ["事件分类"]=O0OO000O0O0O000OO ["PT"]#line:350
		OOO000OOO0O00O0OO =pd .merge (OO000OO0OO0OO0O0O ,O0OO000O0O0O000OO ,on =["事件分类"],how ="left")#line:351
		for OO000OO0O000OOOO0 ,O00O0O000000O000O in OOO000OOO0O00O0OO .iterrows ():#line:352
			OO000OO0OO0OO0O0O .loc [OO000OO0OO0OO0O0O ["事件分类"]==O00O0O000000O000O ["事件分类"],"Chinese"]=O00O0O000000O000O ["Chinese"]#line:353
			OO000OO0OO0OO0O0O .loc [OO000OO0OO0OO0O0O ["事件分类"]==O00O0O000000O000O ["事件分类"],"PT"]=O00O0O000000O000O ["PT"]#line:354
			OO000OO0OO0OO0O0O .loc [OO000OO0OO0OO0O0O ["事件分类"]==O00O0O000000O000O ["事件分类"],"HLT"]=O00O0O000000O000O ["HLT"]#line:355
			OO000OO0OO0OO0O0O .loc [OO000OO0OO0OO0O0O ["事件分类"]==O00O0O000000O000O ["事件分类"],"HLGT"]=O00O0O000000O000O ["HLGT"]#line:356
			OO000OO0OO0OO0O0O .loc [OO000OO0OO0OO0O0O ["事件分类"]==O00O0O000000O000O ["事件分类"],"SOC"]=O00O0O000000O000O ["SOC"]#line:357
	except :#line:358
		pass #line:359
	OO000OO0OO0OO0O0O ["报表类型"]="KETI"#line:362
	TABLE_tree_Level_2 (OO000OO0OO0OO0O0O ,1 ,OO000OO0OO0OO0O0O )#line:363
def TOOLS_ror_mode3 (OOOOOO00OO0OO0000 ,O000OOO0O0000O000 ):#line:365
	OOOOOO00OO0OO0000 ["css"]=0 #line:366
	TOOLS_ror_mode2 (OOOOOO00OO0OO0000 ,O000OOO0O0000O000 )#line:367
def TOOLS_ror_mode4 (O00O0O00OO0OOOO0O ,O00000OO0OO00OOOO ):#line:369
	OOOOOO0O0OOO0O00O =[]#line:370
	for O0O000OOO0OOO000O ,O0000O0000OOO00OO in data .drop_duplicates (O00000OO0OO00OOOO ).iterrows ():#line:371
		OOO0O0OOO0O000OOO =data [(O00O0O00OO0OOOO0O [O00000OO0OO00OOOO ]==O0000O0000OOO00OO [O00000OO0OO00OOOO ])]#line:372
		OO0OO0OOOOO0O0OO0 =Countall (OOO0O0OOO0O000OOO ).df_psur ()#line:373
		OO0OO0OOOOO0O0OO0 [O00000OO0OO00OOOO ]=O0000O0000OOO00OO [O00000OO0OO00OOOO ]#line:374
		if len (OO0OO0OOOOO0O0OO0 )>0 :#line:375
			OOOOOO0O0OOO0O00O .append (OO0OO0OOOOO0O0OO0 )#line:376
	OO0OOOOO0OO00OO0O =pd .concat (OOOOOO0O0OOO0O00O ,ignore_index =True ).sort_values (by ="关键字标记",ascending =[False ],na_position ="last").reset_index ()#line:378
	OO0OOOOO0OO00OO0O ["报表类型"]="KETI"#line:379
	TABLE_tree_Level_2 (OO0OOOOO0OO00OO0O ,1 ,OO0OOOOO0OO00OO0O )#line:380
def STAT_pinzhong (OOO0OO000O0OO0OO0 ,OOOO00OOO000OOO0O ,O0O000O00OOO0O0OO ):#line:382
	OOOOOOOOOO00O0O0O =[OOOO00OOO000OOO0O ]#line:384
	if O0O000O00OOO0O0OO ==-1 :#line:385
		O00000000OO0O0O0O =OOO0OO000O0OO0OO0 .drop_duplicates ("报告编码").copy ()#line:386
		OO00O0OO000OOOOO0 =O00000000OO0O0O0O .groupby ([OOOO00OOO000OOO0O ]).agg (计数 =("报告编码","nunique")).sort_values (by =OOOO00OOO000OOO0O ,ascending =[True ],na_position ="last").reset_index ()#line:387
		OO00O0OO000OOOOO0 ["构成比(%)"]=round (100 *OO00O0OO000OOOOO0 ["计数"]/OO00O0OO000OOOOO0 ["计数"].sum (),2 )#line:388
		OO00O0OO000OOOOO0 [OOOO00OOO000OOO0O ]=OO00O0OO000OOOOO0 [OOOO00OOO000OOO0O ].astype (str )#line:389
		OO00O0OO000OOOOO0 ["报表类型"]="dfx_deepview"+"_"+str (OOOOOOOOOO00O0O0O )#line:390
		TABLE_tree_Level_2 (OO00O0OO000OOOOO0 ,1 ,O00000000OO0O0O0O )#line:391
	if O0O000O00OOO0O0OO ==1 :#line:393
		O00000000OO0O0O0O =OOO0OO000O0OO0OO0 .copy ()#line:394
		OO00O0OO000OOOOO0 =O00000000OO0O0O0O .groupby ([OOOO00OOO000OOO0O ]).agg (计数 =("报告编码","nunique")).sort_values (by ="计数",ascending =[False ],na_position ="last").reset_index ()#line:395
		OO00O0OO000OOOOO0 ["构成比(%)"]=round (100 *OO00O0OO000OOOOO0 ["计数"]/OO00O0OO000OOOOO0 ["计数"].sum (),2 )#line:396
		OO00O0OO000OOOOO0 ["报表类型"]="dfx_deepview"+"_"+str (OOOOOOOOOO00O0O0O )#line:397
		TABLE_tree_Level_2 (OO00O0OO000OOOOO0 ,1 ,O00000000OO0O0O0O )#line:398
	if O0O000O00OOO0O0OO ==4 :#line:400
		O00000000OO0O0O0O =OOO0OO000O0OO0OO0 .copy ()#line:401
		O00000000OO0O0O0O .loc [O00000000OO0O0O0O ["不良反应结果"].str .contains ("好转",na =False ),"不良反应结果2"]="好转"#line:402
		O00000000OO0O0O0O .loc [O00000000OO0O0O0O ["不良反应结果"].str .contains ("痊愈",na =False ),"不良反应结果2"]="痊愈"#line:403
		O00000000OO0O0O0O .loc [O00000000OO0O0O0O ["不良反应结果"].str .contains ("无进展",na =False ),"不良反应结果2"]="无进展"#line:404
		O00000000OO0O0O0O .loc [O00000000OO0O0O0O ["不良反应结果"].str .contains ("死亡",na =False ),"不良反应结果2"]="死亡"#line:405
		O00000000OO0O0O0O .loc [O00000000OO0O0O0O ["不良反应结果"].str .contains ("不详",na =False ),"不良反应结果2"]="不详"#line:406
		O00000000OO0O0O0O .loc [O00000000OO0O0O0O ["不良反应结果"].str .contains ("未好转",na =False ),"不良反应结果2"]="未好转"#line:407
		OO00O0OO000OOOOO0 =O00000000OO0O0O0O .groupby (["不良反应结果2"]).agg (计数 =("报告编码","nunique")).sort_values (by ="计数",ascending =[False ],na_position ="last").reset_index ()#line:408
		OO00O0OO000OOOOO0 ["构成比(%)"]=round (100 *OO00O0OO000OOOOO0 ["计数"]/OO00O0OO000OOOOO0 ["计数"].sum (),2 )#line:409
		OO00O0OO000OOOOO0 ["报表类型"]="dfx_deepview"+"_"+str (["不良反应结果2"])#line:410
		TABLE_tree_Level_2 (OO00O0OO000OOOOO0 ,1 ,O00000000OO0O0O0O )#line:411
	if O0O000O00OOO0O0OO ==5 :#line:413
		O00000000OO0O0O0O =OOO0OO000O0OO0OO0 .copy ()#line:414
		O00000000OO0O0O0O ["关联性评价汇总"]="("+O00000000OO0O0O0O ["评价状态"].astype (str )+"("+O00000000OO0O0O0O ["县评价"].astype (str )+"("+O00000000OO0O0O0O ["市评价"].astype (str )+"("+O00000000OO0O0O0O ["省评价"].astype (str )+"("+O00000000OO0O0O0O ["国家评价"].astype (str )+")"#line:416
		O00000000OO0O0O0O ["关联性评价汇总"]=O00000000OO0O0O0O ["关联性评价汇总"].str .replace ("(nan","",regex =False )#line:417
		O00000000OO0O0O0O ["关联性评价汇总"]=O00000000OO0O0O0O ["关联性评价汇总"].str .replace ("nan)","",regex =False )#line:418
		O00000000OO0O0O0O ["关联性评价汇总"]=O00000000OO0O0O0O ["关联性评价汇总"].str .replace ("nan","",regex =False )#line:419
		O00000000OO0O0O0O ['最终的关联性评价']=O00000000OO0O0O0O ["关联性评价汇总"].str .extract ('.*\((.*)\).*',expand =False )#line:420
		OO00O0OO000OOOOO0 =O00000000OO0O0O0O .groupby ('最终的关联性评价').agg (计数 =("报告编码","nunique")).sort_values (by ="计数",ascending =[False ],na_position ="last").reset_index ()#line:421
		OO00O0OO000OOOOO0 ["构成比(%)"]=round (100 *OO00O0OO000OOOOO0 ["计数"]/OO00O0OO000OOOOO0 ["计数"].sum (),2 )#line:422
		OO00O0OO000OOOOO0 ["报表类型"]="dfx_deepview"+"_"+str (['最终的关联性评价'])#line:423
		TABLE_tree_Level_2 (OO00O0OO000OOOOO0 ,1 ,O00000000OO0O0O0O )#line:424
	if O0O000O00OOO0O0OO ==0 :#line:426
		OOO0OO000O0OO0OO0 [OOOO00OOO000OOO0O ]=OOO0OO000O0OO0OO0 [OOOO00OOO000OOO0O ].fillna ("未填写")#line:427
		OOO0OO000O0OO0OO0 [OOOO00OOO000OOO0O ]=OOO0OO000O0OO0OO0 [OOOO00OOO000OOO0O ].str .replace ("*","",regex =False )#line:428
		O00OOO0000O0OO000 ="use("+str (OOOO00OOO000OOO0O )+").file"#line:429
		OOOO0OO0OO00OO0OO =str (Counter (TOOLS_get_list0 (O00OOO0000O0OO000 ,OOO0OO000O0OO0OO0 ,1000 ))).replace ("Counter({","{")#line:430
		OOOO0OO0OO00OO0OO =OOOO0OO0OO00OO0OO .replace ("})","}")#line:431
		OOOO0OO0OO00OO0OO =ast .literal_eval (OOOO0OO0OO00OO0OO )#line:432
		OO00O0OO000OOOOO0 =pd .DataFrame .from_dict (OOOO0OO0OO00OO0OO ,orient ="index",columns =["计数"]).reset_index ()#line:433
		OO00O0OO000OOOOO0 ["构成比(%)"]=round (100 *OO00O0OO000OOOOO0 ["计数"]/OO00O0OO000OOOOO0 ["计数"].sum (),2 )#line:435
		OO00O0OO000OOOOO0 ["报表类型"]="dfx_deepvie2"+"_"+str (OOOOOOOOOO00O0O0O )#line:436
		TABLE_tree_Level_2 (OO00O0OO000OOOOO0 ,1 ,OOO0OO000O0OO0OO0 )#line:437
		return OO00O0OO000OOOOO0 #line:438
	if O0O000O00OOO0O0OO ==2 or O0O000O00OOO0O0OO ==3 :#line:442
		OOO0OO000O0OO0OO0 [OOOO00OOO000OOO0O ]=OOO0OO000O0OO0OO0 [OOOO00OOO000OOO0O ].astype (str )#line:443
		OOO0OO000O0OO0OO0 [OOOO00OOO000OOO0O ]=OOO0OO000O0OO0OO0 [OOOO00OOO000OOO0O ].fillna ("未填写")#line:444
		O00OOO0000O0OO000 ="use("+str (OOOO00OOO000OOO0O )+").file"#line:446
		OOOO0OO0OO00OO0OO =str (Counter (TOOLS_get_list0 (O00OOO0000O0OO000 ,OOO0OO000O0OO0OO0 ,1000 ))).replace ("Counter({","{")#line:447
		OOOO0OO0OO00OO0OO =OOOO0OO0OO00OO0OO .replace ("})","}")#line:448
		OOOO0OO0OO00OO0OO =ast .literal_eval (OOOO0OO0OO00OO0OO )#line:449
		OO00O0OO000OOOOO0 =pd .DataFrame .from_dict (OOOO0OO0OO00OO0OO ,orient ="index",columns =["计数"]).reset_index ()#line:450
		print ("正在统计，请稍后...")#line:451
		O0OOO0O0O00O0OO00 =peizhidir +""+"0（范例）标准术语"+".xlsx"#line:452
		try :#line:453
			OO00O00000OO0O0O0 =pd .read_excel (O0OOO0O0O00O0OO00 ,sheet_name ="simple",header =0 ,index_col =0 ).reset_index ()#line:454
		except :#line:455
			showinfo (title ="错误信息",message ="标准术语集无法加载。")#line:456
			return 0 #line:457
		try :#line:458
			O00O00OOOOOOOO0OO =pd .read_excel (O0OOO0O0O00O0OO00 ,sheet_name ="my",header =0 ,index_col =0 ).reset_index ()#line:459
		except :#line:460
			showinfo (title ="错误信息",message ="自定义术语集无法加载。")#line:461
			return 0 #line:462
		OO00O00000OO0O0O0 =pd .concat ([O00O00OOOOOOOO0OO ,OO00O00000OO0O0O0 ],ignore_index =True ).drop_duplicates ("code")#line:463
		OO00O00000OO0O0O0 ["code"]=OO00O00000OO0O0O0 ["code"].astype (str )#line:464
		OO00O0OO000OOOOO0 ["index"]=OO00O0OO000OOOOO0 ["index"].astype (str )#line:465
		OO00O0OO000OOOOO0 =OO00O0OO000OOOOO0 .rename (columns ={"index":"code"})#line:467
		OO00O0OO000OOOOO0 =pd .merge (OO00O0OO000OOOOO0 ,OO00O00000OO0O0O0 ,on =["code"],how ="left")#line:468
		OO00O0OO000OOOOO0 ["code构成比(%)"]=round (100 *OO00O0OO000OOOOO0 ["计数"]/OO00O0OO000OOOOO0 ["计数"].sum (),2 )#line:469
		OO00O0000OOOO0O0O =OO00O0OO000OOOOO0 .groupby ("SOC").agg (SOC计数 =("计数","sum")).sort_values (by ="SOC计数",ascending =[False ],na_position ="last").reset_index ()#line:470
		OO00O0000OOOO0O0O ["soc构成比(%)"]=round (100 *OO00O0000OOOO0O0O ["SOC计数"]/OO00O0000OOOO0O0O ["SOC计数"].sum (),2 )#line:471
		OO00O0000OOOO0O0O ["SOC计数"]=OO00O0000OOOO0O0O ["SOC计数"].astype (int )#line:472
		OO00O0OO000OOOOO0 =pd .merge (OO00O0OO000OOOOO0 ,OO00O0000OOOO0O0O ,on =["SOC"],how ="left")#line:473
		if O0O000O00OOO0O0OO ==3 :#line:475
			OO00O0000OOOO0O0O ["具体名称"]=""#line:476
			for O0O0O0000O0O00O00 ,OOOO0000O0O00OO0O in OO00O0000OOOO0O0O .iterrows ():#line:477
				O0OO00000O00O0O0O =""#line:478
				O00O0OOOO0O0000OO =OO00O0OO000OOOOO0 .loc [OO00O0OO000OOOOO0 ["SOC"].str .contains (OOOO0000O0O00OO0O ["SOC"],na =False )].copy ()#line:479
				for O0O0O000O0O0O0OOO ,O0OO0OO0O0OOOOO00 in O00O0OOOO0O0000OO .iterrows ():#line:480
					O0OO00000O00O0O0O =O0OO00000O00O0O0O +str (O0OO0OO0O0OOOOO00 ["PT"])+"("+str (O0OO0OO0O0OOOOO00 ["计数"])+")、"#line:481
				OO00O0000OOOO0O0O .loc [O0O0O0000O0O00O00 ,"具体名称"]=O0OO00000O00O0O0O #line:482
			OO00O0000OOOO0O0O ["报表类型"]="dfx_deepvie2"+"_"+str (["SOC"])#line:483
			TABLE_tree_Level_2 (OO00O0000OOOO0O0O ,1 ,OO00O0OO000OOOOO0 )#line:484
		if O0O000O00OOO0O0OO ==2 :#line:486
			OO00O0OO000OOOOO0 ["报表类型"]="dfx_deepvie2"+"_"+str (OOOOOOOOOO00O0O0O )#line:487
			TABLE_tree_Level_2 (OO00O0OO000OOOOO0 ,1 ,OOO0OO000O0OO0OO0 )#line:488
	pass #line:491
def DRAW_pre (O000O000OOO0OOO0O ):#line:493
	""#line:494
	OO0OO0OO0O0O0OO00 =list (O000O000OOO0OOO0O ["报表类型"])[0 ].replace ("1","")#line:502
	if "dfx_org监测机构"in OO0OO0OO0O0O0OO00 :#line:504
		O000O000OOO0OOO0O =O000O000OOO0OOO0O [:-1 ]#line:505
		DRAW_make_one (O000O000OOO0OOO0O ,"报告图","监测机构","报告数量","超级托帕斯图(严重伤害数)")#line:506
	elif "dfx_org市级监测机构"in OO0OO0OO0O0O0OO00 :#line:507
		O000O000OOO0OOO0O =O000O000OOO0OOO0O [:-1 ]#line:508
		DRAW_make_one (O000O000OOO0OOO0O ,"报告图","市级监测机构","报告数量","超级托帕斯图(严重伤害数)")#line:509
	elif "dfx_user"in OO0OO0OO0O0O0OO00 :#line:510
		O000O000OOO0OOO0O =O000O000OOO0OOO0O [:-1 ]#line:511
		DRAW_make_one (O000O000OOO0OOO0O ,"报告单位图","单位名称","报告数量","超级托帕斯图(严重伤害数)")#line:512
	elif "dfx_deepview"in OO0OO0OO0O0O0OO00 :#line:515
		DRAW_make_one (O000O000OOO0OOO0O ,"柱状图",O000O000OOO0OOO0O .columns [0 ],"计数","柱状图")#line:516
	elif "dfx_chiyouren"in OO0OO0OO0O0O0OO00 :#line:518
		O000O000OOO0OOO0O =O000O000OOO0OOO0O [:-1 ]#line:519
		DRAW_make_one (O000O000OOO0OOO0O ,"涉及持有人图","上市许可持有人名称","总报告数","超级托帕斯图(总待评价数量)")#line:520
	elif "dfx_zhenghao"in OO0OO0OO0O0O0OO00 :#line:522
		O000O000OOO0OOO0O ["产品"]=O000O000OOO0OOO0O ["产品名称"]+"("+O000O000OOO0OOO0O ["注册证编号/曾用注册证编号"]+")"#line:523
		DRAW_make_one (O000O000OOO0OOO0O ,"涉及产品图","产品","证号计数","超级托帕斯图(严重伤害数)")#line:524
	elif "dfx_pihao"in OO0OO0OO0O0O0OO00 :#line:526
		if len (O000O000OOO0OOO0O ["注册证编号/曾用注册证编号"].drop_duplicates ())>1 :#line:527
			O000O000OOO0OOO0O ["产品"]=O000O000OOO0OOO0O ["产品名称"]+"("+O000O000OOO0OOO0O ["注册证编号/曾用注册证编号"]+"--"+O000O000OOO0OOO0O ["产品批号"]+")"#line:528
			DRAW_make_one (O000O000OOO0OOO0O ,"涉及批号图","产品","批号计数","超级托帕斯图(严重伤害数)")#line:529
		else :#line:530
			DRAW_make_one (O000O000OOO0OOO0O ,"涉及批号图","产品批号","批号计数","超级托帕斯图(严重伤害数)")#line:531
	elif "dfx_xinghao"in OO0OO0OO0O0O0OO00 :#line:533
		if len (O000O000OOO0OOO0O ["注册证编号/曾用注册证编号"].drop_duplicates ())>1 :#line:534
			O000O000OOO0OOO0O ["产品"]=O000O000OOO0OOO0O ["产品名称"]+"("+O000O000OOO0OOO0O ["注册证编号/曾用注册证编号"]+"--"+O000O000OOO0OOO0O ["型号"]+")"#line:535
			DRAW_make_one (O000O000OOO0OOO0O ,"涉及型号图","产品","型号计数","超级托帕斯图(严重伤害数)")#line:536
		else :#line:537
			DRAW_make_one (O000O000OOO0OOO0O ,"涉及型号图","型号","型号计数","超级托帕斯图(严重伤害数)")#line:538
	elif "dfx_guige"in OO0OO0OO0O0O0OO00 :#line:540
		if len (O000O000OOO0OOO0O ["注册证编号/曾用注册证编号"].drop_duplicates ())>1 :#line:541
			O000O000OOO0OOO0O ["产品"]=O000O000OOO0OOO0O ["产品名称"]+"("+O000O000OOO0OOO0O ["注册证编号/曾用注册证编号"]+"--"+O000O000OOO0OOO0O ["规格"]+")"#line:542
			DRAW_make_one (O000O000OOO0OOO0O ,"涉及规格图","产品","规格计数","超级托帕斯图(严重伤害数)")#line:543
		else :#line:544
			DRAW_make_one (O000O000OOO0OOO0O ,"涉及规格图","规格","规格计数","超级托帕斯图(严重伤害数)")#line:545
	elif "PSUR"in OO0OO0OO0O0O0OO00 :#line:547
		DRAW_make_mutibar (O000O000OOO0OOO0O ,"总数量","严重","事件分类","总数量","严重","表现分类统计图")#line:548
	elif "keyword_findrisk"in OO0OO0OO0O0O0OO00 :#line:550
		OO00O0O0000O0O0O0 =O000O000OOO0OOO0O .columns .to_list ()#line:552
		O0O0OOOOOO00OO0O0 =OO00O0O0000O0O0O0 [OO00O0O0000O0O0O0 .index ("关键字")+1 ]#line:553
		OOOOOOO000OOOO000 =pd .pivot_table (O000O000OOO0OOO0O ,index =O0O0OOOOOO00OO0O0 ,columns ="关键字",values =["计数"],aggfunc ={"计数":"sum"},fill_value ="0",margins =True ,dropna =False ,)#line:564
		OOOOOOO000OOOO000 .columns =OOOOOOO000OOOO000 .columns .droplevel (0 )#line:565
		OOOOOOO000OOOO000 =OOOOOOO000OOOO000 [:-1 ].reset_index ()#line:566
		OOOOOOO000OOOO000 =pd .merge (OOOOOOO000OOOO000 ,O000O000OOO0OOO0O [[O0O0OOOOOO00OO0O0 ,"该元素总数量"]].drop_duplicates (O0O0OOOOOO00OO0O0 ),on =[O0O0OOOOOO00OO0O0 ],how ="left")#line:568
		del OOOOOOO000OOOO000 ["All"]#line:570
		DRAW_make_risk_plot (OOOOOOO000OOOO000 ,O0O0OOOOOO00OO0O0 ,[O000O00OO00000O00 for O000O00OO00000O00 in OOOOOOO000OOOO000 .columns if O000O00OO00000O00 !=O0O0OOOOOO00OO0O0 ],"关键字趋势图",100 )#line:575
def DRAW_make_risk_plot (O00000OO0000O0000 ,OOO000OOOO0O000OO ,OO0000O0OO0OOOO00 ,O0000O0O00OO0OO00 ,OOO0OOOO00000O0OO ,*O0OO0O0O00OOO0OO0 ):#line:580
    ""#line:581
    O00O00OOOOO00O00O =Toplevel ()#line:584
    O00O00OOOOO00O00O .title (O0000O0O00OO0OO00 )#line:585
    OO00OO0000O0OOO0O =ttk .Frame (O00O00OOOOO00O00O ,height =20 )#line:586
    OO00OO0000O0OOO0O .pack (side =TOP )#line:587
    OOOOOOO000OO0OOOO =Figure (figsize =(12 ,6 ),dpi =100 )#line:589
    OO0OOO0O00000O00O =FigureCanvasTkAgg (OOOOOOO000OO0OOOO ,master =O00O00OOOOO00O00O )#line:590
    OO0OOO0O00000O00O .draw ()#line:591
    OO0OOO0O00000O00O .get_tk_widget ().pack (expand =1 )#line:592
    plt .rcParams ["font.sans-serif"]=["SimHei"]#line:594
    plt .rcParams ['axes.unicode_minus']=False #line:595
    O00O0O00000OOOO0O =NavigationToolbar2Tk (OO0OOO0O00000O00O ,O00O00OOOOO00O00O )#line:597
    O00O0O00000OOOO0O .update ()#line:598
    OO0OOO0O00000O00O .get_tk_widget ().pack ()#line:599
    O00OOO0OO0OO00OOO =OOOOOOO000OO0OOOO .add_subplot (111 )#line:601
    O00OOO0OO0OO00OOO .set_title (O0000O0O00OO0OO00 )#line:603
    O00O0OO0OO0OO0O0O =O00000OO0000O0000 [OOO000OOOO0O000OO ]#line:604
    if OOO0OOOO00000O0OO !=999 :#line:607
        O00OOO0OO0OO00OOO .set_xticklabels (O00O0OO0OO0OO0O0O ,rotation =-90 ,fontsize =8 )#line:608
    O0O0000O0OO0O0000 =range (0 ,len (O00O0OO0OO0OO0O0O ),1 )#line:611
    try :#line:616
        O00OOO0OO0OO00OOO .bar (O00O0OO0OO0OO0O0O ,O00000OO0000O0000 ["报告总数"],color ='skyblue',label ="报告总数")#line:617
        O00OOO0OO0OO00OOO .bar (O00O0OO0OO0OO0O0O ,height =O00000OO0000O0000 ["严重伤害数"],color ="orangered",label ="严重伤害数")#line:618
    except :#line:619
        pass #line:620
    for OOO0O0O0000OO00O0 in OO0000O0OO0OOOO00 :#line:623
        OOOO0OO00000OO000 =O00000OO0000O0000 [OOO0O0O0000OO00O0 ].astype (float )#line:624
        if OOO0O0O0000OO00O0 =="关注区域":#line:626
            O00OOO0OO0OO00OOO .plot (list (O00O0OO0OO0OO0O0O ),list (OOOO0OO00000OO000 ),label =str (OOO0O0O0000OO00O0 ),color ="red")#line:627
        else :#line:628
            O00OOO0OO0OO00OOO .plot (list (O00O0OO0OO0OO0O0O ),list (OOOO0OO00000OO000 ),label =str (OOO0O0O0000OO00O0 ))#line:629
        if OOO0OOOO00000O0OO ==100 :#line:632
            for OOO0OO000OO0O000O ,O0OOO0000OO00OOOO in zip (O00O0OO0OO0OO0O0O ,OOOO0OO00000OO000 ):#line:633
                if O0OOO0000OO00OOOO ==max (OOOO0OO00000OO000 )and O0OOO0000OO00OOOO >=3 :#line:634
                     O00OOO0OO0OO00OOO .text (OOO0OO000OO0O000O ,O0OOO0000OO00OOOO ,(str (OOO0O0O0000OO00O0 )+":"+str (int (O0OOO0000OO00OOOO ))),color ='black',size =8 )#line:635
    try :#line:645
        if O0OO0O0O00OOO0OO0 [0 ]:#line:646
            O0OOO0O00O0O0O0OO =O0OO0O0O00OOO0OO0 [0 ]#line:647
    except :#line:648
        O0OOO0O00O0O0O0OO ="ucl"#line:649
    if len (OO0000O0OO0OOOO00 )==1 :#line:651
        if O0OOO0O00O0O0O0OO =="更多控制线分位数":#line:653
            OO0O0O0000OOOO0O0 =O00000OO0000O0000 [OO0000O0OO0OOOO00 ].astype (float ).values #line:654
            O000O00O0OOO0O0OO =np .where (OO0O0O0000OOOO0O0 >0 ,1 ,0 )#line:655
            O0O0000OO000O0OO0 =np .nonzero (O000O00O0OOO0O0OO )#line:656
            OO0O0O0000OOOO0O0 =OO0O0O0000OOOO0O0 [O0O0000OO000O0OO0 ]#line:657
            O0O0OOOOOO0OO0000 =np .median (OO0O0O0000OOOO0O0 )#line:658
            OOOO0O00OO00OO00O =np .percentile (OO0O0O0000OOOO0O0 ,25 )#line:659
            OO0O000O00O000OOO =np .percentile (OO0O0O0000OOOO0O0 ,75 )#line:660
            O0O000OO0O0O0000O =OO0O000O00O000OOO -OOOO0O00OO00OO00O #line:661
            OOO00OO00000OOOO0 =OO0O000O00O000OOO +1.5 *O0O000OO0O0O0000O #line:662
            O0O0OO0O000O0O0O0 =OOOO0O00OO00OO00O -1.5 *O0O000OO0O0O0000O #line:663
            O00OOO0OO0OO00OOO .axhline (O0O0OO0O000O0O0O0 ,color ='c',linestyle ='--',label ='异常下限')#line:666
            O00OOO0OO0OO00OOO .axhline (OOOO0O00OO00OO00O ,color ='r',linestyle ='--',label ='第25百分位数')#line:668
            O00OOO0OO0OO00OOO .axhline (O0O0OOOOOO0OO0000 ,color ='g',linestyle ='--',label ='中位数')#line:669
            O00OOO0OO0OO00OOO .axhline (OO0O000O00O000OOO ,color ='r',linestyle ='--',label ='第75百分位数')#line:670
            O00OOO0OO0OO00OOO .axhline (OOO00OO00000OOOO0 ,color ='c',linestyle ='--',label ='异常上限')#line:672
            O00OOOOO00O0OO0OO =ttk .Label (O00O00OOOOO00O00O ,text ="中位数="+str (O0O0OOOOOO0OO0000 )+"; 第25百分位数="+str (OOOO0O00OO00OO00O )+"; 第75百分位数="+str (OO0O000O00O000OOO )+"; 异常上限(第75百分位数+1.5IQR)="+str (OOO00OO00000OOOO0 )+"; IQR="+str (O0O000OO0O0O0000O ))#line:673
            O00OOOOO00O0OO0OO .pack ()#line:674
        elif O0OOO0O00O0O0O0OO =="更多控制线STD":#line:676
            OO0O0O0000OOOO0O0 =O00000OO0000O0000 [OO0000O0OO0OOOO00 ].astype (float ).values #line:677
            O000O00O0OOO0O0OO =np .where (OO0O0O0000OOOO0O0 >0 ,1 ,0 )#line:678
            O0O0000OO000O0OO0 =np .nonzero (O000O00O0OOO0O0OO )#line:679
            OO0O0O0000OOOO0O0 =OO0O0O0000OOOO0O0 [O0O0000OO000O0OO0 ]#line:680
            OO00O0OO00000O0OO =OO0O0O0000OOOO0O0 .mean ()#line:682
            OOOOO0O0OOOO0OOO0 =OO0O0O0000OOOO0O0 .std (ddof =1 )#line:683
            O00000O00OO00OO00 =OO00O0OO00000O0OO +3 *OOOOO0O0OOOO0OOO0 #line:684
            O000O0OOO00OOO000 =OOOOO0O0OOOO0OOO0 -3 *OOOOO0O0OOOO0OOO0 #line:685
            if len (OO0O0O0000OOOO0O0 )<30 :#line:687
                O0OOO000OO0000O00 =st .t .interval (0.95 ,df =len (OO0O0O0000OOOO0O0 )-1 ,loc =np .mean (OO0O0O0000OOOO0O0 ),scale =st .sem (OO0O0O0000OOOO0O0 ))#line:688
            else :#line:689
                O0OOO000OO0000O00 =st .norm .interval (0.95 ,loc =np .mean (OO0O0O0000OOOO0O0 ),scale =st .sem (OO0O0O0000OOOO0O0 ))#line:690
            O0OOO000OO0000O00 =O0OOO000OO0000O00 [1 ]#line:691
            O00OOO0OO0OO00OOO .axhline (O00000O00OO00OO00 ,color ='r',linestyle ='--',label ='UCL')#line:692
            O00OOO0OO0OO00OOO .axhline (OO00O0OO00000O0OO +2 *OOOOO0O0OOOO0OOO0 ,color ='m',linestyle ='--',label ='μ+2σ')#line:693
            O00OOO0OO0OO00OOO .axhline (OO00O0OO00000O0OO +OOOOO0O0OOOO0OOO0 ,color ='m',linestyle ='--',label ='μ+σ')#line:694
            O00OOO0OO0OO00OOO .axhline (OO00O0OO00000O0OO ,color ='g',linestyle ='--',label ='CL')#line:695
            O00OOO0OO0OO00OOO .axhline (OO00O0OO00000O0OO -OOOOO0O0OOOO0OOO0 ,color ='m',linestyle ='--',label ='μ-σ')#line:696
            O00OOO0OO0OO00OOO .axhline (OO00O0OO00000O0OO -2 *OOOOO0O0OOOO0OOO0 ,color ='m',linestyle ='--',label ='μ-2σ')#line:697
            O00OOO0OO0OO00OOO .axhline (O000O0OOO00OOO000 ,color ='r',linestyle ='--',label ='LCL')#line:698
            O00OOO0OO0OO00OOO .axhline (O0OOO000OO0000O00 ,color ='g',linestyle ='-',label ='95CI')#line:699
            O0O00OO00O0O000O0 =ttk .Label (O00O00OOOOO00O00O ,text ="mean="+str (OO00O0OO00000O0OO )+"; std="+str (OOOOO0O0OOOO0OOO0 )+"; 99.73%:UCL(μ+3σ)="+str (O00000O00OO00OO00 )+"; LCL(μ-3σ)="+str (O000O0OOO00OOO000 )+"; 95%CI="+str (O0OOO000OO0000O00 ))#line:700
            O0O00OO00O0O000O0 .pack ()#line:701
            O00OOOOO00O0OO0OO =ttk .Label (O00O00OOOOO00O00O ,text ="68.26%:μ+σ="+str (OO00O0OO00000O0OO +OOOOO0O0OOOO0OOO0 )+"; 95.45%:μ+2σ="+str (OO00O0OO00000O0OO +2 *OOOOO0O0OOOO0OOO0 ))#line:703
            O00OOOOO00O0OO0OO .pack ()#line:704
        else :#line:706
            OO0O0O0000OOOO0O0 =O00000OO0000O0000 [OO0000O0OO0OOOO00 ].astype (float ).values #line:707
            O000O00O0OOO0O0OO =np .where (OO0O0O0000OOOO0O0 >0 ,1 ,0 )#line:708
            O0O0000OO000O0OO0 =np .nonzero (O000O00O0OOO0O0OO )#line:709
            OO0O0O0000OOOO0O0 =OO0O0O0000OOOO0O0 [O0O0000OO000O0OO0 ]#line:710
            OO00O0OO00000O0OO =OO0O0O0000OOOO0O0 .mean ()#line:711
            OOOOO0O0OOOO0OOO0 =OO0O0O0000OOOO0O0 .std (ddof =1 )#line:712
            O00000O00OO00OO00 =OO00O0OO00000O0OO +3 *OOOOO0O0OOOO0OOO0 #line:713
            O000O0OOO00OOO000 =OOOOO0O0OOOO0OOO0 -3 *OOOOO0O0OOOO0OOO0 #line:714
            O00OOO0OO0OO00OOO .axhline (O00000O00OO00OO00 ,color ='r',linestyle ='--',label ='UCL')#line:715
            O00OOO0OO0OO00OOO .axhline (OO00O0OO00000O0OO ,color ='g',linestyle ='--',label ='CL')#line:716
            O00OOO0OO0OO00OOO .axhline (O000O0OOO00OOO000 ,color ='r',linestyle ='--',label ='LCL')#line:717
            O0O00OO00O0O000O0 =ttk .Label (O00O00OOOOO00O00O ,text ="mean="+str (OO00O0OO00000O0OO )+"; std="+str (OOOOO0O0OOOO0OOO0 )+"; UCL(μ+3σ)="+str (O00000O00OO00OO00 )+"; LCL(μ-3σ)="+str (O000O0OOO00OOO000 ))#line:718
            O0O00OO00O0O000O0 .pack ()#line:719
    O00OOO0OO0OO00OOO .set_title ("控制图")#line:722
    O00OOO0OO0OO00OOO .set_xlabel ("项")#line:723
    OOOOOOO000OO0OOOO .tight_layout (pad =0.4 ,w_pad =3.0 ,h_pad =3.0 )#line:724
    O0OO00O0OOOOO00OO =O00OOO0OO0OO00OOO .get_position ()#line:725
    O00OOO0OO0OO00OOO .set_position ([O0OO00O0OOOOO00OO .x0 ,O0OO00O0OOOOO00OO .y0 ,O0OO00O0OOOOO00OO .width *0.7 ,O0OO00O0OOOOO00OO .height ])#line:726
    O00OOO0OO0OO00OOO .legend (loc =2 ,bbox_to_anchor =(1.05 ,1.0 ),fontsize =10 ,borderaxespad =0.0 )#line:727
    O00OO0O00OOOO000O =StringVar ()#line:730
    O0OOO0OOOOO0O00O0 =ttk .Combobox (OO00OO0000O0OOO0O ,width =15 ,textvariable =O00OO0O00OOOO000O ,state ='readonly')#line:731
    O0OOO0OOOOO0O00O0 ['values']=OO0000O0OO0OOOO00 #line:732
    O0OOO0OOOOO0O00O0 .pack (side =LEFT )#line:733
    O0OOO0OOOOO0O00O0 .current (0 )#line:734
    OOO0O0O0OO0O0O0OO =Button (OO00OO0000O0OOO0O ,text ="控制图（单项-UCL(μ+3σ)）",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :DRAW_make_risk_plot (O00000OO0000O0000 ,OOO000OOOO0O000OO ,[O00O0OO00000OOO0O for O00O0OO00000OOO0O in OO0000O0OO0OOOO00 if O00OO0O00OOOO000O .get ()in O00O0OO00000OOO0O ],O0000O0O00OO0OO00 ,OOO0OOOO00000O0OO ))#line:744
    OOO0O0O0OO0O0O0OO .pack (side =LEFT ,anchor ="ne")#line:745
    O0OO00O0OO0000OO0 =Button (OO00OO0000O0OOO0O ,text ="控制图（单项-UCL(标准差法)）",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :DRAW_make_risk_plot (O00000OO0000O0000 ,OOO000OOOO0O000OO ,[OOO0O000000OOOOO0 for OOO0O000000OOOOO0 in OO0000O0OO0OOOO00 if O00OO0O00OOOO000O .get ()in OOO0O000000OOOOO0 ],O0000O0O00OO0OO00 ,OOO0OOOO00000O0OO ,"更多控制线STD"))#line:753
    O0OO00O0OO0000OO0 .pack (side =LEFT ,anchor ="ne")#line:754
    O0OO00O0OO0000OO0 =Button (OO00OO0000O0OOO0O ,text ="控制图（单项-分位数）",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :DRAW_make_risk_plot (O00000OO0000O0000 ,OOO000OOOO0O000OO ,[O0O00000O000O0O00 for O0O00000O000O0O00 in OO0000O0OO0OOOO00 if O00OO0O00OOOO000O .get ()in O0O00000O000O0O00 ],O0000O0O00OO0OO00 ,OOO0OOOO00000O0OO ,"更多控制线分位数"))#line:762
    O0OO00O0OO0000OO0 .pack (side =LEFT ,anchor ="ne")#line:763
    OO0O00OO0O00O0OO0 =Button (OO00OO0000O0OOO0O ,text ="去除标记",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :DRAW_make_risk_plot (O00000OO0000O0000 ,OOO000OOOO0O000OO ,OO0000O0OO0OOOO00 ,O0000O0O00OO0OO00 ,0 ))#line:772
    OO0O00OO0O00O0OO0 .pack (side =LEFT ,anchor ="ne")#line:774
    OO0OOO0O00000O00O .draw ()#line:775
def DRAW_make_one (O0OOO0OOOO00OOO0O ,O0O00O00O0OOO0OO0 ,OOO0O0O0OO00O0OOO ,OO00O00O00O00OOO0 ,O00000O0000O00OO0 ):#line:779
    ""#line:780
    warnings .filterwarnings ("ignore")#line:781
    OO0OOO0OOOOO00000 =Toplevel ()#line:782
    OO0OOO0OOOOO00000 .title (O0O00O00O0OOO0OO0 )#line:783
    O00OO0O0O0O0000O0 =ttk .Frame (OO0OOO0OOOOO00000 ,height =20 )#line:784
    O00OO0O0O0O0000O0 .pack (side =TOP )#line:785
    OOO0000000OOO0OOO =Figure (figsize =(12 ,6 ),dpi =100 )#line:787
    OOO0O00OOO0OOOO0O =FigureCanvasTkAgg (OOO0000000OOO0OOO ,master =OO0OOO0OOOOO00000 )#line:788
    OOO0O00OOO0OOOO0O .draw ()#line:789
    OOO0O00OOO0OOOO0O .get_tk_widget ().pack (expand =1 )#line:790
    OOO0OOOO0OOOO0OO0 =OOO0000000OOO0OOO .add_subplot (111 )#line:791
    plt .rcParams ["font.sans-serif"]=["SimHei"]#line:793
    plt .rcParams ['axes.unicode_minus']=False #line:794
    O0OOOOOOOO000OO0O =NavigationToolbar2Tk (OOO0O00OOO0OOOO0O ,OO0OOO0OOOOO00000 )#line:796
    O0OOOOOOOO000OO0O .update ()#line:797
    OOO0O00OOO0OOOO0O .get_tk_widget ().pack ()#line:799
    try :#line:802
        O0OO0OOOO00OOO0O0 =O0OOO0OOOO00OOO0O .columns #line:803
    except :#line:805
        O000O0OOOOO0OOOO0 =eval (O0OOO0OOOO00OOO0O )#line:806
        O000O0OOOOO0OOOO0 =pd .DataFrame .from_dict (O000O0OOOOO0OOOO0 ,orient =OOO0O0O0OO00O0OOO ,columns =[OO00O00O00O00OOO0 ]).reset_index ()#line:809
        O0OOO0OOOO00OOO0O =O000O0OOOOO0OOOO0 .sort_values (by =OO00O00O00O00OOO0 ,ascending =[False ],na_position ="last")#line:810
    if ("日期"in O0O00O00O0OOO0OO0 or "时间"in O0O00O00O0OOO0OO0 or "季度"in O0O00O00O0OOO0OO0 )and "饼图"not in O00000O0000O00OO0 :#line:814
        O0OOO0OOOO00OOO0O [OOO0O0O0OO00O0OOO ]=pd .to_datetime (O0OOO0OOOO00OOO0O [OOO0O0O0OO00O0OOO ],format ="%Y/%m/%d").dt .date #line:815
        O0OOO0OOOO00OOO0O =O0OOO0OOOO00OOO0O .sort_values (by =OOO0O0O0OO00O0OOO ,ascending =[True ],na_position ="last")#line:816
    elif "批号"in O0O00O00O0OOO0OO0 :#line:817
        O0OOO0OOOO00OOO0O [OOO0O0O0OO00O0OOO ]=O0OOO0OOOO00OOO0O [OOO0O0O0OO00O0OOO ].astype (str )#line:818
        O0OOO0OOOO00OOO0O =O0OOO0OOOO00OOO0O .sort_values (by =OOO0O0O0OO00O0OOO ,ascending =[True ],na_position ="last")#line:819
        OOO0OOOO0OOOO0OO0 .set_xticklabels (O0OOO0OOOO00OOO0O [OOO0O0O0OO00O0OOO ],rotation =-90 ,fontsize =8 )#line:820
    else :#line:821
        O0OOO0OOOO00OOO0O [OOO0O0O0OO00O0OOO ]=O0OOO0OOOO00OOO0O [OOO0O0O0OO00O0OOO ].astype (str )#line:822
        OOO0OOOO0OOOO0OO0 .set_xticklabels (O0OOO0OOOO00OOO0O [OOO0O0O0OO00O0OOO ],rotation =-90 ,fontsize =8 )#line:823
    OOOO0O0OOOOO0O0O0 =O0OOO0OOOO00OOO0O [OO00O00O00O00OOO0 ]#line:825
    O00O00000OO0000OO =range (0 ,len (OOOO0O0OOOOO0O0O0 ),1 )#line:826
    OOO0OOOO0OOOO0OO0 .set_title (O0O00O00O0OOO0OO0 )#line:828
    if O00000O0000O00OO0 =="柱状图":#line:832
        OOO0OOOO0OOOO0OO0 .bar (x =O0OOO0OOOO00OOO0O [OOO0O0O0OO00O0OOO ],height =OOOO0O0OOOOO0O0O0 ,width =0.2 ,color ="#87CEFA")#line:833
    elif O00000O0000O00OO0 =="饼图":#line:834
        OOO0OOOO0OOOO0OO0 .pie (x =OOOO0O0OOOOO0O0O0 ,labels =O0OOO0OOOO00OOO0O [OOO0O0O0OO00O0OOO ],autopct ="%0.2f%%")#line:835
    elif O00000O0000O00OO0 =="折线图":#line:836
        OOO0OOOO0OOOO0OO0 .plot (O0OOO0OOOO00OOO0O [OOO0O0O0OO00O0OOO ],OOOO0O0OOOOO0O0O0 ,lw =0.5 ,ls ='-',c ="r",alpha =0.5 )#line:837
    elif "托帕斯图"in str (O00000O0000O00OO0 ):#line:839
        OOO0OOO0OO0O0O0O0 =O0OOO0OOOO00OOO0O [OO00O00O00O00OOO0 ].fillna (0 )#line:840
        O00OOO00OO0O0OOOO =OOO0OOO0OO0O0O0O0 .cumsum ()/OOO0OOO0OO0O0O0O0 .sum ()*100 #line:844
        O0000OOOOO0O0OOO0 =O00OOO00OO0O0OOOO [O00OOO00OO0O0OOOO >0.8 ].index [0 ]#line:846
        O00000O000OO00O00 =OOO0OOO0OO0O0O0O0 .index .tolist ().index (O0000OOOOO0O0OOO0 )#line:847
        OOO0OOOO0OOOO0OO0 .bar (x =O0OOO0OOOO00OOO0O [OOO0O0O0OO00O0OOO ],height =OOO0OOO0OO0O0O0O0 ,color ="C0",label =OO00O00O00O00OOO0 )#line:851
        O00000O00OO00OO0O =OOO0OOOO0OOOO0OO0 .twinx ()#line:852
        O00000O00OO00OO0O .plot (O0OOO0OOOO00OOO0O [OOO0O0O0OO00O0OOO ],O00OOO00OO0O0OOOO ,color ="C1",alpha =0.6 ,label ="累计比例")#line:853
        O00000O00OO00OO0O .yaxis .set_major_formatter (PercentFormatter ())#line:854
        OOO0OOOO0OOOO0OO0 .tick_params (axis ="y",colors ="C0")#line:859
        O00000O00OO00OO0O .tick_params (axis ="y",colors ="C1")#line:860
        if "超级托帕斯图"in str (O00000O0000O00OO0 ):#line:863
            OO0O0000OO00OO000 =re .compile (r'[(](.*?)[)]',re .S )#line:864
            OOO00O0OO0O00O0O0 =re .findall (OO0O0000OO00OO000 ,O00000O0000O00OO0 )[0 ]#line:865
            OOO0OOOO0OOOO0OO0 .bar (x =O0OOO0OOOO00OOO0O [OOO0O0O0OO00O0OOO ],height =O0OOO0OOOO00OOO0O [OOO00O0OO0O00O0O0 ],color ="orangered",label =OOO00O0OO0O00O0O0 )#line:866
    OOO0000000OOO0OOO .tight_layout (pad =0.4 ,w_pad =3.0 ,h_pad =3.0 )#line:868
    OOOO0OOOO00OOOO00 =OOO0OOOO0OOOO0OO0 .get_position ()#line:869
    OOO0OOOO0OOOO0OO0 .set_position ([OOOO0OOOO00OOOO00 .x0 ,OOOO0OOOO00OOOO00 .y0 ,OOOO0OOOO00OOOO00 .width *0.7 ,OOOO0OOOO00OOOO00 .height ])#line:870
    OOO0OOOO0OOOO0OO0 .legend (loc =2 ,bbox_to_anchor =(1.05 ,1.0 ),fontsize =10 ,borderaxespad =0.0 )#line:871
    OOO0O00OOO0OOOO0O .draw ()#line:874
    if len (OOOO0O0OOOOO0O0O0 )<=20 and O00000O0000O00OO0 !="饼图":#line:877
        for OO0O0OOOOOOO0OOOO ,OO0OOO0OO0O0O000O in zip (O00O00000OO0000OO ,OOOO0O0OOOOO0O0O0 ):#line:878
            OO0OOO0O0O0OO0OO0 =str (OO0OOO0OO0O0O000O )#line:879
            OO0OOO000OO0O000O =(OO0O0OOOOOOO0OOOO ,OO0OOO0OO0O0O000O +0.3 )#line:880
            OOO0OOOO0OOOO0OO0 .annotate (OO0OOO0O0O0OO0OO0 ,xy =OO0OOO000OO0O000O ,fontsize =8 ,color ="black",ha ="center",va ="baseline")#line:881
    OO0O0OO0OOO0OOOO0 =Button (O00OO0O0O0O0000O0 ,relief =GROOVE ,activebackground ="green",text ="保存原始数据",command =lambda :TOOLS_save_dict (O0OOO0OOOO00OOO0O ),)#line:891
    OO0O0OO0OOO0OOOO0 .pack (side =RIGHT )#line:892
    O00OO0OOO00OOO00O =Button (O00OO0O0O0O0000O0 ,relief =GROOVE ,text ="查看原始数据",command =lambda :TOOLS_view_dict (O0OOO0OOOO00OOO0O ,0 ))#line:896
    O00OO0OOO00OOO00O .pack (side =RIGHT )#line:897
    O00OOO000OO000O00 =Button (O00OO0O0O0O0000O0 ,relief =GROOVE ,text ="饼图",command =lambda :DRAW_make_one (O0OOO0OOOO00OOO0O ,O0O00O00O0OOO0OO0 ,OOO0O0O0OO00O0OOO ,OO00O00O00O00OOO0 ,"饼图"),)#line:905
    O00OOO000OO000O00 .pack (side =LEFT )#line:906
    O00OOO000OO000O00 =Button (O00OO0O0O0O0000O0 ,relief =GROOVE ,text ="柱状图",command =lambda :DRAW_make_one (O0OOO0OOOO00OOO0O ,O0O00O00O0OOO0OO0 ,OOO0O0O0OO00O0OOO ,OO00O00O00O00OOO0 ,"柱状图"),)#line:913
    O00OOO000OO000O00 .pack (side =LEFT )#line:914
    O00OOO000OO000O00 =Button (O00OO0O0O0O0000O0 ,relief =GROOVE ,text ="折线图",command =lambda :DRAW_make_one (O0OOO0OOOO00OOO0O ,O0O00O00O0OOO0OO0 ,OOO0O0O0OO00O0OOO ,OO00O00O00O00OOO0 ,"折线图"),)#line:920
    O00OOO000OO000O00 .pack (side =LEFT )#line:921
    O00OOO000OO000O00 =Button (O00OO0O0O0O0000O0 ,relief =GROOVE ,text ="托帕斯图",command =lambda :DRAW_make_one (O0OOO0OOOO00OOO0O ,O0O00O00O0OOO0OO0 ,OOO0O0O0OO00O0OOO ,OO00O00O00O00OOO0 ,"托帕斯图"),)#line:928
    O00OOO000OO000O00 .pack (side =LEFT )#line:929
def DRAW_make_mutibar (OO0OOOO000OO00OO0 ,OO0OO0OO0OOOOOO00 ,O0OO00O0O0O0O000O ,OO00OO00000OO00OO ,O0O0000O0000OOOOO ,O0O0000000O00O000 ,O000000OOOO0O0OO0 ):#line:930
    ""#line:931
    O00O0O0O0OOO0O00O =Toplevel ()#line:932
    O00O0O0O0OOO0O00O .title (O000000OOOO0O0OO0 )#line:933
    OOO000O0OO0000OOO =ttk .Frame (O00O0O0O0OOO0O00O ,height =20 )#line:934
    OOO000O0OO0000OOO .pack (side =TOP )#line:935
    OO00OOOOOO0000OO0 =0.2 #line:937
    O0000O000O0000OO0 =Figure (figsize =(12 ,6 ),dpi =100 )#line:938
    OO0OOOO0O000OO00O =FigureCanvasTkAgg (O0000O000O0000OO0 ,master =O00O0O0O0OOO0O00O )#line:939
    OO0OOOO0O000OO00O .draw ()#line:940
    OO0OOOO0O000OO00O .get_tk_widget ().pack (expand =1 )#line:941
    O000000O000O0OO0O =O0000O000O0000OO0 .add_subplot (111 )#line:942
    plt .rcParams ["font.sans-serif"]=["SimHei"]#line:944
    plt .rcParams ['axes.unicode_minus']=False #line:945
    O00O000OOOO0OOO00 =NavigationToolbar2Tk (OO0OOOO0O000OO00O ,O00O0O0O0OOO0O00O )#line:947
    O00O000OOOO0OOO00 .update ()#line:948
    OO0OOOO0O000OO00O .get_tk_widget ().pack ()#line:950
    OO0OO0OO0OOOOOO00 =OO0OOOO000OO00OO0 [OO0OO0OO0OOOOOO00 ]#line:951
    O0OO00O0O0O0O000O =OO0OOOO000OO00OO0 [O0OO00O0O0O0O000O ]#line:952
    OO00OO00000OO00OO =OO0OOOO000OO00OO0 [OO00OO00000OO00OO ]#line:953
    O0O00O0O0OO00O0OO =range (0 ,len (OO0OO0OO0OOOOOO00 ),1 )#line:955
    O000000O000O0OO0O .set_xticklabels (OO00OO00000OO00OO ,rotation =-90 ,fontsize =8 )#line:956
    O000000O000O0OO0O .bar (O0O00O0O0OO00O0OO ,OO0OO0OO0OOOOOO00 ,align ="center",tick_label =OO00OO00000OO00OO ,label =O0O0000O0000OOOOO )#line:959
    O000000O000O0OO0O .bar (O0O00O0O0OO00O0OO ,O0OO00O0O0O0O000O ,align ="center",label =O0O0000000O00O000 )#line:962
    O000000O000O0OO0O .set_title (O000000OOOO0O0OO0 )#line:963
    O000000O000O0OO0O .set_xlabel ("项")#line:964
    O000000O000O0OO0O .set_ylabel ("数量")#line:965
    O0000O000O0000OO0 .tight_layout (pad =0.4 ,w_pad =3.0 ,h_pad =3.0 )#line:967
    OO0O0000000OOO0OO =O000000O000O0OO0O .get_position ()#line:968
    O000000O000O0OO0O .set_position ([OO0O0000000OOO0OO .x0 ,OO0O0000000OOO0OO .y0 ,OO0O0000000OOO0OO .width *0.7 ,OO0O0000000OOO0OO .height ])#line:969
    O000000O000O0OO0O .legend (loc =2 ,bbox_to_anchor =(1.05 ,1.0 ),fontsize =10 ,borderaxespad =0.0 )#line:970
    OO0OOOO0O000OO00O .draw ()#line:972
    OOOO0OO0OOO000000 =Button (OOO000O0OO0000OOO ,relief =GROOVE ,activebackground ="green",text ="保存原始数据",command =lambda :TOOLS_save_dict (OO0OOOO000OO00OO0 ),)#line:979
    OOOO0OO0OOO000000 .pack (side =RIGHT )#line:980
def CLEAN_hzp (O0O000O0O0OOOO0OO ):#line:985
    ""#line:986
    if "报告编码"not in O0O000O0O0OOOO0OO .columns :#line:987
            O0O000O0O0OOOO0OO ["特殊化妆品注册证书编号/普通化妆品备案编号"]=O0O000O0O0OOOO0OO ["特殊化妆品注册证书编号/普通化妆品备案编号"].fillna ("-未填写-")#line:988
            O0O000O0O0OOOO0OO ["省级评价结果"]=O0O000O0O0OOOO0OO ["省级评价结果"].fillna ("-未填写-")#line:989
            O0O000O0O0OOOO0OO ["生产企业"]=O0O000O0O0OOOO0OO ["生产企业"].fillna ("-未填写-")#line:990
            O0O000O0O0OOOO0OO ["提交人"]="不适用"#line:991
            O0O000O0O0OOOO0OO ["医疗机构类别"]="不适用"#line:992
            O0O000O0O0OOOO0OO ["经营企业或使用单位"]="不适用"#line:993
            O0O000O0O0OOOO0OO ["报告状态"]="报告单位评价"#line:994
            O0O000O0O0OOOO0OO ["所属地区"]="不适用"#line:995
            O0O000O0O0OOOO0OO ["医院名称"]="不适用"#line:996
            O0O000O0O0OOOO0OO ["报告地区名称"]="不适用"#line:997
            O0O000O0O0OOOO0OO ["提交人"]="不适用"#line:998
            O0O000O0O0OOOO0OO ["型号"]=O0O000O0O0OOOO0OO ["化妆品分类"]#line:999
            O0O000O0O0OOOO0OO ["关联性评价"]=O0O000O0O0OOOO0OO ["上报单位评价结果"]#line:1000
            O0O000O0O0OOOO0OO ["规格"]="不适用"#line:1001
            O0O000O0O0OOOO0OO ["器械故障表现"]=O0O000O0O0OOOO0OO ["初步判断"]#line:1002
            O0O000O0O0OOOO0OO ["伤害表现"]=O0O000O0O0OOOO0OO ["自觉症状"]+O0O000O0O0OOOO0OO ["皮损部位"]+O0O000O0O0OOOO0OO ["皮损形态"]#line:1003
            O0O000O0O0OOOO0OO ["事件原因分析"]="不适用"#line:1004
            O0O000O0O0OOOO0OO ["事件原因分析描述"]="不适用"#line:1005
            O0O000O0O0OOOO0OO ["调查情况"]="不适用"#line:1006
            O0O000O0O0OOOO0OO ["具体控制措施"]="不适用"#line:1007
            O0O000O0O0OOOO0OO ["未采取控制措施原因"]="不适用"#line:1008
            O0O000O0O0OOOO0OO ["报告地区名称"]="不适用"#line:1009
            O0O000O0O0OOOO0OO ["上报单位所属地区"]="不适用"#line:1010
            O0O000O0O0OOOO0OO ["持有人报告状态"]="不适用"#line:1011
            O0O000O0O0OOOO0OO ["年龄类型"]="岁"#line:1012
            O0O000O0O0OOOO0OO ["经营企业使用单位报告状态"]="不适用"#line:1013
            O0O000O0O0OOOO0OO ["产品归属"]="化妆品"#line:1014
            O0O000O0O0OOOO0OO ["管理类别"]="不适用"#line:1015
            O0O000O0O0OOOO0OO ["超时标记"]="不适用"#line:1016
            O0O000O0O0OOOO0OO =O0O000O0O0OOOO0OO .rename (columns ={"报告表编号":"报告编码","报告类型":"伤害","报告地区":"监测机构","报告单位名称":"单位名称","患者/消费者姓名":"姓名","不良反应发生日期":"事件发生日期","过程描述补充说明":"使用过程","化妆品名称":"产品名称","化妆品分类":"产品类别","生产企业":"上市许可持有人名称","生产批号":"产品批号","特殊化妆品注册证书编号/普通化妆品备案编号":"注册证编号/曾用注册证编号",})#line:1035
            O0O000O0O0OOOO0OO ["时隔"]=pd .to_datetime (O0O000O0O0OOOO0OO ["事件发生日期"])-pd .to_datetime (O0O000O0O0OOOO0OO ["开始使用日期"])#line:1036
            O0O000O0O0OOOO0OO ["时隔"]=O0O000O0O0OOOO0OO ["时隔"].astype (str )#line:1037
            O0O000O0O0OOOO0OO .loc [(O0O000O0O0OOOO0OO ["省级评价结果"]!="-未填写-"),"有效报告"]=1 #line:1038
            O0O000O0O0OOOO0OO ["伤害"]=O0O000O0O0OOOO0OO ["伤害"].str .replace ("严重","严重伤害",regex =False )#line:1039
            try :#line:1040
	            O0O000O0O0OOOO0OO =TOOL_guizheng (O0O000O0O0OOOO0OO ,4 ,True )#line:1041
            except :#line:1042
                pass #line:1043
            return O0O000O0O0OOOO0OO #line:1044
def CLEAN_yp (O0O000O00OOOO0O00 ):#line:1049
    ""#line:1050
    if "报告编码"not in O0O000O00OOOO0O00 .columns :#line:1051
        if "反馈码"in O0O000O00OOOO0O00 .columns and "报告表编码"not in O0O000O00OOOO0O00 .columns :#line:1053
            O0O000O00OOOO0O00 ["提交人"]="不适用"#line:1055
            O0O000O00OOOO0O00 ["经营企业或使用单位"]="不适用"#line:1056
            O0O000O00OOOO0O00 ["报告状态"]="报告单位评价"#line:1057
            O0O000O00OOOO0O00 ["所属地区"]="不适用"#line:1058
            O0O000O00OOOO0O00 ["产品类别"]="无源"#line:1059
            O0O000O00OOOO0O00 ["医院名称"]="不适用"#line:1060
            O0O000O00OOOO0O00 ["报告地区名称"]="不适用"#line:1061
            O0O000O00OOOO0O00 ["提交人"]="不适用"#line:1062
            O0O000O00OOOO0O00 =O0O000O00OOOO0O00 .rename (columns ={"反馈码":"报告表编码","序号":"药品序号","新的":"报告类型-新的","报告类型":"报告类型-严重程度","用药-日数":"用法-日","用药-次数":"用法-次",})#line:1075
        if "唯一标识"not in O0O000O00OOOO0O00 .columns :#line:1080
            O0O000O00OOOO0O00 ["报告编码"]=O0O000O00OOOO0O00 ["报告表编码"].astype (str )+O0O000O00OOOO0O00 ["患者姓名"].astype (str )#line:1081
        if "唯一标识"in O0O000O00OOOO0O00 .columns :#line:1082
            O0O000O00OOOO0O00 ["唯一标识"]=O0O000O00OOOO0O00 ["唯一标识"].astype (str )#line:1083
            O0O000O00OOOO0O00 =O0O000O00OOOO0O00 .rename (columns ={"唯一标识":"报告编码"})#line:1084
        if "医疗机构类别"not in O0O000O00OOOO0O00 .columns :#line:1085
            O0O000O00OOOO0O00 ["医疗机构类别"]="医疗机构"#line:1086
            O0O000O00OOOO0O00 ["经营企业使用单位报告状态"]="已提交"#line:1087
        try :#line:1088
            O0O000O00OOOO0O00 ["年龄和单位"]=O0O000O00OOOO0O00 ["年龄"].astype (str )+O0O000O00OOOO0O00 ["年龄单位"]#line:1089
        except :#line:1090
            O0O000O00OOOO0O00 ["年龄和单位"]=O0O000O00OOOO0O00 ["年龄"].astype (str )+O0O000O00OOOO0O00 ["年龄类型"]#line:1091
        O0O000O00OOOO0O00 .loc [(O0O000O00OOOO0O00 ["报告类型-新的"]=="新的"),"管理类别"]="Ⅲ类"#line:1092
        O0O000O00OOOO0O00 .loc [(O0O000O00OOOO0O00 ["报告类型-严重程度"]=="严重"),"管理类别"]="Ⅲ类"#line:1093
        text .insert (END ,"剔除已删除报告和重复报告...")#line:1094
        if "删除标识"in O0O000O00OOOO0O00 .columns :#line:1095
            O0O000O00OOOO0O00 =O0O000O00OOOO0O00 [(O0O000O00OOOO0O00 ["删除标识"]!="删除")]#line:1096
        if "重复报告"in O0O000O00OOOO0O00 .columns :#line:1097
            O0O000O00OOOO0O00 =O0O000O00OOOO0O00 [(O0O000O00OOOO0O00 ["重复报告"]!="重复报告")]#line:1098
        O0O000O00OOOO0O00 ["报告类型-新的"]=O0O000O00OOOO0O00 ["报告类型-新的"].fillna (" ")#line:1101
        O0O000O00OOOO0O00 .loc [(O0O000O00OOOO0O00 ["报告类型-严重程度"]=="严重"),"伤害"]="严重伤害"#line:1102
        O0O000O00OOOO0O00 ["伤害"]=O0O000O00OOOO0O00 ["伤害"].fillna ("所有一般")#line:1103
        O0O000O00OOOO0O00 ["伤害PSUR"]=O0O000O00OOOO0O00 ["报告类型-新的"].astype (str )+O0O000O00OOOO0O00 ["报告类型-严重程度"].astype (str )#line:1104
        O0O000O00OOOO0O00 ["用量用量单位"]=O0O000O00OOOO0O00 ["用量"].astype (str )+O0O000O00OOOO0O00 ["用量单位"].astype (str )#line:1105
        O0O000O00OOOO0O00 ["规格"]="不适用"#line:1107
        O0O000O00OOOO0O00 ["事件原因分析"]="不适用"#line:1108
        O0O000O00OOOO0O00 ["事件原因分析描述"]="不适用"#line:1109
        O0O000O00OOOO0O00 ["初步处置情况"]="不适用"#line:1110
        O0O000O00OOOO0O00 ["伤害表现"]=O0O000O00OOOO0O00 ["不良反应名称"]#line:1111
        O0O000O00OOOO0O00 ["产品类别"]="无源"#line:1112
        O0O000O00OOOO0O00 ["调查情况"]="不适用"#line:1113
        O0O000O00OOOO0O00 ["具体控制措施"]="不适用"#line:1114
        O0O000O00OOOO0O00 ["上报单位所属地区"]=O0O000O00OOOO0O00 ["报告地区名称"]#line:1115
        O0O000O00OOOO0O00 ["注册证编号/曾用注册证编号"]=O0O000O00OOOO0O00 ["批准文号"]#line:1118
        O0O000O00OOOO0O00 ["器械故障表现"]=O0O000O00OOOO0O00 ["不良反应名称"]#line:1119
        O0O000O00OOOO0O00 ["型号"]=O0O000O00OOOO0O00 ["剂型"]#line:1120
        O0O000O00OOOO0O00 ["未采取控制措施原因"]="不适用"#line:1123
        O0O000O00OOOO0O00 ["报告单位评价"]=O0O000O00OOOO0O00 ["报告类型-新的"].astype (str )+O0O000O00OOOO0O00 ["报告类型-严重程度"].astype (str )#line:1124
        O0O000O00OOOO0O00 .loc [(O0O000O00OOOO0O00 ["报告类型-新的"]=="新的"),"持有人报告状态"]="待评价"#line:1125
        O0O000O00OOOO0O00 ["用法temp日"]="日"#line:1126
        O0O000O00OOOO0O00 ["用法temp次"]="次"#line:1127
        O0O000O00OOOO0O00 ["用药频率"]=(O0O000O00OOOO0O00 ["用法-日"].astype (str )+O0O000O00OOOO0O00 ["用法temp日"]+O0O000O00OOOO0O00 ["用法-次"].astype (str )+O0O000O00OOOO0O00 ["用法temp次"])#line:1133
        try :#line:1134
            O0O000O00OOOO0O00 ["相关疾病信息[疾病名称]-术语"]=O0O000O00OOOO0O00 ["原患疾病"]#line:1135
            O0O000O00OOOO0O00 ["治疗适应症-术语"]=O0O000O00OOOO0O00 ["用药原因"]#line:1136
        except :#line:1137
            pass #line:1138
        try :#line:1140
            O0O000O00OOOO0O00 =O0O000O00OOOO0O00 .rename (columns ={"提交日期":"报告日期"})#line:1141
            O0O000O00OOOO0O00 =O0O000O00OOOO0O00 .rename (columns ={"提交人":"报告人"})#line:1142
            O0O000O00OOOO0O00 =O0O000O00OOOO0O00 .rename (columns ={"报告状态":"持有人报告状态"})#line:1143
            O0O000O00OOOO0O00 =O0O000O00OOOO0O00 .rename (columns ={"所属地区":"使用单位、经营企业所属监测机构"})#line:1144
            O0O000O00OOOO0O00 =O0O000O00OOOO0O00 .rename (columns ={"医院名称":"单位名称"})#line:1145
            O0O000O00OOOO0O00 =O0O000O00OOOO0O00 .rename (columns ={"通用名称":"产品名称"})#line:1147
            O0O000O00OOOO0O00 =O0O000O00OOOO0O00 .rename (columns ={"生产厂家":"上市许可持有人名称"})#line:1148
            O0O000O00OOOO0O00 =O0O000O00OOOO0O00 .rename (columns ={"不良反应发生时间":"事件发生日期"})#line:1149
            O0O000O00OOOO0O00 =O0O000O00OOOO0O00 .rename (columns ={"不良反应过程描述":"使用过程"})#line:1151
            O0O000O00OOOO0O00 =O0O000O00OOOO0O00 .rename (columns ={"生产批号":"产品批号"})#line:1152
            O0O000O00OOOO0O00 =O0O000O00OOOO0O00 .rename (columns ={"报告地区名称":"使用单位、经营企业所属监测机构"})#line:1153
            O0O000O00OOOO0O00 =O0O000O00OOOO0O00 .rename (columns ={"报告人评价":"关联性评价"})#line:1155
            O0O000O00OOOO0O00 =O0O000O00OOOO0O00 .rename (columns ={"年龄单位":"年龄类型"})#line:1156
        except :#line:1157
            text .insert (END ,"数据规整失败。")#line:1158
            return 0 #line:1159
        O0O000O00OOOO0O00 ['报告日期']=O0O000O00OOOO0O00 ['报告日期'].str .strip ()#line:1162
        O0O000O00OOOO0O00 ['事件发生日期']=O0O000O00OOOO0O00 ['事件发生日期'].str .strip ()#line:1163
        O0O000O00OOOO0O00 ['用药开始时间']=O0O000O00OOOO0O00 ['用药开始时间'].str .strip ()#line:1164
        return O0O000O00OOOO0O00 #line:1166
    if "报告编码"in O0O000O00OOOO0O00 .columns :#line:1167
        return O0O000O00OOOO0O00 #line:1168
def CLEAN_qx (OO00OOOO00OO000O0 ):#line:1170
		""#line:1171
		if "使用单位、经营企业所属监测机构"not in OO00OOOO00OO000O0 .columns and "监测机构"not in OO00OOOO00OO000O0 .columns :#line:1173
			OO00OOOO00OO000O0 ["使用单位、经营企业所属监测机构"]="本地"#line:1174
		if "上市许可持有人名称"not in OO00OOOO00OO000O0 .columns :#line:1175
			OO00OOOO00OO000O0 ["上市许可持有人名称"]=OO00OOOO00OO000O0 ["单位名称"]#line:1176
		if "注册证编号/曾用注册证编号"not in OO00OOOO00OO000O0 .columns :#line:1177
			OO00OOOO00OO000O0 ["注册证编号/曾用注册证编号"]=OO00OOOO00OO000O0 ["注册证编号"]#line:1178
		if "事件原因分析描述"not in OO00OOOO00OO000O0 .columns :#line:1179
			OO00OOOO00OO000O0 ["事件原因分析描述"]="  "#line:1180
		if "初步处置情况"not in OO00OOOO00OO000O0 .columns :#line:1181
			OO00OOOO00OO000O0 ["初步处置情况"]="  "#line:1182
		text .insert (END ,"\n正在执行格式规整和增加有关时间、年龄、性别等统计列...")#line:1185
		OO00OOOO00OO000O0 =OO00OOOO00OO000O0 .rename (columns ={"使用单位、经营企业所属监测机构":"监测机构"})#line:1186
		OO00OOOO00OO000O0 ["报告编码"]=OO00OOOO00OO000O0 ["报告编码"].astype ("str")#line:1187
		OO00OOOO00OO000O0 ["产品批号"]=OO00OOOO00OO000O0 ["产品批号"].astype ("str")#line:1188
		OO00OOOO00OO000O0 ["型号"]=OO00OOOO00OO000O0 ["型号"].astype ("str")#line:1189
		OO00OOOO00OO000O0 ["规格"]=OO00OOOO00OO000O0 ["规格"].astype ("str")#line:1190
		OO00OOOO00OO000O0 ["注册证编号/曾用注册证编号"]=OO00OOOO00OO000O0 ["注册证编号/曾用注册证编号"].str .replace ("(","（",regex =False )#line:1191
		OO00OOOO00OO000O0 ["注册证编号/曾用注册证编号"]=OO00OOOO00OO000O0 ["注册证编号/曾用注册证编号"].str .replace (")","）",regex =False )#line:1192
		OO00OOOO00OO000O0 ["注册证编号/曾用注册证编号"]=OO00OOOO00OO000O0 ["注册证编号/曾用注册证编号"].str .replace ("*","※",regex =False )#line:1193
		OO00OOOO00OO000O0 ["注册证编号/曾用注册证编号"]=OO00OOOO00OO000O0 ["注册证编号/曾用注册证编号"].fillna ("-未填写-")#line:1194
		OO00OOOO00OO000O0 ["产品名称"]=OO00OOOO00OO000O0 ["产品名称"].str .replace ("*","※",regex =False )#line:1195
		OO00OOOO00OO000O0 ["产品批号"]=OO00OOOO00OO000O0 ["产品批号"].str .replace ("(","（",regex =False )#line:1196
		OO00OOOO00OO000O0 ["产品批号"]=OO00OOOO00OO000O0 ["产品批号"].str .replace (")","）",regex =False )#line:1197
		OO00OOOO00OO000O0 ["产品批号"]=OO00OOOO00OO000O0 ["产品批号"].str .replace ("*","※",regex =False )#line:1198
		OO00OOOO00OO000O0 ["上市许可持有人名称"]=OO00OOOO00OO000O0 ["上市许可持有人名称"].fillna ("-未填写-")#line:1202
		OO00OOOO00OO000O0 ["产品类别"]=OO00OOOO00OO000O0 ["产品类别"].fillna ("-未填写-")#line:1203
		OO00OOOO00OO000O0 ["产品名称"]=OO00OOOO00OO000O0 ["产品名称"].fillna ("-未填写-")#line:1204
		OO00OOOO00OO000O0 ["注册证编号/曾用注册证编号"]=OO00OOOO00OO000O0 ["注册证编号/曾用注册证编号"].fillna ("-未填写-")#line:1205
		OO00OOOO00OO000O0 ["产品批号"]=OO00OOOO00OO000O0 ["产品批号"].fillna ("-未填写-")#line:1206
		OO00OOOO00OO000O0 ["型号"]=OO00OOOO00OO000O0 ["型号"].fillna ("-未填写-")#line:1207
		OO00OOOO00OO000O0 ["规格"]=OO00OOOO00OO000O0 ["规格"].fillna ("-未填写-")#line:1208
		OO00OOOO00OO000O0 ["伤害与评价"]=OO00OOOO00OO000O0 ["伤害"]+OO00OOOO00OO000O0 ["持有人报告状态"]#line:1211
		OO00OOOO00OO000O0 ["注册证备份"]=OO00OOOO00OO000O0 ["注册证编号/曾用注册证编号"]#line:1212
		OO00OOOO00OO000O0 ['报告日期']=pd .to_datetime (OO00OOOO00OO000O0 ['报告日期'],format ='%Y-%m-%d',errors ='coerce')#line:1215
		OO00OOOO00OO000O0 ['事件发生日期']=pd .to_datetime (OO00OOOO00OO000O0 ['事件发生日期'],format ='%Y-%m-%d',errors ='coerce')#line:1216
		OO00OOOO00OO000O0 ["报告月份"]=OO00OOOO00OO000O0 ["报告日期"].dt .to_period ("M").astype (str )#line:1218
		OO00OOOO00OO000O0 ["报告季度"]=OO00OOOO00OO000O0 ["报告日期"].dt .to_period ("Q").astype (str )#line:1219
		OO00OOOO00OO000O0 ["报告年份"]=OO00OOOO00OO000O0 ["报告日期"].dt .to_period ("Y").astype (str )#line:1220
		OO00OOOO00OO000O0 ["事件发生月份"]=OO00OOOO00OO000O0 ["事件发生日期"].dt .to_period ("M").astype (str )#line:1221
		OO00OOOO00OO000O0 ["事件发生季度"]=OO00OOOO00OO000O0 ["事件发生日期"].dt .to_period ("Q").astype (str )#line:1222
		OO00OOOO00OO000O0 ["事件发生年份"]=OO00OOOO00OO000O0 ["事件发生日期"].dt .to_period ("Y").astype (str )#line:1223
		if ini ["模式"]=="器械":#line:1227
			OO00OOOO00OO000O0 ['发现或获知日期']=pd .to_datetime (OO00OOOO00OO000O0 ['发现或获知日期'],format ='%Y-%m-%d',errors ='coerce')#line:1228
			OO00OOOO00OO000O0 ["时隔"]=pd .to_datetime (OO00OOOO00OO000O0 ["发现或获知日期"])-pd .to_datetime (OO00OOOO00OO000O0 ["事件发生日期"])#line:1229
			OO00OOOO00OO000O0 ["时隔"]=OO00OOOO00OO000O0 ["时隔"].astype (str )#line:1230
			OO00OOOO00OO000O0 ["报告时限"]=pd .to_datetime (OO00OOOO00OO000O0 ["报告日期"])-pd .to_datetime (OO00OOOO00OO000O0 ["发现或获知日期"])#line:1231
			OO00OOOO00OO000O0 ["报告时限"]=OO00OOOO00OO000O0 ["报告时限"].dt .days #line:1232
			OO00OOOO00OO000O0 .loc [(OO00OOOO00OO000O0 ["报告时限"]>20 )&(OO00OOOO00OO000O0 ["伤害"]=="严重伤害"),"超时标记"]=1 #line:1233
			OO00OOOO00OO000O0 .loc [(OO00OOOO00OO000O0 ["报告时限"]>30 )&(OO00OOOO00OO000O0 ["伤害"]=="其他"),"超时标记"]=1 #line:1234
			OO00OOOO00OO000O0 .loc [(OO00OOOO00OO000O0 ["报告时限"]>7 )&(OO00OOOO00OO000O0 ["伤害"]=="死亡"),"超时标记"]=1 #line:1235
			OO00OOOO00OO000O0 .loc [(OO00OOOO00OO000O0 ["经营企业使用单位报告状态"]=="审核通过"),"有效报告"]=1 #line:1237
		if ini ["模式"]=="药品":#line:1240
			OO00OOOO00OO000O0 ['用药开始时间']=pd .to_datetime (OO00OOOO00OO000O0 ['用药开始时间'],format ='%Y-%m-%d',errors ='coerce')#line:1241
			OO00OOOO00OO000O0 ["时隔"]=pd .to_datetime (OO00OOOO00OO000O0 ["事件发生日期"])-pd .to_datetime (OO00OOOO00OO000O0 ["用药开始时间"])#line:1242
			OO00OOOO00OO000O0 ["时隔"]=OO00OOOO00OO000O0 ["时隔"].astype (str )#line:1243
			OO00OOOO00OO000O0 ["报告时限"]=pd .to_datetime (OO00OOOO00OO000O0 ["报告日期"])-pd .to_datetime (OO00OOOO00OO000O0 ["事件发生日期"])#line:1244
			OO00OOOO00OO000O0 ["报告时限"]=OO00OOOO00OO000O0 ["报告时限"].dt .days #line:1245
			OO00OOOO00OO000O0 .loc [(OO00OOOO00OO000O0 ["报告时限"]>15 )&(OO00OOOO00OO000O0 ["报告类型-严重程度"]=="严重"),"超时标记"]=1 #line:1246
			OO00OOOO00OO000O0 .loc [(OO00OOOO00OO000O0 ["报告时限"]>30 )&(OO00OOOO00OO000O0 ["报告类型-严重程度"]=="一般"),"超时标记"]=1 #line:1247
			OO00OOOO00OO000O0 .loc [(OO00OOOO00OO000O0 ["报告时限"]>15 )&(OO00OOOO00OO000O0 ["报告类型-新的"]=="新的"),"超时标记"]=1 #line:1248
			OO00OOOO00OO000O0 .loc [(OO00OOOO00OO000O0 ["报告时限"]>1 )&(OO00OOOO00OO000O0 ["报告类型-严重程度"]=="死亡"),"超时标记"]=1 #line:1249
			OO00OOOO00OO000O0 .loc [(OO00OOOO00OO000O0 ["评价状态"]!="未评价"),"有效报告"]=1 #line:1251
		OO00OOOO00OO000O0 .loc [((OO00OOOO00OO000O0 ["年龄"]=="未填写")|OO00OOOO00OO000O0 ["年龄"].isnull ()),"年龄"]=-1 #line:1253
		OO00OOOO00OO000O0 ["年龄"]=OO00OOOO00OO000O0 ["年龄"].astype (float )#line:1254
		OO00OOOO00OO000O0 ["年龄"]=OO00OOOO00OO000O0 ["年龄"].fillna (-1 )#line:1255
		OO00OOOO00OO000O0 ["性别"]=OO00OOOO00OO000O0 ["性别"].fillna ("未填写")#line:1256
		OO00OOOO00OO000O0 ["年龄段"]="未填写"#line:1257
		try :#line:1258
			OO00OOOO00OO000O0 .loc [(OO00OOOO00OO000O0 ["年龄类型"]=="月"),"年龄"]=OO00OOOO00OO000O0 ["年龄"].values /12 #line:1259
			OO00OOOO00OO000O0 .loc [(OO00OOOO00OO000O0 ["年龄类型"]=="月"),"年龄类型"]="岁"#line:1260
		except :#line:1261
			pass #line:1262
		try :#line:1263
			OO00OOOO00OO000O0 .loc [(OO00OOOO00OO000O0 ["年龄类型"]=="天"),"年龄"]=OO00OOOO00OO000O0 ["年龄"].values /365 #line:1264
			OO00OOOO00OO000O0 .loc [(OO00OOOO00OO000O0 ["年龄类型"]=="天"),"年龄类型"]="岁"#line:1265
		except :#line:1266
			pass #line:1267
		OO00OOOO00OO000O0 .loc [(OO00OOOO00OO000O0 ["年龄"].values <=4 ),"年龄段"]="0-婴幼儿（0-4）"#line:1268
		OO00OOOO00OO000O0 .loc [(OO00OOOO00OO000O0 ["年龄"].values >=5 ),"年龄段"]="1-少儿（5-14）"#line:1269
		OO00OOOO00OO000O0 .loc [(OO00OOOO00OO000O0 ["年龄"].values >=15 ),"年龄段"]="2-青壮年（15-44）"#line:1270
		OO00OOOO00OO000O0 .loc [(OO00OOOO00OO000O0 ["年龄"].values >=45 ),"年龄段"]="3-中年期（45-64）"#line:1271
		OO00OOOO00OO000O0 .loc [(OO00OOOO00OO000O0 ["年龄"].values >=65 ),"年龄段"]="4-老年期（≥65）"#line:1272
		OO00OOOO00OO000O0 .loc [(OO00OOOO00OO000O0 ["年龄"].values ==-1 ),"年龄段"]="未填写"#line:1273
		OO00OOOO00OO000O0 ["规整后品类"]="N"#line:1277
		OO00OOOO00OO000O0 =TOOL_guizheng (OO00OOOO00OO000O0 ,2 ,True )#line:1278
		if ini ['模式']in ["器械"]:#line:1281
			OO00OOOO00OO000O0 =TOOL_guizheng (OO00OOOO00OO000O0 ,3 ,True )#line:1282
		OO00OOOO00OO000O0 =TOOL_guizheng (OO00OOOO00OO000O0 ,"课题",True )#line:1286
		try :#line:1288
			OO00OOOO00OO000O0 ["注册证编号/曾用注册证编号"]=OO00OOOO00OO000O0 ["注册证编号/曾用注册证编号"].fillna ("未填写")#line:1289
		except :#line:1290
			pass #line:1291
		OO00OOOO00OO000O0 ["数据清洗完成标记"]="是"#line:1293
		O0O000OO0000000O0 =OO00OOOO00OO000O0 .loc [:]#line:1294
		return OO00OOOO00OO000O0 #line:1295
def TOOLS_fileopen ():#line:1301
    ""#line:1302
    warnings .filterwarnings ('ignore')#line:1303
    OOOOO0OOOO00OOO00 =filedialog .askopenfilenames (filetypes =[("XLS",".xls"),("XLSX",".xlsx")])#line:1304
    O00OO00O0OOOO0000 =Useful_tools_openfiles (OOOOO0OOOO00OOO00 ,0 )#line:1305
    try :#line:1306
        O00OO00O0OOOO0000 =O00OO00O0OOOO0000 .loc [:,~O00OO00O0OOOO0000 .columns .str .contains ("^Unnamed")]#line:1307
    except :#line:1308
        pass #line:1309
    ini ["模式"]="其他"#line:1311
    O0O00O0OOO000O00O =O00OO00O0OOOO0000 #line:1312
    TABLE_tree_Level_2 (O0O00O0OOO000O00O ,0 ,O0O00O0OOO000O00O )#line:1313
def TOOLS_pinzhong (OOO0O0O0O0OO00O00 ):#line:1316
    ""#line:1317
    OOO0O0O0O0OO00O00 ["患者姓名"]=OOO0O0O0O0OO00O00 ["报告表编码"]#line:1318
    OOO0O0O0O0OO00O00 ["用量"]=OOO0O0O0O0OO00O00 ["用法用量"]#line:1319
    OOO0O0O0O0OO00O00 ["评价状态"]=OOO0O0O0O0OO00O00 ["报告单位评价"]#line:1320
    OOO0O0O0O0OO00O00 ["用量单位"]=""#line:1321
    OOO0O0O0O0OO00O00 ["单位名称"]="不适用"#line:1322
    OOO0O0O0O0OO00O00 ["报告地区名称"]="不适用"#line:1323
    OOO0O0O0O0OO00O00 ["用法-日"]="不适用"#line:1324
    OOO0O0O0O0OO00O00 ["用法-次"]="不适用"#line:1325
    OOO0O0O0O0OO00O00 ["不良反应发生时间"]=OOO0O0O0O0OO00O00 ["不良反应发生时间"].str [0 :10 ]#line:1326
    OOO0O0O0O0OO00O00 ["持有人报告状态"]="待评价"#line:1328
    OOO0O0O0O0OO00O00 =OOO0O0O0O0OO00O00 .rename (columns ={"是否非预期":"报告类型-新的","不良反应-术语":"不良反应名称","持有人/生产厂家":"上市许可持有人名称"})#line:1333
    return OOO0O0O0O0OO00O00 #line:1334
def Useful_tools_openfiles (OO0O0OOOO0OO0O00O ,OOOO000O00OOOO0OO ):#line:1339
    ""#line:1340
    O00O0OO0O0000O000 =[pd .read_excel (OOO00000000O000O0 ,header =0 ,sheet_name =OOOO000O00OOOO0OO )for OOO00000000O000O0 in OO0O0OOOO0OO0O00O ]#line:1341
    OOO00OOO000OOO00O =pd .concat (O00O0OO0O0000O000 ,ignore_index =True ).drop_duplicates ()#line:1342
    return OOO00OOO000OOO00O #line:1343
def TOOLS_allfileopen ():#line:1345
    ""#line:1346
    global ori #line:1347
    global ini #line:1348
    global data #line:1349
    ini ["原始模式"]="否"#line:1350
    warnings .filterwarnings ('ignore')#line:1351
    O000000OOO0OOOO00 =filedialog .askopenfilenames (filetypes =[("XLS",".xls"),("XLSX",".xlsx")])#line:1353
    ori =Useful_tools_openfiles (O000000OOO0OOOO00 ,0 )#line:1354
    try :#line:1358
        O0OOO00O00OOO00OO =Useful_tools_openfiles (O000000OOO0OOOO00 ,"报告信息")#line:1359
        if "是否非预期"in O0OOO00O00OOO00OO .columns :#line:1360
            ori =TOOLS_pinzhong (O0OOO00O00OOO00OO )#line:1361
    except :#line:1362
        pass #line:1363
    ini ["模式"]="其他"#line:1365
    try :#line:1367
        ori =Useful_tools_openfiles (O000000OOO0OOOO00 ,"字典数据")#line:1368
        ini ["原始模式"]="是"#line:1369
        if "UDI"in ori .columns :#line:1370
            ini ["模式"]="器械"#line:1371
            data =ori #line:1372
        if "报告类型-新的"in ori .columns :#line:1373
            ini ["模式"]="药品"#line:1374
            data =ori #line:1375
        else :#line:1376
            ini ["模式"]="其他"#line:1377
    except :#line:1378
        pass #line:1379
    try :#line:1382
        ori =ori .loc [:,~ori .columns .str .contains ("^Unnamed")]#line:1383
    except :#line:1384
        pass #line:1385
    if "UDI"in ori .columns and ini ["原始模式"]!="是":#line:1389
        text .insert (END ,"识别出为器械报表,正在进行数据规整...")#line:1390
        ini ["模式"]="器械"#line:1391
        ori =CLEAN_qx (ori )#line:1392
        data =ori #line:1393
    if "报告类型-新的"in ori .columns and ini ["原始模式"]!="是":#line:1394
        text .insert (END ,"识别出为药品报表,正在进行数据规整...")#line:1395
        ini ["模式"]="药品"#line:1396
        ori =CLEAN_yp (ori )#line:1397
        ori =CLEAN_qx (ori )#line:1398
        data =ori #line:1399
    if "光斑贴试验"in ori .columns and ini ["原始模式"]!="是":#line:1400
        text .insert (END ,"识别出为化妆品报表,正在进行数据规整...")#line:1401
        ini ["模式"]="化妆品"#line:1402
        ori =CLEAN_hzp (ori )#line:1403
        ori =CLEAN_qx (ori )#line:1404
        data =ori #line:1405
    if ini ["模式"]=="其他":#line:1408
        text .insert (END ,"\n数据读取成功，行数："+str (len (ori )))#line:1409
        data =ori #line:1410
        PROGRAM_Menubar (root ,data ,0 ,data )#line:1411
        try :#line:1412
            ini ["button"][0 ].pack_forget ()#line:1413
            ini ["button"][1 ].pack_forget ()#line:1414
            ini ["button"][2 ].pack_forget ()#line:1415
            ini ["button"][3 ].pack_forget ()#line:1416
            ini ["button"][4 ].pack_forget ()#line:1417
        except :#line:1418
            pass #line:1419
    else :#line:1421
        ini ["清洗后的文件"]=data #line:1422
        ini ["证号"]=Countall (data ).df_zhenghao ()#line:1423
        text .insert (END ,"\n数据读取成功，行数："+str (len (data )))#line:1424
        PROGRAM_Menubar (root ,data ,0 ,data )#line:1425
        try :#line:1426
            ini ["button"][0 ].pack_forget ()#line:1427
            ini ["button"][1 ].pack_forget ()#line:1428
            ini ["button"][2 ].pack_forget ()#line:1429
            ini ["button"][3 ].pack_forget ()#line:1430
            ini ["button"][4 ].pack_forget ()#line:1431
        except :#line:1432
            pass #line:1433
        OOOOOO0O00OOO00OO =Button (frame0 ,text ="地市统计",bg ="white",height =2 ,width =12 ,font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :TABLE_tree_Level_2 (Countall (data ).df_org ("市级监测机构"),1 ,ori ),)#line:1444
        OOOOOO0O00OOO00OO .pack ()#line:1445
        O000O0OOO000OOOO0 =Button (frame0 ,text ="县区统计",bg ="white",height =2 ,width =12 ,font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :TABLE_tree_Level_2 (Countall (data ).df_org ("监测机构"),1 ,ori ),)#line:1458
        O000O0OOO000OOOO0 .pack ()#line:1459
        OO00O00O00OOO0000 =Button (frame0 ,text ="上报单位",bg ="white",height =2 ,width =12 ,font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :TABLE_tree_Level_2 (Countall (data ).df_user (),1 ,ori ),)#line:1472
        OO00O00O00OOO0000 .pack ()#line:1473
        O0O0000O0O0OOO00O =Button (frame0 ,text ="生产企业",bg ="white",height =2 ,width =12 ,font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :TABLE_tree_Level_2 (Countall (data ).df_chiyouren (),1 ,ori ),)#line:1484
        O0O0000O0O0OOO00O .pack ()#line:1485
        OO00O000O000O0000 =Button (frame0 ,text ="产品统计",bg ="white",height =2 ,width =12 ,font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :TABLE_tree_Level_2 (ini ["证号"],1 ,ori ,ori ,"dfx_zhenghao"),)#line:1496
        OO00O000O000O0000 .pack ()#line:1497
        ini ["button"]=[OOOOOO0O00OOO00OO ,O000O0OOO000OOOO0 ,OO00O00O00OOO0000 ,O0O0000O0O0OOO00O ,OO00O000O000O0000 ]#line:1498
    text .insert (END ,"\n")#line:1500
def TOOLS_sql (O0OO0O0O00O000O0O ):#line:1502
    ""#line:1503
    warnings .filterwarnings ("ignore")#line:1504
    try :#line:1505
        O000O0O0OOO0O0O0O =O0OO0O0O00O000O0O .columns #line:1506
    except :#line:1507
        return 0 #line:1508
    def O000OO0OOOO0OOO00 (OOOO000O0O0OOO00O ):#line:1510
        try :#line:1511
            OO00O0OOOOOOOO0O0 =pd .read_sql_query (sqltext (OOOO000O0O0OOO00O ),con =O00OOOO00O000O0O0 )#line:1512
        except :#line:1513
            showinfo (title ="提示",message ="SQL语句有误。")#line:1514
            return 0 #line:1515
        try :#line:1516
            del OO00O0OOOOOOOO0O0 ["level_0"]#line:1517
        except :#line:1518
            pass #line:1519
        TABLE_tree_Level_2 (OO00O0OOOOOOOO0O0 ,1 ,O0OO0O0O00O000O0O )#line:1520
    O000OO0OOOOOOO00O ='sqlite://'#line:1524
    OOO0O0O0000000OOO =create_engine (O000OO0OOOOOOO00O )#line:1525
    try :#line:1526
        O0OO0O0O00O000O0O .to_sql ('data',con =OOO0O0O0000000OOO ,chunksize =10000 ,if_exists ='replace',index =True )#line:1527
    except :#line:1528
        showinfo (title ="提示",message ="不支持该表格。")#line:1529
        return 0 #line:1530
    O00OOOO00O000O0O0 =OOO0O0O0000000OOO .connect ()#line:1532
    O00OOO0000O0O00OO ="select * from data"#line:1533
    OOOOO0OOO0O0OOOOO =Toplevel ()#line:1536
    OOOOO0OOO0O0OOOOO .title ("SQL查询")#line:1537
    OOOOO0OOO0O0OOOOO .geometry ("700x500")#line:1538
    OOO0O00O00O00000O =ttk .Frame (OOOOO0OOO0O0OOOOO ,width =700 ,height =20 )#line:1540
    OOO0O00O00O00000O .pack (side =TOP )#line:1541
    O00000OOO000O00OO =ttk .Frame (OOOOO0OOO0O0OOOOO ,width =700 ,height =20 )#line:1542
    O00000OOO000O00OO .pack (side =BOTTOM )#line:1543
    try :#line:1546
        OO0O0OO0OO00000O0 =StringVar ()#line:1547
        OO0O0OO0OO00000O0 .set ("select * from data WHERE 单位名称='佛山市第一人民医院'")#line:1548
        OOO00000O00OOOOOO =Label (OOO0O00O00O00000O ,text ="SQL查询",anchor ='w')#line:1550
        OOO00000O00OOOOOO .pack (side =LEFT )#line:1551
        O0000O000O00OOOOO =Label (OOO0O00O00O00000O ,text ="检索：")#line:1552
        OOOO0O00OO0O000O0 =Button (O00000OOO000O00OO ,text ="执行",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",width =700 ,command =lambda :O000OO0OOOO0OOO00 (O0OO0O0OO0OOOOO00 .get ("1.0","end")),)#line:1566
        OOOO0O00OO0O000O0 .pack (side =LEFT )#line:1567
    except EE :#line:1570
        pass #line:1571
    OOOO00OO00OOOOO00 =Scrollbar (OOOOO0OOO0O0OOOOO )#line:1573
    O0OO0O0OO0OOOOO00 =Text (OOOOO0OOO0O0OOOOO ,height =80 ,width =150 ,bg ="#FFFFFF",font ="微软雅黑")#line:1574
    OOOO00OO00OOOOO00 .pack (side =RIGHT ,fill =Y )#line:1575
    O0OO0O0OO0OOOOO00 .pack ()#line:1576
    OOOO00OO00OOOOO00 .config (command =O0OO0O0OO0OOOOO00 .yview )#line:1577
    O0OO0O0OO0OOOOO00 .config (yscrollcommand =OOOO00OO00OOOOO00 .set )#line:1578
    def O00O0O0O0O00O00O0 (event =None ):#line:1579
        O0OO0O0OO0OOOOO00 .event_generate ('<<Copy>>')#line:1580
    def O0OO0OOO00OOO00O0 (event =None ):#line:1581
        O0OO0O0OO0OOOOO00 .event_generate ('<<Paste>>')#line:1582
    def OOO000OO0OO000O00 (OO0000OOO00O0O0O0 ,O0OO0O0OOO0OO00O0 ):#line:1583
         TOOLS_savetxt (OO0000OOO00O0O0O0 ,O0OO0O0OOO0OO00O0 ,1 )#line:1584
    OOO0OO00OO0O000OO =Menu (O0OO0O0OO0OOOOO00 ,tearoff =False ,)#line:1585
    OOO0OO00OO0O000OO .add_command (label ="复制",command =O00O0O0O0O00O00O0 )#line:1586
    OOO0OO00OO0O000OO .add_command (label ="粘贴",command =O0OO0OOO00OOO00O0 )#line:1587
    OOO0OO00OO0O000OO .add_command (label ="源文件列",command =lambda :PROGRAM_helper (O0OO0O0O00O000O0O .columns .to_list ()))#line:1588
    def O00OOOO00OO0OOOO0 (OOOO0000O000OOO00 ):#line:1589
         OOO0OO00OO0O000OO .post (OOOO0000O000OOO00 .x_root ,OOOO0000O000OOO00 .y_root )#line:1590
    O0OO0O0OO0OOOOO00 .bind ("<Button-3>",O00OOOO00OO0OOOO0 )#line:1591
    O0OO0O0OO0OOOOO00 .insert (END ,O00OOO0000O0O00OO )#line:1595
def TOOLS_view_dict (O0OOOOOO0O0O0OO00 ,OO00OOOO00000000O ):#line:1599
    ""#line:1600
    O0O000O0OOOOO0O0O =Toplevel ()#line:1601
    O0O000O0OOOOO0O0O .title ("查看数据")#line:1602
    O0O000O0OOOOO0O0O .geometry ("700x500")#line:1603
    OO0OO000OOO000OO0 =Scrollbar (O0O000O0OOOOO0O0O )#line:1605
    O00O0O0OO0O00O0OO =Text (O0O000O0OOOOO0O0O ,height =100 ,width =150 )#line:1606
    OO0OO000OOO000OO0 .pack (side =RIGHT ,fill =Y )#line:1607
    O00O0O0OO0O00O0OO .pack ()#line:1608
    OO0OO000OOO000OO0 .config (command =O00O0O0OO0O00O0OO .yview )#line:1609
    O00O0O0OO0O00O0OO .config (yscrollcommand =OO0OO000OOO000OO0 .set )#line:1610
    if OO00OOOO00000000O ==1 :#line:1611
        O00O0O0OO0O00O0OO .insert (END ,O0OOOOOO0O0O0OO00 )#line:1613
        O00O0O0OO0O00O0OO .insert (END ,"\n\n")#line:1614
        return 0 #line:1615
    for OOOOO00OOO000O00O in range (len (O0OOOOOO0O0O0OO00 )):#line:1616
        O00O0O0OO0O00O0OO .insert (END ,O0OOOOOO0O0O0OO00 .iloc [OOOOO00OOO000O00O ,0 ])#line:1617
        O00O0O0OO0O00O0OO .insert (END ,":")#line:1618
        O00O0O0OO0O00O0OO .insert (END ,O0OOOOOO0O0O0OO00 .iloc [OOOOO00OOO000O00O ,1 ])#line:1619
        O00O0O0OO0O00O0OO .insert (END ,"\n\n")#line:1620
def TOOLS_save_dict (O00O000OO00O000OO ):#line:1622
    ""#line:1623
    OOOO0O0O00O0O000O =filedialog .asksaveasfilename (title =u"保存文件",initialfile ="排序后的原始数据",defaultextension ="xls",filetypes =[("Excel 97-2003 工作簿","*.xls")],)#line:1629
    try :#line:1630
        O00O000OO00O000OO ["详细描述T"]=O00O000OO00O000OO ["详细描述T"].astype (str )#line:1631
    except :#line:1632
        pass #line:1633
    try :#line:1634
        O00O000OO00O000OO ["报告编码"]=O00O000OO00O000OO ["报告编码"].astype (str )#line:1635
    except :#line:1636
        pass #line:1637
    OOOOOOO0O0O000OO0 =pd .ExcelWriter (OOOO0O0O00O0O000O ,engine ="xlsxwriter")#line:1639
    O00O000OO00O000OO .to_excel (OOOOOOO0O0O000OO0 ,sheet_name ="字典数据")#line:1640
    OOOOOOO0O0O000OO0 .close ()#line:1641
    showinfo (title ="提示",message ="文件写入成功。")#line:1642
def TOOLS_savetxt (O0O0O0OOOOOO0O0O0 ,OOOO0O0OO0O0O000O ,OO0000O0O00000OO0 ):#line:1644
	""#line:1645
	OO0000OOOO0O0OO00 =open (OOOO0O0OO0O0O000O ,"w",encoding ='utf-8')#line:1646
	OO0000OOOO0O0OO00 .write (O0O0O0OOOOOO0O0O0 )#line:1647
	OO0000OOOO0O0OO00 .flush ()#line:1649
	if OO0000O0O00000OO0 ==1 :#line:1650
		showinfo (title ="提示信息",message ="保存成功。")#line:1651
def TOOLS_deep_view (OOOOOO0O0O0000OO0 ,OOO00OOO00OOOO0OO ,OOO000O0O00OOO00O ,OO0OO00O0000OO0O0 ):#line:1654
    ""#line:1655
    if OO0OO00O0000OO0O0 ==0 :#line:1656
        try :#line:1657
            OOOOOO0O0O0000OO0 [OOO00OOO00OOOO0OO ]=OOOOOO0O0O0000OO0 [OOO00OOO00OOOO0OO ].fillna ("这个没有填写")#line:1658
        except :#line:1659
            pass #line:1660
        O000000OOO00O00OO =OOOOOO0O0O0000OO0 .groupby (OOO00OOO00OOOO0OO ).agg (计数 =(OOO000O0O00OOO00O [0 ],OOO000O0O00OOO00O [1 ]))#line:1661
    if OO0OO00O0000OO0O0 ==1 :#line:1662
            O000000OOO00O00OO =pd .pivot_table (OOOOOO0O0O0000OO0 ,index =OOO00OOO00OOOO0OO [:-1 ],columns =OOO00OOO00OOOO0OO [-1 ],values =[OOO000O0O00OOO00O [0 ]],aggfunc ={OOO000O0O00OOO00O [0 ]:OOO000O0O00OOO00O [1 ]},fill_value ="0",margins =True ,dropna =False ,)#line:1673
            O000000OOO00O00OO .columns =O000000OOO00O00OO .columns .droplevel (0 )#line:1674
            O000000OOO00O00OO =O000000OOO00O00OO .rename (columns ={"All":"计数"})#line:1675
    if "日期"in OOO00OOO00OOOO0OO or "时间"in OOO00OOO00OOOO0OO or "季度"in OOO00OOO00OOOO0OO :#line:1678
        O000000OOO00O00OO =O000000OOO00O00OO .sort_values ([OOO00OOO00OOOO0OO ],ascending =False ,na_position ="last")#line:1681
    else :#line:1682
        O000000OOO00O00OO =O000000OOO00O00OO .sort_values (by =["计数"],ascending =False ,na_position ="last")#line:1686
    O000000OOO00O00OO =O000000OOO00O00OO .reset_index ()#line:1687
    O000000OOO00O00OO ["构成比(%)"]=round (100 *O000000OOO00O00OO ["计数"]/O000000OOO00O00OO ["计数"].sum (),2 )#line:1688
    if "计数"in O000000OOO00O00OO .columns and OO0OO00O0000OO0O0 ==1 :#line:1689
        O000000OOO00O00OO ["构成比(%)"]=O000000OOO00O00OO ["构成比(%)"]*2 #line:1690
    if OO0OO00O0000OO0O0 ==0 :#line:1691
        O000000OOO00O00OO ["报表类型"]="dfx_deepview"+"_"+str (OOO00OOO00OOOO0OO )#line:1692
    if OO0OO00O0000OO0O0 ==1 :#line:1693
        O000000OOO00O00OO ["报表类型"]="dfx_deepview"+"_"+str (OOO00OOO00OOOO0OO [:-1 ])#line:1694
    return O000000OOO00O00OO #line:1695
def TOOLS_easyreadT (O000O00O00OO0000O ):#line:1699
    ""#line:1700
    O000O00O00OO0000O ["#####分隔符#########"]="######################################################################"#line:1703
    O000OO0OOO0000000 =O000O00O00OO0000O .stack (dropna =False )#line:1704
    O000OO0OOO0000000 =pd .DataFrame (O000OO0OOO0000000 ).reset_index ()#line:1705
    O000OO0OOO0000000 .columns =["序号","条目","详细描述T"]#line:1706
    O000OO0OOO0000000 ["逐条查看"]="逐条查看"#line:1707
    O000OO0OOO0000000 ["报表类型"]="逐条查看"#line:1708
    return O000OO0OOO0000000 #line:1709
def TOOLS_data_masking (OO000OOO0O000OO0O ):#line:1711
    ""#line:1712
    from random import choices #line:1713
    from string import ascii_letters ,digits #line:1714
    OO000OOO0O000OO0O =OO000OOO0O000OO0O .reset_index (drop =True )#line:1716
    if "单位名称.1"in OO000OOO0O000OO0O .columns :#line:1717
        OO0O000OOOO00O0OO ="器械"#line:1718
    else :#line:1719
        OO0O000OOOO00O0OO ="药品"#line:1720
    O00000OO0OO0O0O00 =peizhidir +""+"0（范例）数据脱敏"+".xls"#line:1721
    try :#line:1722
        OO0OO0O0O00O000O0 =pd .read_excel (O00000OO0OO0O0O00 ,sheet_name =OO0O000OOOO00O0OO ,header =0 ,index_col =0 ).reset_index ()#line:1725
    except :#line:1726
        showinfo (title ="错误信息",message ="该功能需要配置文件才能使用！")#line:1727
        return 0 #line:1728
    O0OOO000OOO0O0OOO =0 #line:1729
    O0000O0OO0O000000 =len (OO000OOO0O000OO0O )#line:1730
    OO000OOO0O000OO0O ["abcd"]="□"#line:1731
    for OOOO0OO0OO000O0OO in OO0OO0O0O00O000O0 ["要脱敏的列"]:#line:1732
        O0OOO000OOO0O0OOO =O0OOO000OOO0O0OOO +1 #line:1733
        PROGRAM_change_schedule (O0OOO000OOO0O0OOO ,O0000O0OO0O000000 )#line:1734
        text .insert (END ,"\n正在对以下列进行脱敏处理：")#line:1735
        text .see (END )#line:1736
        text .insert (END ,OOOO0OO0OO000O0OO )#line:1737
        try :#line:1738
            O00O0000OOOO0OOOO =set (OO000OOO0O000OO0O [OOOO0OO0OO000O0OO ])#line:1739
        except :#line:1740
            showinfo (title ="提示",message ="脱敏文件配置错误，请修改配置表。")#line:1741
            return 0 #line:1742
        OOO0000O0OO0O0OO0 ={OOOOO0O0O0000OO00 :"".join (choices (digits ,k =10 ))for OOOOO0O0O0000OO00 in O00O0000OOOO0OOOO }#line:1743
        OO000OOO0O000OO0O [OOOO0OO0OO000O0OO ]=OO000OOO0O000OO0O [OOOO0OO0OO000O0OO ].map (OOO0000O0OO0O0OO0 )#line:1744
        OO000OOO0O000OO0O [OOOO0OO0OO000O0OO ]=OO000OOO0O000OO0O ["abcd"]+OO000OOO0O000OO0O [OOOO0OO0OO000O0OO ].astype (str )#line:1745
    try :#line:1746
        PROGRAM_change_schedule (10 ,10 )#line:1747
        del OO000OOO0O000OO0O ["abcd"]#line:1748
        O0O000O0000O0O000 =filedialog .asksaveasfilename (title =u"保存脱敏后的文件",initialfile ="脱敏后的文件",defaultextension ="xlsx",filetypes =[("Excel 工作簿","*.xlsx"),("Excel 97-2003 工作簿","*.xls")],)#line:1754
        OO0O000OO0O0OO00O =pd .ExcelWriter (O0O000O0000O0O000 ,engine ="xlsxwriter")#line:1755
        OO000OOO0O000OO0O .to_excel (OO0O000OO0O0OO00O ,sheet_name ="sheet0")#line:1756
        OO0O000OO0O0OO00O .close ()#line:1757
    except :#line:1758
        text .insert (END ,"\n文件未保存，但导入的数据已按要求脱敏。")#line:1759
    text .insert (END ,"\n脱敏操作完成。")#line:1760
    text .see (END )#line:1761
    return OO000OOO0O000OO0O #line:1762
def TOOLS_get_new (O0OOOOOOOOO0OO0OO ,OO0OOO00OOO00OOO0 ):#line:1764
	""#line:1765
	def OOOOOO0000OOOO0O0 (O0O00O000O0O00O0O ):#line:1766
		""#line:1767
		O0O00O000O0O00O0O =O0O00O000O0O00O0O .drop_duplicates ("报告编码")#line:1768
		OOOO000OOO0O00O0O =str (Counter (TOOLS_get_list0 ("use(器械故障表现).file",O0O00O000O0O00O0O ,1000 ))).replace ("Counter({","{")#line:1769
		OOOO000OOO0O00O0O =OOOO000OOO0O00O0O .replace ("})","}")#line:1770
		import ast #line:1771
		OO00OOOO00O0O0000 =ast .literal_eval (OOOO000OOO0O00O0O )#line:1772
		O000O00O0000OO000 =TOOLS_easyreadT (pd .DataFrame ([OO00OOOO00O0O0000 ]))#line:1773
		O000O00O0000OO000 =O000O00O0000OO000 .rename (columns ={"逐条查看":"ADR名称规整"})#line:1774
		return O000O00O0000OO000 #line:1775
	if OO0OOO00OOO00OOO0 =="证号":#line:1776
		root .attributes ("-topmost",True )#line:1777
		root .attributes ("-topmost",False )#line:1778
		O00O0OO0O00OO00OO =O0OOOOOOOOO0OO0OO .groupby (["上市许可持有人名称","产品类别","产品名称","注册证编号/曾用注册证编号"]).agg (计数 =("报告编码","nunique")).reset_index ()#line:1779
		OOOOO00OOOO0O00O0 =O00O0OO0O00OO00OO .drop_duplicates ("注册证编号/曾用注册证编号").copy ()#line:1780
		OOOOO00OOOO0O00O0 ["所有不良反应"]=""#line:1781
		OOOOO00OOOO0O00O0 ["关注建议"]=""#line:1782
		OOOOO00OOOO0O00O0 ["疑似新的"]=""#line:1783
		OOOOO00OOOO0O00O0 ["疑似旧的"]=""#line:1784
		OOOOO00OOOO0O00O0 ["疑似新的（高敏）"]=""#line:1785
		OOOOO00OOOO0O00O0 ["疑似旧的（高敏）"]=""#line:1786
		OO0OO0OOO000000O0 =1 #line:1787
		OO0OO0O00OOO00OO0 =int (len (OOOOO00OOOO0O00O0 ))#line:1788
		for O00O000O00OOO00OO ,OOOOOOO0O0O0O0O0O in OOOOO00OOOO0O00O0 .iterrows ():#line:1789
			OO00000O00000O000 =O0OOOOOOOOO0OO0OO [(O0OOOOOOOOO0OO0OO ["注册证编号/曾用注册证编号"]==OOOOOOO0O0O0O0O0O ["注册证编号/曾用注册证编号"])]#line:1790
			OOO000O000000O0OO =OO00000O00000O000 .loc [OO00000O00000O000 ["报告类型-新的"].str .contains ("新",na =False )].copy ()#line:1791
			OO0000O00OO00O0OO =OO00000O00000O000 .loc [~OO00000O00000O000 ["报告类型-新的"].str .contains ("新",na =False )].copy ()#line:1792
			OOO0OOO0O0OO00O00 =OOOOOO0000OOOO0O0 (OOO000O000000O0OO )#line:1793
			OO0000O0O0OO0OO00 =OOOOOO0000OOOO0O0 (OO0000O00OO00O0OO )#line:1794
			OOO000O0OOOO000OO =OOOOOO0000OOOO0O0 (OO00000O00000O000 )#line:1795
			PROGRAM_change_schedule (OO0OO0OOO000000O0 ,OO0OO0O00OOO00OO0 )#line:1796
			OO0OO0OOO000000O0 =OO0OO0OOO000000O0 +1 #line:1797
			for O0OO0O00OO000OO0O ,O0OOOO0O0OOO0OO00 in OOO000O0OOOO000OO .iterrows ():#line:1799
					if "分隔符"not in O0OOOO0O0OOO0OO00 ["条目"]:#line:1800
						O0O0000OOOOOOOOO0 ="'"+str (O0OOOO0O0OOO0OO00 ["条目"])+"':"+str (O0OOOO0O0OOO0OO00 ["详细描述T"])+","#line:1801
						OOOOO00OOOO0O00O0 .loc [O00O000O00OOO00OO ,"所有不良反应"]=OOOOO00OOOO0O00O0 .loc [O00O000O00OOO00OO ,"所有不良反应"]+O0O0000OOOOOOOOO0 #line:1802
			for O0OO0O00OO000OO0O ,O0OOOO0O0OOO0OO00 in OO0000O0O0OO0OO00 .iterrows ():#line:1804
					if "分隔符"not in O0OOOO0O0OOO0OO00 ["条目"]:#line:1805
						O0O0000OOOOOOOOO0 ="'"+str (O0OOOO0O0OOO0OO00 ["条目"])+"':"+str (O0OOOO0O0OOO0OO00 ["详细描述T"])+","#line:1806
						OOOOO00OOOO0O00O0 .loc [O00O000O00OOO00OO ,"疑似旧的"]=OOOOO00OOOO0O00O0 .loc [O00O000O00OOO00OO ,"疑似旧的"]+O0O0000OOOOOOOOO0 #line:1807
					if "分隔符"not in O0OOOO0O0OOO0OO00 ["条目"]and int (O0OOOO0O0OOO0OO00 ["详细描述T"])>=2 :#line:1809
						O0O0000OOOOOOOOO0 ="'"+str (O0OOOO0O0OOO0OO00 ["条目"])+"':"+str (O0OOOO0O0OOO0OO00 ["详细描述T"])+","#line:1810
						OOOOO00OOOO0O00O0 .loc [O00O000O00OOO00OO ,"疑似旧的（高敏）"]=OOOOO00OOOO0O00O0 .loc [O00O000O00OOO00OO ,"疑似旧的（高敏）"]+O0O0000OOOOOOOOO0 #line:1811
			for O0OO0O00OO000OO0O ,O0OOOO0O0OOO0OO00 in OOO0OOO0O0OO00O00 .iterrows ():#line:1813
				if str (O0OOOO0O0OOO0OO00 ["条目"]).strip ()not in str (OOOOO00OOOO0O00O0 .loc [O00O000O00OOO00OO ,"疑似旧的"])and "分隔符"not in str (O0OOOO0O0OOO0OO00 ["条目"]):#line:1814
					O0O0000OOOOOOOOO0 ="'"+str (O0OOOO0O0OOO0OO00 ["条目"])+"':"+str (O0OOOO0O0OOO0OO00 ["详细描述T"])+","#line:1815
					OOOOO00OOOO0O00O0 .loc [O00O000O00OOO00OO ,"疑似新的"]=OOOOO00OOOO0O00O0 .loc [O00O000O00OOO00OO ,"疑似新的"]+O0O0000OOOOOOOOO0 #line:1816
					if int (O0OOOO0O0OOO0OO00 ["详细描述T"])>=3 :#line:1817
						OOOOO00OOOO0O00O0 .loc [O00O000O00OOO00OO ,"关注建议"]=OOOOO00OOOO0O00O0 .loc [O00O000O00OOO00OO ,"关注建议"]+"！"#line:1818
					if int (O0OOOO0O0OOO0OO00 ["详细描述T"])>=5 :#line:1819
						OOOOO00OOOO0O00O0 .loc [O00O000O00OOO00OO ,"关注建议"]=OOOOO00OOOO0O00O0 .loc [O00O000O00OOO00OO ,"关注建议"]+"●"#line:1820
				if str (O0OOOO0O0OOO0OO00 ["条目"]).strip ()not in str (OOOOO00OOOO0O00O0 .loc [O00O000O00OOO00OO ,"疑似旧的（高敏）"])and "分隔符"not in str (O0OOOO0O0OOO0OO00 ["条目"])and int (O0OOOO0O0OOO0OO00 ["详细描述T"])>=2 :#line:1822
					O0O0000OOOOOOOOO0 ="'"+str (O0OOOO0O0OOO0OO00 ["条目"])+"':"+str (O0OOOO0O0OOO0OO00 ["详细描述T"])+","#line:1823
					OOOOO00OOOO0O00O0 .loc [O00O000O00OOO00OO ,"疑似新的（高敏）"]=OOOOO00OOOO0O00O0 .loc [O00O000O00OOO00OO ,"疑似新的（高敏）"]+O0O0000OOOOOOOOO0 #line:1824
		OOOOO00OOOO0O00O0 ["疑似新的"]="{"+OOOOO00OOOO0O00O0 ["疑似新的"]+"}"#line:1826
		OOOOO00OOOO0O00O0 ["疑似旧的"]="{"+OOOOO00OOOO0O00O0 ["疑似旧的"]+"}"#line:1827
		OOOOO00OOOO0O00O0 ["所有不良反应"]="{"+OOOOO00OOOO0O00O0 ["所有不良反应"]+"}"#line:1828
		OOOOO00OOOO0O00O0 ["疑似新的（高敏）"]="{"+OOOOO00OOOO0O00O0 ["疑似新的（高敏）"]+"}"#line:1829
		OOOOO00OOOO0O00O0 ["疑似旧的（高敏）"]="{"+OOOOO00OOOO0O00O0 ["疑似旧的（高敏）"]+"}"#line:1830
		OOOOO00OOOO0O00O0 =OOOOO00OOOO0O00O0 .rename (columns ={"器械待评价(药品新的报告比例)":"新的报告比例"})#line:1832
		OOOOO00OOOO0O00O0 =OOOOO00OOOO0O00O0 .rename (columns ={"严重伤害待评价比例(药品严重中新的比例)":"严重报告中新的比例"})#line:1833
		OOOOO00OOOO0O00O0 ["报表类型"]="dfx_zhenghao"#line:1834
		O000O0OOO00OOO0O0 =pd .pivot_table (O0OOOOOOOOO0OO0OO ,values =["报告编码"],index =["注册证编号/曾用注册证编号"],columns ="报告单位评价",aggfunc ={"报告编码":"nunique"},fill_value ="0",margins =True ,dropna =False ,).rename (columns ={"报告编码":"数量"})#line:1836
		O000O0OOO00OOO0O0 .columns =O000O0OOO00OOO0O0 .columns .droplevel (0 )#line:1837
		OOOOO00OOOO0O00O0 =pd .merge (OOOOO00OOOO0O00O0 ,O000O0OOO00OOO0O0 .reset_index (),on =["注册证编号/曾用注册证编号"],how ="left")#line:1838
		TABLE_tree_Level_2 (OOOOO00OOOO0O00O0 .sort_values (by ="计数",ascending =[False ],na_position ="last"),1 ,O0OOOOOOOOO0OO0OO )#line:1842
	if OO0OOO00OOO00OOO0 =="品种":#line:1843
		root .attributes ("-topmost",True )#line:1844
		root .attributes ("-topmost",False )#line:1845
		O00O0OO0O00OO00OO =O0OOOOOOOOO0OO0OO .groupby (["产品类别","产品名称"]).agg (计数 =("报告编码","nunique")).reset_index ()#line:1846
		OOOOO00OOOO0O00O0 =O00O0OO0O00OO00OO .drop_duplicates ("产品名称").copy ()#line:1847
		OOOOO00OOOO0O00O0 ["产品名称"]=OOOOO00OOOO0O00O0 ["产品名称"].str .replace ("*","",regex =False )#line:1848
		OOOOO00OOOO0O00O0 ["所有不良反应"]=""#line:1849
		OOOOO00OOOO0O00O0 ["关注建议"]=""#line:1850
		OOOOO00OOOO0O00O0 ["疑似新的"]=""#line:1851
		OOOOO00OOOO0O00O0 ["疑似旧的"]=""#line:1852
		OOOOO00OOOO0O00O0 ["疑似新的（高敏）"]=""#line:1853
		OOOOO00OOOO0O00O0 ["疑似旧的（高敏）"]=""#line:1854
		OO0OO0OOO000000O0 =1 #line:1855
		OO0OO0O00OOO00OO0 =int (len (OOOOO00OOOO0O00O0 ))#line:1856
		for O00O000O00OOO00OO ,OOOOOOO0O0O0O0O0O in OOOOO00OOOO0O00O0 .iterrows ():#line:1859
			OO00000O00000O000 =O0OOOOOOOOO0OO0OO [(O0OOOOOOOOO0OO0OO ["产品名称"]==OOOOOOO0O0O0O0O0O ["产品名称"])]#line:1861
			OOO000O000000O0OO =OO00000O00000O000 .loc [OO00000O00000O000 ["报告类型-新的"].str .contains ("新",na =False )].copy ()#line:1863
			OO0000O00OO00O0OO =OO00000O00000O000 .loc [~OO00000O00000O000 ["报告类型-新的"].str .contains ("新",na =False )].copy ()#line:1864
			OOO000O0OOOO000OO =OOOOOO0000OOOO0O0 (OO00000O00000O000 )#line:1865
			OOO0OOO0O0OO00O00 =OOOOOO0000OOOO0O0 (OOO000O000000O0OO )#line:1866
			OO0000O0O0OO0OO00 =OOOOOO0000OOOO0O0 (OO0000O00OO00O0OO )#line:1867
			PROGRAM_change_schedule (OO0OO0OOO000000O0 ,OO0OO0O00OOO00OO0 )#line:1868
			OO0OO0OOO000000O0 =OO0OO0OOO000000O0 +1 #line:1869
			for O0OO0O00OO000OO0O ,O0OOOO0O0OOO0OO00 in OOO000O0OOOO000OO .iterrows ():#line:1871
					if "分隔符"not in O0OOOO0O0OOO0OO00 ["条目"]:#line:1872
						O0O0000OOOOOOOOO0 ="'"+str (O0OOOO0O0OOO0OO00 ["条目"])+"':"+str (O0OOOO0O0OOO0OO00 ["详细描述T"])+","#line:1873
						OOOOO00OOOO0O00O0 .loc [O00O000O00OOO00OO ,"所有不良反应"]=OOOOO00OOOO0O00O0 .loc [O00O000O00OOO00OO ,"所有不良反应"]+O0O0000OOOOOOOOO0 #line:1874
			for O0OO0O00OO000OO0O ,O0OOOO0O0OOO0OO00 in OO0000O0O0OO0OO00 .iterrows ():#line:1877
					if "分隔符"not in O0OOOO0O0OOO0OO00 ["条目"]:#line:1878
						O0O0000OOOOOOOOO0 ="'"+str (O0OOOO0O0OOO0OO00 ["条目"])+"':"+str (O0OOOO0O0OOO0OO00 ["详细描述T"])+","#line:1879
						OOOOO00OOOO0O00O0 .loc [O00O000O00OOO00OO ,"疑似旧的"]=OOOOO00OOOO0O00O0 .loc [O00O000O00OOO00OO ,"疑似旧的"]+O0O0000OOOOOOOOO0 #line:1880
					if "分隔符"not in O0OOOO0O0OOO0OO00 ["条目"]and int (O0OOOO0O0OOO0OO00 ["详细描述T"])>=2 :#line:1882
						O0O0000OOOOOOOOO0 ="'"+str (O0OOOO0O0OOO0OO00 ["条目"])+"':"+str (O0OOOO0O0OOO0OO00 ["详细描述T"])+","#line:1883
						OOOOO00OOOO0O00O0 .loc [O00O000O00OOO00OO ,"疑似旧的（高敏）"]=OOOOO00OOOO0O00O0 .loc [O00O000O00OOO00OO ,"疑似旧的（高敏）"]+O0O0000OOOOOOOOO0 #line:1884
			for O0OO0O00OO000OO0O ,O0OOOO0O0OOO0OO00 in OOO0OOO0O0OO00O00 .iterrows ():#line:1886
				if str (O0OOOO0O0OOO0OO00 ["条目"]).strip ()not in str (OOOOO00OOOO0O00O0 .loc [O00O000O00OOO00OO ,"疑似旧的"])and "分隔符"not in str (O0OOOO0O0OOO0OO00 ["条目"]):#line:1887
					O0O0000OOOOOOOOO0 ="'"+str (O0OOOO0O0OOO0OO00 ["条目"])+"':"+str (O0OOOO0O0OOO0OO00 ["详细描述T"])+","#line:1888
					OOOOO00OOOO0O00O0 .loc [O00O000O00OOO00OO ,"疑似新的"]=OOOOO00OOOO0O00O0 .loc [O00O000O00OOO00OO ,"疑似新的"]+O0O0000OOOOOOOOO0 #line:1889
					if int (O0OOOO0O0OOO0OO00 ["详细描述T"])>=3 :#line:1890
						OOOOO00OOOO0O00O0 .loc [O00O000O00OOO00OO ,"关注建议"]=OOOOO00OOOO0O00O0 .loc [O00O000O00OOO00OO ,"关注建议"]+"！"#line:1891
					if int (O0OOOO0O0OOO0OO00 ["详细描述T"])>=5 :#line:1892
						OOOOO00OOOO0O00O0 .loc [O00O000O00OOO00OO ,"关注建议"]=OOOOO00OOOO0O00O0 .loc [O00O000O00OOO00OO ,"关注建议"]+"●"#line:1893
				if str (O0OOOO0O0OOO0OO00 ["条目"]).strip ()not in str (OOOOO00OOOO0O00O0 .loc [O00O000O00OOO00OO ,"疑似旧的（高敏）"])and "分隔符"not in str (O0OOOO0O0OOO0OO00 ["条目"])and int (O0OOOO0O0OOO0OO00 ["详细描述T"])>=2 :#line:1895
					O0O0000OOOOOOOOO0 ="'"+str (O0OOOO0O0OOO0OO00 ["条目"])+"':"+str (O0OOOO0O0OOO0OO00 ["详细描述T"])+","#line:1896
					OOOOO00OOOO0O00O0 .loc [O00O000O00OOO00OO ,"疑似新的（高敏）"]=OOOOO00OOOO0O00O0 .loc [O00O000O00OOO00OO ,"疑似新的（高敏）"]+O0O0000OOOOOOOOO0 #line:1897
		OOOOO00OOOO0O00O0 ["疑似新的"]="{"+OOOOO00OOOO0O00O0 ["疑似新的"]+"}"#line:1899
		OOOOO00OOOO0O00O0 ["疑似旧的"]="{"+OOOOO00OOOO0O00O0 ["疑似旧的"]+"}"#line:1900
		OOOOO00OOOO0O00O0 ["所有不良反应"]="{"+OOOOO00OOOO0O00O0 ["所有不良反应"]+"}"#line:1901
		OOOOO00OOOO0O00O0 ["疑似新的（高敏）"]="{"+OOOOO00OOOO0O00O0 ["疑似新的（高敏）"]+"}"#line:1902
		OOOOO00OOOO0O00O0 ["疑似旧的（高敏）"]="{"+OOOOO00OOOO0O00O0 ["疑似旧的（高敏）"]+"}"#line:1903
		OOOOO00OOOO0O00O0 ["报表类型"]="dfx_chanpin"#line:1904
		O000O0OOO00OOO0O0 =pd .pivot_table (O0OOOOOOOOO0OO0OO ,values =["报告编码"],index =["产品名称"],columns ="报告单位评价",aggfunc ={"报告编码":"nunique"},fill_value ="0",margins =True ,dropna =False ,).rename (columns ={"报告编码":"数量"})#line:1906
		O000O0OOO00OOO0O0 .columns =O000O0OOO00OOO0O0 .columns .droplevel (0 )#line:1907
		OOOOO00OOOO0O00O0 =pd .merge (OOOOO00OOOO0O00O0 ,O000O0OOO00OOO0O0 .reset_index (),on =["产品名称"],how ="left")#line:1908
		TABLE_tree_Level_2 (OOOOO00OOOO0O00O0 .sort_values (by ="计数",ascending =[False ],na_position ="last"),1 ,O0OOOOOOOOO0OO0OO )#line:1909
	if OO0OOO00OOO00OOO0 =="页面":#line:1911
		OOOO00O0OOO000OO0 =""#line:1912
		OO0000OOO0OO00OOO =""#line:1913
		OOO000O000000O0OO =O0OOOOOOOOO0OO0OO .loc [O0OOOOOOOOO0OO0OO ["报告类型-新的"].str .contains ("新",na =False )].copy ()#line:1914
		OO0000O00OO00O0OO =O0OOOOOOOOO0OO0OO .loc [~O0OOOOOOOOO0OO0OO ["报告类型-新的"].str .contains ("新",na =False )].copy ()#line:1915
		OOO0OOO0O0OO00O00 =OOOOOO0000OOOO0O0 (OOO000O000000O0OO )#line:1916
		OO0000O0O0OO0OO00 =OOOOOO0000OOOO0O0 (OO0000O00OO00O0OO )#line:1917
		if 1 ==1 :#line:1918
			for O0OO0O00OO000OO0O ,O0OOOO0O0OOO0OO00 in OO0000O0O0OO0OO00 .iterrows ():#line:1919
					if "分隔符"not in O0OOOO0O0OOO0OO00 ["条目"]:#line:1920
						O0O0000OOOOOOOOO0 ="'"+str (O0OOOO0O0OOO0OO00 ["条目"])+"':"+str (O0OOOO0O0OOO0OO00 ["详细描述T"])+","#line:1921
						OO0000OOO0OO00OOO =OO0000OOO0OO00OOO +O0O0000OOOOOOOOO0 #line:1922
			for O0OO0O00OO000OO0O ,O0OOOO0O0OOO0OO00 in OOO0OOO0O0OO00O00 .iterrows ():#line:1923
				if str (O0OOOO0O0OOO0OO00 ["条目"]).strip ()not in OO0000OOO0OO00OOO and "分隔符"not in str (O0OOOO0O0OOO0OO00 ["条目"]):#line:1924
					O0O0000OOOOOOOOO0 ="'"+str (O0OOOO0O0OOO0OO00 ["条目"])+"':"+str (O0OOOO0O0OOO0OO00 ["详细描述T"])+","#line:1925
					OOOO00O0OOO000OO0 =OOOO00O0OOO000OO0 +O0O0000OOOOOOOOO0 #line:1926
		OO0000OOO0OO00OOO ="{"+OO0000OOO0OO00OOO +"}"#line:1927
		OOOO00O0OOO000OO0 ="{"+OOOO00O0OOO000OO0 +"}"#line:1928
		O00O00OO0OO0O0OOO ="\n可能是新的不良反应：\n\n"+OOOO00O0OOO000OO0 +"\n\n\n可能不是新的不良反应：\n\n"+OO0000OOO0OO00OOO #line:1929
		TOOLS_view_dict (O00O00OO0OO0O0OOO ,1 )#line:1930
def TOOLS_strdict_to_pd (OOOOOO00OOOOO00O0 ):#line:1932
	""#line:1933
	return pd .DataFrame .from_dict (eval (OOOOOO00OOOOO00O0 ),orient ="index",columns =["content"]).reset_index ()#line:1934
def TOOLS_xuanze (OOOOO0O0OO0OO00O0 ,OO000OO0OOO0000O0 ):#line:1936
    ""#line:1937
    if OO000OO0OOO0000O0 ==0 :#line:1938
        O0O0000OOO0O00000 =pd .read_excel (filedialog .askopenfilename (filetypes =[("XLS",".xls")]),sheet_name =0 ,header =0 ,index_col =0 ,).reset_index ()#line:1939
    else :#line:1940
        O0O0000OOO0O00000 =pd .read_excel (peizhidir +"0（范例）批量筛选.xls",sheet_name =0 ,header =0 ,index_col =0 ,).reset_index ()#line:1941
    OOOOO0O0OO0OO00O0 ["temppr"]=""#line:1942
    for OO0OOO000OOOO0000 in O0O0000OOO0O00000 .columns .tolist ():#line:1943
        OOOOO0O0OO0OO00O0 ["temppr"]=OOOOO0O0OO0OO00O0 ["temppr"]+"----"+OOOOO0O0OO0OO00O0 [OO0OOO000OOOO0000 ]#line:1944
    OOO0OO0OOO00OO0OO ="测试字段MMMMM"#line:1945
    for OO0OOO000OOOO0000 in O0O0000OOO0O00000 .columns .tolist ():#line:1946
        for OOOO000OO0O000O0O in O0O0000OOO0O00000 [OO0OOO000OOOO0000 ].drop_duplicates ():#line:1948
            if OOOO000OO0O000O0O :#line:1949
                OOO0OO0OOO00OO0OO =OOO0OO0OOO00OO0OO +"|"+str (OOOO000OO0O000O0O )#line:1950
    OOOOO0O0OO0OO00O0 =OOOOO0O0OO0OO00O0 .loc [OOOOO0O0OO0OO00O0 ["temppr"].str .contains (OOO0OO0OOO00OO0OO ,na =False )].copy ()#line:1951
    del OOOOO0O0OO0OO00O0 ["temppr"]#line:1952
    OOOOO0O0OO0OO00O0 =OOOOO0O0OO0OO00O0 .reset_index (drop =True )#line:1953
    TABLE_tree_Level_2 (OOOOO0O0OO0OO00O0 ,0 ,OOOOO0O0OO0OO00O0 )#line:1955
def TOOLS_add_c (O0OO0OO00000O0O00 ,O0O00O00000OOO00O ):#line:1957
			O0OO0OO00000O0O00 ["关键字查找列o"]=""#line:1958
			for O00OO00OO0O0OOOO0 in TOOLS_get_list (O0O00O00000OOO00O ["查找列"]):#line:1959
				O0OO0OO00000O0O00 ["关键字查找列o"]=O0OO0OO00000O0O00 ["关键字查找列o"]+O0OO0OO00000O0O00 [O00OO00OO0O0OOOO0 ].astype ("str")#line:1960
			if O0O00O00000OOO00O ["条件"]=="等于":#line:1961
				O0OO0OO00000O0O00 .loc [(O0OO0OO00000O0O00 [O0O00O00000OOO00O ["查找列"]].astype (str )==str (O0O00O00000OOO00O ["条件值"])),O0O00O00000OOO00O ["赋值列名"]]=O0O00O00000OOO00O ["赋值"]#line:1962
			if O0O00O00000OOO00O ["条件"]=="大于":#line:1963
				O0OO0OO00000O0O00 .loc [(O0OO0OO00000O0O00 [O0O00O00000OOO00O ["查找列"]].astype (float )>O0O00O00000OOO00O ["条件值"]),O0O00O00000OOO00O ["赋值列名"]]=O0O00O00000OOO00O ["赋值"]#line:1964
			if O0O00O00000OOO00O ["条件"]=="小于":#line:1965
				O0OO0OO00000O0O00 .loc [(O0OO0OO00000O0O00 [O0O00O00000OOO00O ["查找列"]].astype (float )<O0O00O00000OOO00O ["条件值"]),O0O00O00000OOO00O ["赋值列名"]]=O0O00O00000OOO00O ["赋值"]#line:1966
			if O0O00O00000OOO00O ["条件"]=="介于":#line:1967
				O00O00OOOO00O00O0 =TOOLS_get_list (O0O00O00000OOO00O ["条件值"])#line:1968
				O0OO0OO00000O0O00 .loc [((O0OO0OO00000O0O00 [O0O00O00000OOO00O ["查找列"]].astype (float )<float (O00O00OOOO00O00O0 [1 ]))&(O0OO0OO00000O0O00 [O0O00O00000OOO00O ["查找列"]].astype (float )>float (O00O00OOOO00O00O0 [0 ]))),O0O00O00000OOO00O ["赋值列名"]]=O0O00O00000OOO00O ["赋值"]#line:1969
			if O0O00O00000OOO00O ["条件"]=="不含":#line:1970
				O0OO0OO00000O0O00 .loc [(~O0OO0OO00000O0O00 ["关键字查找列o"].str .contains (O0O00O00000OOO00O ["条件值"])),O0O00O00000OOO00O ["赋值列名"]]=O0O00O00000OOO00O ["赋值"]#line:1971
			if O0O00O00000OOO00O ["条件"]=="包含":#line:1972
				O0OO0OO00000O0O00 .loc [O0OO0OO00000O0O00 ["关键字查找列o"].str .contains (O0O00O00000OOO00O ["条件值"],na =False ),O0O00O00000OOO00O ["赋值列名"]]=O0O00O00000OOO00O ["赋值"]#line:1973
			if O0O00O00000OOO00O ["条件"]=="同时包含":#line:1974
				OOOOOO0000OO00O00 =TOOLS_get_list0 (O0O00O00000OOO00O ["条件值"],0 )#line:1975
				if len (OOOOOO0000OO00O00 )==1 :#line:1976
				    O0OO0OO00000O0O00 .loc [O0OO0OO00000O0O00 ["关键字查找列o"].str .contains (OOOOOO0000OO00O00 [0 ],na =False ),O0O00O00000OOO00O ["赋值列名"]]=O0O00O00000OOO00O ["赋值"]#line:1977
				if len (OOOOOO0000OO00O00 )==2 :#line:1978
				    O0OO0OO00000O0O00 .loc [(O0OO0OO00000O0O00 ["关键字查找列o"].str .contains (OOOOOO0000OO00O00 [0 ],na =False ))&(O0OO0OO00000O0O00 ["关键字查找列o"].str .contains (OOOOOO0000OO00O00 [1 ],na =False )),O0O00O00000OOO00O ["赋值列名"]]=O0O00O00000OOO00O ["赋值"]#line:1979
				if len (OOOOOO0000OO00O00 )==3 :#line:1980
				    O0OO0OO00000O0O00 .loc [(O0OO0OO00000O0O00 ["关键字查找列o"].str .contains (OOOOOO0000OO00O00 [0 ],na =False ))&(O0OO0OO00000O0O00 ["关键字查找列o"].str .contains (OOOOOO0000OO00O00 [1 ],na =False ))&(O0OO0OO00000O0O00 ["关键字查找列o"].str .contains (OOOOOO0000OO00O00 [2 ],na =False )),O0O00O00000OOO00O ["赋值列名"]]=O0O00O00000OOO00O ["赋值"]#line:1981
				if len (OOOOOO0000OO00O00 )==4 :#line:1982
				    O0OO0OO00000O0O00 .loc [(O0OO0OO00000O0O00 ["关键字查找列o"].str .contains (OOOOOO0000OO00O00 [0 ],na =False ))&(O0OO0OO00000O0O00 ["关键字查找列o"].str .contains (OOOOOO0000OO00O00 [1 ],na =False ))&(O0OO0OO00000O0O00 ["关键字查找列o"].str .contains (OOOOOO0000OO00O00 [2 ],na =False ))&(O0OO0OO00000O0O00 ["关键字查找列o"].str .contains (OOOOOO0000OO00O00 [3 ],na =False )),O0O00O00000OOO00O ["赋值列名"]]=O0O00O00000OOO00O ["赋值"]#line:1983
				if len (OOOOOO0000OO00O00 )==5 :#line:1984
				    O0OO0OO00000O0O00 .loc [(O0OO0OO00000O0O00 ["关键字查找列o"].str .contains (OOOOOO0000OO00O00 [0 ],na =False ))&(O0OO0OO00000O0O00 ["关键字查找列o"].str .contains (OOOOOO0000OO00O00 [1 ],na =False ))&(O0OO0OO00000O0O00 ["关键字查找列o"].str .contains (OOOOOO0000OO00O00 [2 ],na =False ))&(O0OO0OO00000O0O00 ["关键字查找列o"].str .contains (OOOOOO0000OO00O00 [3 ],na =False ))&(O0OO0OO00000O0O00 ["关键字查找列o"].str .contains (OOOOOO0000OO00O00 [4 ],na =False )),O0O00O00000OOO00O ["赋值列名"]]=O0O00O00000OOO00O ["赋值"]#line:1985
			return O0OO0OO00000O0O00 #line:1986
def TOOL_guizheng (OO000OOO0OO0O0OOO ,O00O00O0O0O000000 ,O000OO000O000OO0O ):#line:1989
	""#line:1990
	if O00O00O0O0O000000 ==0 :#line:1991
		OOOO0O000O0OO00OO =pd .read_excel (filedialog .askopenfilename (filetypes =[("XLSX",".xlsx")]),sheet_name =0 ,header =0 ,index_col =0 ,).reset_index ()#line:1992
		OOOO0O000O0OO00OO =OOOO0O000O0OO00OO [(OOOO0O000O0OO00OO ["执行标记"]=="是")].reset_index ()#line:1993
		for OO00O0OOOOO00OO00 ,OO00O0OOO0OOOOO00 in OOOO0O000O0OO00OO .iterrows ():#line:1994
			OO000OOO0OO0O0OOO =TOOLS_add_c (OO000OOO0OO0O0OOO ,OO00O0OOO0OOOOO00 )#line:1995
		del OO000OOO0OO0O0OOO ["关键字查找列o"]#line:1996
	elif O00O00O0O0O000000 ==1 :#line:1998
		OOOO0O000O0OO00OO =pd .read_excel (peizhidir +"0（范例）数据规整.xlsx",sheet_name =0 ,header =0 ,index_col =0 ,).reset_index ()#line:1999
		OOOO0O000O0OO00OO =OOOO0O000O0OO00OO [(OOOO0O000O0OO00OO ["执行标记"]=="是")].reset_index ()#line:2000
		for OO00O0OOOOO00OO00 ,OO00O0OOO0OOOOO00 in OOOO0O000O0OO00OO .iterrows ():#line:2001
			OO000OOO0OO0O0OOO =TOOLS_add_c (OO000OOO0OO0O0OOO ,OO00O0OOO0OOOOO00 )#line:2002
		del OO000OOO0OO0O0OOO ["关键字查找列o"]#line:2003
	elif O00O00O0O0O000000 =="课题":#line:2005
		OOOO0O000O0OO00OO =pd .read_excel (peizhidir +"0（范例）品类规整.xlsx",sheet_name =0 ,header =0 ,index_col =0 ,).reset_index ()#line:2006
		OOOO0O000O0OO00OO =OOOO0O000O0OO00OO [(OOOO0O000O0OO00OO ["执行标记"]=="是")].reset_index ()#line:2007
		for OO00O0OOOOO00OO00 ,OO00O0OOO0OOOOO00 in OOOO0O000O0OO00OO .iterrows ():#line:2008
			OO000OOO0OO0O0OOO =TOOLS_add_c (OO000OOO0OO0O0OOO ,OO00O0OOO0OOOOO00 )#line:2009
		del OO000OOO0OO0O0OOO ["关键字查找列o"]#line:2010
	elif O00O00O0O0O000000 ==2 :#line:2012
		text .insert (END ,"\n开展报告单位和监测机构名称规整...")#line:2013
		OOOO0OOO0O000OO0O =pd .read_excel (peizhidir +"0（范例）上报单位.xls",sheet_name ="报告单位",header =0 ,index_col =0 ,).fillna ("没有定义好X").reset_index ()#line:2014
		OO0OOOO000O0O0OOO =pd .read_excel (peizhidir +"0（范例）上报单位.xls",sheet_name ="监测机构",header =0 ,index_col =0 ,).fillna ("没有定义好X").reset_index ()#line:2015
		O000000OO0O0O00O0 =pd .read_excel (peizhidir +"0（范例）上报单位.xls",sheet_name ="地市清单",header =0 ,index_col =0 ,).fillna ("没有定义好X").reset_index ()#line:2016
		for OO00O0OOOOO00OO00 ,OO00O0OOO0OOOOO00 in OOOO0OOO0O000OO0O .iterrows ():#line:2017
			OO000OOO0OO0O0OOO .loc [(OO000OOO0OO0O0OOO ["单位名称"]==OO00O0OOO0OOOOO00 ["曾用名1"]),"单位名称"]=OO00O0OOO0OOOOO00 ["单位名称"]#line:2018
			OO000OOO0OO0O0OOO .loc [(OO000OOO0OO0O0OOO ["单位名称"]==OO00O0OOO0OOOOO00 ["曾用名2"]),"单位名称"]=OO00O0OOO0OOOOO00 ["单位名称"]#line:2019
			OO000OOO0OO0O0OOO .loc [(OO000OOO0OO0O0OOO ["单位名称"]==OO00O0OOO0OOOOO00 ["曾用名3"]),"单位名称"]=OO00O0OOO0OOOOO00 ["单位名称"]#line:2020
			OO000OOO0OO0O0OOO .loc [(OO000OOO0OO0O0OOO ["单位名称"]==OO00O0OOO0OOOOO00 ["曾用名4"]),"单位名称"]=OO00O0OOO0OOOOO00 ["单位名称"]#line:2021
			OO000OOO0OO0O0OOO .loc [(OO000OOO0OO0O0OOO ["单位名称"]==OO00O0OOO0OOOOO00 ["曾用名5"]),"单位名称"]=OO00O0OOO0OOOOO00 ["单位名称"]#line:2022
			OO000OOO0OO0O0OOO .loc [(OO000OOO0OO0O0OOO ["单位名称"]==OO00O0OOO0OOOOO00 ["单位名称"]),"医疗机构类别"]=OO00O0OOO0OOOOO00 ["医疗机构类别"]#line:2024
			OO000OOO0OO0O0OOO .loc [(OO000OOO0OO0O0OOO ["单位名称"]==OO00O0OOO0OOOOO00 ["单位名称"]),"监测机构"]=OO00O0OOO0OOOOO00 ["监测机构"]#line:2025
		for OO00O0OOOOO00OO00 ,OO00O0OOO0OOOOO00 in OO0OOOO000O0O0OOO .iterrows ():#line:2027
			OO000OOO0OO0O0OOO .loc [(OO000OOO0OO0O0OOO ["监测机构"]==OO00O0OOO0OOOOO00 ["曾用名1"]),"监测机构"]=OO00O0OOO0OOOOO00 ["监测机构"]#line:2028
			OO000OOO0OO0O0OOO .loc [(OO000OOO0OO0O0OOO ["监测机构"]==OO00O0OOO0OOOOO00 ["曾用名2"]),"监测机构"]=OO00O0OOO0OOOOO00 ["监测机构"]#line:2029
			OO000OOO0OO0O0OOO .loc [(OO000OOO0OO0O0OOO ["监测机构"]==OO00O0OOO0OOOOO00 ["曾用名3"]),"监测机构"]=OO00O0OOO0OOOOO00 ["监测机构"]#line:2030
		for O00O0O00O00000O0O in O000000OO0O0O00O0 ["地市列表"]:#line:2032
			OO000OOO0OO0O0OOO .loc [(OO000OOO0OO0O0OOO ["上报单位所属地区"].str .contains (O00O0O00O00000O0O ,na =False )),"市级监测机构"]=O00O0O00O00000O0O #line:2033
		OO000OOO0OO0O0OOO .loc [(OO000OOO0OO0O0OOO ["上报单位所属地区"].str .contains ("顺德",na =False )),"市级监测机构"]="佛山"#line:2036
		OO000OOO0OO0O0OOO ["市级监测机构"]=OO000OOO0OO0O0OOO ["市级监测机构"].fillna ("-未规整的-")#line:2037
	elif O00O00O0O0O000000 ==3 :#line:2039
			OO00O0O0OOO0OOOOO =(OO000OOO0OO0O0OOO .groupby (["上市许可持有人名称","产品类别","产品名称","注册证编号/曾用注册证编号"]).aggregate ({"报告编码":"count"}).reset_index ())#line:2044
			OO00O0O0OOO0OOOOO =OO00O0O0OOO0OOOOO .sort_values (by =["注册证编号/曾用注册证编号","报告编码"],ascending =[False ,False ],na_position ="last").reset_index ()#line:2047
			text .insert (END ,"\n开展产品名称规整..")#line:2048
			del OO00O0O0OOO0OOOOO ["报告编码"]#line:2049
			OO00O0O0OOO0OOOOO =OO00O0O0OOO0OOOOO .drop_duplicates (["注册证编号/曾用注册证编号"])#line:2050
			OO000OOO0OO0O0OOO =OO000OOO0OO0O0OOO .rename (columns ={"上市许可持有人名称":"上市许可持有人名称（规整前）","产品类别":"产品类别（规整前）","产品名称":"产品名称（规整前）"})#line:2052
			OO000OOO0OO0O0OOO =pd .merge (OO000OOO0OO0O0OOO ,OO00O0O0OOO0OOOOO ,on =["注册证编号/曾用注册证编号"],how ="left")#line:2053
	elif O00O00O0O0O000000 ==4 :#line:2055
		text .insert (END ,"\n正在开展化妆品注册单位规整...")#line:2056
		OO0OOOO000O0O0OOO =pd .read_excel (peizhidir +"0（范例）注册单位.xlsx",sheet_name ="机构列表",header =0 ,index_col =0 ,).reset_index ()#line:2057
		for OO00O0OOOOO00OO00 ,OO00O0OOO0OOOOO00 in OO0OOOO000O0O0OOO .iterrows ():#line:2059
			OO000OOO0OO0O0OOO .loc [(OO000OOO0OO0O0OOO ["单位名称"]==OO00O0OOO0OOOOO00 ["中文全称"]),"监测机构"]=OO00O0OOO0OOOOO00 ["归属地区"]#line:2060
			OO000OOO0OO0O0OOO .loc [(OO000OOO0OO0O0OOO ["单位名称"]==OO00O0OOO0OOOOO00 ["中文全称"]),"市级监测机构"]=OO00O0OOO0OOOOO00 ["地市"]#line:2061
		OO000OOO0OO0O0OOO ["监测机构"]=OO000OOO0OO0O0OOO ["监测机构"].fillna ("未规整")#line:2062
		OO000OOO0OO0O0OOO ["市级监测机构"]=OO000OOO0OO0O0OOO ["市级监测机构"].fillna ("未规整")#line:2063
	if O000OO000O000OO0O ==True :#line:2064
		return OO000OOO0OO0O0OOO #line:2065
	else :#line:2066
		TABLE_tree_Level_2 (OO000OOO0OO0O0OOO ,0 ,OO000OOO0OO0O0OOO )#line:2067
def TOOL_person (O0OOO0OO0000000O0 ):#line:2069
	""#line:2070
	OOOOOOOO0OO0OO0OO =pd .read_excel (peizhidir +"0（范例）注册单位.xlsx",sheet_name ="专家列表",header =0 ,index_col =0 ,).reset_index ()#line:2071
	for O0O00O0OO00OO0O0O ,OO0O00OO0O0O00OO0 in OOOOOOOO0OO0OO0OO .iterrows ():#line:2072
		O0OOO0OO0000000O0 .loc [(O0OOO0OO0000000O0 ["市级监测机构"]==OO0O00OO0O0O00OO0 ["市级监测机构"]),"评表人员"]=OO0O00OO0O0O00OO0 ["评表人员"]#line:2073
		O0OOO0OO0000000O0 ["评表人员"]=O0OOO0OO0000000O0 ["评表人员"].fillna ("未规整")#line:2074
		O00O0OO0OOOO0O00O =O0OOO0OO0000000O0 .groupby (["评表人员"]).agg (报告数量 =("报告编码","nunique"),地市 =("市级监测机构",STAT_countx ),).sort_values (by ="报告数量",ascending =[False ],na_position ="last").reset_index ()#line:2078
	TABLE_tree_Level_2 (O00O0OO0OOOO0O00O ,0 ,O00O0OO0OOOO0O00O )#line:2079
def TOOLS_get_list (O000O0OO0O0OOO00O ):#line:2081
    ""#line:2082
    O000O0OO0O0OOO00O =str (O000O0OO0O0OOO00O )#line:2083
    O00OOOOO0O000O0O0 =[]#line:2084
    O00OOOOO0O000O0O0 .append (O000O0OO0O0OOO00O )#line:2085
    O00OOOOO0O000O0O0 =",".join (O00OOOOO0O000O0O0 )#line:2086
    O00OOOOO0O000O0O0 =O00OOOOO0O000O0O0 .split ("|")#line:2087
    OO00OOO00OOOOO0O0 =O00OOOOO0O000O0O0 [:]#line:2088
    O00OOOOO0O000O0O0 =list (set (O00OOOOO0O000O0O0 ))#line:2089
    O00OOOOO0O000O0O0 .sort (key =OO00OOO00OOOOO0O0 .index )#line:2090
    return O00OOOOO0O000O0O0 #line:2091
def TOOLS_get_list_m (O0OO000000OOO000O ,OOO00O0OO00000OOO ):#line:2093
    ""#line:2094
    O0OO000000OOO000O =str (O0OO000000OOO000O )#line:2095
    if OOO00O0OO00000OOO :#line:2098
        O00000OOOO0OO00OO =re .split (OOO00O0OO00000OOO ,O0OO000000OOO000O )#line:2099
    else :#line:2100
         O00000OOOO0OO00OO =re .split ("/||,|，|;|；|┋|、",O0OO000000OOO000O )#line:2101
    return O00000OOOO0OO00OO #line:2102
def TOOLS_get_list0 (OO0000O000O0OO000 ,O00O00O000O0OO0OO ,*OOO000OO0O00OOOO0 ):#line:2104
    ""#line:2105
    OO0000O000O0OO000 =str (OO0000O000O0OO000 )#line:2106
    if pd .notnull (OO0000O000O0OO000 ):#line:2108
        try :#line:2109
            if "use("in str (OO0000O000O0OO000 ):#line:2110
                OOOO0O0O000OO00O0 =OO0000O000O0OO000 #line:2111
                O000OOOO0OOO00O00 =re .compile (r"[(](.*?)[)]",re .S )#line:2112
                O0000000O0OOOO000 =re .findall (O000OOOO0OOO00O00 ,OOOO0O0O000OO00O0 )#line:2113
                O0O000OOOO00OO000 =[]#line:2114
                if ").list"in OO0000O000O0OO000 :#line:2115
                    O0000O0OO000O00OO =peizhidir +""+str (O0000000O0OOOO000 [0 ])+".xls"#line:2116
                    O000O0OO0OO0OO00O =pd .read_excel (O0000O0OO000O00OO ,sheet_name =O0000000O0OOOO000 [0 ],header =0 ,index_col =0 ).reset_index ()#line:2119
                    O000O0OO0OO0OO00O ["检索关键字"]=O000O0OO0OO0OO00O ["检索关键字"].astype (str )#line:2120
                    O0O000OOOO00OO000 =O000O0OO0OO0OO00O ["检索关键字"].tolist ()+O0O000OOOO00OO000 #line:2121
                if ").file"in OO0000O000O0OO000 :#line:2122
                    O0O000OOOO00OO000 =O00O00O000O0OO0OO [O0000000O0OOOO000 [0 ]].astype (str ).tolist ()+O0O000OOOO00OO000 #line:2124
                try :#line:2127
                    if "报告类型-新的"in O00O00O000O0OO0OO .columns :#line:2128
                        O0O000OOOO00OO000 =",".join (O0O000OOOO00OO000 )#line:2129
                        O0O000OOOO00OO000 =O0O000OOOO00OO000 .split (";")#line:2130
                        O0O000OOOO00OO000 =",".join (O0O000OOOO00OO000 )#line:2131
                        O0O000OOOO00OO000 =O0O000OOOO00OO000 .split ("；")#line:2132
                        O0O000OOOO00OO000 =[OOO000OOO0OOO0O00 .replace ("（严重）","")for OOO000OOO0OOO0O00 in O0O000OOOO00OO000 ]#line:2133
                        O0O000OOOO00OO000 =[OO0O0O0OO0OO0O00O .replace ("（一般）","")for OO0O0O0OO0OO0O00O in O0O000OOOO00OO000 ]#line:2134
                except :#line:2135
                    pass #line:2136
                O0O000OOOO00OO000 =",".join (O0O000OOOO00OO000 )#line:2138
                O0O000OOOO00OO000 =O0O000OOOO00OO000 .split ("┋")#line:2139
                O0O000OOOO00OO000 =",".join (O0O000OOOO00OO000 )#line:2140
                O0O000OOOO00OO000 =O0O000OOOO00OO000 .split (";")#line:2141
                O0O000OOOO00OO000 =",".join (O0O000OOOO00OO000 )#line:2142
                O0O000OOOO00OO000 =O0O000OOOO00OO000 .split ("；")#line:2143
                O0O000OOOO00OO000 =",".join (O0O000OOOO00OO000 )#line:2144
                O0O000OOOO00OO000 =O0O000OOOO00OO000 .split ("、")#line:2145
                O0O000OOOO00OO000 =",".join (O0O000OOOO00OO000 )#line:2146
                O0O000OOOO00OO000 =O0O000OOOO00OO000 .split ("，")#line:2147
                O0O000OOOO00OO000 =",".join (O0O000OOOO00OO000 )#line:2148
                O0O000OOOO00OO000 =O0O000OOOO00OO000 .split (",")#line:2149
                O000O0OO0OO0OOO00 =O0O000OOOO00OO000 [:]#line:2152
                try :#line:2153
                    if OOO000OO0O00OOOO0 [0 ]==1000 :#line:2154
                      pass #line:2155
                except :#line:2156
                      O0O000OOOO00OO000 =list (set (O0O000OOOO00OO000 ))#line:2157
                O0O000OOOO00OO000 .sort (key =O000O0OO0OO0OOO00 .index )#line:2158
            else :#line:2160
                OO0000O000O0OO000 =str (OO0000O000O0OO000 )#line:2161
                O0O000OOOO00OO000 =[]#line:2162
                O0O000OOOO00OO000 .append (OO0000O000O0OO000 )#line:2163
                O0O000OOOO00OO000 =",".join (O0O000OOOO00OO000 )#line:2164
                O0O000OOOO00OO000 =O0O000OOOO00OO000 .split ("┋")#line:2165
                O0O000OOOO00OO000 =",".join (O0O000OOOO00OO000 )#line:2166
                O0O000OOOO00OO000 =O0O000OOOO00OO000 .split ("、")#line:2167
                O0O000OOOO00OO000 =",".join (O0O000OOOO00OO000 )#line:2168
                O0O000OOOO00OO000 =O0O000OOOO00OO000 .split ("，")#line:2169
                O0O000OOOO00OO000 =",".join (O0O000OOOO00OO000 )#line:2170
                O0O000OOOO00OO000 =O0O000OOOO00OO000 .split (",")#line:2171
                O000O0OO0OO0OOO00 =O0O000OOOO00OO000 [:]#line:2173
                try :#line:2174
                    if OOO000OO0O00OOOO0 [0 ]==1000 :#line:2175
                      O0O000OOOO00OO000 =list (set (O0O000OOOO00OO000 ))#line:2176
                except :#line:2177
                      pass #line:2178
                O0O000OOOO00OO000 .sort (key =O000O0OO0OO0OOO00 .index )#line:2179
                O0O000OOOO00OO000 .sort (key =O000O0OO0OO0OOO00 .index )#line:2180
        except ValueError2 :#line:2182
            showinfo (title ="提示信息",message ="创建单元格支持多个甚至表单（文件）传入的方法，返回一个经过整理的清单出错，任务终止。")#line:2183
            return False #line:2184
    return O0O000OOOO00OO000 #line:2186
def TOOLS_easyread2 (O000000O0000OOOO0 ):#line:2188
    ""#line:2189
    O000000O0000OOOO0 ["分隔符"]="●"#line:2191
    O000000O0000OOOO0 ["上报机构描述"]=(O000000O0000OOOO0 ["使用过程"].astype ("str")+O000000O0000OOOO0 ["分隔符"]+O000000O0000OOOO0 ["事件原因分析"].astype ("str")+O000000O0000OOOO0 ["分隔符"]+O000000O0000OOOO0 ["事件原因分析描述"].astype ("str")+O000000O0000OOOO0 ["分隔符"]+O000000O0000OOOO0 ["初步处置情况"].astype ("str"))#line:2200
    O000000O0000OOOO0 ["持有人处理描述"]=(O000000O0000OOOO0 ["关联性评价"].astype ("str")+O000000O0000OOOO0 ["分隔符"]+O000000O0000OOOO0 ["调查情况"].astype ("str")+O000000O0000OOOO0 ["分隔符"]+O000000O0000OOOO0 ["事件原因分析"].astype ("str")+O000000O0000OOOO0 ["分隔符"]+O000000O0000OOOO0 ["具体控制措施"].astype ("str")+O000000O0000OOOO0 ["分隔符"]+O000000O0000OOOO0 ["未采取控制措施原因"].astype ("str"))#line:2211
    O00OO00OOOOOO0000 =O000000O0000OOOO0 [["报告编码","事件发生日期","报告日期","单位名称","产品名称","注册证编号/曾用注册证编号","产品批号","型号","规格","上市许可持有人名称","管理类别","伤害","伤害表现","器械故障表现","上报机构描述","持有人处理描述","经营企业使用单位报告状态","监测机构","产品类别","医疗机构类别","年龄","年龄类型","性别"]]#line:2238
    O00OO00OOOOOO0000 =O00OO00OOOOOO0000 .sort_values (by =["事件发生日期"],ascending =[False ],na_position ="last",)#line:2243
    O00OO00OOOOOO0000 =O00OO00OOOOOO0000 .rename (columns ={"报告编码":"规整编码"})#line:2244
    return O00OO00OOOOOO0000 #line:2245
def fenci0 (OO0OO0OOO000000OO ):#line:2248
	""#line:2249
	O00O000O000O00O00 =Toplevel ()#line:2250
	O00O000O000O00O00 .title ('词频统计')#line:2251
	OO0O0O00000OOO0O0 =O00O000O000O00O00 .winfo_screenwidth ()#line:2252
	OOOOO00O0OOO0O0OO =O00O000O000O00O00 .winfo_screenheight ()#line:2254
	OOOOO0OOOO00OOOO0 =400 #line:2256
	O00O00OO000O0OO0O =120 #line:2257
	OOO000OOO0O0O0OO0 =(OO0O0O00000OOO0O0 -OOOOO0OOOO00OOOO0 )/2 #line:2259
	O00000O00O00O0000 =(OOOOO00O0OOO0O0OO -O00O00OO000O0OO0O )/2 #line:2260
	O00O000O000O00O00 .geometry ("%dx%d+%d+%d"%(OOOOO0OOOO00OOOO0 ,O00O00OO000O0OO0O ,OOO000OOO0O0O0OO0 ,O00000O00O00O0000 ))#line:2261
	OO0OO0O00OO0O00OO =Label (O00O000O000O00O00 ,text ="配置文件：")#line:2262
	OO0OO0O00OO0O00OO .pack ()#line:2263
	O0000O00000O00O0O =Label (O00O000O000O00O00 ,text ="需要分词的列：")#line:2264
	OOO000OOO0O00O000 =Entry (O00O000O000O00O00 ,width =80 )#line:2266
	OOO000OOO0O00O000 .insert (0 ,peizhidir +"0（范例）中文分词工作文件.xls")#line:2267
	O0OOOOOO0OOO00O00 =Entry (O00O000O000O00O00 ,width =80 )#line:2268
	O0OOOOOO0OOO00O00 .insert (0 ,"器械故障表现，伤害表现")#line:2269
	OOO000OOO0O00O000 .pack ()#line:2270
	O0000O00000O00O0O .pack ()#line:2271
	O0OOOOOO0OOO00O00 .pack ()#line:2272
	OO000O00OO000OOOO =LabelFrame (O00O000O000O00O00 )#line:2273
	OO000OOOO00O0OOOO =Button (OO000O00OO000OOOO ,text ="确定",width =10 ,command =lambda :PROGRAM_thread_it (tree_Level_2 ,fenci (OOO000OOO0O00O000 .get (),O0OOOOOO0OOO00O00 .get (),OO0OO0OOO000000OO ),1 ,0 ))#line:2274
	OO000OOOO00O0OOOO .pack (side =LEFT ,padx =1 ,pady =1 )#line:2275
	OO000O00OO000OOOO .pack ()#line:2276
def fenci (OO0000O0000O0OO0O ,OOOOO000OOOOOO0O0 ,OOO0O0O00O0OOOOOO ):#line:2278
    ""#line:2279
    import glob #line:2280
    import jieba #line:2281
    import random #line:2282
    try :#line:2284
        OOO0O0O00O0OOOOOO =OOO0O0O00O0OOOOOO .drop_duplicates (["报告编码"])#line:2285
    except :#line:2286
        pass #line:2287
    def O000000OO00OOOOO0 (OOO00O0OO0O00OOO0 ,O0OOO00O00O000000 ):#line:2288
        O000OO00O0O0OOOO0 ={}#line:2289
        for O000OO0OOOO0OOOOO in OOO00O0OO0O00OOO0 :#line:2290
            O000OO00O0O0OOOO0 [O000OO0OOOO0OOOOO ]=O000OO00O0O0OOOO0 .get (O000OO0OOOO0OOOOO ,0 )+1 #line:2291
        return sorted (O000OO00O0O0OOOO0 .items (),key =lambda OO00OOO00O0O0O000 :OO00OOO00O0O0O000 [1 ],reverse =True )[:O0OOO00O00O000000 ]#line:2292
    OOO0O0O000OOO0OOO =pd .read_excel (OO0000O0000O0OO0O ,sheet_name ="初始化",header =0 ,index_col =0 ).reset_index ()#line:2296
    OO0OO0OOOO0000O0O =OOO0O0O000OOO0OOO .iloc [0 ,2 ]#line:2298
    O00O0O0O0O00OO00O =pd .read_excel (OO0000O0000O0OO0O ,sheet_name ="停用词",header =0 ,index_col =0 ).reset_index ()#line:2301
    O00O0O0O0O00OO00O ["停用词"]=O00O0O0O0O00OO00O ["停用词"].astype (str )#line:2303
    OO0OOO00OOOO0O000 =[OOOOOO00OOOO0OOO0 .strip ()for OOOOOO00OOOO0OOO0 in O00O0O0O0O00OO00O ["停用词"]]#line:2304
    O00OOO000OOOO00O0 =pd .read_excel (OO0000O0000O0OO0O ,sheet_name ="本地词库",header =0 ,index_col =0 ).reset_index ()#line:2307
    O00O00O0O00000O00 =O00OOO000OOOO00O0 ["本地词库"]#line:2308
    jieba .load_userdict (O00O00O0O00000O00 )#line:2309
    OOO00OOO000000O00 =""#line:2312
    O0OOOOOO00OOO0000 =get_list0 (OOOOO000OOOOOO0O0 ,OOO0O0O00O0OOOOOO )#line:2315
    try :#line:2316
        for OOO0000OO0OO00OOO in O0OOOOOO00OOO0000 :#line:2317
            for O0000OOOO0OOOOOO0 in OOO0O0O00O0OOOOOO [OOO0000OO0OO00OOO ]:#line:2318
                OOO00OOO000000O00 =OOO00OOO000000O00 +str (O0000OOOO0OOOOOO0 )#line:2319
    except :#line:2320
        text .insert (END ,"分词配置文件未正确设置，将对整个表格进行分词。")#line:2321
        for OOO0000OO0OO00OOO in OOO0O0O00O0OOOOOO .columns .tolist ():#line:2322
            for O0000OOOO0OOOOOO0 in OOO0O0O00O0OOOOOO [OOO0000OO0OO00OOO ]:#line:2323
                OOO00OOO000000O00 =OOO00OOO000000O00 +str (O0000OOOO0OOOOOO0 )#line:2324
    OO00000O0O0OO0OO0 =[]#line:2325
    OO00000O0O0OO0OO0 =OO00000O0O0OO0OO0 +[O000O0000000OOO00 for O000O0000000OOO00 in jieba .cut (OOO00OOO000000O00 )if O000O0000000OOO00 not in OO0OOO00OOOO0O000 ]#line:2326
    O00O00OO00O000O0O =dict (O000000OO00OOOOO0 (OO00000O0O0OO0OO0 ,OO0OO0OOOO0000O0O ))#line:2327
    OO0O0O0OO000O000O =pd .DataFrame ([O00O00OO00O000O0O ]).T #line:2328
    OO0O0O0OO000O000O =OO0O0O0OO000O000O .reset_index ()#line:2329
    return OO0O0O0OO000O000O #line:2330
def TOOLS_time (O0OO0O0O000OO0OOO ,OOO0O0O000OO0OO0O ,OO0O0O000O00O0O00 ):#line:2332
	""#line:2333
	OOOO0O0000000O00O =O0OO0O0O000OO0OOO .drop_duplicates (["报告编码"]).groupby ([OOO0O0O000OO0OO0O ]).agg (报告总数 =("报告编码","nunique"),).sort_values (by =OOO0O0O000OO0OO0O ,ascending =[True ],na_position ="last").reset_index ()#line:2336
	OOOO0O0000000O00O =OOOO0O0000000O00O .set_index (OOO0O0O000OO0OO0O )#line:2338
	OOOO0O0000000O00O =OOOO0O0000000O00O .resample ('D').asfreq (fill_value =0 )#line:2340
	OOOO0O0000000O00O ["time"]=OOOO0O0000000O00O .index .values #line:2342
	OOOO0O0000000O00O ["time"]=pd .to_datetime (OOOO0O0000000O00O ["time"],format ="%Y/%m/%d").dt .date #line:2343
	O0O0OO000O0OOO0O0 =30 #line:2348
	OO0O0OO0O0000OO00 =30 #line:2349
	OOOO0O0000000O00O ["30日移动平均数"]=round (OOOO0O0000000O00O ["报告总数"].rolling (O0O0OO000O0OOO0O0 ,min_periods =1 ).mean (),2 )#line:2351
	OOOO0O0000000O00O ["目标值"]=round (OOOO0O0000000O00O ["30日移动平均数"].rolling (OO0O0OO0O0000OO00 ,min_periods =1 ).mean (),2 )#line:2353
	OOOO0O0000000O00O ["均值"]=round (OOOO0O0000000O00O ["目标值"].rolling (OO0O0OO0O0000OO00 ,min_periods =1 ).mean (),2 )#line:2355
	OOOO0O0000000O00O ["标准差"]=round (OOOO0O0000000O00O ["目标值"].rolling (OO0O0OO0O0000OO00 ,min_periods =1 ).std (ddof =1 ),2 )#line:2357
	OOOO0O0000000O00O ["1STD"]=round ((OOOO0O0000000O00O ["均值"]+OOOO0O0000000O00O ["标准差"]),2 )#line:2358
	OOOO0O0000000O00O ["2STD"]=round ((OOOO0O0000000O00O ["均值"]+OOOO0O0000000O00O ["标准差"]*2 ),2 )#line:2359
	OOOO0O0000000O00O ["UCL_3STD"]=round ((OOOO0O0000000O00O ["均值"]+OOOO0O0000000O00O ["标准差"]*3 ),2 )#line:2360
	DRAW_make_risk_plot (OOOO0O0000000O00O ,"time",["30日移动平均数","UCL_3STD"],"折线图",999 )#line:2382
def TOOLS_time_bak (OOOO000OOOO000O00 ,O00O000000OO0O0O0 ,O0OOOO0OO0O0OO000 ):#line:2385
	""#line:2386
	OO000O0O0O0O0OOOO =OOOO000OOOO000O00 .drop_duplicates (["报告编码"]).groupby ([O00O000000OO0O0O0 ]).agg (报告总数 =("报告编码","nunique"),严重伤害数 =("伤害",lambda OOOOO0000O0000000 :STAT_countpx (OOOOO0000O0000000 .values ,"严重伤害")),死亡数量 =("伤害",lambda OOO00O00O0OO000OO :STAT_countpx (OOO00O00O0OO000OO .values ,"死亡")),).sort_values (by =O00O000000OO0O0O0 ,ascending =[True ],na_position ="last").reset_index ()#line:2391
	OO000O0O0O0O0OOOO =OO000O0O0O0O0OOOO .set_index (O00O000000OO0O0O0 )#line:2395
	OO000O0O0O0O0OOOO =OO000O0O0O0O0OOOO .resample ('D').asfreq (fill_value =0 )#line:2397
	OO000O0O0O0O0OOOO ["time"]=OO000O0O0O0O0OOOO .index .values #line:2399
	OO000O0O0O0O0OOOO ["time"]=pd .to_datetime (OO000O0O0O0O0OOOO ["time"],format ="%Y/%m/%d").dt .date #line:2400
	if O0OOOO0OO0O0OO000 ==1 :#line:2402
		return OO000O0O0O0O0OOOO .reset_index (drop =True )#line:2404
	OO000O0O0O0O0OOOO ["30天累计数"]=OO000O0O0O0O0OOOO ["报告总数"].rolling (30 ,min_periods =1 ).agg (lambda OOOOO0OO0O000OOOO :sum (OOOOO0OO0O000OOOO )).astype (int )#line:2406
	OO000O0O0O0O0OOOO ["30天严重伤害累计数"]=OO000O0O0O0O0OOOO ["严重伤害数"].rolling (30 ,min_periods =1 ).agg (lambda OOO00000OOO0O00O0 :sum (OOO00000OOO0O00O0 )).astype (int )#line:2407
	OO000O0O0O0O0OOOO ["30天死亡累计数"]=OO000O0O0O0O0OOOO ["死亡数量"].rolling (30 ,min_periods =1 ).agg (lambda O000000O0000O0000 :sum (O000000O0000O0000 )).astype (int )#line:2408
	OO000O0O0O0O0OOOO .loc [(((OO000O0O0O0O0OOOO ["30天累计数"]>=3 )&(OO000O0O0O0O0OOOO ["30天严重伤害累计数"]>=1 ))|(OO000O0O0O0O0OOOO ["30天累计数"]>=5 )|(OO000O0O0O0O0OOOO ["30天死亡累计数"]>=1 )),"关注区域"]=OO000O0O0O0O0OOOO ["30天累计数"]#line:2429
	DRAW_make_risk_plot (OO000O0O0O0O0OOOO ,"time",["30天累计数","30天严重伤害累计数","关注区域"],"折线图",999 )#line:2434
def TOOLS_keti (O00OOOOO0O0OOO00O ):#line:2438
	""#line:2439
	import datetime #line:2440
	def OO00000OO0O0OO00O (OOO000O0OOOO00O00 ,OOO0OOOO0OOO00000 ):#line:2442
		if ini ["模式"]=="药品":#line:2443
			OO0O0OOO00OOOOOOO =pd .read_excel (peizhidir +"0（范例）预警参数.xlsx",header =0 ,sheet_name ="药品").reset_index (drop =True )#line:2444
		if ini ["模式"]=="器械":#line:2445
			OO0O0OOO00OOOOOOO =pd .read_excel (peizhidir +"0（范例）预警参数.xlsx",header =0 ,sheet_name ="器械").reset_index (drop =True )#line:2446
		if ini ["模式"]=="化妆品":#line:2447
			OO0O0OOO00OOOOOOO =pd .read_excel (peizhidir +"0（范例）预警参数.xlsx",header =0 ,sheet_name ="化妆品").reset_index (drop =True )#line:2448
		OO00OO0O0OO000OO0 =OO0O0OOO00OOOOOOO ["权重"][0 ]#line:2449
		O00OOOO000OO0OO0O =OO0O0OOO00OOOOOOO ["权重"][1 ]#line:2450
		O000O00O00O0OOOO0 =OO0O0OOO00OOOOOOO ["权重"][2 ]#line:2451
		OOOO0O00OOO000O0O =OO0O0OOO00OOOOOOO ["权重"][3 ]#line:2452
		O0OO00OOO000OO0OO =OO0O0OOO00OOOOOOO ["值"][3 ]#line:2453
		OO0OO0OOO0O00O000 =OO0O0OOO00OOOOOOO ["权重"][4 ]#line:2455
		OO000OOOOOO0O000O =OO0O0OOO00OOOOOOO ["值"][4 ]#line:2456
		OOO0O00OOO0000O00 =OO0O0OOO00OOOOOOO ["权重"][5 ]#line:2458
		O00O00O0000O0O000 =OO0O0OOO00OOOOOOO ["值"][5 ]#line:2459
		O0000O00O00OOO00O =OO0O0OOO00OOOOOOO ["权重"][6 ]#line:2461
		O0OO0O0O0000O0OOO =OO0O0OOO00OOOOOOO ["值"][6 ]#line:2462
		OOO0OO0OO000O00OO =pd .to_datetime (OOO000O0OOOO00O00 )#line:2464
		O00O00O000O0OO000 =OOO0OOOO0OOO00000 .copy ().set_index ('报告日期')#line:2465
		O00O00O000O0OO000 =O00O00O000O0OO000 .sort_index ()#line:2466
		if ini ["模式"]=="器械":#line:2467
			O00O00O000O0OO000 ["关键字查找列"]=O00O00O000O0OO000 ["器械故障表现"].astype (str )+O00O00O000O0OO000 ["伤害表现"].astype (str )+O00O00O000O0OO000 ["使用过程"].astype (str )+O00O00O000O0OO000 ["事件原因分析描述"].astype (str )+O00O00O000O0OO000 ["初步处置情况"].astype (str )#line:2468
		else :#line:2469
			O00O00O000O0OO000 ["关键字查找列"]=O00O00O000O0OO000 ["器械故障表现"].astype (str )#line:2470
		O00O00O000O0OO000 .loc [O00O00O000O0OO000 ["关键字查找列"].str .contains (O0OO00OOO000OO0OO ,na =False ),"高度关注关键字"]=1 #line:2471
		O00O00O000O0OO000 .loc [O00O00O000O0OO000 ["关键字查找列"].str .contains (OO000OOOOOO0O000O ,na =False ),"二级敏感词"]=1 #line:2472
		O00O00O000O0OO000 .loc [O00O00O000O0OO000 ["关键字查找列"].str .contains (O00O00O0000O0O000 ,na =False ),"减分项"]=1 #line:2473
		OOOOOO0O0O000O0O0 =O00O00O000O0OO000 .loc [OOO0OO0OO000O00OO -pd .Timedelta (days =30 ):OOO0OO0OO000O00OO ].reset_index ()#line:2475
		OO0OOO0OO0OOO0OO0 =O00O00O000O0OO000 .loc [OOO0OO0OO000O00OO -pd .Timedelta (days =365 ):OOO0OO0OO000O00OO ].reset_index ()#line:2476
		O00OOO0OO0O0OO000 =OOOOOO0O0O000O0O0 .groupby (["上市许可持有人名称","产品类别","规整后品类","产品名称","注册证编号/曾用注册证编号"]).agg (证号计数 =("报告编码","nunique"),批号个数 =("产品批号","nunique"),批号列表 =("产品批号",STAT_countx ),型号个数 =("型号","nunique"),型号列表 =("型号",STAT_countx ),规格个数 =("规格","nunique"),规格列表 =("规格",STAT_countx ),).sort_values (by ="证号计数",ascending =[False ],na_position ="last").reset_index ()#line:2489
		OOOOO0OOOOOO0OOO0 =OOOOOO0O0O000O0O0 .drop_duplicates (["报告编码"]).groupby (["上市许可持有人名称","产品类别","规整后品类","产品名称","注册证编号/曾用注册证编号"]).agg (严重伤害数 =("伤害",lambda O0OO00O0000O00O00 :STAT_countpx (O0OO00O0000O00O00 .values ,"严重伤害")),死亡数量 =("伤害",lambda O0OOO0OO000O0OOO0 :STAT_countpx (O0OOO0OO000O0OOO0 .values ,"死亡")),单位个数 =("单位名称","nunique"),单位列表 =("单位名称",STAT_countx ),待评价数 =("持有人报告状态",lambda O0OOOO00O0OO0OO00 :STAT_countpx (O0OOOO00O0OO0OO00 .values ,"待评价")),严重伤害待评价数 =("伤害与评价",lambda OOO000OOOO0OO0000 :STAT_countpx (OOO000OOOO0OO0000 .values ,"严重伤害待评价")),高度关注关键字 =("高度关注关键字","sum"),二级敏感词 =("二级敏感词","sum"),减分项 =("减分项","sum"),).reset_index ()#line:2501
		OO00OO0OOOOO0O000 =pd .merge (O00OOO0OO0O0OO000 ,OOOOO0OOOOOO0OOO0 ,on =["上市许可持有人名称","产品类别","规整后品类","产品名称","注册证编号/曾用注册证编号"],how ="left")#line:2503
		O00O00000000OOOOO =OOOOOO0O0O000O0O0 .groupby (["上市许可持有人名称","产品类别","产品名称","注册证编号/曾用注册证编号","型号"]).agg (型号计数 =("报告编码","nunique"),).sort_values (by ="型号计数",ascending =[False ],na_position ="last").reset_index ()#line:2510
		O00O00000000OOOOO =O00O00000000OOOOO .drop_duplicates ("注册证编号/曾用注册证编号")#line:2511
		OOOO0O00000OO0O00 =OOOOOO0O0O000O0O0 .drop_duplicates (["报告编码"]).groupby (["上市许可持有人名称","产品类别","产品名称","注册证编号/曾用注册证编号","产品批号"]).agg (批号计数 =("报告编码","nunique"),严重伤害数 =("伤害",lambda OO00OO0O00O000O00 :STAT_countpx (OO00OO0O00O000O00 .values ,"严重伤害")),).sort_values (by ="批号计数",ascending =[False ],na_position ="last").reset_index ()#line:2516
		OOOO0O00000OO0O00 ["风险评分-影响"]=0 #line:2520
		OOOO0O00000OO0O00 ["评分说明"]=""#line:2521
		OOOO0O00000OO0O00 .loc [((OOOO0O00000OO0O00 ["批号计数"]>=3 )&(OOOO0O00000OO0O00 ["严重伤害数"]>=1 )&(OOOO0O00000OO0O00 ["产品类别"]!="有源"))|((OOOO0O00000OO0O00 ["批号计数"]>=5 )&(OOOO0O00000OO0O00 ["产品类别"]!="有源")),"风险评分-影响"]=OOOO0O00000OO0O00 ["风险评分-影响"]+3 #line:2522
		OOOO0O00000OO0O00 .loc [(OOOO0O00000OO0O00 ["风险评分-影响"]>=3 ),"评分说明"]=OOOO0O00000OO0O00 ["评分说明"]+"●符合省中心无源规则+3;"#line:2523
		OOOO0O00000OO0O00 =OOOO0O00000OO0O00 .sort_values (by ="风险评分-影响",ascending =[False ],na_position ="last").reset_index (drop =True )#line:2527
		OOOO0O00000OO0O00 =OOOO0O00000OO0O00 .drop_duplicates ("注册证编号/曾用注册证编号")#line:2528
		O00O00000000OOOOO =O00O00000000OOOOO [["上市许可持有人名称","产品类别","产品名称","注册证编号/曾用注册证编号","型号","型号计数"]]#line:2529
		OOOO0O00000OO0O00 =OOOO0O00000OO0O00 [["上市许可持有人名称","产品类别","产品名称","注册证编号/曾用注册证编号","产品批号","批号计数","风险评分-影响","评分说明"]]#line:2530
		OO00OO0OOOOO0O000 =pd .merge (OO00OO0OOOOO0O000 ,O00O00000000OOOOO ,on =["上市许可持有人名称","产品类别","产品名称","注册证编号/曾用注册证编号"],how ="left")#line:2531
		OO00OO0OOOOO0O000 =pd .merge (OO00OO0OOOOO0O000 ,OOOO0O00000OO0O00 ,on =["上市许可持有人名称","产品类别","产品名称","注册证编号/曾用注册证编号"],how ="left")#line:2533
		OO00OO0OOOOO0O000 .loc [((OO00OO0OOOOO0O000 ["证号计数"]>=3 )&(OO00OO0OOOOO0O000 ["严重伤害数"]>=1 )&(OO00OO0OOOOO0O000 ["产品类别"]=="有源"))|((OO00OO0OOOOO0O000 ["证号计数"]>=5 )&(OO00OO0OOOOO0O000 ["产品类别"]=="有源")),"风险评分-影响"]=OO00OO0OOOOO0O000 ["风险评分-影响"]+3 #line:2537
		OO00OO0OOOOO0O000 .loc [(OO00OO0OOOOO0O000 ["风险评分-影响"]>=3 )&(OO00OO0OOOOO0O000 ["产品类别"]=="有源"),"评分说明"]=OO00OO0OOOOO0O000 ["评分说明"]+"●符合省中心有源规则+3;"#line:2538
		OO00OO0OOOOO0O000 .loc [(OO00OO0OOOOO0O000 ["死亡数量"]>=1 ),"风险评分-影响"]=OO00OO0OOOOO0O000 ["风险评分-影响"]+10 #line:2543
		OO00OO0OOOOO0O000 .loc [(OO00OO0OOOOO0O000 ["风险评分-影响"]>=10 ),"评分说明"]=OO00OO0OOOOO0O000 ["评分说明"]+"存在死亡报告;"#line:2544
		O000O00O0OO0OO0O0 =round (OO00OO0O0OO000OO0 *(OO00OO0OOOOO0O000 ["严重伤害数"]/OO00OO0OOOOO0O000 ["证号计数"]),2 )#line:2547
		OO00OO0OOOOO0O000 ["风险评分-影响"]=OO00OO0OOOOO0O000 ["风险评分-影响"]+O000O00O0OO0OO0O0 #line:2548
		OO00OO0OOOOO0O000 ["评分说明"]=OO00OO0OOOOO0O000 ["评分说明"]+"严重比评分"+O000O00O0OO0OO0O0 .astype (str )+";"#line:2549
		O00O0O0OO00OO0O00 =round (O00OOOO000OO0OO0O *(np .log (OO00OO0OOOOO0O000 ["单位个数"])),2 )#line:2552
		OO00OO0OOOOO0O000 ["风险评分-影响"]=OO00OO0OOOOO0O000 ["风险评分-影响"]+O00O0O0OO00OO0O00 #line:2553
		OO00OO0OOOOO0O000 ["评分说明"]=OO00OO0OOOOO0O000 ["评分说明"]+"报告单位评分"+O00O0O0OO00OO0O00 .astype (str )+";"#line:2554
		OO00OO0OOOOO0O000 .loc [(OO00OO0OOOOO0O000 ["产品类别"]=="有源")&(OO00OO0OOOOO0O000 ["证号计数"]>=3 ),"风险评分-影响"]=OO00OO0OOOOO0O000 ["风险评分-影响"]+O000O00O00O0OOOO0 *OO00OO0OOOOO0O000 ["型号计数"]/OO00OO0OOOOO0O000 ["证号计数"]#line:2557
		OO00OO0OOOOO0O000 .loc [(OO00OO0OOOOO0O000 ["产品类别"]=="有源")&(OO00OO0OOOOO0O000 ["证号计数"]>=3 ),"评分说明"]=OO00OO0OOOOO0O000 ["评分说明"]+"型号集中度评分"+(round (O000O00O00O0OOOO0 *OO00OO0OOOOO0O000 ["型号计数"]/OO00OO0OOOOO0O000 ["证号计数"],2 )).astype (str )+";"#line:2558
		OO00OO0OOOOO0O000 .loc [(OO00OO0OOOOO0O000 ["产品类别"]!="有源")&(OO00OO0OOOOO0O000 ["证号计数"]>=3 ),"风险评分-影响"]=OO00OO0OOOOO0O000 ["风险评分-影响"]+O000O00O00O0OOOO0 *OO00OO0OOOOO0O000 ["批号计数"]/OO00OO0OOOOO0O000 ["证号计数"]#line:2559
		OO00OO0OOOOO0O000 .loc [(OO00OO0OOOOO0O000 ["产品类别"]!="有源")&(OO00OO0OOOOO0O000 ["证号计数"]>=3 ),"评分说明"]=OO00OO0OOOOO0O000 ["评分说明"]+"批号集中度评分"+(round (O000O00O00O0OOOO0 *OO00OO0OOOOO0O000 ["批号计数"]/OO00OO0OOOOO0O000 ["证号计数"],2 )).astype (str )+";"#line:2560
		OO00OO0OOOOO0O000 .loc [(OO00OO0OOOOO0O000 ["高度关注关键字"]>=1 ),"风险评分-影响"]=OO00OO0OOOOO0O000 ["风险评分-影响"]+OOOO0O00OOO000O0O #line:2563
		OO00OO0OOOOO0O000 .loc [(OO00OO0OOOOO0O000 ["高度关注关键字"]>=1 ),"评分说明"]=OO00OO0OOOOO0O000 ["评分说明"]+"●含有高度关注关键字评分"+str (OOOO0O00OOO000O0O )+"；"#line:2564
		OO00OO0OOOOO0O000 .loc [(OO00OO0OOOOO0O000 ["二级敏感词"]>=1 ),"风险评分-影响"]=OO00OO0OOOOO0O000 ["风险评分-影响"]+OO0OO0OOO0O00O000 #line:2567
		OO00OO0OOOOO0O000 .loc [(OO00OO0OOOOO0O000 ["二级敏感词"]>=1 ),"评分说明"]=OO00OO0OOOOO0O000 ["评分说明"]+"含有二级敏感词评分"+str (OO0OO0OOO0O00O000 )+"；"#line:2568
		OO00OO0OOOOO0O000 .loc [(OO00OO0OOOOO0O000 ["减分项"]>=1 ),"风险评分-影响"]=OO00OO0OOOOO0O000 ["风险评分-影响"]+OOO0O00OOO0000O00 #line:2571
		OO00OO0OOOOO0O000 .loc [(OO00OO0OOOOO0O000 ["减分项"]>=1 ),"评分说明"]=OO00OO0OOOOO0O000 ["评分说明"]+"减分项评分"+str (OOO0O00OOO0000O00 )+"；"#line:2572
		O00000OOOOOOO000O =Countall (OO0OOO0OO0OOO0OO0 ).df_findrisk ("事件发生月份")#line:2575
		O00000OOOOOOO000O =O00000OOOOOOO000O .drop_duplicates ("注册证编号/曾用注册证编号")#line:2576
		O00000OOOOOOO000O =O00000OOOOOOO000O [["注册证编号/曾用注册证编号","均值","标准差","CI上限"]]#line:2577
		OO00OO0OOOOO0O000 =pd .merge (OO00OO0OOOOO0O000 ,O00000OOOOOOO000O ,on =["注册证编号/曾用注册证编号"],how ="left")#line:2578
		OO00OO0OOOOO0O000 ["风险评分-月份"]=1 #line:2580
		OO00OO0OOOOO0O000 ["mfc"]=""#line:2581
		OO00OO0OOOOO0O000 .loc [((OO00OO0OOOOO0O000 ["证号计数"]>OO00OO0OOOOO0O000 ["均值"])&(OO00OO0OOOOO0O000 ["标准差"].astype (str )=="nan")),"风险评分-月份"]=OO00OO0OOOOO0O000 ["风险评分-月份"]+1 #line:2582
		OO00OO0OOOOO0O000 .loc [(OO00OO0OOOOO0O000 ["证号计数"]>OO00OO0OOOOO0O000 ["均值"]),"mfc"]="月份计数超过历史均值"+OO00OO0OOOOO0O000 ["均值"].astype (str )+"；"#line:2583
		OO00OO0OOOOO0O000 .loc [(OO00OO0OOOOO0O000 ["证号计数"]>=(OO00OO0OOOOO0O000 ["均值"]+OO00OO0OOOOO0O000 ["标准差"]))&(OO00OO0OOOOO0O000 ["证号计数"]>=3 ),"风险评分-月份"]=OO00OO0OOOOO0O000 ["风险评分-月份"]+1 #line:2585
		OO00OO0OOOOO0O000 .loc [(OO00OO0OOOOO0O000 ["证号计数"]>=(OO00OO0OOOOO0O000 ["均值"]+OO00OO0OOOOO0O000 ["标准差"]))&(OO00OO0OOOOO0O000 ["证号计数"]>=3 ),"mfc"]="月份计数超过3例超过历史均值一个标准差("+OO00OO0OOOOO0O000 ["标准差"].astype (str )+")；"#line:2586
		OO00OO0OOOOO0O000 .loc [(OO00OO0OOOOO0O000 ["证号计数"]>=OO00OO0OOOOO0O000 ["CI上限"])&(OO00OO0OOOOO0O000 ["证号计数"]>=3 ),"风险评分-月份"]=OO00OO0OOOOO0O000 ["风险评分-月份"]+2 #line:2588
		OO00OO0OOOOO0O000 .loc [(OO00OO0OOOOO0O000 ["证号计数"]>=OO00OO0OOOOO0O000 ["CI上限"])&(OO00OO0OOOOO0O000 ["证号计数"]>=3 ),"mfc"]="月份计数超过3例且超过历史95%CI上限("+OO00OO0OOOOO0O000 ["CI上限"].astype (str )+")；"#line:2589
		OO00OO0OOOOO0O000 .loc [(OO00OO0OOOOO0O000 ["证号计数"]>=OO00OO0OOOOO0O000 ["CI上限"])&(OO00OO0OOOOO0O000 ["证号计数"]>=5 ),"风险评分-月份"]=OO00OO0OOOOO0O000 ["风险评分-月份"]+1 #line:2591
		OO00OO0OOOOO0O000 .loc [(OO00OO0OOOOO0O000 ["证号计数"]>=OO00OO0OOOOO0O000 ["CI上限"])&(OO00OO0OOOOO0O000 ["证号计数"]>=5 ),"mfc"]="月份计数超过5例且超过历史95%CI上限("+OO00OO0OOOOO0O000 ["CI上限"].astype (str )+")；"#line:2592
		OO00OO0OOOOO0O000 .loc [(OO00OO0OOOOO0O000 ["证号计数"]>=OO00OO0OOOOO0O000 ["CI上限"])&(OO00OO0OOOOO0O000 ["证号计数"]>=7 ),"风险评分-月份"]=OO00OO0OOOOO0O000 ["风险评分-月份"]+1 #line:2594
		OO00OO0OOOOO0O000 .loc [(OO00OO0OOOOO0O000 ["证号计数"]>=OO00OO0OOOOO0O000 ["CI上限"])&(OO00OO0OOOOO0O000 ["证号计数"]>=7 ),"mfc"]="月份计数超过7例且超过历史95%CI上限("+OO00OO0OOOOO0O000 ["CI上限"].astype (str )+")；"#line:2595
		OO00OO0OOOOO0O000 .loc [(OO00OO0OOOOO0O000 ["证号计数"]>=OO00OO0OOOOO0O000 ["CI上限"])&(OO00OO0OOOOO0O000 ["证号计数"]>=9 ),"风险评分-月份"]=OO00OO0OOOOO0O000 ["风险评分-月份"]+1 #line:2597
		OO00OO0OOOOO0O000 .loc [(OO00OO0OOOOO0O000 ["证号计数"]>=OO00OO0OOOOO0O000 ["CI上限"])&(OO00OO0OOOOO0O000 ["证号计数"]>=9 ),"mfc"]="月份计数超过9例且超过历史95%CI上限("+OO00OO0OOOOO0O000 ["CI上限"].astype (str )+")；"#line:2598
		OO00OO0OOOOO0O000 .loc [(OO00OO0OOOOO0O000 ["证号计数"]>=3 )&(OO00OO0OOOOO0O000 ["标准差"].astype (str )=="nan"),"风险评分-月份"]=3 #line:2602
		OO00OO0OOOOO0O000 .loc [(OO00OO0OOOOO0O000 ["证号计数"]>=3 )&(OO00OO0OOOOO0O000 ["标准差"].astype (str )=="nan"),"mfc"]="无历史数据但数量超过3例；"#line:2603
		OO00OO0OOOOO0O000 ["评分说明"]=OO00OO0OOOOO0O000 ["评分说明"]+"●●证号数量："+OO00OO0OOOOO0O000 ["证号计数"].astype (str )+";"+OO00OO0OOOOO0O000 ["mfc"]#line:2606
		del OO00OO0OOOOO0O000 ["mfc"]#line:2607
		OO00OO0OOOOO0O000 =OO00OO0OOOOO0O000 .rename (columns ={"均值":"月份均值","标准差":"月份标准差","CI上限":"月份CI上限"})#line:2608
		O00000OOOOOOO000O =Countall (OO0OOO0OO0OOO0OO0 ).df_findrisk ("产品批号")#line:2612
		O00000OOOOOOO000O =O00000OOOOOOO000O .drop_duplicates ("注册证编号/曾用注册证编号")#line:2613
		O00000OOOOOOO000O =O00000OOOOOOO000O [["注册证编号/曾用注册证编号","均值","标准差","CI上限"]]#line:2614
		OO00OO0OOOOO0O000 =pd .merge (OO00OO0OOOOO0O000 ,O00000OOOOOOO000O ,on =["注册证编号/曾用注册证编号"],how ="left")#line:2615
		OO00OO0OOOOO0O000 ["风险评分-批号"]=1 #line:2617
		OO00OO0OOOOO0O000 .loc [(OO00OO0OOOOO0O000 ["产品类别"]!="有源"),"评分说明"]=OO00OO0OOOOO0O000 ["评分说明"]+"●●高峰批号数量："+OO00OO0OOOOO0O000 ["批号计数"].astype (str )+";"#line:2618
		OO00OO0OOOOO0O000 .loc [(OO00OO0OOOOO0O000 ["批号计数"]>OO00OO0OOOOO0O000 ["均值"]),"风险评分-批号"]=OO00OO0OOOOO0O000 ["风险评分-批号"]+1 #line:2620
		OO00OO0OOOOO0O000 .loc [(OO00OO0OOOOO0O000 ["批号计数"]>OO00OO0OOOOO0O000 ["均值"]),"评分说明"]=OO00OO0OOOOO0O000 ["评分说明"]+"高峰批号计数超过历史均值"+OO00OO0OOOOO0O000 ["均值"].astype (str )+"；"#line:2621
		OO00OO0OOOOO0O000 .loc [(OO00OO0OOOOO0O000 ["批号计数"]>(OO00OO0OOOOO0O000 ["均值"]+OO00OO0OOOOO0O000 ["标准差"]))&(OO00OO0OOOOO0O000 ["批号计数"]>=3 ),"风险评分-批号"]=OO00OO0OOOOO0O000 ["风险评分-批号"]+1 #line:2622
		OO00OO0OOOOO0O000 .loc [(OO00OO0OOOOO0O000 ["批号计数"]>(OO00OO0OOOOO0O000 ["均值"]+OO00OO0OOOOO0O000 ["标准差"]))&(OO00OO0OOOOO0O000 ["批号计数"]>=3 ),"评分说明"]=OO00OO0OOOOO0O000 ["评分说明"]+"高峰批号计数超过3例超过历史均值一个标准差("+OO00OO0OOOOO0O000 ["标准差"].astype (str )+")；"#line:2623
		OO00OO0OOOOO0O000 .loc [(OO00OO0OOOOO0O000 ["批号计数"]>OO00OO0OOOOO0O000 ["CI上限"])&(OO00OO0OOOOO0O000 ["批号计数"]>=3 ),"风险评分-批号"]=OO00OO0OOOOO0O000 ["风险评分-批号"]+1 #line:2624
		OO00OO0OOOOO0O000 .loc [(OO00OO0OOOOO0O000 ["批号计数"]>OO00OO0OOOOO0O000 ["CI上限"])&(OO00OO0OOOOO0O000 ["批号计数"]>=3 ),"评分说明"]=OO00OO0OOOOO0O000 ["评分说明"]+"高峰批号计数超过3例且超过历史95%CI上限("+OO00OO0OOOOO0O000 ["CI上限"].astype (str )+")；"#line:2625
		OO00OO0OOOOO0O000 .loc [(OO00OO0OOOOO0O000 ["批号计数"]>=3 )&(OO00OO0OOOOO0O000 ["标准差"].astype (str )=="nan"),"风险评分-月份"]=3 #line:2627
		OO00OO0OOOOO0O000 .loc [(OO00OO0OOOOO0O000 ["批号计数"]>=3 )&(OO00OO0OOOOO0O000 ["标准差"].astype (str )=="nan"),"评分说明"]=OO00OO0OOOOO0O000 ["评分说明"]+"无历史数据但数量超过3例；"#line:2628
		OO00OO0OOOOO0O000 =OO00OO0OOOOO0O000 .rename (columns ={"均值":"高峰批号均值","标准差":"高峰批号标准差","CI上限":"高峰批号CI上限"})#line:2629
		OO00OO0OOOOO0O000 ["风险评分-影响"]=round (OO00OO0OOOOO0O000 ["风险评分-影响"],2 )#line:2632
		OO00OO0OOOOO0O000 ["风险评分-月份"]=round (OO00OO0OOOOO0O000 ["风险评分-月份"],2 )#line:2633
		OO00OO0OOOOO0O000 ["风险评分-批号"]=round (OO00OO0OOOOO0O000 ["风险评分-批号"],2 )#line:2634
		OO00OO0OOOOO0O000 ["总体评分"]=OO00OO0OOOOO0O000 ["风险评分-影响"].copy ()#line:2636
		OO00OO0OOOOO0O000 ["关注建议"]=""#line:2637
		OO00OO0OOOOO0O000 .loc [(OO00OO0OOOOO0O000 ["风险评分-影响"]>=3 ),"关注建议"]=OO00OO0OOOOO0O000 ["关注建议"]+"●建议关注(影响范围)；"#line:2638
		OO00OO0OOOOO0O000 .loc [(OO00OO0OOOOO0O000 ["风险评分-月份"]>=3 ),"关注建议"]=OO00OO0OOOOO0O000 ["关注建议"]+"●建议关注(当月数量异常)；"#line:2639
		OO00OO0OOOOO0O000 .loc [(OO00OO0OOOOO0O000 ["风险评分-批号"]>=3 ),"关注建议"]=OO00OO0OOOOO0O000 ["关注建议"]+"●建议关注(高峰批号数量异常)。"#line:2640
		OO00OO0OOOOO0O000 .loc [(OO00OO0OOOOO0O000 ["风险评分-月份"]>=OO00OO0OOOOO0O000 ["风险评分-批号"]),"总体评分"]=OO00OO0OOOOO0O000 ["风险评分-影响"]*OO00OO0OOOOO0O000 ["风险评分-月份"]#line:2644
		OO00OO0OOOOO0O000 .loc [(OO00OO0OOOOO0O000 ["风险评分-月份"]<OO00OO0OOOOO0O000 ["风险评分-批号"]),"总体评分"]=OO00OO0OOOOO0O000 ["风险评分-影响"]*OO00OO0OOOOO0O000 ["风险评分-批号"]#line:2645
		OO00OO0OOOOO0O000 ["总体评分"]=round (OO00OO0OOOOO0O000 ["总体评分"],2 )#line:2647
		OO00OO0OOOOO0O000 ["评分说明"]=OO00OO0OOOOO0O000 ["关注建议"]+OO00OO0OOOOO0O000 ["评分说明"]#line:2648
		OO00OO0OOOOO0O000 =OO00OO0OOOOO0O000 .sort_values (by =["总体评分","风险评分-影响"],ascending =[False ,False ],na_position ="last").reset_index (drop =True )#line:2649
		OO00OO0OOOOO0O000 ["主要故障分类"]=""#line:2652
		for OOO00O00O0O00OO0O ,OOO0OOOO00OOOOO00 in OO00OO0OOOOO0O000 .iterrows ():#line:2653
			OO0OOO0O0OOO0OO00 =OOOOOO0O0O000O0O0 [(OOOOOO0O0O000O0O0 ["注册证编号/曾用注册证编号"]==OOO0OOOO00OOOOO00 ["注册证编号/曾用注册证编号"])].copy ()#line:2654
			if OOO0OOOO00OOOOO00 ["总体评分"]>=float (O0000O00O00OOO00O ):#line:2655
				if OOO0OOOO00OOOOO00 ["规整后品类"]!="N":#line:2656
					OOOO000000OO0O000 =Countall (OO0OOO0O0OOO0OO00 ).df_psur ("特定品种",OOO0OOOO00OOOOO00 ["规整后品类"])#line:2657
				elif OOO0OOOO00OOOOO00 ["产品类别"]=="无源":#line:2658
					OOOO000000OO0O000 =Countall (OO0OOO0O0OOO0OO00 ).df_psur ("通用无源")#line:2659
				elif OOO0OOOO00OOOOO00 ["产品类别"]=="有源":#line:2660
					OOOO000000OO0O000 =Countall (OO0OOO0O0OOO0OO00 ).df_psur ("通用有源")#line:2661
				elif OOO0OOOO00OOOOO00 ["产品类别"]=="体外诊断试剂":#line:2662
					OOOO000000OO0O000 =Countall (OO0OOO0O0OOO0OO00 ).df_psur ("体外诊断试剂")#line:2663
				OO00OOOOO0OOO00OO =OOOO000000OO0O000 [["事件分类","总数量"]].copy ()#line:2665
				OOOO00000OOO0O00O =""#line:2666
				for OO0OO0O000OO0O0O0 ,OOO00000O00O0O000 in OO00OOOOO0OOO00OO .iterrows ():#line:2667
					OOOO00000OOO0O00O =OOOO00000OOO0O00O +str (OOO00000O00O0O000 ["事件分类"])+":"+str (OOO00000O00O0O000 ["总数量"])+";"#line:2668
				OO00OO0OOOOO0O000 .loc [OOO00O00O0O00OO0O ,"主要故障分类"]=OOOO00000OOO0O00O #line:2669
			else :#line:2670
				break #line:2671
		OO00OO0OOOOO0O000 =OO00OO0OOOOO0O000 [["上市许可持有人名称","产品类别","规整后品类","产品名称","注册证编号/曾用注册证编号","证号计数","严重伤害数","死亡数量","总体评分","风险评分-影响","风险评分-月份","风险评分-批号","主要故障分类","评分说明","单位个数","单位列表","批号个数","批号列表","型号个数","型号列表","规格个数","规格列表","待评价数","严重伤害待评价数","高度关注关键字","二级敏感词","月份均值","月份标准差","月份CI上限","高峰批号均值","高峰批号标准差","高峰批号CI上限","型号","型号计数","产品批号","批号计数"]]#line:2675
		OO00OO0OOOOO0O000 ["报表类型"]="dfx_zhenghao"#line:2676
		TABLE_tree_Level_2 (OO00OO0OOOOO0O000 ,1 ,OOOOOO0O0O000O0O0 ,OO0OOO0OO0OOO0OO0 )#line:2677
		pass #line:2678
	OO00000O0OO0O000O =Toplevel ()#line:2681
	OO00000O0OO0O000O .title ('风险预警')#line:2682
	O0OO00O0OO00O0O0O =OO00000O0OO0O000O .winfo_screenwidth ()#line:2683
	O000000000O00OOO0 =OO00000O0OO0O000O .winfo_screenheight ()#line:2685
	O0O0O0OO000OO000O =350 #line:2687
	O0000OOO000O00O00 =35 #line:2688
	O00O000O0O0O0O00O =(O0OO00O0OO00O0O0O -O0O0O0OO000OO000O )/2 #line:2690
	OO0OOOOOOOO0OO0OO =(O000000000O00OOO0 -O0000OOO000O00O00 )/2 #line:2691
	OO00000O0OO0O000O .geometry ("%dx%d+%d+%d"%(O0O0O0OO000OO000O ,O0000OOO000O00O00 ,O00O000O0O0O0O00O ,OO0OOOOOOOO0OO0OO ))#line:2692
	OOO0O0OOOO00000OO =Label (OO00000O0OO0O000O ,text ="预警日期：")#line:2694
	OOO0O0OOOO00000OO .grid (row =1 ,column =0 ,sticky ="w")#line:2695
	O00OO0O0OOO0O0OO0 =Entry (OO00000O0OO0O000O ,width =30 )#line:2696
	O00OO0O0OOO0O0OO0 .insert (0 ,datetime .date .today ())#line:2697
	O00OO0O0OOO0O0OO0 .grid (row =1 ,column =1 ,sticky ="w")#line:2698
	OOO0OOOOO00OOOO00 =Button (OO00000O0OO0O000O ,text ="确定",width =10 ,command =lambda :TABLE_tree_Level_2 (OO00000OO0O0OO00O (O00OO0O0OOO0O0OO0 .get (),O00OOOOO0O0OOO00O ),1 ,O00OOOOO0O0OOO00O ))#line:2702
	OOO0OOOOO00OOOO00 .grid (row =1 ,column =3 ,sticky ="w")#line:2703
	pass #line:2705
def TOOLS_count_elements (OO000000O00OO0O0O ,OOO0O0O0OO0OO0O00 ,OO00O0OO0OO0O00OO ):#line:2707
    ""#line:2708
    O000O00OO0OO00OOO =pd .DataFrame (columns =[OO00O0OO0OO0O00OO ,'count'])#line:2710
    O00O0O0OOOOO0OOOO =[]#line:2711
    OO00O00O000OOO0O0 =[]#line:2712
    for OO00000O00O00O0OO in TOOLS_get_list (OOO0O0O0OO0OO0O00 ):#line:2715
        O00O0O00000O00O0O =OO000000O00OO0O0O [OO000000O00OO0O0O [OO00O0OO0OO0O00OO ].str .contains (OO00000O00O00O0OO )].shape [0 ]#line:2717
        if O00O0O00000O00O0O >0 :#line:2720
            O00O0O0OOOOO0OOOO .append (O00O0O00000O00O0O )#line:2721
            OO00O00O000OOO0O0 .append (OO00000O00O00O0OO )#line:2722
    OO00O00OOOO0O0OOO =pd .DataFrame ({"index":OO00O00O000OOO0O0 ,'计数':O00O0O0OOOOO0OOOO })#line:2723
    OO00O00OOOO0O0OOO ["构成比(%)"]=round (100 *OO00O00OOOO0O0OOO ["计数"]/OO00O00OOOO0O0OOO ["计数"].sum (),2 )#line:2724
    OO00O00OOOO0O0OOO ["报表类型"]="dfx_deepvie2"+"_"+str ([OO00O0OO0OO0O00OO ])#line:2725
    return OO00O00OOOO0O0OOO #line:2727
def TOOLS_autocount (O00O0O0OOOO00OO0O ,O000OO0O0OO00OOOO ):#line:2729
    ""#line:2730
    OO0000O000000OO00 =pd .read_excel (peizhidir +"0（范例）上报单位.xls",sheet_name ="监测机构",header =0 ,index_col =0 ).reset_index ()#line:2733
    O0000OO0O000O0O0O =pd .read_excel (peizhidir +"0（范例）上报单位.xls",sheet_name ="报告单位",header =0 ,index_col =0 ).reset_index ()#line:2736
    O00OO0O000O0OO0OO =O0000OO0O000O0O0O [(O0000OO0O000O0O0O ["是否属于二级以上医疗机构"]=="是")]#line:2737
    if O000OO0O0OO00OOOO =="药品":#line:2740
        O00O0O0OOOO00OO0O =O00O0O0OOOO00OO0O .reset_index (drop =True )#line:2741
        if "再次使用可疑药是否出现同样反应"not in O00O0O0OOOO00OO0O .columns :#line:2742
            showinfo (title ="错误信息",message ="导入的疑似不是药品报告表。")#line:2743
            return 0 #line:2744
        O00O0O0OO0OOO0OOO =Countall (O00O0O0OOOO00OO0O ).df_org ("监测机构")#line:2746
        O00O0O0OO0OOO0OOO =pd .merge (O00O0O0OO0OOO0OOO ,OO0000O000000OO00 ,on ="监测机构",how ="left")#line:2747
        O00O0O0OO0OOO0OOO =O00O0O0OO0OOO0OOO [["监测机构序号","监测机构","药品数量指标","报告数量","审核通过数","新严比","严重比","超时比"]].sort_values (by =["监测机构序号"],ascending =True ,na_position ="last").fillna (0 )#line:2748
        O0OO0OOO00O0OO000 =["药品数量指标","审核通过数","报告数量"]#line:2749
        O00O0O0OO0OOO0OOO [O0OO0OOO00O0OO000 ]=O00O0O0OO0OOO0OOO [O0OO0OOO00O0OO000 ].apply (lambda OO0OOOOO0O0OO0000 :OO0OOOOO0O0OO0000 .astype (int ))#line:2750
        OOOOOO00O000O0O0O =Countall (O00O0O0OOOO00OO0O ).df_user ()#line:2752
        OOOOOO00O000O0O0O =pd .merge (OOOOOO00O000O0O0O ,O0000OO0O000O0O0O ,on =["监测机构","单位名称"],how ="left")#line:2753
        OOOOOO00O000O0O0O =pd .merge (OOOOOO00O000O0O0O ,OO0000O000000OO00 [["监测机构序号","监测机构"]],on ="监测机构",how ="left")#line:2754
        OOOOOO00O000O0O0O =OOOOOO00O000O0O0O [["监测机构序号","监测机构","单位名称","药品数量指标","报告数量","审核通过数","新严比","严重比","超时比"]].sort_values (by =["监测机构序号","报告数量"],ascending =[True ,False ],na_position ="last").fillna (0 )#line:2756
        O0OO0OOO00O0OO000 =["药品数量指标","审核通过数","报告数量"]#line:2757
        OOOOOO00O000O0O0O [O0OO0OOO00O0OO000 ]=OOOOOO00O000O0O0O [O0OO0OOO00O0OO000 ].apply (lambda OO0OOO0000OO0O0O0 :OO0OOO0000OO0O0O0 .astype (int ))#line:2758
        O000O0O0OO0000OOO =pd .merge (O00OO0O000O0OO0OO ,OOOOOO00O000O0O0O ,on =["监测机构","单位名称"],how ="left").sort_values (by =["监测机构"],ascending =True ,na_position ="last").fillna (0 )#line:2760
        O000O0O0OO0000OOO =O000O0O0OO0000OOO [(O000O0O0OO0000OOO ["审核通过数"]<1 )]#line:2761
        O000O0O0OO0000OOO =O000O0O0OO0000OOO [["监测机构","单位名称","报告数量","审核通过数","严重比","超时比"]]#line:2762
    if O000OO0O0OO00OOOO =="器械":#line:2764
        O00O0O0OOOO00OO0O =O00O0O0OOOO00OO0O .reset_index (drop =True )#line:2765
        if "产品编号"not in O00O0O0OOOO00OO0O .columns :#line:2766
            showinfo (title ="错误信息",message ="导入的疑似不是器械报告表。")#line:2767
            return 0 #line:2768
        O00O0O0OO0OOO0OOO =Countall (O00O0O0OOOO00OO0O ).df_org ("监测机构")#line:2770
        O00O0O0OO0OOO0OOO =pd .merge (O00O0O0OO0OOO0OOO ,OO0000O000000OO00 ,on ="监测机构",how ="left")#line:2771
        O00O0O0OO0OOO0OOO =O00O0O0OO0OOO0OOO [["监测机构序号","监测机构","器械数量指标","报告数量","审核通过数","严重比","超时比"]].sort_values (by =["监测机构序号"],ascending =True ,na_position ="last").fillna (0 )#line:2772
        O0OO0OOO00O0OO000 =["器械数量指标","审核通过数","报告数量"]#line:2773
        O00O0O0OO0OOO0OOO [O0OO0OOO00O0OO000 ]=O00O0O0OO0OOO0OOO [O0OO0OOO00O0OO000 ].apply (lambda OO0O000O000O0OO00 :OO0O000O000O0OO00 .astype (int ))#line:2774
        OOOOOO00O000O0O0O =Countall (O00O0O0OOOO00OO0O ).df_user ()#line:2776
        OOOOOO00O000O0O0O =pd .merge (OOOOOO00O000O0O0O ,O0000OO0O000O0O0O ,on =["监测机构","单位名称"],how ="left")#line:2777
        OOOOOO00O000O0O0O =pd .merge (OOOOOO00O000O0O0O ,OO0000O000000OO00 [["监测机构序号","监测机构"]],on ="监测机构",how ="left")#line:2778
        OOOOOO00O000O0O0O =OOOOOO00O000O0O0O [["监测机构序号","监测机构","单位名称","器械数量指标","报告数量","审核通过数","严重比","超时比"]].sort_values (by =["监测机构序号","报告数量"],ascending =[True ,False ],na_position ="last").fillna (0 )#line:2780
        O0OO0OOO00O0OO000 =["器械数量指标","审核通过数","报告数量"]#line:2781
        OOOOOO00O000O0O0O [O0OO0OOO00O0OO000 ]=OOOOOO00O000O0O0O [O0OO0OOO00O0OO000 ].apply (lambda OO00O00O000000OO0 :OO00O00O000000OO0 .astype (int ))#line:2783
        O000O0O0OO0000OOO =pd .merge (O00OO0O000O0OO0OO ,OOOOOO00O000O0O0O ,on =["监测机构","单位名称"],how ="left").sort_values (by =["监测机构"],ascending =True ,na_position ="last").fillna (0 )#line:2785
        O000O0O0OO0000OOO =O000O0O0OO0000OOO [(O000O0O0OO0000OOO ["审核通过数"]<1 )]#line:2786
        O000O0O0OO0000OOO =O000O0O0OO0000OOO [["监测机构","单位名称","报告数量","审核通过数","严重比","超时比"]]#line:2787
    if O000OO0O0OO00OOOO =="化妆品":#line:2790
        O00O0O0OOOO00OO0O =O00O0O0OOOO00OO0O .reset_index (drop =True )#line:2791
        if "初步判断"not in O00O0O0OOOO00OO0O .columns :#line:2792
            showinfo (title ="错误信息",message ="导入的疑似不是化妆品报告表。")#line:2793
            return 0 #line:2794
        O00O0O0OO0OOO0OOO =Countall (O00O0O0OOOO00OO0O ).df_org ("监测机构")#line:2796
        O00O0O0OO0OOO0OOO =pd .merge (O00O0O0OO0OOO0OOO ,OO0000O000000OO00 ,on ="监测机构",how ="left")#line:2797
        O00O0O0OO0OOO0OOO =O00O0O0OO0OOO0OOO [["监测机构序号","监测机构","化妆品数量指标","报告数量","审核通过数"]].sort_values (by =["监测机构序号"],ascending =True ,na_position ="last").fillna (0 )#line:2798
        O0OO0OOO00O0OO000 =["化妆品数量指标","审核通过数","报告数量"]#line:2799
        O00O0O0OO0OOO0OOO [O0OO0OOO00O0OO000 ]=O00O0O0OO0OOO0OOO [O0OO0OOO00O0OO000 ].apply (lambda OO0OOO0OOO0OO00O0 :OO0OOO0OOO0OO00O0 .astype (int ))#line:2800
        OOOOOO00O000O0O0O =Countall (O00O0O0OOOO00OO0O ).df_user ()#line:2802
        OOOOOO00O000O0O0O =pd .merge (OOOOOO00O000O0O0O ,O0000OO0O000O0O0O ,on =["监测机构","单位名称"],how ="left")#line:2803
        OOOOOO00O000O0O0O =pd .merge (OOOOOO00O000O0O0O ,OO0000O000000OO00 [["监测机构序号","监测机构"]],on ="监测机构",how ="left")#line:2804
        OOOOOO00O000O0O0O =OOOOOO00O000O0O0O [["监测机构序号","监测机构","单位名称","化妆品数量指标","报告数量","审核通过数"]].sort_values (by =["监测机构序号","报告数量"],ascending =[True ,False ],na_position ="last").fillna (0 )#line:2805
        O0OO0OOO00O0OO000 =["化妆品数量指标","审核通过数","报告数量"]#line:2806
        OOOOOO00O000O0O0O [O0OO0OOO00O0OO000 ]=OOOOOO00O000O0O0O [O0OO0OOO00O0OO000 ].apply (lambda O0OO0O0000OO00OOO :O0OO0O0000OO00OOO .astype (int ))#line:2807
        O000O0O0OO0000OOO =pd .merge (O00OO0O000O0OO0OO ,OOOOOO00O000O0O0O ,on =["监测机构","单位名称"],how ="left").sort_values (by =["监测机构"],ascending =True ,na_position ="last").fillna (0 )#line:2809
        O000O0O0OO0000OOO =O000O0O0OO0000OOO [(O000O0O0OO0000OOO ["审核通过数"]<1 )]#line:2810
        O000O0O0OO0000OOO =O000O0O0OO0000OOO [["监测机构","单位名称","报告数量","审核通过数"]]#line:2811
    O00OO0O0O000O0OO0 =filedialog .asksaveasfilename (title =u"保存文件",initialfile =O000OO0O0OO00OOOO ,defaultextension ="xls",filetypes =[("Excel 97-2003 工作簿","*.xls")],)#line:2818
    O00000000OOO000OO =pd .ExcelWriter (O00OO0O0O000O0OO0 ,engine ="xlsxwriter")#line:2819
    O00O0O0OO0OOO0OOO .to_excel (O00000000OOO000OO ,sheet_name ="监测机构")#line:2820
    OOOOOO00O000O0O0O .to_excel (O00000000OOO000OO ,sheet_name ="上报单位")#line:2821
    O000O0O0OO0000OOO .to_excel (O00000000OOO000OO ,sheet_name ="未上报的二级以上医疗机构")#line:2822
    O00000000OOO000OO .close ()#line:2823
    showinfo (title ="提示",message ="文件写入成功。")#line:2824
def TOOLS_web_view (O0O000O0OOOOO000O ):#line:2826
    ""#line:2827
    import pybi as pbi #line:2828
    O0OOO000OOO000OOO =pd .ExcelWriter ("temp_webview.xls")#line:2829
    O0O000O0OOOOO000O .to_excel (O0OOO000OOO000OOO ,sheet_name ="temp_webview")#line:2830
    O0OOO000OOO000OOO .close ()#line:2831
    O0O000O0OOOOO000O =pd .read_excel ("temp_webview.xls",header =0 ,sheet_name =0 ).reset_index (drop =True )#line:2832
    O00O00000O000O0OO =pbi .set_source (O0O000O0OOOOO000O )#line:2833
    with pbi .flowBox ():#line:2834
        for O0O00O00OOO0000O0 in O0O000O0OOOOO000O .columns :#line:2835
            pbi .add_slicer (O00O00000O000O0OO [O0O00O00OOO0000O0 ])#line:2836
    pbi .add_table (O00O00000O000O0OO )#line:2837
    OO000O0O0O00OOO00 ="temp_webview.html"#line:2838
    pbi .to_html (OO000O0O0O00OOO00 )#line:2839
    webbrowser .open_new_tab (OO000O0O0O00OOO00 )#line:2840
def TOOLS_Autotable_0 (OOO000O00000OO0O0 ,O0OOOOO00O000O0OO ,*OOOO00O0OO000OOO0 ):#line:2845
    ""#line:2846
    O00OO000O00O0000O =[OOOO00O0OO000OOO0 [0 ],OOOO00O0OO000OOO0 [1 ],OOOO00O0OO000OOO0 [2 ]]#line:2848
    O0OO00O00OOO0O00O =list (set ([OOO0OOO0O0O0000O0 for OOO0OOO0O0O0000O0 in O00OO000O00O0000O if OOO0OOO0O0O0000O0 !='']))#line:2850
    O0OO00O00OOO0O00O .sort (key =O00OO000O00O0000O .index )#line:2851
    if len (O0OO00O00OOO0O00O )==0 :#line:2852
        showinfo (title ="提示信息",message ="分组项请选择至少一列。")#line:2853
        return 0 #line:2854
    OOOO000O0O0O000OO =[OOOO00O0OO000OOO0 [3 ],OOOO00O0OO000OOO0 [4 ]]#line:2855
    if (OOOO00O0OO000OOO0 [3 ]==""or OOOO00O0OO000OOO0 [4 ]=="")and O0OOOOO00O000O0OO in ["数据透视","分组统计"]:#line:2856
        if "报告编码"in OOO000O00000OO0O0 .columns :#line:2857
            OOOO000O0O0O000OO [0 ]="报告编码"#line:2858
            OOOO000O0O0O000OO [1 ]="nunique"#line:2859
            text .insert (END ,"值项未配置,将使用报告编码进行唯一值计数。")#line:2860
        else :#line:2861
            showinfo (title ="提示信息",message ="值项未配置。")#line:2862
            return 0 #line:2863
    if OOOO00O0OO000OOO0 [4 ]=="计数":#line:2865
        OOOO000O0O0O000OO [1 ]="count"#line:2866
    elif OOOO00O0OO000OOO0 [4 ]=="求和":#line:2867
        OOOO000O0O0O000OO [1 ]="sum"#line:2868
    elif OOOO00O0OO000OOO0 [4 ]=="唯一值计数":#line:2869
        OOOO000O0O0O000OO [1 ]="nunique"#line:2870
    if O0OOOOO00O000O0OO =="分组统计":#line:2873
        TABLE_tree_Level_2 (TOOLS_deep_view (OOO000O00000OO0O0 ,O0OO00O00OOO0O00O ,OOOO000O0O0O000OO ,0 ),1 ,OOO000O00000OO0O0 )#line:2874
    if O0OOOOO00O000O0OO =="数据透视":#line:2876
        TABLE_tree_Level_2 (TOOLS_deep_view (OOO000O00000OO0O0 ,O0OO00O00OOO0O00O ,OOOO000O0O0O000OO ,1 ),1 ,OOO000O00000OO0O0 )#line:2877
    if O0OOOOO00O000O0OO =="描述性统计(X)":#line:2879
        TABLE_tree_Level_2 (OOO000O00000OO0O0 [O0OO00O00OOO0O00O ].describe ().reset_index (),1 ,OOO000O00000OO0O0 )#line:2880
    if O0OOOOO00O000O0OO =="拆分成字典(X-Y)":#line:2883
        OO00O0000O0OO0O0O =OOO000O00000OO0O0 .copy ()#line:2886
        OO00O0000O0OO0O0O ["c"]="c"#line:2887
        OO000OOOO000O0000 =OO00O0000O0OO0O0O .groupby ([OOOO00O0OO000OOO0 [0 ]]).agg (计数 =("c","count")).reset_index ()#line:2888
        OO000O0OOOOOOOOOO =OO000OOOO000O0000 .copy ()#line:2889
        OO000O0OOOOOOOOOO [OOOO00O0OO000OOO0 [0 ]]=OO000O0OOOOOOOOOO [OOOO00O0OO000OOO0 [0 ]].str .replace ("*","",regex =False )#line:2890
        OO000O0OOOOOOOOOO ["所有项目"]=""#line:2891
        O000O0OOOO00O000O =1 #line:2892
        OOO0OO000000O0O0O =int (len (OO000O0OOOOOOOOOO ))#line:2893
        for OO0O00O0OOO00O00O ,O00OOO00O0O00O0OO in OO000O0OOOOOOOOOO .iterrows ():#line:2894
            OO000OO00O0000000 =OO00O0000O0OO0O0O [(OO00O0000O0OO0O0O [OOOO00O0OO000OOO0 [0 ]]==O00OOO00O0O00O0OO [OOOO00O0OO000OOO0 [0 ]])]#line:2896
            OO000OOO00O0O0OOO =str (Counter (TOOLS_get_list0 ("use("+str (OOOO00O0OO000OOO0 [1 ])+").file",OO000OO00O0000000 ,1000 ))).replace ("Counter({","{")#line:2898
            OO000OOO00O0O0OOO =OO000OOO00O0O0OOO .replace ("})","}")#line:2899
            import ast #line:2900
            O0OO0000O00O0OO00 =ast .literal_eval (OO000OOO00O0O0OOO )#line:2901
            OO0OOO0OOO00OOOOO =TOOLS_easyreadT (pd .DataFrame ([O0OO0000O00O0OO00 ]))#line:2902
            OO0OOO0OOO00OOOOO =OO0OOO0OOO00OOOOO .rename (columns ={"逐条查看":"名称规整"})#line:2903
            PROGRAM_change_schedule (O000O0OOOO00O000O ,OOO0OO000000O0O0O )#line:2905
            O000O0OOOO00O000O =O000O0OOOO00O000O +1 #line:2906
            for O000OOOOO0O0OOOOO ,OOOO0OO00O0O00000 in OO0OOO0OOO00OOOOO .iterrows ():#line:2907
                    if "分隔符"not in OOOO0OO00O0O00000 ["条目"]:#line:2908
                        OOO0000OOOO0OO0O0 ="'"+str (OOOO0OO00O0O00000 ["条目"])+"':"+str (OOOO0OO00O0O00000 ["详细描述T"])+","#line:2909
                        OO000O0OOOOOOOOOO .loc [OO0O00O0OOO00O00O ,"所有项目"]=OO000O0OOOOOOOOOO .loc [OO0O00O0OOO00O00O ,"所有项目"]+OOO0000OOOO0OO0O0 #line:2910
        OO000O0OOOOOOOOOO ["所有项目"]="{"+OO000O0OOOOOOOOOO ["所有项目"]+"}"#line:2912
        OO000O0OOOOOOOOOO ["报表类型"]="dfx_deepview_"+str ([OOOO00O0OO000OOO0 [0 ]])#line:2913
        TABLE_tree_Level_2 (OO000O0OOOOOOOOOO .sort_values (by ="计数",ascending =[False ],na_position ="last"),1 ,OO00O0000O0OO0O0O )#line:2915
    if O0OOOOO00O000O0OO =="追加外部表格信息":#line:2917
        O000OOOO0O00O0O00 =filedialog .askopenfilenames (filetypes =[("XLS",".xls"),("XLSX",".xlsx")])#line:2920
        O000O0OOOO00O000O =[pd .read_excel (OO0O0000O00OOO0O0 ,header =0 ,sheet_name =0 )for OO0O0000O00OOO0O0 in O000OOOO0O00O0O00 ]#line:2921
        OOOOOO000000O00OO =pd .concat (O000O0OOOO00O000O ,ignore_index =True ).drop_duplicates (O0OO00O00OOO0O00O )#line:2922
        O00OOOOOO00OOO00O =pd .merge (OOO000O00000OO0O0 ,OOOOOO000000O00OO ,on =O0OO00O00OOO0O00O ,how ="left")#line:2923
        TABLE_tree_Level_2 (O00OOOOOO00OOO00O ,1 ,O00OOOOOO00OOO00O )#line:2924
    if O0OOOOO00O000O0OO =="添加到外部表格":#line:2926
        O000OOOO0O00O0O00 =filedialog .askopenfilenames (filetypes =[("XLS",".xls"),("XLSX",".xlsx")])#line:2929
        O000O0OOOO00O000O =[pd .read_excel (O0OO00000OO00OO0O ,header =0 ,sheet_name =0 )for O0OO00000OO00OO0O in O000OOOO0O00O0O00 ]#line:2930
        OOOOOO000000O00OO =pd .concat (O000O0OOOO00O000O ,ignore_index =True ).drop_duplicates ()#line:2931
        O00OOOOOO00OOO00O =pd .merge (OOOOOO000000O00OO ,OOO000O00000OO0O0 .drop_duplicates (O0OO00O00OOO0O00O ),on =O0OO00O00OOO0O00O ,how ="left")#line:2932
        TABLE_tree_Level_2 (O00OOOOOO00OOO00O ,1 ,O00OOOOOO00OOO00O )#line:2933
    if O0OOOOO00O000O0OO =="饼图(XY)":#line:2936
        DRAW_make_one (OOO000O00000OO0O0 ,"饼图",OOOO00O0OO000OOO0 [0 ],OOOO00O0OO000OOO0 [1 ],"饼图")#line:2937
    if O0OOOOO00O000O0OO =="柱状图(XY)":#line:2938
        DRAW_make_one (OOO000O00000OO0O0 ,"柱状图",OOOO00O0OO000OOO0 [0 ],OOOO00O0OO000OOO0 [1 ],"柱状图")#line:2939
    if O0OOOOO00O000O0OO =="折线图(XY)":#line:2940
        DRAW_make_one (OOO000O00000OO0O0 ,"折线图",OOOO00O0OO000OOO0 [0 ],OOOO00O0OO000OOO0 [1 ],"折线图")#line:2941
    if O0OOOOO00O000O0OO =="托帕斯图(XY)":#line:2942
        DRAW_make_one (OOO000O00000OO0O0 ,"托帕斯图",OOOO00O0OO000OOO0 [0 ],OOOO00O0OO000OOO0 [1 ],"托帕斯图")#line:2943
    if O0OOOOO00O000O0OO =="堆叠柱状图（X-YZ）":#line:2944
        DRAW_make_mutibar (OOO000O00000OO0O0 ,O00OO000O00O0000O [1 ],O00OO000O00O0000O [2 ],O00OO000O00O0000O [0 ],O00OO000O00O0000O [1 ],O00OO000O00O0000O [2 ],"堆叠柱状图")#line:2945
def STAT_countx (OOOO000000OOO00OO ):#line:2955
	""#line:2956
	return OOOO000000OOO00OO .value_counts ().to_dict ()#line:2957
def STAT_countpx (OOOO0O0OO0O0OOOO0 ,O0O00O0O0OOOOOOOO ):#line:2959
	""#line:2960
	return len (OOOO0O0OO0O0OOOO0 [(OOOO0O0OO0O0OOOO0 ==O0O00O0O0OOOOOOOO )])#line:2961
def STAT_countnpx (O0OO0000OOOO0O00O ,OO0O0OOOOOO000000 ):#line:2963
	""#line:2964
	return len (O0OO0000OOOO0O00O [(O0OO0000OOOO0O00O not in OO0O0OOOOOO000000 )])#line:2965
def STAT_get_max (O00OOOO0OOOO0O00O ):#line:2967
	""#line:2968
	return O00OOOO0OOOO0O00O .value_counts ().max ()#line:2969
def STAT_get_mean (O0O00O0O0OOO0000O ):#line:2971
	""#line:2972
	return round (O0O00O0O0OOO0000O .value_counts ().mean (),2 )#line:2973
def STAT_get_std (OO0OO00OOOO0OO0OO ):#line:2975
	""#line:2976
	return round (OO0OO00OOOO0OO0OO .value_counts ().std (ddof =1 ),2 )#line:2977
def STAT_get_95ci (O0OO0OO0000O0O0OO ):#line:2979
	""#line:2980
	O000O0O0O00OOOO00 =0.95 #line:2981
	OOO000000O00000O0 =O0OO0OO0000O0O0OO .value_counts ().tolist ()#line:2982
	if len (OOO000000O00000O0 )<30 :#line:2983
		OO00OOO0OOO000O00 =st .t .interval (O000O0O0O00OOOO00 ,df =len (OOO000000O00000O0 )-1 ,loc =np .mean (OOO000000O00000O0 ),scale =st .sem (OOO000000O00000O0 ))#line:2984
	else :#line:2985
		OO00OOO0OOO000O00 =st .norm .interval (O000O0O0O00OOOO00 ,loc =np .mean (OOO000000O00000O0 ),scale =st .sem (OOO000000O00000O0 ))#line:2986
	return round (OO00OOO0OOO000O00 [1 ],2 )#line:2987
def STAT_get_mean_std_ci (O0O0O00O000OOO000 ,OO00OOOOOOO0OO00O ):#line:2989
	""#line:2990
	warnings .filterwarnings ("ignore")#line:2991
	OOO000000OOOOO0O0 =TOOLS_strdict_to_pd (str (O0O0O00O000OOO000 ))["content"].values /OO00OOOOOOO0OO00O #line:2992
	OOO0O0O000OOOOO00 =round (OOO000000OOOOO0O0 .mean (),2 )#line:2993
	O0OO00OOOO0O0OO0O =round (OOO000000OOOOO0O0 .std (ddof =1 ),2 )#line:2994
	if len (OOO000000OOOOO0O0 )<30 :#line:2996
		OO000O000O0OO0OOO =st .t .interval (0.95 ,df =len (OOO000000OOOOO0O0 )-1 ,loc =np .mean (OOO000000OOOOO0O0 ),scale =st .sem (OOO000000OOOOO0O0 ))#line:2997
	else :#line:2998
		OO000O000O0OO0OOO =st .norm .interval (0.95 ,loc =np .mean (OOO000000OOOOO0O0 ),scale =st .sem (OOO000000OOOOO0O0 ))#line:2999
	return pd .Series ((OOO0O0O000OOOOO00 ,O0OO00OOOO0O0OO0O ,OO000O000O0OO0OOO [1 ]))#line:3003
def STAT_findx_value (O0OOOOOO0O0O0000O ,OO0OOO00000OOO00O ):#line:3005
	""#line:3006
	warnings .filterwarnings ("ignore")#line:3007
	OO00OOO0000OO0O00 =TOOLS_strdict_to_pd (str (O0OOOOOO0O0O0000O ))#line:3008
	O00000O00O00O000O =OO00OOO0000OO0O00 .where (OO00OOO0000OO0O00 ["index"]==str (OO0OOO00000OOO00O ))#line:3010
	print (O00000O00O00O000O )#line:3011
	return O00000O00O00O000O #line:3012
def STAT_judge_x (OO00000OOO00OO0OO ,OOOOOOO0OOOOO0O0O ):#line:3014
	""#line:3015
	for O0OO00O00OO0OOOOO in OOOOOOO0OOOOO0O0O :#line:3016
		if OO00000OOO00OO0OO .find (O0OO00O00OO0OOOOO )>-1 :#line:3017
			return 1 #line:3018
def STAT_recent30 (OOO00O000OO0O0O00 ,OO0O0O0OOO00O0OO0 ):#line:3020
	""#line:3021
	import datetime #line:3022
	O0OOO0O00O000000O =OOO00O000OO0O0O00 [(OOO00O000OO0O0O00 ["报告日期"].dt .date >(datetime .date .today ()-datetime .timedelta (days =30 )))]#line:3026
	OO0O00O0000OO00O0 =O0OOO0O00O000000O .drop_duplicates (["报告编码"]).groupby (OO0O0O0OOO00O0OO0 ).agg (最近30天报告数 =("报告编码","nunique"),最近30天报告严重伤害数 =("伤害",lambda OO000O0O0OOOO0OOO :STAT_countpx (OO000O0O0OOOO0OOO .values ,"严重伤害")),最近30天报告死亡数量 =("伤害",lambda O000O0OO00OO000O0 :STAT_countpx (O000O0OO00OO000O0 .values ,"死亡")),最近30天报告单位个数 =("单位名称","nunique"),).reset_index ()#line:3033
	OO0O00O0000OO00O0 =STAT_basic_risk (OO0O00O0000OO00O0 ,"最近30天报告数","最近30天报告严重伤害数","最近30天报告死亡数量","最近30天报告单位个数").fillna (0 )#line:3034
	OO0O00O0000OO00O0 =OO0O00O0000OO00O0 .rename (columns ={"风险评分":"最近30天风险评分"})#line:3036
	return OO0O00O0000OO00O0 #line:3037
def STAT_PPR_ROR_1 (OO0OO0OO0O00OOOOO ,OOOO0O00O00O0OOOO ,O00O000OOOO00O0O0 ,OOO0O00O0OOO0O0OO ,O0O0O00OOOOOO0000 ):#line:3040
    ""#line:3041
    O0OO000O0O00O000O =O0O0O00OOOOOO0000 [(O0O0O00OOOOOO0000 [OO0OO0OO0O00OOOOO ]==OOOO0O00O00O0OOOO )]#line:3044
    O0O0O00OO0000000O =O0OO000O0O00O000O .loc [O0OO000O0O00O000O [O00O000OOOO00O0O0 ].str .contains (OOO0O00O0OOO0O0OO ,na =False )]#line:3045
    OO00OO0000O0000OO =O0O0O00OOOOOO0000 [(O0O0O00OOOOOO0000 [OO0OO0OO0O00OOOOO ]!=OOOO0O00O00O0OOOO )]#line:3046
    OOOOOOOO0OOOO0O00 =OO00OO0000O0000OO .loc [OO00OO0000O0000OO [O00O000OOOO00O0O0 ].str .contains (OOO0O00O0OOO0O0OO ,na =False )]#line:3047
    OOOOOO000O0OO00OO =(len (O0O0O00OO0000000O ),(len (O0OO000O0O00O000O )-len (O0O0O00OO0000000O )),len (OOOOOOOO0OOOO0O00 ),(len (OO00OO0000O0000OO )-len (OOOOOOOO0OOOO0O00 )))#line:3048
    if len (O0O0O00OO0000000O )>0 :#line:3049
        O000O00OO0O00000O =STAT_PPR_ROR_0 (len (O0O0O00OO0000000O ),(len (O0OO000O0O00O000O )-len (O0O0O00OO0000000O )),len (OOOOOOOO0OOOO0O00 ),(len (OO00OO0000O0000OO )-len (OOOOOOOO0OOOO0O00 )))#line:3050
    else :#line:3051
        O000O00OO0O00000O =(0 ,0 ,0 ,0 ,0 )#line:3052
    O000O00OOOOOO0OO0 =len (O0OO000O0O00O000O )#line:3055
    if O000O00OOOOOO0OO0 ==0 :#line:3056
        O000O00OOOOOO0OO0 =0.5 #line:3057
    return (OOO0O00O0OOO0O0OO ,len (O0O0O00OO0000000O ),round (len (O0O0O00OO0000000O )/O000O00OOOOOO0OO0 *100 ,2 ),round (O000O00OO0O00000O [0 ],2 ),round (O000O00OO0O00000O [1 ],2 ),round (O000O00OO0O00000O [2 ],2 ),round (O000O00OO0O00000O [3 ],2 ),round (O000O00OO0O00000O [4 ],2 ),str (OOOOOO000O0OO00OO ),)#line:3068
def STAT_basic_risk (OOOOOO0OOO0OO0000 ,O0O0OOO0OOOO0O000 ,OOOO00O0O0OO0O0OO ,O0000O0O0O0OOOO00 ,OOO0O0OOO0000OOOO ):#line:3072
	""#line:3073
	OOOOOO0OOO0OO0000 ["风险评分"]=0 #line:3074
	OOOOOO0OOO0OO0000 .loc [((OOOOOO0OOO0OO0000 [O0O0OOO0OOOO0O000 ]>=3 )&(OOOOOO0OOO0OO0000 [OOOO00O0O0OO0O0OO ]>=1 ))|(OOOOOO0OOO0OO0000 [O0O0OOO0OOOO0O000 ]>=5 ),"风险评分"]=OOOOOO0OOO0OO0000 ["风险评分"]+5 #line:3075
	OOOOOO0OOO0OO0000 .loc [(OOOOOO0OOO0OO0000 [OOOO00O0O0OO0O0OO ]>=3 ),"风险评分"]=OOOOOO0OOO0OO0000 ["风险评分"]+1 #line:3076
	OOOOOO0OOO0OO0000 .loc [(OOOOOO0OOO0OO0000 [O0000O0O0O0OOOO00 ]>=1 ),"风险评分"]=OOOOOO0OOO0OO0000 ["风险评分"]+10 #line:3077
	OOOOOO0OOO0OO0000 ["风险评分"]=OOOOOO0OOO0OO0000 ["风险评分"]+OOOOOO0OOO0OO0000 [OOO0O0OOO0000OOOO ]/100 #line:3078
	return OOOOOO0OOO0OO0000 #line:3079
def STAT_PPR_ROR_0 (OOOO000000O0OOO0O ,OO0O0OOOO000O0OOO ,OO0OOO00O0O000OO0 ,O0OO0OOOOOO0000O0 ):#line:3082
    ""#line:3083
    if OOOO000000O0OOO0O *OO0O0OOOO000O0OOO *OO0OOO00O0O000OO0 *O0OO0OOOOOO0000O0 ==0 :#line:3088
        OOOO000000O0OOO0O =OOOO000000O0OOO0O +1 #line:3089
        OO0O0OOOO000O0OOO =OO0O0OOOO000O0OOO +1 #line:3090
        OO0OOO00O0O000OO0 =OO0OOO00O0O000OO0 +1 #line:3091
        O0OO0OOOOOO0000O0 =O0OO0OOOOOO0000O0 +1 #line:3092
    O0O00O000OOO0OO00 =(OOOO000000O0OOO0O /(OOOO000000O0OOO0O +OO0O0OOOO000O0OOO ))/(OO0OOO00O0O000OO0 /(OO0OOO00O0O000OO0 +O0OO0OOOOOO0000O0 ))#line:3093
    O0OOO0O0O00000000 =math .sqrt (1 /OOOO000000O0OOO0O -1 /(OOOO000000O0OOO0O +OO0O0OOOO000O0OOO )+1 /OO0OOO00O0O000OO0 -1 /(OO0OOO00O0O000OO0 +O0OO0OOOOOO0000O0 ))#line:3094
    O000OOO0O0OO00OO0 =(math .exp (math .log (O0O00O000OOO0OO00 )-1.96 *O0OOO0O0O00000000 ),math .exp (math .log (O0O00O000OOO0OO00 )+1.96 *O0OOO0O0O00000000 ),)#line:3098
    O00OOOO0O0000OO0O =(OOOO000000O0OOO0O /OO0OOO00O0O000OO0 )/(OO0O0OOOO000O0OOO /O0OO0OOOOOO0000O0 )#line:3099
    OO00O0OO000O0OOO0 =math .sqrt (1 /OOOO000000O0OOO0O +1 /OO0O0OOOO000O0OOO +1 /OO0OOO00O0O000OO0 +1 /O0OO0OOOOOO0000O0 )#line:3100
    O00O00O00OO00O000 =(math .exp (math .log (O00OOOO0O0000OO0O )-1.96 *OO00O0OO000O0OOO0 ),math .exp (math .log (O00OOOO0O0000OO0O )+1.96 *OO00O0OO000O0OOO0 ),)#line:3104
    OO0O0O0OO0O0OO000 =((OOOO000000O0OOO0O *OO0O0OOOO000O0OOO -OO0O0OOOO000O0OOO *OO0OOO00O0O000OO0 )*(OOOO000000O0OOO0O *OO0O0OOOO000O0OOO -OO0O0OOOO000O0OOO *OO0OOO00O0O000OO0 )*(OOOO000000O0OOO0O +OO0O0OOOO000O0OOO +OO0OOO00O0O000OO0 +O0OO0OOOOOO0000O0 ))/((OOOO000000O0OOO0O +OO0O0OOOO000O0OOO )*(OO0OOO00O0O000OO0 +O0OO0OOOOOO0000O0 )*(OOOO000000O0OOO0O +OO0OOO00O0O000OO0 )*(OO0O0OOOO000O0OOO +O0OO0OOOOOO0000O0 ))#line:3107
    return O00OOOO0O0000OO0O ,O00O00O00OO00O000 [0 ],O0O00O000OOO0OO00 ,O000OOO0O0OO00OO0 [0 ],OO0O0O0OO0O0OO000 #line:3108
def STAT_find_keyword_risk (O0O00O0OO00000000 ,OO00O000OOOOOO000 ,O0OOOO0OOO0O0O00O ,OO000000OOOO0O000 ,OO000O0000OOOOOOO ):#line:3110
		""#line:3111
		O0O00O0OO00000000 =O0O00O0OO00000000 .drop_duplicates (["报告编码"]).reset_index (drop =True )#line:3112
		O000O00OO0000O0O0 =O0O00O0OO00000000 .groupby (OO00O000OOOOOO000 ).agg (证号关键字总数量 =(O0OOOO0OOO0O0O00O ,"count"),包含元素个数 =(OO000000OOOO0O000 ,"nunique"),包含元素 =(OO000000OOOO0O000 ,STAT_countx ),).reset_index ()#line:3117
		O0O00OO000O000O0O =OO00O000OOOOOO000 .copy ()#line:3119
		O0O00OO000O000O0O .append (OO000000OOOO0O000 )#line:3120
		OO00OO0O0O0O0O0O0 =O0O00O0OO00000000 .groupby (O0O00OO000O000O0O ).agg (计数 =(OO000000OOOO0O000 ,"count"),严重伤害数 =("伤害",lambda OO000OOO0O00OO0O0 :STAT_countpx (OO000OOO0O00OO0O0 .values ,"严重伤害")),死亡数量 =("伤害",lambda O00O0O0OO000O00OO :STAT_countpx (O00O0O0OO000O00OO .values ,"死亡")),单位个数 =("单位名称","nunique"),单位列表 =("单位名称",STAT_countx ),).reset_index ()#line:3127
		O00O0O0OO0OOOO0O0 =O0O00OO000O000O0O .copy ()#line:3130
		O00O0O0OO0OOOO0O0 .remove ("关键字")#line:3131
		O0O000OOOOO0O0O0O =O0O00O0OO00000000 .groupby (O00O0O0OO0OOOO0O0 ).agg (该元素总数 =(OO000000OOOO0O000 ,"count"),).reset_index ()#line:3134
		OO00OO0O0O0O0O0O0 ["证号总数"]=OO000O0000OOOOOOO #line:3136
		OO0OO0O0O0OO0O0O0 =pd .merge (OO00OO0O0O0O0O0O0 ,O000O00OO0000O0O0 ,on =OO00O000OOOOOO000 ,how ="left")#line:3137
		if len (OO0OO0O0O0OO0O0O0 )>0 :#line:3142
			OO0OO0O0O0OO0O0O0 [['数量均值','数量标准差','数量CI']]=OO0OO0O0O0OO0O0O0 .包含元素 .apply (lambda OO0OO0OO00OOO0O00 :STAT_get_mean_std_ci (OO0OO0OO00OOO0O00 ,1 ))#line:3143
		return OO0OO0O0O0OO0O0O0 #line:3146
def STAT_find_risk (OOO00O000O000OOO0 ,OOO0O0O0OO0000O0O ,OO00OO0OOOO0OO0OO ,OOO0OO0O00OOO0O00 ):#line:3152
		""#line:3153
		OOO00O000O000OOO0 =OOO00O000O000OOO0 .drop_duplicates (["报告编码"]).reset_index (drop =True )#line:3154
		O0O0000O000000OO0 =OOO00O000O000OOO0 .groupby (OOO0O0O0OO0000O0O ).agg (证号总数量 =(OO00OO0OOOO0OO0OO ,"count"),包含元素个数 =(OOO0OO0O00OOO0O00 ,"nunique"),包含元素 =(OOO0OO0O00OOO0O00 ,STAT_countx ),均值 =(OOO0OO0O00OOO0O00 ,STAT_get_mean ),标准差 =(OOO0OO0O00OOO0O00 ,STAT_get_std ),CI上限 =(OOO0OO0O00OOO0O00 ,STAT_get_95ci ),).reset_index ()#line:3162
		O0O00O00000000000 =OOO0O0O0OO0000O0O .copy ()#line:3164
		O0O00O00000000000 .append (OOO0OO0O00OOO0O00 )#line:3165
		OOO0OO0OO0O000O0O =OOO00O000O000OOO0 .groupby (O0O00O00000000000 ).agg (计数 =(OOO0OO0O00OOO0O00 ,"count"),严重伤害数 =("伤害",lambda OO0O0OO000OO00000 :STAT_countpx (OO0O0OO000OO00000 .values ,"严重伤害")),死亡数量 =("伤害",lambda O0O000O0O00O0O00O :STAT_countpx (O0O000O0O00O0O00O .values ,"死亡")),单位个数 =("单位名称","nunique"),单位列表 =("单位名称",STAT_countx ),).reset_index ()#line:3172
		OO00000OO00000000 =pd .merge (OOO0OO0OO0O000O0O ,O0O0000O000000OO0 ,on =OOO0O0O0OO0000O0O ,how ="left")#line:3174
		OO00000OO00000000 ["风险评分"]=0 #line:3176
		OO00000OO00000000 ["报表类型"]="dfx_findrisk"+OOO0OO0O00OOO0O00 #line:3177
		OO00000OO00000000 .loc [((OO00000OO00000000 ["计数"]>=3 )&(OO00000OO00000000 ["严重伤害数"]>=1 )|(OO00000OO00000000 ["计数"]>=5 )),"风险评分"]=OO00000OO00000000 ["风险评分"]+5 #line:3178
		OO00000OO00000000 .loc [(OO00000OO00000000 ["计数"]>=(OO00000OO00000000 ["均值"]+OO00000OO00000000 ["标准差"])),"风险评分"]=OO00000OO00000000 ["风险评分"]+1 #line:3179
		OO00000OO00000000 .loc [(OO00000OO00000000 ["计数"]>=OO00000OO00000000 ["CI上限"]),"风险评分"]=OO00000OO00000000 ["风险评分"]+1 #line:3180
		OO00000OO00000000 .loc [(OO00000OO00000000 ["严重伤害数"]>=3 )&(OO00000OO00000000 ["风险评分"]>=7 ),"风险评分"]=OO00000OO00000000 ["风险评分"]+1 #line:3181
		OO00000OO00000000 .loc [(OO00000OO00000000 ["死亡数量"]>=1 ),"风险评分"]=OO00000OO00000000 ["风险评分"]+10 #line:3182
		OO00000OO00000000 ["风险评分"]=OO00000OO00000000 ["风险评分"]+OO00000OO00000000 ["单位个数"]/100 #line:3183
		OO00000OO00000000 =OO00000OO00000000 .sort_values (by ="风险评分",ascending =[False ],na_position ="last").reset_index (drop =True )#line:3184
		return OO00000OO00000000 #line:3186
def TABLE_tree_Level_2 (O0O0O0OO0OO0OOOOO ,O0OO0OO0000O00000 ,OO0OOO000O00OOO0O ,*O0OOOO00OOO000OOO ):#line:3193
    ""#line:3194
    try :#line:3196
        OO0O00OOO0O0O00OO =O0O0O0OO0OO0OOOOO .columns #line:3197
    except :#line:3198
        return 0 #line:3199
    if "报告编码"in O0O0O0OO0OO0OOOOO .columns :#line:3201
        O0OO0OO0000O00000 =0 #line:3202
    try :#line:3203
        OOO0OOO00O0OO0000 =len (np .unique (O0O0O0OO0OO0OOOOO ["注册证编号/曾用注册证编号"].values ))#line:3204
    except :#line:3205
        OOO0OOO00O0OO0000 =10 #line:3206
    OOOO0000000O00000 =Toplevel ()#line:3209
    OOOO0000000O00000 .title ("报表查看器")#line:3210
    O000O0OOOOO000O0O =OOOO0000000O00000 .winfo_screenwidth ()#line:3211
    OOO00OO0OOO0OO0O0 =OOOO0000000O00000 .winfo_screenheight ()#line:3213
    OOOOO0OO0O00O00OO =1350 #line:3215
    OO0OO00O000OO00O0 =600 #line:3216
    try :#line:3217
        if O0OOOO00OOO000OOO [0 ]=="tools_x":#line:3218
           OO0OO00O000OO00O0 =60 #line:3219
    except :#line:3220
            pass #line:3221
    OOOOO00OOOO0O00OO =(O000O0OOOOO000O0O -OOOOO0OO0O00O00OO )/2 #line:3224
    O00O0O0O00000OO00 =(OOO00OO0OOO0OO0O0 -OO0OO00O000OO00O0 )/2 #line:3225
    OOOO0000000O00000 .geometry ("%dx%d+%d+%d"%(OOOOO0OO0O00O00OO ,OO0OO00O000OO00O0 ,OOOOO00OOOO0O00OO ,O00O0O0O00000OO00 ))#line:3226
    O00OO0O00O00OOOOO =ttk .Frame (OOOO0000000O00000 ,width =1310 ,height =20 )#line:3229
    O00OO0O00O00OOOOO .pack (side =TOP )#line:3230
    O0O0OO0O0OOO00000 =ttk .Frame (OOOO0000000O00000 ,width =1310 ,height =20 )#line:3231
    O0O0OO0O0OOO00000 .pack (side =BOTTOM )#line:3232
    OOOOOO0O0O0OO0O00 =ttk .Frame (OOOO0000000O00000 ,width =1310 ,height =600 )#line:3233
    OOOOOO0O0O0OO0O00 .pack (fill ="both",expand ="false")#line:3234
    if O0OO0OO0000O00000 ==0 :#line:3238
        PROGRAM_Menubar (OOOO0000000O00000 ,O0O0O0OO0OO0OOOOO ,O0OO0OO0000O00000 ,OO0OOO000O00OOO0O )#line:3239
    try :#line:3242
        OO00O0OOOO000000O =StringVar ()#line:3243
        OO00O0OOOO000000O .set ("产品类别")#line:3244
        def O0OOO000O0OOO0O00 (*OOO0O0OO0O0OOOO00 ):#line:3245
            OO00O0OOOO000000O .set (OO0OOOOOO0O000O00 .get ())#line:3246
        O0000O00OOOOO00O0 =StringVar ()#line:3247
        O0000O00OOOOO00O0 .set ("无源|诊断试剂")#line:3248
        O00000OO000O0000O =Label (O00OO0O00O00OOOOO ,text ="")#line:3249
        O00000OO000O0000O .pack (side =LEFT )#line:3250
        O00000OO000O0000O =Label (O00OO0O00O00OOOOO ,text ="位置：")#line:3251
        O00000OO000O0000O .pack (side =LEFT )#line:3252
        OOOO00O0O0O0OOO00 =StringVar ()#line:3253
        OO0OOOOOO0O000O00 =ttk .Combobox (O00OO0O00O00OOOOO ,width =12 ,height =30 ,state ="readonly",textvariable =OOOO00O0O0O0OOO00 )#line:3256
        OO0OOOOOO0O000O00 ["values"]=O0O0O0OO0OO0OOOOO .columns .tolist ()#line:3257
        OO0OOOOOO0O000O00 .current (0 )#line:3258
        OO0OOOOOO0O000O00 .bind ("<<ComboboxSelected>>",O0OOO000O0OOO0O00 )#line:3259
        OO0OOOOOO0O000O00 .pack (side =LEFT )#line:3260
        OOOOO000O0O0O0O00 =Label (O00OO0O00O00OOOOO ,text ="检索：")#line:3261
        OOOOO000O0O0O0O00 .pack (side =LEFT )#line:3262
        O0OOOOOOOOOO000OO =Entry (O00OO0O00O00OOOOO ,width =12 ,textvariable =O0000O00OOOOO00O0 ).pack (side =LEFT )#line:3263
        def OO00O0O0000O0OOO0 ():#line:3265
            pass #line:3266
        OOOOO0O0O00000O00 =Button (O00OO0O00O00OOOOO ,text ="导出",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :TOOLS_save_dict (O0O0O0OO0OO0OOOOO ),)#line:3280
        OOOOO0O0O00000O00 .pack (side =LEFT )#line:3281
        OO00O0O0OOOO0OOOO =Button (O00OO0O00O00OOOOO ,text ="视图",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :TABLE_tree_Level_2 (TOOLS_easyreadT (O0O0O0OO0OO0OOOOO ),1 ,OO0OOO000O00OOO0O ),)#line:3290
        if "详细描述T"not in O0O0O0OO0OO0OOOOO .columns :#line:3291
            OO00O0O0OOOO0OOOO .pack (side =LEFT )#line:3292
        OO00O0O0OOOO0OOOO =Button (O00OO0O00O00OOOOO ,text ="网",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :TOOLS_web_view (O0O0O0OO0OO0OOOOO ),)#line:3302
        if "详细描述T"not in O0O0O0OO0OO0OOOOO .columns :#line:3303
            pass #line:3304
        O0OO000O0OO0O00O0 =Button (O00OO0O00O00OOOOO ,text ="含",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :TABLE_tree_Level_2 (O0O0O0OO0OO0OOOOO .loc [O0O0O0OO0OO0OOOOO [OO00O0OOOO000000O .get ()].astype (str ).str .contains (str (O0000O00OOOOO00O0 .get ()),na =False )],1 ,OO0OOO000O00OOO0O ,),)#line:3323
        O0OO000O0OO0O00O0 .pack (side =LEFT )#line:3324
        O0OO000O0OO0O00O0 =Button (O00OO0O00O00OOOOO ,text ="无",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :TABLE_tree_Level_2 (O0O0O0OO0OO0OOOOO .loc [~O0O0O0OO0OO0OOOOO [OO00O0OOOO000000O .get ()].astype (str ).str .contains (str (O0000O00OOOOO00O0 .get ()),na =False )],1 ,OO0OOO000O00OOO0O ,),)#line:3341
        O0OO000O0OO0O00O0 .pack (side =LEFT )#line:3342
        O0OO000O0OO0O00O0 =Button (O00OO0O00O00OOOOO ,text ="大",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :TABLE_tree_Level_2 (O0O0O0OO0OO0OOOOO .loc [O0O0O0OO0OO0OOOOO [OO00O0OOOO000000O .get ()].astype (float )>float (O0000O00OOOOO00O0 .get ())],1 ,OO0OOO000O00OOO0O ,),)#line:3357
        O0OO000O0OO0O00O0 .pack (side =LEFT )#line:3358
        O0OO000O0OO0O00O0 =Button (O00OO0O00O00OOOOO ,text ="小",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :TABLE_tree_Level_2 (O0O0O0OO0OO0OOOOO .loc [O0O0O0OO0OO0OOOOO [OO00O0OOOO000000O .get ()].astype (float )<float (O0000O00OOOOO00O0 .get ())],1 ,OO0OOO000O00OOO0O ,),)#line:3373
        O0OO000O0OO0O00O0 .pack (side =LEFT )#line:3374
        O0OO000O0OO0O00O0 =Button (O00OO0O00O00OOOOO ,text ="等",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :TABLE_tree_Level_2 (O0O0O0OO0OO0OOOOO .loc [O0O0O0OO0OO0OOOOO [OO00O0OOOO000000O .get ()].astype (float )==float (O0000O00OOOOO00O0 .get ())],1 ,OO0OOO000O00OOO0O ,),)#line:3389
        O0OO000O0OO0O00O0 .pack (side =LEFT )#line:3390
        O0OO000O0OO0O00O0 =Button (O00OO0O00O00OOOOO ,text ="式",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :TOOLS_findin (O0O0O0OO0OO0OOOOO ,OO0OOO000O00OOO0O ))#line:3399
        O0OO000O0OO0O00O0 .pack (side =LEFT )#line:3400
        O0OO000O0OO0O00O0 =Button (O00OO0O00O00OOOOO ,text ="前",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :TABLE_tree_Level_2 (O0O0O0OO0OO0OOOOO .head (int (O0000O00OOOOO00O0 .get ())),1 ,OO0OOO000O00OOO0O ,),)#line:3415
        O0OO000O0OO0O00O0 .pack (side =LEFT )#line:3416
        O0OO000O0OO0O00O0 =Button (O00OO0O00O00OOOOO ,text ="升",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :TABLE_tree_Level_2 (O0O0O0OO0OO0OOOOO .sort_values (by =(OO00O0OOOO000000O .get ()),ascending =[True ],na_position ="last"),1 ,OO0OOO000O00OOO0O ,),)#line:3431
        O0OO000O0OO0O00O0 .pack (side =LEFT )#line:3432
        O0OO000O0OO0O00O0 =Button (O00OO0O00O00OOOOO ,text ="降",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :TABLE_tree_Level_2 (O0O0O0OO0OO0OOOOO .sort_values (by =(OO00O0OOOO000000O .get ()),ascending =[False ],na_position ="last"),1 ,OO0OOO000O00OOO0O ,),)#line:3447
        O0OO000O0OO0O00O0 .pack (side =LEFT )#line:3448
        O0OO000O0OO0O00O0 =Button (O00OO0O00O00OOOOO ,text ="重",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :TABLE_tree_Level_2 (O0O0O0OO0OO0OOOOO .drop_duplicates (OO00O0OOOO000000O .get ()),1 ,OO0OOO000O00OOO0O ,),)#line:3464
        O0OO000O0OO0O00O0 .pack (side =LEFT )#line:3465
        O0OO000O0OO0O00O0 =Button (O00OO0O00O00OOOOO ,text ="统",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :TABLE_tree_Level_2 (STAT_pinzhong (O0O0O0OO0OO0OOOOO ,OO00O0OOOO000000O .get (),0 ),1 ,OO0OOO000O00OOO0O ,),)#line:3480
        O0OO000O0OO0O00O0 .pack (side =LEFT )#line:3481
        O0OO000O0OO0O00O0 =Button (O00OO0O00O00OOOOO ,text ="SQL",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :TOOLS_sql (O0O0O0OO0OO0OOOOO ),)#line:3492
        O0OO000O0OO0O00O0 .pack (side =LEFT )#line:3493
    except :#line:3496
        pass #line:3497
    if ini ["模式"]!="其他":#line:3500
        O000OO00000O0OO0O =Button (O00OO0O00O00OOOOO ,text ="近月",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :TABLE_tree_Level_2 (O0O0O0OO0OO0OOOOO [(O0O0O0OO0OO0OOOOO ["最近30天报告单位个数"]>=1 )],1 ,OO0OOO000O00OOO0O ,),)#line:3513
        if "最近30天报告数"in O0O0O0OO0OO0OOOOO .columns :#line:3514
            O000OO00000O0OO0O .pack (side =LEFT )#line:3515
        O0OO000O0OO0O00O0 =Button (O00OO0O00O00OOOOO ,text ="图表",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :DRAW_pre (O0O0O0OO0OO0OOOOO ),)#line:3527
        if O0OO0OO0000O00000 !=0 :#line:3528
            O0OO000O0OO0O00O0 .pack (side =LEFT )#line:3529
        def O0OOOOOOOOOO0OO0O ():#line:3534
            pass #line:3535
        if O0OO0OO0000O00000 ==0 :#line:3538
            O000OO00000O0OO0O =Button (O00OO0O00O00OOOOO ,text ="精简",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :TABLE_tree_Level_2 (TOOLS_easyread2 (O0O0O0OO0OO0OOOOO ),1 ,OO0OOO000O00OOO0O ,),)#line:3552
            O000OO00000O0OO0O .pack (side =LEFT )#line:3553
        if O0OO0OO0000O00000 ==0 :#line:3556
            O000OO00000O0OO0O =Button (O00OO0O00O00OOOOO ,text ="证号",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :TABLE_tree_Level_2 (Countall (O0O0O0OO0OO0OOOOO ).df_zhenghao (),1 ,OO0OOO000O00OOO0O ,),)#line:3570
            O000OO00000O0OO0O .pack (side =LEFT )#line:3571
            O000OO00000O0OO0O =Button (O00OO0O00O00OOOOO ,text ="图",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :DRAW_pre (Countall (O0O0O0OO0OO0OOOOO ).df_zhenghao ()))#line:3580
            O000OO00000O0OO0O .pack (side =LEFT )#line:3581
            O000OO00000O0OO0O =Button (O00OO0O00O00OOOOO ,text ="批号",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :TABLE_tree_Level_2 (Countall (O0O0O0OO0OO0OOOOO ).df_pihao (),1 ,OO0OOO000O00OOO0O ,),)#line:3596
            O000OO00000O0OO0O .pack (side =LEFT )#line:3597
            O000OO00000O0OO0O =Button (O00OO0O00O00OOOOO ,text ="图",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :DRAW_pre (Countall (O0O0O0OO0OO0OOOOO ).df_pihao ()))#line:3606
            O000OO00000O0OO0O .pack (side =LEFT )#line:3607
            O000OO00000O0OO0O =Button (O00OO0O00O00OOOOO ,text ="型号",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :TABLE_tree_Level_2 (Countall (O0O0O0OO0OO0OOOOO ).df_xinghao (),1 ,OO0OOO000O00OOO0O ,),)#line:3622
            O000OO00000O0OO0O .pack (side =LEFT )#line:3623
            O000OO00000O0OO0O =Button (O00OO0O00O00OOOOO ,text ="图",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :DRAW_pre (Countall (O0O0O0OO0OO0OOOOO ).df_xinghao ()))#line:3632
            O000OO00000O0OO0O .pack (side =LEFT )#line:3633
            O000OO00000O0OO0O =Button (O00OO0O00O00OOOOO ,text ="规格",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :TABLE_tree_Level_2 (Countall (O0O0O0OO0OO0OOOOO ).df_guige (),1 ,OO0OOO000O00OOO0O ,),)#line:3648
            O000OO00000O0OO0O .pack (side =LEFT )#line:3649
            O000OO00000O0OO0O =Button (O00OO0O00O00OOOOO ,text ="图",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :DRAW_pre (Countall (O0O0O0OO0OO0OOOOO ).df_guige ()))#line:3658
            O000OO00000O0OO0O .pack (side =LEFT )#line:3659
            O000OO00000O0OO0O =Button (O00OO0O00O00OOOOO ,text ="企业",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :TABLE_tree_Level_2 (Countall (O0O0O0OO0OO0OOOOO ).df_chiyouren (),1 ,OO0OOO000O00OOO0O ,),)#line:3674
            O000OO00000O0OO0O .pack (side =LEFT )#line:3675
            O000OO00000O0OO0O =Button (O00OO0O00O00OOOOO ,text ="县区",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :TABLE_tree_Level_2 (Countall (O0O0O0OO0OO0OOOOO ).df_org ("监测机构"),1 ,OO0OOO000O00OOO0O ,),)#line:3691
            O000OO00000O0OO0O .pack (side =LEFT )#line:3692
            O000OO00000O0OO0O =Button (O00OO0O00O00OOOOO ,text ="单位",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :TABLE_tree_Level_2 (Countall (O0O0O0OO0OO0OOOOO ).df_user (),1 ,OO0OOO000O00OOO0O ,),)#line:3705
            O000OO00000O0OO0O .pack (side =LEFT )#line:3706
            O000OO00000O0OO0O =Button (O00OO0O00O00OOOOO ,text ="年龄",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :TABLE_tree_Level_2 (Countall (O0O0O0OO0OO0OOOOO ).df_age (),1 ,OO0OOO000O00OOO0O ,),)#line:3720
            O000OO00000O0OO0O .pack (side =LEFT )#line:3721
            O000OO00000O0OO0O =Button (O00OO0O00O00OOOOO ,text ="时隔",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :TABLE_tree_Level_2 (TOOLS_deep_view (O0O0O0OO0OO0OOOOO ,["时隔"],["报告编码","nunique"],0 ),1 ,OO0OOO000O00OOO0O ,),)#line:3735
            O000OO00000O0OO0O .pack (side =LEFT )#line:3736
            O000OO00000O0OO0O =Button (O00OO0O00O00OOOOO ,text ="表现",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :TABLE_tree_Level_2 (Countall (O0O0O0OO0OO0OOOOO ).df_psur (),1 ,OO0OOO000O00OOO0O ,),)#line:3750
            if "UDI"not in O0O0O0OO0OO0OOOOO .columns :#line:3751
                O000OO00000O0OO0O .pack (side =LEFT )#line:3752
            O000OO00000O0OO0O =Button (O00OO0O00O00OOOOO ,text ="表现",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :TABLE_tree_Level_2 (TOOLS_get_guize2 (O0O0O0OO0OO0OOOOO ),1 ,OO0OOO000O00OOO0O ,),)#line:3765
            if "UDI"in O0O0O0OO0OO0OOOOO .columns :#line:3766
                O000OO00000O0OO0O .pack (side =LEFT )#line:3767
            O000OO00000O0OO0O =Button (O00OO0O00O00OOOOO ,text ="发生时间",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :TOOLS_time (O0O0O0OO0OO0OOOOO ,"事件发生日期",0 ),)#line:3776
            O000OO00000O0OO0O .pack (side =LEFT )#line:3777
            O000OO00000O0OO0O =Button (O00OO0O00O00OOOOO ,text ="报告时间",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :DRAW_make_one (TOOLS_time (O0O0O0OO0OO0OOOOO ,"报告日期",1 ),"时间托帕斯图","time","报告总数","超级托帕斯图(严重伤害数)"),)#line:3787
            O000OO00000O0OO0O .pack (side =LEFT )#line:3788
    try :#line:3794
        OOOO0O00O000OOOO0 =ttk .Label (O0O0OO0O0OOO00000 ,text ="方法：")#line:3796
        OOOO0O00O000OOOO0 .pack (side =LEFT )#line:3797
        O00OO00O00OO00O00 =StringVar ()#line:3798
        O00OOOOO0OO0OO0O0 =ttk .Combobox (O0O0OO0O0OOO00000 ,width =15 ,textvariable =O00OO00O00OO00O00 ,state ='readonly')#line:3799
        O00OOOOO0OO0OO0O0 ['values']=("分组统计","数据透视","拆分成字典(X-Y)","描述性统计(X)","饼图(XY)","柱状图(XY)","折线图(XY)","托帕斯图(XY)","堆叠柱状图（X-YZ）","追加外部表格信息","添加到外部表格")#line:3800
        O00OOOOO0OO0OO0O0 .pack (side =LEFT )#line:3804
        O00OOOOO0OO0OO0O0 .current (0 )#line:3805
        OO0OOOOO0OOO000O0 =ttk .Label (O0O0OO0O0OOO00000 ,text ="分组列（X-Y-Z）:")#line:3806
        OO0OOOOO0OOO000O0 .pack (side =LEFT )#line:3807
        OOOO0OO00OO0O0OO0 =StringVar ()#line:3810
        O0000OO00OOOO0000 =ttk .Combobox (O0O0OO0O0OOO00000 ,width =15 ,textvariable =OOOO0OO00OO0O0OO0 ,state ='readonly')#line:3811
        O0000OO00OOOO0000 ['values']=O0O0O0OO0OO0OOOOO .columns .tolist ()#line:3812
        O0000OO00OOOO0000 .pack (side =LEFT )#line:3813
        O0OO0OOO0OOOOO000 =StringVar ()#line:3814
        O0000000O0O00000O =ttk .Combobox (O0O0OO0O0OOO00000 ,width =15 ,textvariable =O0OO0OOO0OOOOO000 ,state ='readonly')#line:3815
        O0000000O0O00000O ['values']=O0O0O0OO0OO0OOOOO .columns .tolist ()#line:3816
        O0000000O0O00000O .pack (side =LEFT )#line:3817
        O0O000O0OO0OO0O00 =StringVar ()#line:3818
        O0O0OO000O00O00O0 =ttk .Combobox (O0O0OO0O0OOO00000 ,width =15 ,textvariable =O0O000O0OO0OO0O00 ,state ='readonly')#line:3819
        O0O0OO000O00O00O0 ['values']=O0O0O0OO0OO0OOOOO .columns .tolist ()#line:3820
        O0O0OO000O00O00O0 .pack (side =LEFT )#line:3821
        OOO0O00OO0OO000O0 =StringVar ()#line:3822
        O00OO00O00000O00O =StringVar ()#line:3823
        OO0OOOOO0OOO000O0 =ttk .Label (O0O0OO0O0OOO00000 ,text ="计算列（V-M）:")#line:3824
        OO0OOOOO0OOO000O0 .pack (side =LEFT )#line:3825
        O000O00O0O0OOOOOO =ttk .Combobox (O0O0OO0O0OOO00000 ,width =10 ,textvariable =OOO0O00OO0OO000O0 ,state ='readonly')#line:3827
        O000O00O0O0OOOOOO ['values']=O0O0O0OO0OO0OOOOO .columns .tolist ()#line:3828
        O000O00O0O0OOOOOO .pack (side =LEFT )#line:3829
        O0O000O0000O0OOOO =ttk .Combobox (O0O0OO0O0OOO00000 ,width =10 ,textvariable =O00OO00O00000O00O ,state ='readonly')#line:3830
        O0O000O0000O0OOOO ['values']=["计数","求和","唯一值计数"]#line:3831
        O0O000O0000O0OOOO .pack (side =LEFT )#line:3832
        OOOO000OOOO00OOO0 =Button (O0O0OO0O0OOO00000 ,text ="自助报表",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :TOOLS_Autotable_0 (O0O0O0OO0OO0OOOOO ,O00OOOOO0OO0OO0O0 .get (),OOOO0OO00OO0O0OO0 .get (),O0OO0OOO0OOOOO000 .get (),O0O000O0OO0OO0O00 .get (),OOO0O00OO0OO000O0 .get (),O00OO00O00000O00O .get (),O0O0O0OO0OO0OOOOO ))#line:3834
        OOOO000OOOO00OOO0 .pack (side =LEFT )#line:3835
        O0OO000O0OO0O00O0 =Button (O0O0OO0O0OOO00000 ,text ="去首行",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :TABLE_tree_Level_2 (O0O0O0OO0OO0OOOOO [1 :],1 ,OO0OOO000O00OOO0O ,))#line:3852
        O0OO000O0OO0O00O0 .pack (side =LEFT )#line:3853
        O0OO000O0OO0O00O0 =Button (O0O0OO0O0OOO00000 ,text ="去尾行",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :TABLE_tree_Level_2 (O0O0O0OO0OO0OOOOO [:-1 ],1 ,OO0OOO000O00OOO0O ,),)#line:3868
        O0OO000O0OO0O00O0 .pack (side =LEFT )#line:3869
        O000OO00000O0OO0O =Button (O0O0OO0O0OOO00000 ,text ="行数:"+str (len (O0O0O0OO0OO0OOOOO )),bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",)#line:3879
        O000OO00000O0OO0O .pack (side =LEFT )#line:3880
    except :#line:3883
        showinfo (title ="提示信息",message ="界面初始化失败。")#line:3884
    try :#line:3889
        if O0OOOO00OOO000OOO [0 ]=="tools_x":#line:3890
           return 0 #line:3891
    except :#line:3892
            pass #line:3893
    O00O00O0000O0OO00 =O0O0O0OO0OO0OOOOO .values .tolist ()#line:3896
    OOOO00OO0O00O0OOO =O0O0O0OO0OO0OOOOO .columns .values .tolist ()#line:3897
    OOOO00OO000O0OOO0 =ttk .Treeview (OOOOOO0O0O0OO0O00 ,columns =OOOO00OO0O00O0OOO ,show ="headings",height =45 )#line:3898
    for O0OO00OO000OOO00O in OOOO00OO0O00O0OOO :#line:3901
        OOOO00OO000O0OOO0 .heading (O0OO00OO000OOO00O ,text =O0OO00OO000OOO00O )#line:3902
    for OO0O00000000O0O00 in O00O00O0000O0OO00 :#line:3903
        OOOO00OO000O0OOO0 .insert ("","end",values =OO0O00000000O0O00 )#line:3904
    for OO0OOOOOO00OOOOO0 in OOOO00OO0O00O0OOO :#line:3906
        try :#line:3907
            OOOO00OO000O0OOO0 .column (OO0OOOOOO00OOOOO0 ,minwidth =0 ,width =80 ,stretch =NO )#line:3908
            if "只剩"in OO0OOOOOO00OOOOO0 :#line:3909
                OOOO00OO000O0OOO0 .column (OO0OOOOOO00OOOOO0 ,minwidth =0 ,width =150 ,stretch =NO )#line:3910
        except :#line:3911
            pass #line:3912
    OO0O0OO0000OOOO00 =["评分说明"]#line:3916
    OO00O0OOO00OOOOOO =["该单位喜好上报的品种统计","报告编码","产品名称","上报机构描述","持有人处理描述","该注册证编号/曾用注册证编号报告数量","通用名称","该批准文号报告数量","上市许可持有人名称",]#line:3929
    OO0O0O000O0O00OO0 =["注册证编号/曾用注册证编号","监测机构","报告月份","报告季度","单位列表","单位名称",]#line:3937
    O0OOO00O0O00O00OO =["管理类别",]#line:3941
    for OO0OOOOOO00OOOOO0 in OO00O0OOO00OOOOOO :#line:3944
        try :#line:3945
            OOOO00OO000O0OOO0 .column (OO0OOOOOO00OOOOO0 ,minwidth =0 ,width =200 ,stretch =NO )#line:3946
        except :#line:3947
            pass #line:3948
    for OO0OOOOOO00OOOOO0 in OO0O0O000O0O00OO0 :#line:3951
        try :#line:3952
            OOOO00OO000O0OOO0 .column (OO0OOOOOO00OOOOO0 ,minwidth =0 ,width =140 ,stretch =NO )#line:3953
        except :#line:3954
            pass #line:3955
    for OO0OOOOOO00OOOOO0 in O0OOO00O0O00O00OO :#line:3956
        try :#line:3957
            OOOO00OO000O0OOO0 .column (OO0OOOOOO00OOOOO0 ,minwidth =0 ,width =40 ,stretch =NO )#line:3958
        except :#line:3959
            pass #line:3960
    for OO0OOOOOO00OOOOO0 in OO0O0OO0000OOOO00 :#line:3961
        try :#line:3962
            OOOO00OO000O0OOO0 .column (OO0OOOOOO00OOOOO0 ,minwidth =0 ,width =800 ,stretch =NO )#line:3963
        except :#line:3964
            pass #line:3965
    try :#line:3967
        OOOO00OO000O0OOO0 .column ("请选择需要查看的表格",minwidth =1 ,width =300 ,stretch =NO )#line:3970
    except :#line:3971
        pass #line:3972
    try :#line:3974
        OOOO00OO000O0OOO0 .column ("详细描述T",minwidth =1 ,width =2300 ,stretch =NO )#line:3977
    except :#line:3978
        pass #line:3979
    OOO0000O0OO0OOOOO =Scrollbar (OOOOOO0O0O0OO0O00 ,orient ="vertical")#line:3981
    OOO0000O0OO0OOOOO .pack (side =RIGHT ,fill =Y )#line:3982
    OOO0000O0OO0OOOOO .config (command =OOOO00OO000O0OOO0 .yview )#line:3983
    OOOO00OO000O0OOO0 .config (yscrollcommand =OOO0000O0OO0OOOOO .set )#line:3984
    OOO00O0O0OO0OO0O0 =Scrollbar (OOOOOO0O0O0OO0O00 ,orient ="horizontal")#line:3986
    OOO00O0O0OO0OO0O0 .pack (side =BOTTOM ,fill =X )#line:3987
    OOO00O0O0OO0OO0O0 .config (command =OOOO00OO000O0OOO0 .xview )#line:3988
    OOOO00OO000O0OOO0 .config (yscrollcommand =OOO0000O0OO0OOOOO .set )#line:3989
    def O0OOO0O0O0OOO00O0 (OOO0000O00000O0O0 ,OOOO0OOO0O0O0O0O0 ,OO00O0OOOO0O00000 ):#line:3992
        for OOOOO0OO0O0O0O0OO in OOOO00OO000O0OOO0 .selection ():#line:3994
            O0OOO000OO000OO0O =OOOO00OO000O0OOO0 .item (OOOOO0OO0O0O0O0OO ,"values")#line:3995
        OO00OOO00O0000O0O =dict (zip (OOOO0OOO0O0O0O0O0 ,O0OOO000OO000OO0O ))#line:3996
        if "详细描述T"in OOOO0OOO0O0O0O0O0 and "{"in OO00OOO00O0000O0O ["详细描述T"]:#line:4000
            OO00OOO0O0O0000OO =eval (OO00OOO00O0000O0O ["详细描述T"])#line:4001
            OO00OOO0O0O0000OO =pd .DataFrame .from_dict (OO00OOO0O0O0000OO ,orient ="index",columns =["content"]).reset_index ()#line:4002
            OO00OOO0O0O0000OO =OO00OOO0O0O0000OO .sort_values (by ="content",ascending =[False ],na_position ="last")#line:4003
            DRAW_make_one (OO00OOO0O0O0000OO ,OO00OOO00O0000O0O ["条目"],"index","content","饼图")#line:4004
            return 0 #line:4005
        if "dfx_deepview"in OO00OOO00O0000O0O ["报表类型"]:#line:4010
            O0O00OOO000000O0O =eval (OO00OOO00O0000O0O ["报表类型"][13 :])#line:4011
            O0OO000OO0O0OO000 =OO00O0OOOO0O00000 .copy ()#line:4012
            for O0OO0O00O00OOO0OO in O0O00OOO000000O0O :#line:4013
                O0OO000OO0O0OO000 =O0OO000OO0O0OO000 [(O0OO000OO0O0OO000 [O0OO0O00O00OOO0OO ].astype (str )==O0OOO000OO000OO0O [O0O00OOO000000O0O .index (O0OO0O00O00OOO0OO )])].copy ()#line:4014
            O0OO000OO0O0OO000 ["报表类型"]="ori_dfx_deepview"#line:4015
            TABLE_tree_Level_2 (O0OO000OO0O0OO000 ,0 ,O0OO000OO0O0OO000 )#line:4016
            return 0 #line:4017
        if "dfx_deepvie2"in OO00OOO00O0000O0O ["报表类型"]:#line:4020
            O0O00OOO000000O0O =eval (OO00OOO00O0000O0O ["报表类型"][13 :])#line:4021
            O0OO000OO0O0OO000 =OO00O0OOOO0O00000 .copy ()#line:4022
            for O0OO0O00O00OOO0OO in O0O00OOO000000O0O :#line:4023
                O0OO000OO0O0OO000 =O0OO000OO0O0OO000 [O0OO000OO0O0OO000 [O0OO0O00O00OOO0OO ].str .contains (O0OOO000OO000OO0O [O0O00OOO000000O0O .index (O0OO0O00O00OOO0OO )],na =False )].copy ()#line:4024
            O0OO000OO0O0OO000 ["报表类型"]="ori_dfx_deepview"#line:4025
            TABLE_tree_Level_2 (O0OO000OO0O0OO000 ,0 ,O0OO000OO0O0OO000 )#line:4026
            return 0 #line:4027
        if "dfx_zhenghao"in OO00OOO00O0000O0O ["报表类型"]:#line:4031
            O0OO000OO0O0OO000 =OO00O0OOOO0O00000 [(OO00O0OOOO0O00000 ["注册证编号/曾用注册证编号"]==OO00OOO00O0000O0O ["注册证编号/曾用注册证编号"])].copy ()#line:4032
            O0OO000OO0O0OO000 ["报表类型"]="ori_dfx_zhenghao"#line:4033
            TABLE_tree_Level_2 (O0OO000OO0O0OO000 ,0 ,O0OO000OO0O0OO000 )#line:4034
            return 0 #line:4035
        if ("dfx_pihao"in OO00OOO00O0000O0O ["报表类型"]or "dfx_findrisk"in OO00OOO00O0000O0O ["报表类型"]or "dfx_xinghao"in OO00OOO00O0000O0O ["报表类型"]or "dfx_guige"in OO00OOO00O0000O0O ["报表类型"])and OOO0OOO00O0OO0000 ==1 :#line:4039
            O0OO0O00O0000O0OO ="CLT"#line:4040
            if "pihao"in OO00OOO00O0000O0O ["报表类型"]or "产品批号"in OO00OOO00O0000O0O ["报表类型"]:#line:4041
                O0OO0O00O0000O0OO ="产品批号"#line:4042
            if "xinghao"in OO00OOO00O0000O0O ["报表类型"]or "型号"in OO00OOO00O0000O0O ["报表类型"]:#line:4043
                O0OO0O00O0000O0OO ="型号"#line:4044
            if "guige"in OO00OOO00O0000O0O ["报表类型"]or "规格"in OO00OOO00O0000O0O ["报表类型"]:#line:4045
                O0OO0O00O0000O0OO ="规格"#line:4046
            if "事件发生季度"in OO00OOO00O0000O0O ["报表类型"]:#line:4047
                O0OO0O00O0000O0OO ="事件发生季度"#line:4048
            if "事件发生月份"in OO00OOO00O0000O0O ["报表类型"]:#line:4049
                O0OO0O00O0000O0OO ="事件发生月份"#line:4050
            if "性别"in OO00OOO00O0000O0O ["报表类型"]:#line:4051
                O0OO0O00O0000O0OO ="性别"#line:4052
            if "年龄段"in OO00OOO00O0000O0O ["报表类型"]:#line:4053
                O0OO0O00O0000O0OO ="年龄段"#line:4054
            O0OO000OO0O0OO000 =OO00O0OOOO0O00000 [(OO00O0OOOO0O00000 ["注册证编号/曾用注册证编号"]==OO00OOO00O0000O0O ["注册证编号/曾用注册证编号"])&(OO00O0OOOO0O00000 [O0OO0O00O0000O0OO ]==OO00OOO00O0000O0O [O0OO0O00O0000O0OO ])].copy ()#line:4055
            O0OO000OO0O0OO000 ["报表类型"]="ori_pihao"#line:4056
            TABLE_tree_Level_2 (O0OO000OO0O0OO000 ,0 ,O0OO000OO0O0OO000 )#line:4057
            return 0 #line:4058
        if ("findrisk"in OO00OOO00O0000O0O ["报表类型"]or "dfx_pihao"in OO00OOO00O0000O0O ["报表类型"]or "dfx_xinghao"in OO00OOO00O0000O0O ["报表类型"]or "dfx_guige"in OO00OOO00O0000O0O ["报表类型"])and OOO0OOO00O0OO0000 !=1 :#line:4062
            O0OO000OO0O0OO000 =O0O0O0OO0OO0OOOOO [(O0O0O0OO0OO0OOOOO ["注册证编号/曾用注册证编号"]==OO00OOO00O0000O0O ["注册证编号/曾用注册证编号"])].copy ()#line:4063
            O0OO000OO0O0OO000 ["报表类型"]=OO00OOO00O0000O0O ["报表类型"]+"1"#line:4064
            TABLE_tree_Level_2 (O0OO000OO0O0OO000 ,1 ,OO00O0OOOO0O00000 )#line:4065
            return 0 #line:4067
        if "dfx_org监测机构"in OO00OOO00O0000O0O ["报表类型"]:#line:4070
            O0OO000OO0O0OO000 =OO00O0OOOO0O00000 [(OO00O0OOOO0O00000 ["监测机构"]==OO00OOO00O0000O0O ["监测机构"])].copy ()#line:4071
            O0OO000OO0O0OO000 ["报表类型"]="ori_dfx_org"#line:4072
            TABLE_tree_Level_2 (O0OO000OO0O0OO000 ,0 ,O0OO000OO0O0OO000 )#line:4073
            return 0 #line:4074
        if "dfx_org市级监测机构"in OO00OOO00O0000O0O ["报表类型"]:#line:4076
            O0OO000OO0O0OO000 =OO00O0OOOO0O00000 [(OO00O0OOOO0O00000 ["市级监测机构"]==OO00OOO00O0000O0O ["市级监测机构"])].copy ()#line:4077
            O0OO000OO0O0OO000 ["报表类型"]="ori_dfx_org"#line:4078
            TABLE_tree_Level_2 (O0OO000OO0O0OO000 ,0 ,O0OO000OO0O0OO000 )#line:4079
            return 0 #line:4080
        if "dfx_user"in OO00OOO00O0000O0O ["报表类型"]:#line:4083
            O0OO000OO0O0OO000 =OO00O0OOOO0O00000 [(OO00O0OOOO0O00000 ["单位名称"]==OO00OOO00O0000O0O ["单位名称"])].copy ()#line:4084
            O0OO000OO0O0OO000 ["报表类型"]="ori_dfx_user"#line:4085
            TABLE_tree_Level_2 (O0OO000OO0O0OO000 ,0 ,O0OO000OO0O0OO000 )#line:4086
            return 0 #line:4087
        if "dfx_chiyouren"in OO00OOO00O0000O0O ["报表类型"]:#line:4091
            O0OO000OO0O0OO000 =OO00O0OOOO0O00000 [(OO00O0OOOO0O00000 ["上市许可持有人名称"]==OO00OOO00O0000O0O ["上市许可持有人名称"])].copy ()#line:4092
            O0OO000OO0O0OO000 ["报表类型"]="ori_dfx_chiyouren"#line:4093
            TABLE_tree_Level_2 (O0OO000OO0O0OO000 ,0 ,O0OO000OO0O0OO000 )#line:4094
            return 0 #line:4095
        if "dfx_chanpin"in OO00OOO00O0000O0O ["报表类型"]:#line:4097
            O0OO000OO0O0OO000 =OO00O0OOOO0O00000 [(OO00O0OOOO0O00000 ["产品名称"]==OO00OOO00O0000O0O ["产品名称"])].copy ()#line:4098
            O0OO000OO0O0OO000 ["报表类型"]="ori_dfx_chanpin"#line:4099
            TABLE_tree_Level_2 (O0OO000OO0O0OO000 ,0 ,O0OO000OO0O0OO000 )#line:4100
            return 0 #line:4101
        if "dfx_findrisk事件发生季度1"in OO00OOO00O0000O0O ["报表类型"]:#line:4106
            O0OO000OO0O0OO000 =OO00O0OOOO0O00000 [(OO00O0OOOO0O00000 ["注册证编号/曾用注册证编号"]==OO00OOO00O0000O0O ["注册证编号/曾用注册证编号"])&(OO00O0OOOO0O00000 ["事件发生季度"]==OO00OOO00O0000O0O ["事件发生季度"])].copy ()#line:4107
            O0OO000OO0O0OO000 ["报表类型"]="ori_dfx_findrisk事件发生季度"#line:4108
            TABLE_tree_Level_2 (O0OO000OO0O0OO000 ,0 ,O0OO000OO0O0OO000 )#line:4109
            return 0 #line:4110
        if "dfx_findrisk事件发生月份1"in OO00OOO00O0000O0O ["报表类型"]:#line:4113
            O0OO000OO0O0OO000 =OO00O0OOOO0O00000 [(OO00O0OOOO0O00000 ["注册证编号/曾用注册证编号"]==OO00OOO00O0000O0O ["注册证编号/曾用注册证编号"])&(OO00O0OOOO0O00000 ["事件发生月份"]==OO00OOO00O0000O0O ["事件发生月份"])].copy ()#line:4114
            O0OO000OO0O0OO000 ["报表类型"]="ori_dfx_findrisk事件发生月份"#line:4115
            TABLE_tree_Level_2 (O0OO000OO0O0OO000 ,0 ,O0OO000OO0O0OO000 )#line:4116
            return 0 #line:4117
        if ("keyword_findrisk"in OO00OOO00O0000O0O ["报表类型"])and OOO0OOO00O0OO0000 ==1 :#line:4120
            O0OO0O00O0000O0OO ="CLT"#line:4121
            if "批号"in OO00OOO00O0000O0O ["报表类型"]:#line:4122
                O0OO0O00O0000O0OO ="产品批号"#line:4123
            if "事件发生季度"in OO00OOO00O0000O0O ["报表类型"]:#line:4124
                O0OO0O00O0000O0OO ="事件发生季度"#line:4125
            if "事件发生月份"in OO00OOO00O0000O0O ["报表类型"]:#line:4126
                O0OO0O00O0000O0OO ="事件发生月份"#line:4127
            if "性别"in OO00OOO00O0000O0O ["报表类型"]:#line:4128
                O0OO0O00O0000O0OO ="性别"#line:4129
            if "年龄段"in OO00OOO00O0000O0O ["报表类型"]:#line:4130
                O0OO0O00O0000O0OO ="年龄段"#line:4131
            O0OO000OO0O0OO000 =OO00O0OOOO0O00000 [(OO00O0OOOO0O00000 ["注册证编号/曾用注册证编号"]==OO00OOO00O0000O0O ["注册证编号/曾用注册证编号"])&(OO00O0OOOO0O00000 [O0OO0O00O0000O0OO ]==OO00OOO00O0000O0O [O0OO0O00O0000O0OO ])].copy ()#line:4132
            O0OO000OO0O0OO000 ["关键字查找列"]=""#line:4133
            for OO0O000OOOO00O0O0 in TOOLS_get_list (OO00OOO00O0000O0O ["关键字查找列"]):#line:4134
                O0OO000OO0O0OO000 ["关键字查找列"]=O0OO000OO0O0OO000 ["关键字查找列"]+O0OO000OO0O0OO000 [OO0O000OOOO00O0O0 ].astype ("str")#line:4135
            O0OO000OO0O0OO000 =O0OO000OO0O0OO000 [(O0OO000OO0O0OO000 ["关键字查找列"].str .contains (OO00OOO00O0000O0O ["关键字组合"],na =False ))]#line:4136
            if str (OO00OOO00O0000O0O ["排除值"])!="nan":#line:4138
                O0OO000OO0O0OO000 =O0OO000OO0O0OO000 .loc [~O0OO000OO0O0OO000 ["关键字查找列"].str .contains (OO00OOO00O0000O0O ["排除值"],na =False )]#line:4139
            O0OO000OO0O0OO000 ["报表类型"]="ori_"+OO00OOO00O0000O0O ["报表类型"]#line:4141
            TABLE_tree_Level_2 (O0OO000OO0O0OO000 ,0 ,O0OO000OO0O0OO000 )#line:4142
            return 0 #line:4143
        if ("PSUR"in OO00OOO00O0000O0O ["报表类型"]):#line:4148
            O0OO000OO0O0OO000 =OO00O0OOOO0O00000 .copy ()#line:4149
            if ini ["模式"]=="器械":#line:4150
                O0OO000OO0O0OO000 ["关键字查找列"]=O0OO000OO0O0OO000 ["器械故障表现"].astype (str )+O0OO000OO0O0OO000 ["伤害表现"].astype (str )+O0OO000OO0O0OO000 ["使用过程"].astype (str )+O0OO000OO0O0OO000 ["事件原因分析描述"].astype (str )+O0OO000OO0O0OO000 ["初步处置情况"].astype (str )#line:4151
            else :#line:4152
                O0OO000OO0O0OO000 ["关键字查找列"]=O0OO000OO0O0OO000 ["器械故障表现"]#line:4153
            if "-其他关键字-"in str (OO00OOO00O0000O0O ["关键字标记"]):#line:4155
                O0OO000OO0O0OO000 =O0OO000OO0O0OO000 .loc [~O0OO000OO0O0OO000 ["关键字查找列"].str .contains (OO00OOO00O0000O0O ["关键字标记"],na =False )].copy ()#line:4156
                TABLE_tree_Level_2 (O0OO000OO0O0OO000 ,0 ,O0OO000OO0O0OO000 )#line:4157
                return 0 #line:4158
            O0OO000OO0O0OO000 =O0OO000OO0O0OO000 [(O0OO000OO0O0OO000 ["关键字查找列"].str .contains (OO00OOO00O0000O0O ["关键字标记"],na =False ))]#line:4161
            if str (OO00OOO00O0000O0O ["排除值"])!="没有排除值":#line:4162
                O0OO000OO0O0OO000 =O0OO000OO0O0OO000 .loc [~O0OO000OO0O0OO000 ["关键字查找列"].str .contains (OO00OOO00O0000O0O ["排除值"],na =False )]#line:4163
            TABLE_tree_Level_2 (O0OO000OO0O0OO000 ,0 ,O0OO000OO0O0OO000 )#line:4167
            return 0 #line:4168
        if ("ROR"in OO00OOO00O0000O0O ["报表类型"]):#line:4171
            O0OOO0OOO00O00OOO ={'nan':"-未定义-"}#line:4172
            O00OO0O0O0O0O0OOO =eval (OO00OOO00O0000O0O ["报表定位"],O0OOO0OOO00O00OOO )#line:4173
            O0OO000OO0O0OO000 =OO00O0OOOO0O00000 .copy ()#line:4174
            for OOOOO0000O0OOO000 ,O0O0OO0OO0OOO00O0 in O00OO0O0O0O0O0OOO .items ():#line:4176
                if OOOOO0000O0OOO000 =="合并列"and O0O0OO0OO0OOO00O0 !={}:#line:4178
                    for O00O00O00O0O000O0 ,O0OO0000OOO00OOOO in O0O0OO0OO0OOO00O0 .items ():#line:4179
                        if O0OO0000OOO00OOOO !="-未定义-":#line:4180
                            O000O0OOOO0O000OO =TOOLS_get_list (O0OO0000OOO00OOOO )#line:4181
                            O0OO000OO0O0OO000 [O00O00O00O0O000O0 ]=""#line:4182
                            for O00000O00O0O0OOO0 in O000O0OOOO0O000OO :#line:4183
                                O0OO000OO0O0OO000 [O00O00O00O0O000O0 ]=O0OO000OO0O0OO000 [O00O00O00O0O000O0 ]+O0OO000OO0O0OO000 [O00000O00O0O0OOO0 ].astype ("str")#line:4184
                if OOOOO0000O0OOO000 =="等于"and O0O0OO0OO0OOO00O0 !={}:#line:4186
                    for O00O00O00O0O000O0 ,O0OO0000OOO00OOOO in O0O0OO0OO0OOO00O0 .items ():#line:4187
                        O0OO000OO0O0OO000 =O0OO000OO0O0OO000 [(O0OO000OO0O0OO000 [O00O00O00O0O000O0 ]==O0OO0000OOO00OOOO )]#line:4188
                if OOOOO0000O0OOO000 =="不等于"and O0O0OO0OO0OOO00O0 !={}:#line:4190
                    for O00O00O00O0O000O0 ,O0OO0000OOO00OOOO in O0O0OO0OO0OOO00O0 .items ():#line:4191
                        if O0OO0000OOO00OOOO !="-未定义-":#line:4192
                            O0OO000OO0O0OO000 =O0OO000OO0O0OO000 [(O0OO000OO0O0OO000 [O00O00O00O0O000O0 ]!=O0OO0000OOO00OOOO )]#line:4193
                if OOOOO0000O0OOO000 =="包含"and O0O0OO0OO0OOO00O0 !={}:#line:4195
                    for O00O00O00O0O000O0 ,O0OO0000OOO00OOOO in O0O0OO0OO0OOO00O0 .items ():#line:4196
                        if O0OO0000OOO00OOOO !="-未定义-":#line:4197
                            O0OO000OO0O0OO000 =O0OO000OO0O0OO000 .loc [O0OO000OO0O0OO000 [O00O00O00O0O000O0 ].str .contains (O0OO0000OOO00OOOO ,na =False )]#line:4198
                if OOOOO0000O0OOO000 =="不包含"and O0O0OO0OO0OOO00O0 !={}:#line:4200
                    for O00O00O00O0O000O0 ,O0OO0000OOO00OOOO in O0O0OO0OO0OOO00O0 .items ():#line:4201
                        if O0OO0000OOO00OOOO !="-未定义-":#line:4202
                            O0OO000OO0O0OO000 =O0OO000OO0O0OO000 .loc [~O0OO000OO0O0OO000 [O00O00O00O0O000O0 ].str .contains (O0OO0000OOO00OOOO ,na =False )]#line:4203
            TABLE_tree_Level_2 (O0OO000OO0O0OO000 ,0 ,O0OO000OO0O0OO000 )#line:4205
            return 0 #line:4206
    if ("关键字标记"in OO0OOOOOO0O000O00 ["values"])and ("该类别不良事件计数"in OO0OOOOOO0O000O00 ["values"]):#line:4209
            def OOO00OO0O00O000OO (event =None ):#line:4210
                for O0O0O0OO0OOOO0O00 in OOOO00OO000O0OOO0 .selection ():#line:4211
                    O0O00OOO0O00O0000 =OOOO00OO000O0OOO0 .item (O0O0O0OO0OOOO0O00 ,"values")#line:4212
                OOOOOO0000OO0O0OO =dict (zip (OOOO00OO0O00O0OOO ,O0O00OOO0O00O0000 ))#line:4213
                OO00OO000000O0OO0 =OO0OOO000O00OOO0O .copy ()#line:4214
                if ini ["模式"]=="器械":#line:4215
                    OO00OO000000O0OO0 ["关键字查找列"]=OO00OO000000O0OO0 ["器械故障表现"].astype (str )+OO00OO000000O0OO0 ["伤害表现"].astype (str )+OO00OO000000O0OO0 ["使用过程"].astype (str )+OO00OO000000O0OO0 ["事件原因分析描述"].astype (str )+OO00OO000000O0OO0 ["初步处置情况"].astype (str )#line:4216
                else :#line:4217
                    OO00OO000000O0OO0 ["关键字查找列"]=OO00OO000000O0OO0 ["器械故障表现"]#line:4218
                if "-其他关键字-"in str (OOOOOO0000OO0O0OO ["关键字标记"]):#line:4219
                    OO00OO000000O0OO0 =OO00OO000000O0OO0 .loc [~OO00OO000000O0OO0 ["关键字查找列"].str .contains (OOOOOO0000OO0O0OO ["关键字标记"],na =False )].copy ()#line:4220
                OO00OO000000O0OO0 =OO00OO000000O0OO0 [(OO00OO000000O0OO0 ["关键字查找列"].str .contains (OOOOOO0000OO0O0OO ["关键字标记"],na =False ))]#line:4222
                if str (OOOOOO0000OO0O0OO ["排除值"])!="没有排除值":#line:4223
                    OO00OO000000O0OO0 =OO00OO000000O0OO0 .loc [~OO00OO000000O0OO0 ["关键字查找列"].str .contains (OOOOOO0000OO0O0OO ["排除值"],na =False )]#line:4224
                O0OO000OOOO0O0OOO =TOOLS_count_elements (OO00OO000000O0OO0 ,OOOOOO0000OO0O0OO ["关键字标记"],"关键字查找列")#line:4225
                O0OO000OOOO0O0OOO =O0OO000OOOO0O0OOO .sort_values (by ="计数",ascending =[False ],na_position ="last").reset_index (drop =True )#line:4226
                TABLE_tree_Level_2 (O0OO000OOOO0O0OOO ,1 ,OO00OO000000O0OO0 )#line:4227
            O0OOO0O00OO0000OO =Menu (OOOO0000000O00000 ,tearoff =False ,)#line:4228
            O0OOO0O00OO0000OO .add_command (label ="表现具体细项",command =OOO00OO0O00O000OO )#line:4229
            def OO000O000O0OOO00O (OO000O0O00000OOOO ):#line:4230
                O0OOO0O00OO0000OO .post (OO000O0O00000OOOO .x_root ,OO000O0O00000OOOO .y_root )#line:4231
            OOOO0000000O00000 .bind ("<Button-3>",OO000O000O0OOO00O )#line:4232
    try :#line:4236
        if O0OOOO00OOO000OOO [1 ]=="dfx_zhenghao":#line:4237
            OO00O0OO00O0OOOOO ="dfx_zhenghao"#line:4238
            OO000O00O0O000OO0 =""#line:4239
    except :#line:4240
            OO00O0OO00O0OOOOO =""#line:4241
            OO000O00O0O000OO0 ="近一年"#line:4242
    if (("总体评分"in OO0OOOOOO0O000O00 ["values"])and ("高峰批号均值"in OO0OOOOOO0O000O00 ["values"])and ("月份均值"in OO0OOOOOO0O000O00 ["values"]))or OO00O0OO00O0OOOOO =="dfx_zhenghao":#line:4244
            def OO00OOO000O0O00O0 (event =None ):#line:4247
                for OOOOO00O00O000OO0 in OOOO00OO000O0OOO0 .selection ():#line:4248
                    OO0000000O0O0O00O =OOOO00OO000O0OOO0 .item (OOOOO00O00O000OO0 ,"values")#line:4249
                OOOO0OO0OO00O000O =dict (zip (OOOO00OO0O00O0OOO ,OO0000000O0O0O00O ))#line:4250
                O000O00OOOOOOO000 =OO0OOO000O00OOO0O [(OO0OOO000O00OOO0O ["注册证编号/曾用注册证编号"]==OOOO0OO0OO00O000O ["注册证编号/曾用注册证编号"])].copy ()#line:4251
                O000O00OOOOOOO000 ["报表类型"]=OOOO0OO0OO00O000O ["报表类型"]+"1"#line:4252
                TABLE_tree_Level_2 (O000O00OOOOOOO000 ,1 ,OO0OOO000O00OOO0O )#line:4253
            def OO000OO00O00O0000 (event =None ):#line:4254
                for OOO0O0O00000O0OOO in OOOO00OO000O0OOO0 .selection ():#line:4255
                    OOO0O0O00OO0O0O00 =OOOO00OO000O0OOO0 .item (OOO0O0O00000O0OOO ,"values")#line:4256
                OO000OO00O00OO000 =dict (zip (OOOO00OO0O00O0OOO ,OOO0O0O00OO0O0O00 ))#line:4257
                OO0OOOOO0OOO0OO00 =O0OOOO00OOO000OOO [0 ][(O0OOOO00OOO000OOO [0 ]["注册证编号/曾用注册证编号"]==OO000OO00O00OO000 ["注册证编号/曾用注册证编号"])].copy ()#line:4258
                OO0OOOOO0OOO0OO00 ["报表类型"]=OO000OO00O00OO000 ["报表类型"]+"1"#line:4259
                TABLE_tree_Level_2 (OO0OOOOO0OOO0OO00 ,1 ,O0OOOO00OOO000OOO [0 ])#line:4260
            def O0O00O0OOO000OOO0 (OO00OO000OO0000OO ):#line:4261
                for OO00O0OOO0O0O0OO0 in OOOO00OO000O0OOO0 .selection ():#line:4262
                    OO0OO0OOOOOO0O00O =OOOO00OO000O0OOO0 .item (OO00O0OOO0O0O0OO0 ,"values")#line:4263
                O0OO0O0O0O000OO00 =dict (zip (OOOO00OO0O00O0OOO ,OO0OO0OOOOOO0O00O ))#line:4264
                O00O00O000OO00OOO =OO0OOO000O00OOO0O [(OO0OOO000O00OOO0O ["注册证编号/曾用注册证编号"]==O0OO0O0O0O000OO00 ["注册证编号/曾用注册证编号"])].copy ()#line:4267
                O00O00O000OO00OOO ["报表类型"]=O0OO0O0O0O000OO00 ["报表类型"]+"1"#line:4268
                OO000O00OO0OOO0O0 =Countall (O00O00O000OO00OOO ).df_psur (OO00OO000OO0000OO ,O0OO0O0O0O000OO00 ["规整后品类"])[["关键字标记","总数量","严重比"]]#line:4269
                OO000O00OO0OOO0O0 =OO000O00OO0OOO0O0 .rename (columns ={"总数量":"最近30天总数量"})#line:4270
                OO000O00OO0OOO0O0 =OO000O00OO0OOO0O0 .rename (columns ={"严重比":"最近30天严重比"})#line:4271
                O00O00O000OO00OOO =O0OOOO00OOO000OOO [0 ][(O0OOOO00OOO000OOO [0 ]["注册证编号/曾用注册证编号"]==O0OO0O0O0O000OO00 ["注册证编号/曾用注册证编号"])].copy ()#line:4273
                O00O00O000OO00OOO ["报表类型"]=O0OO0O0O0O000OO00 ["报表类型"]+"1"#line:4274
                O0O000O000O00O0OO =Countall (O00O00O000OO00OOO ).df_psur (OO00OO000OO0000OO ,O0OO0O0O0O000OO00 ["规整后品类"])#line:4275
                OOOO0000O0OOOOO00 =pd .merge (O0O000O000O00O0OO ,OO000O00OO0OOO0O0 ,on ="关键字标记",how ="left")#line:4277
                del OOOO0000O0OOOOO00 ["报表类型"]#line:4278
                OOOO0000O0OOOOO00 ["报表类型"]="PSUR"#line:4279
                TABLE_tree_Level_2 (OOOO0000O0OOOOO00 ,1 ,O00O00O000OO00OOO )#line:4281
            def O0OO0000O0OOOOO00 (O0OOOOO0OO0O0O00O ):#line:4284
                for OOO00OOO0O00O0000 in OOOO00OO000O0OOO0 .selection ():#line:4285
                    OOOO0000OO00OOOO0 =OOOO00OO000O0OOO0 .item (OOO00OOO0O00O0000 ,"values")#line:4286
                OOOOO0O0O000OOOOO =dict (zip (OOOO00OO0O00O0OOO ,OOOO0000OO00OOOO0 ))#line:4287
                OOO00000OO0OOOO00 =O0OOOO00OOO000OOO [0 ]#line:4288
                if OOOOO0O0O000OOOOO ["规整后品类"]=="N":#line:4289
                    if O0OOOOO0OO0O0O00O =="特定品种":#line:4290
                        showinfo (title ="关于",message ="未能适配该品种规则，可能未制定或者数据规整不完善。")#line:4291
                        return 0 #line:4292
                    OOO00000OO0OOOO00 =OOO00000OO0OOOO00 .loc [OOO00000OO0OOOO00 ["产品名称"].str .contains (OOOOO0O0O000OOOOO ["产品名称"],na =False )].copy ()#line:4293
                else :#line:4294
                    OOO00000OO0OOOO00 =OOO00000OO0OOOO00 .loc [OOO00000OO0OOOO00 ["规整后品类"].str .contains (OOOOO0O0O000OOOOO ["规整后品类"],na =False )].copy ()#line:4295
                OOO00000OO0OOOO00 =OOO00000OO0OOOO00 .loc [OOO00000OO0OOOO00 ["产品类别"].str .contains (OOOOO0O0O000OOOOO ["产品类别"],na =False )].copy ()#line:4296
                OOO00000OO0OOOO00 ["报表类型"]=OOOOO0O0O000OOOOO ["报表类型"]+"1"#line:4298
                if O0OOOOO0OO0O0O00O =="特定品种":#line:4299
                    TABLE_tree_Level_2 (Countall (OOO00000OO0OOOO00 ).df_ror (["产品类别","规整后品类","产品名称","注册证编号/曾用注册证编号"],OOOOO0O0O000OOOOO ["规整后品类"],OOOOO0O0O000OOOOO ["注册证编号/曾用注册证编号"]),1 ,OOO00000OO0OOOO00 )#line:4300
                else :#line:4301
                    TABLE_tree_Level_2 (Countall (OOO00000OO0OOOO00 ).df_ror (["产品类别","规整后品类","产品名称","注册证编号/曾用注册证编号"],O0OOOOO0OO0O0O00O ,OOOOO0O0O000OOOOO ["注册证编号/曾用注册证编号"]),1 ,OOO00000OO0OOOO00 )#line:4302
            def O0O0000OOOOO0OOO0 (event =None ):#line:4304
                for OO0O0OO00000000OO in OOOO00OO000O0OOO0 .selection ():#line:4305
                    O000O00O0O0O000OO =OOOO00OO000O0OOO0 .item (OO0O0OO00000000OO ,"values")#line:4306
                OO0O0O0O0000O0O0O =dict (zip (OOOO00OO0O00O0OOO ,O000O00O0O0O000OO ))#line:4307
                OO0O0O0OOO00O0O0O =O0OOOO00OOO000OOO [0 ][(O0OOOO00OOO000OOO [0 ]["注册证编号/曾用注册证编号"]==OO0O0O0O0000O0O0O ["注册证编号/曾用注册证编号"])].copy ()#line:4308
                OO0O0O0OOO00O0O0O ["报表类型"]=OO0O0O0O0000O0O0O ["报表类型"]+"1"#line:4309
                TABLE_tree_Level_2 (Countall (OO0O0O0OOO00O0O0O ).df_pihao (),1 ,OO0O0O0OOO00O0O0O ,)#line:4314
            def O0O00OOOOO0000OOO (event =None ):#line:4316
                for O000OOOO0O0OO0O0O in OOOO00OO000O0OOO0 .selection ():#line:4317
                    OOO0OOOOOOOO00OOO =OOOO00OO000O0OOO0 .item (O000OOOO0O0OO0O0O ,"values")#line:4318
                OO0O000O0OO00O00O =dict (zip (OOOO00OO0O00O0OOO ,OOO0OOOOOOOO00OOO ))#line:4319
                O0OO00OO00000OOOO =O0OOOO00OOO000OOO [0 ][(O0OOOO00OOO000OOO [0 ]["注册证编号/曾用注册证编号"]==OO0O000O0OO00O00O ["注册证编号/曾用注册证编号"])].copy ()#line:4320
                O0OO00OO00000OOOO ["报表类型"]=OO0O000O0OO00O00O ["报表类型"]+"1"#line:4321
                TABLE_tree_Level_2 (Countall (O0OO00OO00000OOOO ).df_xinghao (),1 ,O0OO00OO00000OOOO ,)#line:4326
            def OO00O0O0O0O00OO00 (event =None ):#line:4328
                for OOOOO000O0OOOO0OO in OOOO00OO000O0OOO0 .selection ():#line:4329
                    O0O00OO00O0O0OOO0 =OOOO00OO000O0OOO0 .item (OOOOO000O0OOOO0OO ,"values")#line:4330
                O00O00O00000000OO =dict (zip (OOOO00OO0O00O0OOO ,O0O00OO00O0O0OOO0 ))#line:4331
                OO00O0000OOOOOO00 =O0OOOO00OOO000OOO [0 ][(O0OOOO00OOO000OOO [0 ]["注册证编号/曾用注册证编号"]==O00O00O00000000OO ["注册证编号/曾用注册证编号"])].copy ()#line:4332
                OO00O0000OOOOOO00 ["报表类型"]=O00O00O00000000OO ["报表类型"]+"1"#line:4333
                TABLE_tree_Level_2 (Countall (OO00O0000OOOOOO00 ).df_user (),1 ,OO00O0000OOOOOO00 ,)#line:4338
            def O0OO0O0OOO000OO0O (event =None ):#line:4340
                for OOO0OOOOOO0OOOOO0 in OOOO00OO000O0OOO0 .selection ():#line:4342
                    O0O00OO0000O00O00 =OOOO00OO000O0OOO0 .item (OOO0OOOOOO0OOOOO0 ,"values")#line:4343
                OOO0O00O0O00000O0 =dict (zip (OOOO00OO0O00O0OOO ,O0O00OO0000O00O00 ))#line:4344
                O00O0O0O0O0O000OO =O0OOOO00OOO000OOO [0 ][(O0OOOO00OOO000OOO [0 ]["注册证编号/曾用注册证编号"]==OOO0O00O0O00000O0 ["注册证编号/曾用注册证编号"])].copy ()#line:4345
                O00O0O0O0O0O000OO ["报表类型"]=OOO0O00O0O00000O0 ["报表类型"]+"1"#line:4346
                O0O0OOOOOO000O00O =pd .read_excel (peizhidir +"0（范例）预警参数.xlsx",header =0 ,sheet_name =0 ).reset_index (drop =True )#line:4347
                if ini ["模式"]=="药品":#line:4348
                    O0O0OOOOOO000O00O =pd .read_excel (peizhidir +"0（范例）预警参数.xlsx",header =0 ,sheet_name ="药品").reset_index (drop =True )#line:4349
                if ini ["模式"]=="器械":#line:4350
                    O0O0OOOOOO000O00O =pd .read_excel (peizhidir +"0（范例）预警参数.xlsx",header =0 ,sheet_name ="器械").reset_index (drop =True )#line:4351
                if ini ["模式"]=="化妆品":#line:4352
                    O0O0OOOOOO000O00O =pd .read_excel (peizhidir +"0（范例）预警参数.xlsx",header =0 ,sheet_name ="化妆品").reset_index (drop =True )#line:4353
                OO00O00OOOO000000 =O0O0OOOOOO000O00O ["值"][3 ]+"|"+O0O0OOOOOO000O00O ["值"][4 ]#line:4354
                if ini ["模式"]=="器械":#line:4355
                    O00O0O0O0O0O000OO ["关键字查找列"]=O00O0O0O0O0O000OO ["器械故障表现"].astype (str )+O00O0O0O0O0O000OO ["伤害表现"].astype (str )+O00O0O0O0O0O000OO ["使用过程"].astype (str )+O00O0O0O0O0O000OO ["事件原因分析描述"].astype (str )+O00O0O0O0O0O000OO ["初步处置情况"].astype (str )#line:4356
                else :#line:4357
                    O00O0O0O0O0O000OO ["关键字查找列"]=O00O0O0O0O0O000OO ["器械故障表现"].astype (str )#line:4358
                O00O0O0O0O0O000OO =O00O0O0O0O0O000OO .loc [O00O0O0O0O0O000OO ["关键字查找列"].str .contains (OO00O00OOOO000000 ,na =False )].copy ().reset_index (drop =True )#line:4359
                TABLE_tree_Level_2 (O00O0O0O0O0O000OO ,0 ,O00O0O0O0O0O000OO ,)#line:4365
            def OO000OOO0OO0OOO00 (event =None ):#line:4368
                for O0O00OO00O0OOO0OO in OOOO00OO000O0OOO0 .selection ():#line:4369
                    OO0O0O00000OO0000 =OOOO00OO000O0OOO0 .item (O0O00OO00O0OOO0OO ,"values")#line:4370
                OOOO0O0OO000OO000 =dict (zip (OOOO00OO0O00O0OOO ,OO0O0O00000OO0000 ))#line:4371
                OOO0OOO0OOOOO0000 =O0OOOO00OOO000OOO [0 ][(O0OOOO00OOO000OOO [0 ]["注册证编号/曾用注册证编号"]==OOOO0O0OO000OO000 ["注册证编号/曾用注册证编号"])].copy ()#line:4372
                OOO0OOO0OOOOO0000 ["报表类型"]=OOOO0O0OO000OO000 ["报表类型"]+"1"#line:4373
                TOOLS_time (OOO0OOO0OOOOO0000 ,"事件发生日期",0 )#line:4374
            def OOOO0OO0O0O0000O0 (O00OOO0OO0O0O00OO ,OOOOOOOO0O0OOOO0O ):#line:4376
                for OO0OOOOOO00OO00OO in OOOO00OO000O0OOO0 .selection ():#line:4378
                    OO00OO0OO00O0O000 =OOOO00OO000O0OOO0 .item (OO0OOOOOO00OO00OO ,"values")#line:4379
                O00000OOOO0OO0000 =dict (zip (OOOO00OO0O00O0OOO ,OO00OO0OO00O0O000 ))#line:4380
                O0OO0O0O0OOO0OO0O =O0OOOO00OOO000OOO [0 ]#line:4381
                if O00000OOOO0OO0000 ["规整后品类"]=="N":#line:4382
                    if O00OOO0OO0O0O00OO =="特定品种":#line:4383
                        showinfo (title ="关于",message ="未能适配该品种规则，可能未制定或者数据规整不完善。")#line:4384
                        return 0 #line:4385
                O0OO0O0O0OOO0OO0O =O0OO0O0O0OOO0OO0O .loc [O0OO0O0O0OOO0OO0O ["注册证编号/曾用注册证编号"].str .contains (O00000OOOO0OO0000 ["注册证编号/曾用注册证编号"],na =False )].copy ()#line:4386
                O0OO0O0O0OOO0OO0O ["报表类型"]=O00000OOOO0OO0000 ["报表类型"]+"1"#line:4387
                if O00OOO0OO0O0O00OO =="特定品种":#line:4388
                    TABLE_tree_Level_2 (Countall (O0OO0O0O0OOO0OO0O ).df_find_all_keword_risk (OOOOOOOO0O0OOOO0O ,O00000OOOO0OO0000 ["规整后品类"]),1 ,O0OO0O0O0OOO0OO0O )#line:4389
                else :#line:4390
                    TABLE_tree_Level_2 (Countall (O0OO0O0O0OOO0OO0O ).df_find_all_keword_risk (OOOOOOOO0O0OOOO0O ,O00OOO0OO0O0O00OO ),1 ,O0OO0O0O0OOO0OO0O )#line:4391
            O0OOO0O00OO0000OO =Menu (OOOO0000000O00000 ,tearoff =False ,)#line:4395
            O0OOO0O00OO0000OO .add_command (label =OO000O00O0O000OO0 +"故障表现分类（无源）",command =lambda :O0O00O0OOO000OOO0 ("通用无源"))#line:4396
            O0OOO0O00OO0000OO .add_command (label =OO000O00O0O000OO0 +"故障表现分类（有源）",command =lambda :O0O00O0OOO000OOO0 ("通用有源"))#line:4397
            O0OOO0O00OO0000OO .add_command (label =OO000O00O0O000OO0 +"故障表现分类（特定品种）",command =lambda :O0O00O0OOO000OOO0 ("特定品种"))#line:4398
            O0OOO0O00OO0000OO .add_separator ()#line:4400
            if OO00O0OO00O0OOOOO =="":#line:4401
                O0OOO0O00OO0000OO .add_command (label =OO000O00O0O000OO0 +"同类比较(ROR-无源)",command =lambda :O0OO0000O0OOOOO00 ("无源"))#line:4402
                O0OOO0O00OO0000OO .add_command (label =OO000O00O0O000OO0 +"同类比较(ROR-有源)",command =lambda :O0OO0000O0OOOOO00 ("有源"))#line:4403
                O0OOO0O00OO0000OO .add_command (label =OO000O00O0O000OO0 +"同类比较(ROR-特定品种)",command =lambda :O0OO0000O0OOOOO00 ("特定品种"))#line:4404
            O0OOO0O00OO0000OO .add_separator ()#line:4406
            O0OOO0O00OO0000OO .add_command (label =OO000O00O0O000OO0 +"关键字趋势(批号-无源)",command =lambda :OOOO0OO0O0O0000O0 ("无源","产品批号"))#line:4407
            O0OOO0O00OO0000OO .add_command (label =OO000O00O0O000OO0 +"关键字趋势(批号-特定品种)",command =lambda :OOOO0OO0O0O0000O0 ("特定品种","产品批号"))#line:4408
            O0OOO0O00OO0000OO .add_command (label =OO000O00O0O000OO0 +"关键字趋势(月份-无源)",command =lambda :OOOO0OO0O0O0000O0 ("无源","事件发生月份"))#line:4409
            O0OOO0O00OO0000OO .add_command (label =OO000O00O0O000OO0 +"关键字趋势(月份-有源)",command =lambda :OOOO0OO0O0O0000O0 ("有源","事件发生月份"))#line:4410
            O0OOO0O00OO0000OO .add_command (label =OO000O00O0O000OO0 +"关键字趋势(月份-特定品种)",command =lambda :OOOO0OO0O0O0000O0 ("特定品种","事件发生月份"))#line:4411
            O0OOO0O00OO0000OO .add_command (label =OO000O00O0O000OO0 +"关键字趋势(季度-无源)",command =lambda :OOOO0OO0O0O0000O0 ("无源","事件发生季度"))#line:4412
            O0OOO0O00OO0000OO .add_command (label =OO000O00O0O000OO0 +"关键字趋势(季度-有源)",command =lambda :OOOO0OO0O0O0000O0 ("有源","事件发生季度"))#line:4413
            O0OOO0O00OO0000OO .add_command (label =OO000O00O0O000OO0 +"关键字趋势(季度-特定品种)",command =lambda :OOOO0OO0O0O0000O0 ("特定品种","事件发生季度"))#line:4414
            O0OOO0O00OO0000OO .add_separator ()#line:4416
            O0OOO0O00OO0000OO .add_command (label =OO000O00O0O000OO0 +"各批号报送情况",command =O0O0000OOOOO0OOO0 )#line:4417
            O0OOO0O00OO0000OO .add_command (label =OO000O00O0O000OO0 +"各型号报送情况",command =O0O00OOOOO0000OOO )#line:4418
            O0OOO0O00OO0000OO .add_command (label =OO000O00O0O000OO0 +"报告单位情况",command =OO00O0O0O0O00OO00 )#line:4419
            O0OOO0O00OO0000OO .add_command (label =OO000O00O0O000OO0 +"事件发生时间曲线",command =OO000OOO0OO0OOO00 )#line:4420
            O0OOO0O00OO0000OO .add_separator ()#line:4421
            O0OOO0O00OO0000OO .add_command (label =OO000O00O0O000OO0 +"原始数据",command =OO000OO00O00O0000 )#line:4422
            if OO00O0OO00O0OOOOO =="":#line:4423
                O0OOO0O00OO0000OO .add_command (label ="近30天原始数据",command =OO00OOO000O0O00O0 )#line:4424
            O0OOO0O00OO0000OO .add_command (label =OO000O00O0O000OO0 +"高度关注(一级和二级)",command =O0OO0O0OOO000OO0O )#line:4425
            def OO000O000O0OOO00O (O0OO0OO000O00O000 ):#line:4427
                O0OOO0O00OO0000OO .post (O0OO0OO000O00O000 .x_root ,O0OO0OO000O00O000 .y_root )#line:4428
            OOOO0000000O00000 .bind ("<Button-3>",OO000O000O0OOO00O )#line:4429
    if O0OO0OO0000O00000 ==0 or "规整编码"in O0O0O0OO0OO0OOOOO .columns :#line:4432
        OOOO00OO000O0OOO0 .bind ("<Double-1>",lambda OOO0O00O00O0OO000 :OOO0OO0000OO0OOO0 (OOO0O00O00O0OO000 ,O0O0O0OO0OO0OOOOO ))#line:4433
    if O0OO0OO0000O00000 ==1 and "规整编码"not in O0O0O0OO0OO0OOOOO .columns :#line:4434
        OOOO00OO000O0OOO0 .bind ("<Double-1>",lambda OO00OO0OOO00OO0O0 :O0OOO0O0O0OOO00O0 (OO00OO0OOO00OO0O0 ,OOOO00OO0O00O0OOO ,OO0OOO000O00OOO0O ))#line:4435
    def O0OOO000OOO00O00O (O0OOOO0O0OO0O0000 ,O000OOO0OO00OO000 ,OO00O0OO0OOOOO0OO ):#line:4438
        OO00OOOO0OOOOO000 =[(O0OOOO0O0OO0O0000 .set (OOO00OOO00O000O0O ,O000OOO0OO00OO000 ),OOO00OOO00O000O0O )for OOO00OOO00O000O0O in O0OOOO0O0OO0O0000 .get_children ("")]#line:4439
        OO00OOOO0OOOOO000 .sort (reverse =OO00O0OO0OOOOO0OO )#line:4440
        for O0OO0O000OO00O0OO ,(O00OO0O000000OOOO ,O0OO0OO00O0O00O0O )in enumerate (OO00OOOO0OOOOO000 ):#line:4442
            O0OOOO0O0OO0O0000 .move (O0OO0OO00O0O00O0O ,"",O0OO0O000OO00O0OO )#line:4443
        O0OOOO0O0OO0O0000 .heading (O000OOO0OO00OO000 ,command =lambda :O0OOO000OOO00O00O (O0OOOO0O0OO0O0000 ,O000OOO0OO00OO000 ,not OO00O0OO0OOOOO0OO ))#line:4446
    for O000O0000OO0OO0O0 in OOOO00OO0O00O0OOO :#line:4448
        OOOO00OO000O0OOO0 .heading (O000O0000OO0OO0O0 ,text =O000O0000OO0OO0O0 ,command =lambda _col =O000O0000OO0OO0O0 :O0OOO000OOO00O00O (OOOO00OO000O0OOO0 ,_col ,False ),)#line:4453
    def OOO0OO0000OO0OOO0 (O0OOOOO0000OO00O0 ,O00O0O00OOO0000O0 ):#line:4457
        if "规整编码"in O00O0O00OOO0000O0 .columns :#line:4459
            O00O0O00OOO0000O0 =O00O0O00OOO0000O0 .rename (columns ={"规整编码":"报告编码"})#line:4460
        for O0OOO00OO00O0O00O in OOOO00OO000O0OOO0 .selection ():#line:4462
            OOO0OO0O000000OO0 =OOOO00OO000O0OOO0 .item (O0OOO00OO00O0O00O ,"values")#line:4463
            OOOOOOO00OO00O0OO =Toplevel ()#line:4466
            O0O0O0OO00OOO0OO0 =OOOOOOO00OO00O0OO .winfo_screenwidth ()#line:4468
            OOO0OOOO0OO0O00OO =OOOOOOO00OO00O0OO .winfo_screenheight ()#line:4470
            OO0OOOO0OO0O000OO =800 #line:4472
            O00O00OO0O00OOOOO =600 #line:4473
            O0OO0O00000O0OO00 =(O0O0O0OO00OOO0OO0 -OO0OOOO0OO0O000OO )/2 #line:4475
            O00O0OO000O000O00 =(OOO0OOOO0OO0O00OO -O00O00OO0O00OOOOO )/2 #line:4476
            OOOOOOO00OO00O0OO .geometry ("%dx%d+%d+%d"%(OO0OOOO0OO0O000OO ,O00O00OO0O00OOOOO ,O0OO0O00000O0OO00 ,O00O0OO000O000O00 ))#line:4477
            OO0OO00O00O00OO00 =ScrolledText (OOOOOOO00OO00O0OO ,height =1100 ,width =1100 ,bg ="#FFFFFF")#line:4481
            OO0OO00O00O00OO00 .pack (padx =10 ,pady =10 )#line:4482
            def OOO00O00O0OO000O0 (event =None ):#line:4483
                OO0OO00O00O00OO00 .event_generate ('<<Copy>>')#line:4484
            def O000OO0O0000O0000 (O00O0OOO0OO000OO0 ,O000O00O0O0000000 ):#line:4485
                TOOLS_savetxt (O00O0OOO0OO000OO0 ,O000O00O0O0000000 ,1 )#line:4486
            OO0O00OO0OOOOO0OO =Menu (OO0OO00O00O00OO00 ,tearoff =False ,)#line:4487
            OO0O00OO0OOOOO0OO .add_command (label ="复制",command =OOO00O00O0OO000O0 )#line:4488
            OO0O00OO0OOOOO0OO .add_command (label ="导出",command =lambda :PROGRAM_thread_it (O000OO0O0000O0000 ,OO0OO00O00O00OO00 .get (1.0 ,'end'),filedialog .asksaveasfilename (title =u"保存文件",initialfile =O00O0O00OOO0000O0 .iloc [0 ,0 ],defaultextension ="txt",filetypes =[("txt","*.txt")])))#line:4489
            def OOO0000OOO000OO00 (OOO0OOOOOO000O0OO ):#line:4491
                OO0O00OO0OOOOO0OO .post (OOO0OOOOOO000O0OO .x_root ,OOO0OOOOOO000O0OO .y_root )#line:4492
            OO0OO00O00O00OO00 .bind ("<Button-3>",OOO0000OOO000OO00 )#line:4493
            try :#line:4495
                OOOOOOO00OO00O0OO .title (str (OOO0OO0O000000OO0 [0 ]))#line:4496
                O00O0O00OOO0000O0 ["报告编码"]=O00O0O00OOO0000O0 ["报告编码"].astype ("str")#line:4497
                O00O00OOO0000OOOO =O00O0O00OOO0000O0 [(O00O0O00OOO0000O0 ["报告编码"]==str (OOO0OO0O000000OO0 [0 ]))]#line:4498
            except :#line:4499
                pass #line:4500
            OO0O00O00O00OO0O0 =O00O0O00OOO0000O0 .columns .values .tolist ()#line:4502
            for O00O00O0O0O0OOO00 in range (len (OO0O00O00O00OO0O0 )):#line:4503
                try :#line:4505
                    if OO0O00O00O00OO0O0 [O00O00O0O0O0OOO00 ]=="报告编码.1":#line:4506
                        OO0OO00O00O00OO00 .insert (END ,"\n\n")#line:4507
                    if OO0O00O00O00OO0O0 [O00O00O0O0O0OOO00 ]=="产品名称":#line:4508
                        OO0OO00O00O00OO00 .insert (END ,"\n\n")#line:4509
                    if OO0O00O00O00OO0O0 [O00O00O0O0O0OOO00 ]=="事件发生日期":#line:4510
                        OO0OO00O00O00OO00 .insert (END ,"\n\n")#line:4511
                    if OO0O00O00O00OO0O0 [O00O00O0O0O0OOO00 ]=="是否开展了调查":#line:4512
                        OO0OO00O00O00OO00 .insert (END ,"\n\n")#line:4513
                    if OO0O00O00O00OO0O0 [O00O00O0O0O0OOO00 ]=="市级监测机构":#line:4514
                        OO0OO00O00O00OO00 .insert (END ,"\n\n")#line:4515
                    if OO0O00O00O00OO0O0 [O00O00O0O0O0OOO00 ]=="上报机构描述":#line:4516
                        OO0OO00O00O00OO00 .insert (END ,"\n\n")#line:4517
                    if OO0O00O00O00OO0O0 [O00O00O0O0O0OOO00 ]=="持有人处理描述":#line:4518
                        OO0OO00O00O00OO00 .insert (END ,"\n\n")#line:4519
                    if O00O00O0O0O0OOO00 >1 and OO0O00O00O00OO0O0 [O00O00O0O0O0OOO00 -1 ]=="持有人处理描述":#line:4520
                        OO0OO00O00O00OO00 .insert (END ,"\n\n")#line:4521
                except :#line:4523
                    pass #line:4524
                try :#line:4525
                    if OO0O00O00O00OO0O0 [O00O00O0O0O0OOO00 ]in ["单位名称","产品名称ori","上报机构描述","持有人处理描述","产品名称","注册证编号/曾用注册证编号","型号","规格","产品批号","上市许可持有人名称ori","上市许可持有人名称","伤害","伤害表现","器械故障表现","使用过程","事件原因分析描述","初步处置情况","调查情况","关联性评价","事件原因分析.1","具体控制措施"]:#line:4526
                        OO0OO00O00O00OO00 .insert (END ,"●")#line:4527
                except :#line:4528
                    pass #line:4529
                OO0OO00O00O00OO00 .insert (END ,OO0O00O00O00OO0O0 [O00O00O0O0O0OOO00 ])#line:4530
                OO0OO00O00O00OO00 .insert (END ,"：")#line:4531
                try :#line:4532
                    OO0OO00O00O00OO00 .insert (END ,O00O00OOO0000OOOO .iloc [0 ,O00O00O0O0O0OOO00 ])#line:4533
                except :#line:4534
                    OO0OO00O00O00OO00 .insert (END ,OOO0OO0O000000OO0 [O00O00O0O0O0OOO00 ])#line:4535
                OO0OO00O00O00OO00 .insert (END ,"\n")#line:4536
            OO0OO00O00O00OO00 .config (state =DISABLED )#line:4537
    OOOO00OO000O0OOO0 .pack ()#line:4539
def TOOLS_get_guize2 (OO0OOO0000000000O ):#line:4542
	""#line:4543
	O0000O0OOO0000O00 =peizhidir +"0（范例）比例失衡关键字库.xls"#line:4544
	O0OOO00OOO0O00O00 =pd .read_excel (O0000O0OOO0000O00 ,header =0 ,sheet_name ="器械")#line:4545
	OOO0O000OO0000OO0 =O0OOO00OOO0O00O00 [["适用范围列","适用范围"]].drop_duplicates ("适用范围")#line:4546
	text .insert (END ,OOO0O000OO0000OO0 )#line:4547
	text .see (END )#line:4548
	OO0OOO0O0O0000000 =Toplevel ()#line:4549
	OO0OOO0O0O0000000 .title ('切换通用规则')#line:4550
	O0OOOO0O0O0OO0OOO =OO0OOO0O0O0000000 .winfo_screenwidth ()#line:4551
	OO0OOOO0O0OOOOOOO =OO0OOO0O0O0000000 .winfo_screenheight ()#line:4553
	OOOOO0OOOO000OOO0 =450 #line:4555
	OOOOO00O0O000OOO0 =100 #line:4556
	O0O000OOO0O000O00 =(O0OOOO0O0O0OO0OOO -OOOOO0OOOO000OOO0 )/2 #line:4558
	O0OO00OO00OOO0OO0 =(OO0OOOO0O0OOOOOOO -OOOOO00O0O000OOO0 )/2 #line:4559
	OO0OOO0O0O0000000 .geometry ("%dx%d+%d+%d"%(OOOOO0OOOO000OOO0 ,OOOOO00O0O000OOO0 ,O0O000OOO0O000O00 ,O0OO00OO00OOO0OO0 ))#line:4560
	O00OOO00O0O0O00O0 =Label (OO0OOO0O0O0000000 ,text ="查找位置：器械故障表现+伤害表现+使用过程+事件原因分析描述+初步处置情况")#line:4561
	O00OOO00O0O0O00O0 .pack ()#line:4562
	O00O000OO000OOOO0 =Label (OO0OOO0O0O0000000 ,text ="请选择您所需要的通用规则关键字：")#line:4563
	O00O000OO000OOOO0 .pack ()#line:4564
	def O0OOO0O0000O0OO0O (*O000O0O0000OO0O00 ):#line:4565
		OO0O0O0OO0000O0O0 .set (OOO00OOO00O00O00O .get ())#line:4566
	OO0O0O0OO0000O0O0 =StringVar ()#line:4567
	OOO00OOO00O00O00O =ttk .Combobox (OO0OOO0O0O0000000 ,width =14 ,height =30 ,state ="readonly",textvariable =OO0O0O0OO0000O0O0 )#line:4568
	OOO00OOO00O00O00O ["values"]=OOO0O000OO0000OO0 ["适用范围"].to_list ()#line:4569
	OOO00OOO00O00O00O .current (0 )#line:4570
	OOO00OOO00O00O00O .bind ("<<ComboboxSelected>>",O0OOO0O0000O0OO0O )#line:4571
	OOO00OOO00O00O00O .pack ()#line:4572
	OO0OOO0OO0OOO0O00 =LabelFrame (OO0OOO0O0O0000000 )#line:4575
	OO0OOO00OO00O00OO =Button (OO0OOO0OO0OOO0O00 ,text ="确定",width =10 ,command =lambda :O000O00000O00OOOO (O0OOO00OOO0O00O00 ,OO0O0O0OO0000O0O0 .get ()))#line:4576
	OO0OOO00OO00O00OO .pack (side =LEFT ,padx =1 ,pady =1 )#line:4577
	OO0OOO0OO0OOO0O00 .pack ()#line:4578
	def O000O00000O00OOOO (O0O00O0OOOO0O00O0 ,OO000O0OO0O0O0OOO ):#line:4580
		O00O0OOOOOOO00O00 =O0O00O0OOOO0O00O0 .loc [O0O00O0OOOO0O00O0 ["适用范围"].str .contains (OO000O0OO0O0O0OOO ,na =False )].copy ().reset_index (drop =True )#line:4581
		TABLE_tree_Level_2 (Countall (OO0OOO0000000000O ).df_psur ("特定品种作为通用关键字",O00O0OOOOOOO00O00 ),1 ,OO0OOO0000000000O )#line:4582
def TOOLS_findin (OO0OOOOO00OO0O0OO ,O000000OO0OO0OO0O ):#line:4583
	""#line:4584
	OOO00OO0000O000O0 =Toplevel ()#line:4585
	OOO00OO0000O000O0 .title ('高级查找')#line:4586
	OOOO0O0OO000OOOOO =OOO00OO0000O000O0 .winfo_screenwidth ()#line:4587
	OOO000O00OO000OO0 =OOO00OO0000O000O0 .winfo_screenheight ()#line:4589
	O0OO0O0O0O0O00O0O =400 #line:4591
	OOOO000O00OOOOOOO =120 #line:4592
	OOO0O0OOO000O0OOO =(OOOO0O0OO000OOOOO -O0OO0O0O0O0O00O0O )/2 #line:4594
	OOOOOOOO00OOO00O0 =(OOO000O00OO000OO0 -OOOO000O00OOOOOOO )/2 #line:4595
	OOO00OO0000O000O0 .geometry ("%dx%d+%d+%d"%(O0OO0O0O0O0O00O0O ,OOOO000O00OOOOOOO ,OOO0O0OOO000O0OOO ,OOOOOOOO00OOO00O0 ))#line:4596
	OO0OOO000OOO0OO00 =Label (OOO00OO0000O000O0 ,text ="需要查找的关键字（用|隔开）：")#line:4597
	OO0OOO000OOO0OO00 .pack ()#line:4598
	OO00000OO00OOO000 =Label (OOO00OO0000O000O0 ,text ="在哪些列查找（用|隔开）：")#line:4599
	OO0O00O000OOOO00O =Entry (OOO00OO0000O000O0 ,width =80 )#line:4601
	OO0O00O000OOOO00O .insert (0 ,"破裂|断裂")#line:4602
	O0O0OOO0000O00000 =Entry (OOO00OO0000O000O0 ,width =80 )#line:4603
	O0O0OOO0000O00000 .insert (0 ,"器械故障表现|伤害表现")#line:4604
	OO0O00O000OOOO00O .pack ()#line:4605
	OO00000OO00OOO000 .pack ()#line:4606
	O0O0OOO0000O00000 .pack ()#line:4607
	OOOO0OO0OOOO00OOO =LabelFrame (OOO00OO0000O000O0 )#line:4608
	OO0OOOO00O0O0OOO0 =Button (OOOO0OO0OOOO00OOO ,text ="确定",width =10 ,command =lambda :PROGRAM_thread_it (TABLE_tree_Level_2 ,OOO00OO00OOOOOOO0 (OO0O00O000OOOO00O .get (),O0O0OOO0000O00000 .get (),OO0OOOOO00OO0O0OO ),1 ,O000000OO0OO0OO0O ))#line:4609
	OO0OOOO00O0O0OOO0 .pack (side =LEFT ,padx =1 ,pady =1 )#line:4610
	OOOO0OO0OOOO00OOO .pack ()#line:4611
	def OOO00OO00OOOOOOO0 (O0O000OO0000OO000 ,O0OO00OOOO000O0OO ,OOO0000OOO00O00O0 ):#line:4614
		OOO0000OOO00O00O0 ["关键字查找列10"]="######"#line:4615
		for O0O00000O00000O0O in TOOLS_get_list (O0OO00OOOO000O0OO ):#line:4616
			OOO0000OOO00O00O0 ["关键字查找列10"]=OOO0000OOO00O00O0 ["关键字查找列10"].astype (str )+OOO0000OOO00O00O0 [O0O00000O00000O0O ].astype (str )#line:4617
		OOO0000OOO00O00O0 =OOO0000OOO00O00O0 .loc [OOO0000OOO00O00O0 ["关键字查找列10"].str .contains (O0O000OO0000OO000 ,na =False )]#line:4618
		del OOO0000OOO00O00O0 ["关键字查找列10"]#line:4619
		return OOO0000OOO00O00O0 #line:4620
def PROGRAM_about ():#line:4622
    ""#line:4623
    O00O0OO000OOO0OO0 =" 佛山市食品药品检验检测中心 \n(佛山市药品不良反应监测中心)\n蔡权周（QQ或微信411703730）\n仅供政府设立的不良反应监测机构使用。"#line:4624
    showinfo (title ="关于",message =O00O0OO000OOO0OO0 )#line:4625
def PROGRAM_thread_it (O0OO0OOO00OOO0O0O ,*OO00O0OOOOO0O0O0O ):#line:4628
    ""#line:4629
    OOO00OOOOO0O000OO =threading .Thread (target =O0OO0OOO00OOO0O0O ,args =OO00O0OOOOO0O0O0O )#line:4631
    OOO00OOOOO0O000OO .setDaemon (True )#line:4633
    OOO00OOOOO0O000OO .start ()#line:4635
def PROGRAM_Menubar (O000OO0O0O00OOOOO ,OO0O0000OO0O0000O ,OOOOOO00OOO0OOO00 ,O0OOOOOOO0O0OOOOO ):#line:4636
	""#line:4637
	OO0O0000000000O00 =Menu (O000OO0O0O00OOOOO )#line:4639
	O000OO0O0O00OOOOO .config (menu =OO0O0000000000O00 )#line:4641
	O00OOOO0O0O00O0OO =Menu (OO0O0000000000O00 ,tearoff =0 )#line:4643
	OO0O0000000000O00 .add_cascade (label ="实用工具",menu =O00OOOO0O0O00O0OO )#line:4644
	O00OOOO0O0O00O0OO .add_command (label ="统计工具箱",command =lambda :TABLE_tree_Level_2 (OO0O0000OO0O0000O ,1 ,O0OOOOOOO0O0OOOOO ,"tools_x"))#line:4646
	O00OOOO0O0O00O0OO .add_command (label ="数据规整（自定义）",command =lambda :TOOL_guizheng (OO0O0000OO0O0000O ,0 ,False ))#line:4648
	O00OOOO0O0O00O0OO .add_command (label ="批量筛选（自定义）",command =lambda :TOOLS_xuanze (OO0O0000OO0O0000O ,0 ))#line:4650
	O00OOOO0O0O00O0OO .add_separator ()#line:4651
	O00OOOO0O0O00O0OO .add_command (label ="原始导入",command =TOOLS_fileopen )#line:4653
	if ini ["模式"]=="其他":#line:4658
		return 0 #line:4659
	if ini ["模式"]=="药品"or ini ["模式"]=="器械":#line:4661
		OOOOO00OO00OOO0O0 =Menu (OO0O0000000000O00 ,tearoff =0 )#line:4662
		OO0O0000000000O00 .add_cascade (label ="信号检测",menu =OOOOO00OO00OOO0O0 )#line:4663
		OOOOO00OO00OOO0O0 .add_command (label ="预警（单日）",command =lambda :TOOLS_keti (OO0O0000OO0O0000O ))#line:4665
		OOOOO00OO00OOO0O0 .add_separator ()#line:4666
		OOOOO00OO00OOO0O0 .add_command (label ="数量比例失衡监测-证号内批号",command =lambda :TABLE_tree_Level_2 (Countall (OO0O0000OO0O0000O ).df_findrisk ("产品批号"),1 ,O0OOOOOOO0O0OOOOO ))#line:4668
		OOOOO00OO00OOO0O0 .add_command (label ="数量比例失衡监测-证号内季度",command =lambda :TABLE_tree_Level_2 (Countall (OO0O0000OO0O0000O ).df_findrisk ("事件发生季度"),1 ,O0OOOOOOO0O0OOOOO ))#line:4670
		OOOOO00OO00OOO0O0 .add_command (label ="数量比例失衡监测-证号内月份",command =lambda :TABLE_tree_Level_2 (Countall (OO0O0000OO0O0000O ).df_findrisk ("事件发生月份"),1 ,O0OOOOOOO0O0OOOOO ))#line:4672
		OOOOO00OO00OOO0O0 .add_command (label ="数量比例失衡监测-证号内性别",command =lambda :TABLE_tree_Level_2 (Countall (OO0O0000OO0O0000O ).df_findrisk ("性别"),1 ,O0OOOOOOO0O0OOOOO ))#line:4674
		OOOOO00OO00OOO0O0 .add_command (label ="数量比例失衡监测-证号内年龄段",command =lambda :TABLE_tree_Level_2 (Countall (OO0O0000OO0O0000O ).df_findrisk ("年龄段"),1 ,O0OOOOOOO0O0OOOOO ))#line:4676
		OOOOO00OO00OOO0O0 .add_separator ()#line:4678
		OOOOO00OO00OOO0O0 .add_command (label ="关键字检测（同证号内不同批号比对）",command =lambda :TABLE_tree_Level_2 (Countall (OO0O0000OO0O0000O ).df_find_all_keword_risk ("产品批号"),1 ,O0OOOOOOO0O0OOOOO ))#line:4680
		OOOOO00OO00OOO0O0 .add_command (label ="关键字检测（同证号内不同月份比对）",command =lambda :TABLE_tree_Level_2 (Countall (OO0O0000OO0O0000O ).df_find_all_keword_risk ("事件发生月份"),1 ,O0OOOOOOO0O0OOOOO ))#line:4682
		OOOOO00OO00OOO0O0 .add_command (label ="关键字检测（同证号内不同季度比对）",command =lambda :TABLE_tree_Level_2 (Countall (OO0O0000OO0O0000O ).df_find_all_keword_risk ("事件发生季度"),1 ,O0OOOOOOO0O0OOOOO ))#line:4684
		OOOOO00OO00OOO0O0 .add_command (label ="关键字检测（同证号内不同性别比对）",command =lambda :TABLE_tree_Level_2 (Countall (OO0O0000OO0O0000O ).df_find_all_keword_risk ("性别"),1 ,O0OOOOOOO0O0OOOOO ))#line:4686
		OOOOO00OO00OOO0O0 .add_command (label ="关键字检测（同证号内不同年龄段比对）",command =lambda :TABLE_tree_Level_2 (Countall (OO0O0000OO0O0000O ).df_find_all_keword_risk ("年龄段"),1 ,O0OOOOOOO0O0OOOOO ))#line:4688
		OOOOO00OO00OOO0O0 .add_separator ()#line:4690
		OOOOO00OO00OOO0O0 .add_command (label ="关键字ROR-页面内同证号的批号间比对",command =lambda :TABLE_tree_Level_2 (Countall (OO0O0000OO0O0000O ).df_ror (["上市许可持有人名称","产品类别","规整后品类","产品名称","注册证编号/曾用注册证编号","产品批号"]),1 ,O0OOOOOOO0O0OOOOO ))#line:4692
		OOOOO00OO00OOO0O0 .add_command (label ="关键字ROR-页面内同证号的月份间比对",command =lambda :TABLE_tree_Level_2 (Countall (OO0O0000OO0O0000O ).df_ror (["上市许可持有人名称","产品类别","规整后品类","产品名称","注册证编号/曾用注册证编号","事件发生月份"]),1 ,O0OOOOOOO0O0OOOOO ))#line:4694
		OOOOO00OO00OOO0O0 .add_command (label ="关键字ROR-页面内同证号的季度间比对",command =lambda :TABLE_tree_Level_2 (Countall (OO0O0000OO0O0000O ).df_ror (["上市许可持有人名称","产品类别","规整后品类","产品名称","注册证编号/曾用注册证编号","事件发生季度"]),1 ,O0OOOOOOO0O0OOOOO ))#line:4696
		OOOOO00OO00OOO0O0 .add_command (label ="关键字ROR-页面内同证号的年龄段间比对",command =lambda :TABLE_tree_Level_2 (Countall (OO0O0000OO0O0000O ).df_ror (["上市许可持有人名称","产品类别","规整后品类","产品名称","注册证编号/曾用注册证编号","年龄段"]),1 ,O0OOOOOOO0O0OOOOO ))#line:4698
		OOOOO00OO00OOO0O0 .add_command (label ="关键字ROR-页面内同证号的性别间比对",command =lambda :TABLE_tree_Level_2 (Countall (OO0O0000OO0O0000O ).df_ror (["上市许可持有人名称","产品类别","规整后品类","产品名称","注册证编号/曾用注册证编号","性别"]),1 ,O0OOOOOOO0O0OOOOO ))#line:4700
		OOOOO00OO00OOO0O0 .add_separator ()#line:4702
		OOOOO00OO00OOO0O0 .add_command (label ="关键字ROR-页面内同品名的证号间比对",command =lambda :TABLE_tree_Level_2 (Countall (OO0O0000OO0O0000O ).df_ror (["产品类别","规整后品类","产品名称","注册证编号/曾用注册证编号"]),1 ,O0OOOOOOO0O0OOOOO ))#line:4704
		OOOOO00OO00OOO0O0 .add_command (label ="关键字ROR-页面内同品名的年龄段间比对",command =lambda :TABLE_tree_Level_2 (Countall (OO0O0000OO0O0000O ).df_ror (["产品类别","规整后品类","产品名称","年龄段"]),1 ,O0OOOOOOO0O0OOOOO ))#line:4706
		OOOOO00OO00OOO0O0 .add_command (label ="关键字ROR-页面内同品名的性别间比对",command =lambda :TABLE_tree_Level_2 (Countall (OO0O0000OO0O0000O ).df_ror (["产品类别","规整后品类","产品名称","性别"]),1 ,O0OOOOOOO0O0OOOOO ))#line:4708
		OOOOO00OO00OOO0O0 .add_separator ()#line:4710
		OOOOO00OO00OOO0O0 .add_command (label ="关键字ROR-页面内同类别的名称间比对",command =lambda :TABLE_tree_Level_2 (Countall (OO0O0000OO0O0000O ).df_ror (["产品类别","产品名称"]),1 ,O0OOOOOOO0O0OOOOO ))#line:4712
		OOOOO00OO00OOO0O0 .add_command (label ="关键字ROR-页面内同类别的年龄段间比对",command =lambda :TABLE_tree_Level_2 (Countall (OO0O0000OO0O0000O ).df_ror (["产品类别","年龄段"]),1 ,O0OOOOOOO0O0OOOOO ))#line:4714
		OOOOO00OO00OOO0O0 .add_command (label ="关键字ROR-页面内同类别的性别间比对",command =lambda :TABLE_tree_Level_2 (Countall (OO0O0000OO0O0000O ).df_ror (["产品类别","性别"]),1 ,O0OOOOOOO0O0OOOOO ))#line:4716
	OO0O0OOO0O0O00O0O =Menu (OO0O0000000000O00 ,tearoff =0 )#line:4720
	OO0O0000000000O00 .add_cascade (label ="简报制作",menu =OO0O0OOO0O0O00O0O )#line:4721
	OO0O0OOO0O0O00O0O .add_command (label ="药品简报",command =lambda :TOOLS_autocount (OO0O0000OO0O0000O ,"药品"))#line:4724
	OO0O0OOO0O0O00O0O .add_command (label ="器械简报",command =lambda :TOOLS_autocount (OO0O0000OO0O0000O ,"器械"))#line:4726
	OO0O0OOO0O0O00O0O .add_command (label ="化妆品简报",command =lambda :TOOLS_autocount (OO0O0000OO0O0000O ,"化妆品"))#line:4728
	OO0OO00O0O0O0O00O =Menu (OO0O0000000000O00 ,tearoff =0 )#line:4732
	OO0O0000000000O00 .add_cascade (label ="品种评价",menu =OO0OO00O0O0O0O00O )#line:4733
	OO0OO00O0O0O0O00O .add_command (label ="报告年份",command =lambda :STAT_pinzhong (OO0O0000OO0O0000O ,"报告年份",-1 ))#line:4735
	OO0OO00O0O0O0O00O .add_command (label ="发生年份",command =lambda :STAT_pinzhong (OO0O0000OO0O0000O ,"事件发生年份",-1 ))#line:4737
	OO0OO00O0O0O0O00O .add_separator ()#line:4738
	OO0OO00O0O0O0O00O .add_command (label ="涉及企业",command =lambda :STAT_pinzhong (OO0O0000OO0O0000O ,"上市许可持有人名称",1 ))#line:4741
	OO0OO00O0O0O0O00O .add_command (label ="产品名称",command =lambda :STAT_pinzhong (OO0O0000OO0O0000O ,"产品名称",1 ))#line:4743
	OO0OO00O0O0O0O00O .add_command (label ="注册证号",command =lambda :TABLE_tree_Level_2 (Countall (OO0O0000OO0O0000O ).df_zhenghao (),1 ,O0OOOOOOO0O0OOOOO ))#line:4745
	OO0OO00O0O0O0O00O .add_separator ()#line:4746
	OO0OO00O0O0O0O00O .add_command (label ="年龄段分布",command =lambda :STAT_pinzhong (OO0O0000OO0O0000O ,"年龄段",1 ))#line:4748
	OO0OO00O0O0O0O00O .add_command (label ="性别分布",command =lambda :STAT_pinzhong (OO0O0000OO0O0000O ,"性别",1 ))#line:4750
	OO0OO00O0O0O0O00O .add_command (label ="年龄性别分布",command =lambda :TABLE_tree_Level_2 (Countall (OO0O0000OO0O0000O ).df_age (),1 ,O0OOOOOOO0O0OOOOO ,))#line:4752
	OO0OO00O0O0O0O00O .add_separator ()#line:4753
	OO0OO00O0O0O0O00O .add_command (label ="事件发生时间",command =lambda :STAT_pinzhong (OO0O0000OO0O0000O ,"时隔",1 ))#line:4755
	if ini ["模式"]=="器械":#line:4756
		OO0OO00O0O0O0O00O .add_command (label ="事件分布（故障表现）",command =lambda :STAT_pinzhong (OO0O0000OO0O0000O ,"器械故障表现",0 ))#line:4758
		OO0OO00O0O0O0O00O .add_command (label ="事件分布（关键词）",command =lambda :TOOLS_get_guize2 (OO0O0000OO0O0000O ))#line:4760
	if ini ["模式"]=="药品":#line:4761
		OO0OO00O0O0O0O00O .add_command (label ="怀疑/并用",command =lambda :STAT_pinzhong (OO0O0000OO0O0000O ,"怀疑/并用",1 ))#line:4763
		OO0OO00O0O0O0O00O .add_command (label ="报告类型-严重程度",command =lambda :STAT_pinzhong (OO0O0000OO0O0000O ,"报告类型-严重程度",1 ))#line:4765
		OO0OO00O0O0O0O00O .add_command (label ="停药减药后反应是否减轻或消失",command =lambda :STAT_pinzhong (OO0O0000OO0O0000O ,"停药减药后反应是否减轻或消失",1 ))#line:4767
		OO0OO00O0O0O0O00O .add_command (label ="再次使用可疑药是否出现同样反应",command =lambda :STAT_pinzhong (OO0O0000OO0O0000O ,"再次使用可疑药是否出现同样反应",1 ))#line:4769
		OO0OO00O0O0O0O00O .add_command (label ="对原患疾病影响",command =lambda :STAT_pinzhong (OO0O0000OO0O0000O ,"对原患疾病影响",1 ))#line:4771
		OO0OO00O0O0O0O00O .add_command (label ="不良反应结果",command =lambda :STAT_pinzhong (OO0O0000OO0O0000O ,"不良反应结果",1 ))#line:4773
		OO0OO00O0O0O0O00O .add_command (label ="报告单位关联性评价",command =lambda :STAT_pinzhong (OO0O0000OO0O0000O ,"关联性评价",1 ))#line:4775
		OO0OO00O0O0O0O00O .add_separator ()#line:4776
		OO0OO00O0O0O0O00O .add_command (label ="不良反应转归情况",command =lambda :STAT_pinzhong (OO0O0000OO0O0000O ,"不良反应结果2",4 ))#line:4778
		OO0OO00O0O0O0O00O .add_command (label ="品种评价-关联性评价汇总",command =lambda :STAT_pinzhong (OO0O0000OO0O0000O ,"关联性评价汇总",5 ))#line:4780
		OO0OO00O0O0O0O00O .add_separator ()#line:4784
		OO0OO00O0O0O0O00O .add_command (label ="不良反应-术语",command =lambda :STAT_pinzhong (OO0O0000OO0O0000O ,"器械故障表现",0 ))#line:4786
		OO0OO00O0O0O0O00O .add_command (label ="不良反应器官系统-术语",command =lambda :TABLE_tree_Level_2 (Countall (OO0O0000OO0O0000O ).df_psur (),1 ,O0OOOOOOO0O0OOOOO ))#line:4788
		if "不良反应-code"in OO0O0000OO0O0000O .columns :#line:4789
			OO0OO00O0O0O0O00O .add_command (label ="不良反应-由code转化",command =lambda :STAT_pinzhong (OO0O0000OO0O0000O ,"不良反应-code",2 ))#line:4791
			OO0OO00O0O0O0O00O .add_command (label ="不良反应器官系统-由code转化",command =lambda :STAT_pinzhong (OO0O0000OO0O0000O ,"不良反应-code",3 ))#line:4793
			OO0OO00O0O0O0O00O .add_separator ()#line:4794
		OO0OO00O0O0O0O00O .add_command (label ="疾病名称-术语",command =lambda :STAT_pinzhong (OO0O0000OO0O0000O ,"相关疾病信息[疾病名称]-术语",0 ))#line:4796
		if "不良反应-code"in OO0O0000OO0O0000O .columns :#line:4797
			OO0OO00O0O0O0O00O .add_command (label ="疾病名称-由code转化",command =lambda :STAT_pinzhong (OO0O0000OO0O0000O ,"相关疾病信息[疾病名称]-code",2 ))#line:4799
			OO0OO00O0O0O0O00O .add_command (label ="疾病器官系统-由code转化",command =lambda :STAT_pinzhong (OO0O0000OO0O0000O ,"相关疾病信息[疾病名称]-code",3 ))#line:4801
			OO0OO00O0O0O0O00O .add_separator ()#line:4802
		OO0OO00O0O0O0O00O .add_command (label ="适应症-术语",command =lambda :STAT_pinzhong (OO0O0000OO0O0000O ,"治疗适应症-术语",0 ))#line:4804
		if "不良反应-code"in OO0O0000OO0O0000O .columns :#line:4805
			OO0OO00O0O0O0O00O .add_command (label ="适应症-由code转化",command =lambda :STAT_pinzhong (OO0O0000OO0O0000O ,"治疗适应症-code",2 ))#line:4807
			OO0OO00O0O0O0O00O .add_command (label ="适应症器官系统-由code转化",command =lambda :STAT_pinzhong (OO0O0000OO0O0000O ,"治疗适应症-code",3 ))#line:4809
	if ini ["模式"]=="药品":#line:4811
		OO0O000OO00O0OOO0 =Menu (OO0O0000000000O00 ,tearoff =0 )#line:4812
		OO0O0000000000O00 .add_cascade (label ="药品探索",menu =OO0O000OO00O0OOO0 )#line:4813
		OO0O000OO00O0OOO0 .add_command (label ="新的不良反应检测(证号)",command =lambda :PROGRAM_thread_it (TOOLS_get_new ,O0OOOOOOO0O0OOOOO ,"证号"))#line:4814
		OO0O000OO00O0OOO0 .add_command (label ="新的不良反应检测(品种)",command =lambda :PROGRAM_thread_it (TOOLS_get_new ,O0OOOOOOO0O0OOOOO ,"品种"))#line:4815
		OO0O000OO00O0OOO0 .add_separator ()#line:4816
		OO0O000OO00O0OOO0 .add_command (label ="基础信息批量操作（品名）",command =lambda :TOOLS_ror_mode1 (OO0O0000OO0O0000O ,"产品名称"))#line:4818
		OO0O000OO00O0OOO0 .add_command (label ="器官系统分类批量操作（品名）",command =lambda :TOOLS_ror_mode4 (OO0O0000OO0O0000O ,"产品名称"))#line:4820
		OO0O000OO00O0OOO0 .add_command (label ="器官系统ROR批量操作（品名）",command =lambda :TOOLS_ror_mode2 (OO0O0000OO0O0000O ,"产品名称"))#line:4822
		OO0O000OO00O0OOO0 .add_command (label ="ADR-ROR批量操作（品名）",command =lambda :TOOLS_ror_mode3 (OO0O0000OO0O0000O ,"产品名称"))#line:4824
		OO0O000OO00O0OOO0 .add_separator ()#line:4825
		OO0O000OO00O0OOO0 .add_command (label ="基础信息批量操作（批准文号）",command =lambda :TOOLS_ror_mode1 (OO0O0000OO0O0000O ,"注册证编号/曾用注册证编号"))#line:4827
		OO0O000OO00O0OOO0 .add_command (label ="器官系统分类批量操作（批准文号）",command =lambda :TOOLS_ror_mode4 (OO0O0000OO0O0000O ,"注册证编号/曾用注册证编号"))#line:4829
		OO0O000OO00O0OOO0 .add_command (label ="器官系统ROR批量操作（批准文号）",command =lambda :TOOLS_ror_mode2 (OO0O0000OO0O0000O ,"注册证编号/曾用注册证编号"))#line:4831
		OO0O000OO00O0OOO0 .add_command (label ="ADR-ROR批量操作（批准文号）",command =lambda :TOOLS_ror_mode3 (OO0O0000OO0O0000O ,"注册证编号/曾用注册证编号"))#line:4833
	OO0OO00O0O0O0O0OO =Menu (OO0O0000000000O00 ,tearoff =0 )#line:4850
	OO0O0000000000O00 .add_cascade (label ="其他",menu =OO0OO00O0O0O0O0OO )#line:4851
	OO0OO00O0O0O0O0OO .add_command (label ="数据规整（报告单位）",command =lambda :TOOL_guizheng (OO0O0000OO0O0000O ,2 ,False ))#line:4855
	OO0OO00O0O0O0O0OO .add_command (label ="数据规整（产品名称）",command =lambda :TOOL_guizheng (OO0O0000OO0O0000O ,3 ,False ))#line:4857
	OO0OO00O0O0O0O0OO .add_command (label ="脱敏保存",command =lambda :TOOLS_data_masking (OO0O0000OO0O0000O ))#line:4859
	OO0OO00O0O0O0O0OO .add_separator ()#line:4860
	OO0OO00O0O0O0O0OO .add_command (label ="评价人员（广东化妆品）",command =lambda :TOOL_person (OO0O0000OO0O0000O ))#line:4862
	OO0OO00O0O0O0O0OO .add_command (label ="意见反馈",command =lambda :PROGRAM_helper (["","  药械妆不良反应报表统计分析工作站","  开发者：蔡权周","  邮箱：411703730@qq.com","  微信号：sysucai","  手机号：18575757461"]))#line:4864
	OO0OO00O0O0O0O0OO .add_command (label ="更改用户组",command =lambda :PROGRAM_thread_it (display_random_number ))#line:4866
def PROGRAM_helper (OOOOOO0O00OOO0000 ):#line:4870
    ""#line:4871
    O0000OO000O00OOOO =Toplevel ()#line:4872
    O0000OO000O00OOOO .title ("信息查看")#line:4873
    O0000OO000O00OOOO .geometry ("700x500")#line:4874
    O0O0OO0OOO0O0OO0O =Scrollbar (O0000OO000O00OOOO )#line:4876
    OO0O0O00000OOOOOO =Text (O0000OO000O00OOOO ,height =80 ,width =150 ,bg ="#FFFFFF",font ="微软雅黑")#line:4877
    O0O0OO0OOO0O0OO0O .pack (side =RIGHT ,fill =Y )#line:4878
    OO0O0O00000OOOOOO .pack ()#line:4879
    O0O0OO0OOO0O0OO0O .config (command =OO0O0O00000OOOOOO .yview )#line:4880
    OO0O0O00000OOOOOO .config (yscrollcommand =O0O0OO0OOO0O0OO0O .set )#line:4881
    for OO0O000OOOO0O000O in OOOOOO0O00OOO0000 :#line:4883
        OO0O0O00000OOOOOO .insert (END ,OO0O000OOOO0O000O )#line:4884
        OO0O0O00000OOOOOO .insert (END ,"\n")#line:4885
    def OO0O0O00O00OOOO0O (event =None ):#line:4888
        OO0O0O00000OOOOOO .event_generate ('<<Copy>>')#line:4889
    O000OOO0000000OOO =Menu (OO0O0O00000OOOOOO ,tearoff =False ,)#line:4892
    O000OOO0000000OOO .add_command (label ="复制",command =OO0O0O00O00OOOO0O )#line:4893
    def O00OOOOOO00O0O0O0 (O0OOO000O00O00O00 ):#line:4894
         O000OOO0000000OOO .post (O0OOO000O00O00O00 .x_root ,O0OOO000O00O00O00 .y_root )#line:4895
    OO0O0O00000OOOOOO .bind ("<Button-3>",O00OOOOOO00O0O0O0 )#line:4896
    OO0O0O00000OOOOOO .config (state =DISABLED )#line:4898
def PROGRAM_change_schedule (O0OOO00O00O0O00OO ,O00O000000OOO00O0 ):#line:4900
    ""#line:4901
    canvas .coords (fill_rec ,(5 ,5 ,(O0OOO00O00O0O00OO /O00O000000OOO00O0 )*680 ,25 ))#line:4903
    root .update ()#line:4904
    x .set (str (round (O0OOO00O00O0O00OO /O00O000000OOO00O0 *100 ,2 ))+"%")#line:4905
    if round (O0OOO00O00O0O00OO /O00O000000OOO00O0 *100 ,2 )==100.00 :#line:4906
        x .set ("完成")#line:4907
def PROGRAM_showWelcome ():#line:4910
    ""#line:4911
    O0OO00000OO000OO0 =roox .winfo_screenwidth ()#line:4912
    O00OO00O0OO0OOO0O =roox .winfo_screenheight ()#line:4914
    roox .overrideredirect (True )#line:4916
    roox .attributes ("-alpha",1 )#line:4917
    OOOOOO00OO000OOOO =(O0OO00000OO000OO0 -475 )/2 #line:4918
    OOO00OO000OOO0OO0 =(O00OO00O0OO0OOO0O -200 )/2 #line:4919
    roox .geometry ("675x130+%d+%d"%(OOOOOO00OO000OOOO ,OOO00OO000OOO0OO0 ))#line:4921
    roox ["bg"]="royalblue"#line:4922
    O00O00OOO0O0O0OOO =Label (roox ,text =title_all2 ,fg ="white",bg ="royalblue",font =("微软雅黑",20 ))#line:4925
    O00O00OOO0O0O0OOO .place (x =0 ,y =15 ,width =675 ,height =90 )#line:4926
    OOOOO0OO0OOOO00O0 =Label (roox ,text ="仅供监测机构使用 ",fg ="white",bg ="cornflowerblue",font =("微软雅黑",15 ))#line:4929
    OOOOO0OO0OOOO00O0 .place (x =0 ,y =90 ,width =675 ,height =40 )#line:4930
def PROGRAM_closeWelcome ():#line:4933
    ""#line:4934
    for O0O0O0OOO0OOOO0O0 in range (2 ):#line:4935
        root .attributes ("-alpha",0 )#line:4936
        time .sleep (1 )#line:4937
    root .attributes ("-alpha",1 )#line:4938
    roox .destroy ()#line:4939
class Countall ():#line:4954
	""#line:4955
	def __init__ (O0OO0O0O0OOOO00OO ,OOO000O00O00OOO00 ):#line:4956
		""#line:4957
		O0OO0O0O0OOOO00OO .df =OOO000O00O00OOO00 #line:4958
		O0OO0O0O0OOOO00OO .mode =ini ["模式"]#line:4959
	def df_org (O0O0O000OO0OOOO0O ,O0O0O0OOOO0OO00OO ):#line:4961
		""#line:4962
		O0O0OO000000O0000 =O0O0O000OO0OOOO0O .df .drop_duplicates (["报告编码"]).groupby ([O0O0O0OOOO0OO00OO ]).agg (报告数量 =("注册证编号/曾用注册证编号","count"),审核通过数 =("有效报告","sum"),严重伤害数 =("伤害",lambda OO000OOOO0O0OO0OO :STAT_countpx (OO000OOOO0O0OO0OO .values ,"严重伤害")),死亡数量 =("伤害",lambda O0OOO0O00OO0O00O0 :STAT_countpx (O0OOO0O00OO0O00O0 .values ,"死亡")),超时报告数 =("超时标记",lambda O000OOOO00OOOO0OO :STAT_countpx (O000OOOO00OOOO0OO .values ,1 )),有源 =("产品类别",lambda OO0000OOO00OO0O0O :STAT_countpx (OO0000OOO00OO0O0O .values ,"有源")),无源 =("产品类别",lambda O0OO0O00OOOOOOOOO :STAT_countpx (O0OO0O00OOOOOOOOO .values ,"无源")),体外诊断试剂 =("产品类别",lambda OOO0O0O00OOOO00OO :STAT_countpx (OOO0O0O00OOOO00OO .values ,"体外诊断试剂")),三类数量 =("管理类别",lambda O00OO00O000O0O0OO :STAT_countpx (O00OO00O000O0O0OO .values ,"Ⅲ类")),单位个数 =("单位名称","nunique"),单位列表 =("单位名称",STAT_countx ),报告季度 =("报告季度",STAT_countx ),报告月份 =("报告月份",STAT_countx ),).sort_values (by ="报告数量",ascending =[False ],na_position ="last").reset_index ()#line:4977
		O000OOOOOO0OOO0O0 =["报告数量","审核通过数","严重伤害数","死亡数量","超时报告数","有源","无源","体外诊断试剂","三类数量","单位个数"]#line:4979
		O0O0OO000000O0000 .loc ["合计"]=O0O0OO000000O0000 [O000OOOOOO0OOO0O0 ].apply (lambda OO0O0OO00000O0OOO :OO0O0OO00000O0OOO .sum ())#line:4980
		O0O0OO000000O0000 [O000OOOOOO0OOO0O0 ]=O0O0OO000000O0000 [O000OOOOOO0OOO0O0 ].apply (lambda O0OOO00000OOO0O0O :O0OOO00000OOO0O0O .astype (int ))#line:4981
		O0O0OO000000O0000 .iloc [-1 ,0 ]="合计"#line:4982
		O0O0OO000000O0000 ["严重比"]=round ((O0O0OO000000O0000 ["严重伤害数"]+O0O0OO000000O0000 ["死亡数量"])/O0O0OO000000O0000 ["报告数量"]*100 ,2 )#line:4984
		O0O0OO000000O0000 ["Ⅲ类比"]=round ((O0O0OO000000O0000 ["三类数量"])/O0O0OO000000O0000 ["报告数量"]*100 ,2 )#line:4985
		O0O0OO000000O0000 ["超时比"]=round ((O0O0OO000000O0000 ["超时报告数"])/O0O0OO000000O0000 ["报告数量"]*100 ,2 )#line:4986
		O0O0OO000000O0000 ["报表类型"]="dfx_org"+O0O0O0OOOO0OO00OO #line:4987
		if ini ["模式"]=="药品":#line:4990
			del O0O0OO000000O0000 ["有源"]#line:4992
			del O0O0OO000000O0000 ["无源"]#line:4993
			del O0O0OO000000O0000 ["体外诊断试剂"]#line:4994
			O0O0OO000000O0000 =O0O0OO000000O0000 .rename (columns ={"三类数量":"新的和严重的数量"})#line:4995
			O0O0OO000000O0000 =O0O0OO000000O0000 .rename (columns ={"Ⅲ类比":"新严比"})#line:4996
		return O0O0OO000000O0000 #line:4998
	def df_user (OO0OO0000OO00O0O0 ):#line:5002
		""#line:5003
		OO0OO0000OO00O0O0 .df ["医疗机构类别"]=OO0OO0000OO00O0O0 .df ["医疗机构类别"].fillna ("未填写")#line:5004
		O000O0O000OOO0OO0 =OO0OO0000OO00O0O0 .df .drop_duplicates (["报告编码"]).groupby (["监测机构","单位名称","医疗机构类别"]).agg (报告数量 =("注册证编号/曾用注册证编号","count"),审核通过数 =("有效报告","sum"),严重伤害数 =("伤害",lambda OOO00O00OO00O0OOO :STAT_countpx (OOO00O00OO00O0OOO .values ,"严重伤害")),死亡数量 =("伤害",lambda OO0OO00OOO000O000 :STAT_countpx (OO0OO00OOO000O000 .values ,"死亡")),超时报告数 =("超时标记",lambda O00OOOOO0O0OOOOOO :STAT_countpx (O00OOOOO0O0OOOOOO .values ,1 )),有源 =("产品类别",lambda O0OO000000O0O0000 :STAT_countpx (O0OO000000O0O0000 .values ,"有源")),无源 =("产品类别",lambda O00OOO000OO0OOOO0 :STAT_countpx (O00OOO000OO0OOOO0 .values ,"无源")),体外诊断试剂 =("产品类别",lambda OOO0OO0OOO0O000OO :STAT_countpx (OOO0OO0OOO0O000OO .values ,"体外诊断试剂")),三类数量 =("管理类别",lambda OOO0O0OO00O0OOO0O :STAT_countpx (OOO0O0OO00O0OOO0O .values ,"Ⅲ类")),产品数量 =("产品名称","nunique"),产品清单 =("产品名称",STAT_countx ),报告季度 =("报告季度",STAT_countx ),报告月份 =("报告月份",STAT_countx ),).sort_values (by ="报告数量",ascending =[False ],na_position ="last").reset_index ()#line:5019
		O00000O000OO00OO0 =["报告数量","审核通过数","严重伤害数","死亡数量","超时报告数","有源","无源","体外诊断试剂","三类数量"]#line:5022
		O000O0O000OOO0OO0 .loc ["合计"]=O000O0O000OOO0OO0 [O00000O000OO00OO0 ].apply (lambda OO0000OO0000000O0 :OO0000OO0000000O0 .sum ())#line:5023
		O000O0O000OOO0OO0 [O00000O000OO00OO0 ]=O000O0O000OOO0OO0 [O00000O000OO00OO0 ].apply (lambda OOOOO00O000000O0O :OOOOO00O000000O0O .astype (int ))#line:5024
		O000O0O000OOO0OO0 .iloc [-1 ,0 ]="合计"#line:5025
		O000O0O000OOO0OO0 ["严重比"]=round ((O000O0O000OOO0OO0 ["严重伤害数"]+O000O0O000OOO0OO0 ["死亡数量"])/O000O0O000OOO0OO0 ["报告数量"]*100 ,2 )#line:5027
		O000O0O000OOO0OO0 ["Ⅲ类比"]=round ((O000O0O000OOO0OO0 ["三类数量"])/O000O0O000OOO0OO0 ["报告数量"]*100 ,2 )#line:5028
		O000O0O000OOO0OO0 ["超时比"]=round ((O000O0O000OOO0OO0 ["超时报告数"])/O000O0O000OOO0OO0 ["报告数量"]*100 ,2 )#line:5029
		O000O0O000OOO0OO0 ["报表类型"]="dfx_user"#line:5030
		if ini ["模式"]=="药品":#line:5032
			del O000O0O000OOO0OO0 ["有源"]#line:5034
			del O000O0O000OOO0OO0 ["无源"]#line:5035
			del O000O0O000OOO0OO0 ["体外诊断试剂"]#line:5036
			O000O0O000OOO0OO0 =O000O0O000OOO0OO0 .rename (columns ={"三类数量":"新的和严重的数量"})#line:5037
			O000O0O000OOO0OO0 =O000O0O000OOO0OO0 .rename (columns ={"Ⅲ类比":"新严比"})#line:5038
		return O000O0O000OOO0OO0 #line:5040
	def df_zhenghao (OO00O000000000OOO ):#line:5045
		""#line:5046
		OO0OO0O0O0O0OOO00 =OO00O000000000OOO .df .groupby (["上市许可持有人名称","产品类别","规整后品类","产品名称","注册证编号/曾用注册证编号"]).agg (证号计数 =("报告编码","nunique"),批号个数 =("产品批号","nunique"),批号列表 =("产品批号",STAT_countx ),型号个数 =("型号","nunique"),型号列表 =("型号",STAT_countx ),规格个数 =("规格","nunique"),规格列表 =("规格",STAT_countx ),).sort_values (by ="证号计数",ascending =[False ],na_position ="last").reset_index ()#line:5056
		OOO0OO00OO00000OO =OO00O000000000OOO .df .drop_duplicates (["报告编码"]).groupby (["上市许可持有人名称","产品类别","规整后品类","产品名称","注册证编号/曾用注册证编号"]).agg (严重伤害数 =("伤害",lambda OO0OOOO0000OO00OO :STAT_countpx (OO0OOOO0000OO00OO .values ,"严重伤害")),死亡数量 =("伤害",lambda OOOOO000OOOO0O0O0 :STAT_countpx (OOOOO000OOOO0O0O0 .values ,"死亡")),单位个数 =("单位名称","nunique"),单位列表 =("单位名称",STAT_countx ),待评价数 =("持有人报告状态",lambda O00O0000O0000O0O0 :STAT_countpx (O00O0000O0000O0O0 .values ,"待评价")),严重伤害待评价数 =("伤害与评价",lambda OO0OOO0O000O000O0 :STAT_countpx (OO0OOO0O000O000O0 .values ,"严重伤害待评价")),).reset_index ()#line:5065
		OO000OO0OO0OO00OO =pd .merge (OO0OO0O0O0O0OOO00 ,OOO0OO00OO00000OO ,on =["上市许可持有人名称","产品类别","规整后品类","产品名称","注册证编号/曾用注册证编号"],how ="left")#line:5067
		OO000OO0OO0OO00OO =STAT_basic_risk (OO000OO0OO0OO00OO ,"证号计数","严重伤害数","死亡数量","单位个数")#line:5068
		OO000OO0OO0OO00OO =pd .merge (OO000OO0OO0OO00OO ,STAT_recent30 (OO00O000000000OOO .df ,["注册证编号/曾用注册证编号"]),on =["注册证编号/曾用注册证编号"],how ="left")#line:5070
		OO000OO0OO0OO00OO ["最近30天报告数"]=OO000OO0OO0OO00OO ["最近30天报告数"].fillna (0 ).astype (int )#line:5071
		OO000OO0OO0OO00OO ["最近30天报告严重伤害数"]=OO000OO0OO0OO00OO ["最近30天报告严重伤害数"].fillna (0 ).astype (int )#line:5072
		OO000OO0OO0OO00OO ["最近30天报告死亡数量"]=OO000OO0OO0OO00OO ["最近30天报告死亡数量"].fillna (0 ).astype (int )#line:5073
		OO000OO0OO0OO00OO ["最近30天报告单位个数"]=OO000OO0OO0OO00OO ["最近30天报告单位个数"].fillna (0 ).astype (int )#line:5074
		OO000OO0OO0OO00OO ["最近30天风险评分"]=OO000OO0OO0OO00OO ["最近30天风险评分"].fillna (0 ).astype (int )#line:5075
		OO000OO0OO0OO00OO ["报表类型"]="dfx_zhenghao"#line:5077
		if ini ["模式"]=="药品":#line:5079
			OO000OO0OO0OO00OO =OO000OO0OO0OO00OO .rename (columns ={"待评价数":"新的数量"})#line:5080
			OO000OO0OO0OO00OO =OO000OO0OO0OO00OO .rename (columns ={"严重伤害待评价数":"新的严重的数量"})#line:5081
		return OO000OO0OO0OO00OO #line:5083
	def df_pihao (OOOO0000OO000O0OO ):#line:5085
		""#line:5086
		O0OO000OO00OO0OO0 =OOOO0000OO000O0OO .df .groupby (["上市许可持有人名称","产品类别","产品名称","注册证编号/曾用注册证编号","产品批号"]).agg (批号计数 =("报告编码","nunique"),型号个数 =("型号","nunique"),型号列表 =("型号",STAT_countx ),规格个数 =("规格","nunique"),规格列表 =("规格",STAT_countx ),).sort_values (by ="批号计数",ascending =[False ],na_position ="last").reset_index ()#line:5093
		O00OOOOOOOO0OO00O =OOOO0000OO000O0OO .df .drop_duplicates (["报告编码"]).groupby (["上市许可持有人名称","产品类别","产品名称","注册证编号/曾用注册证编号","产品批号"]).agg (严重伤害数 =("伤害",lambda O0OOO000000O0O000 :STAT_countpx (O0OOO000000O0O000 .values ,"严重伤害")),死亡数量 =("伤害",lambda OOO00OOOO0OO0O0O0 :STAT_countpx (OOO00OOOO0OO0O0O0 .values ,"死亡")),单位个数 =("单位名称","nunique"),单位列表 =("单位名称",STAT_countx ),待评价数 =("持有人报告状态",lambda OO00O00OO00O0O000 :STAT_countpx (OO00O00OO00O0O000 .values ,"待评价")),严重伤害待评价数 =("伤害与评价",lambda O0OO00O0O00OOO000 :STAT_countpx (O0OO00O0O00OOO000 .values ,"严重伤害待评价")),).reset_index ()#line:5102
		O00OO000O0OO0OO0O =pd .merge (O0OO000OO00OO0OO0 ,O00OOOOOOOO0OO00O ,on =["上市许可持有人名称","产品类别","产品名称","注册证编号/曾用注册证编号","产品批号"],how ="left")#line:5104
		O00OO000O0OO0OO0O =STAT_basic_risk (O00OO000O0OO0OO0O ,"批号计数","严重伤害数","死亡数量","单位个数")#line:5106
		O00OO000O0OO0OO0O =pd .merge (O00OO000O0OO0OO0O ,STAT_recent30 (OOOO0000OO000O0OO .df ,["注册证编号/曾用注册证编号","产品批号"]),on =["注册证编号/曾用注册证编号","产品批号"],how ="left")#line:5108
		O00OO000O0OO0OO0O ["最近30天报告数"]=O00OO000O0OO0OO0O ["最近30天报告数"].fillna (0 ).astype (int )#line:5109
		O00OO000O0OO0OO0O ["最近30天报告严重伤害数"]=O00OO000O0OO0OO0O ["最近30天报告严重伤害数"].fillna (0 ).astype (int )#line:5110
		O00OO000O0OO0OO0O ["最近30天报告死亡数量"]=O00OO000O0OO0OO0O ["最近30天报告死亡数量"].fillna (0 ).astype (int )#line:5111
		O00OO000O0OO0OO0O ["最近30天报告单位个数"]=O00OO000O0OO0OO0O ["最近30天报告单位个数"].fillna (0 ).astype (int )#line:5112
		O00OO000O0OO0OO0O ["最近30天风险评分"]=O00OO000O0OO0OO0O ["最近30天风险评分"].fillna (0 ).astype (int )#line:5113
		O00OO000O0OO0OO0O ["报表类型"]="dfx_pihao"#line:5115
		if ini ["模式"]=="药品":#line:5116
			O00OO000O0OO0OO0O =O00OO000O0OO0OO0O .rename (columns ={"待评价数":"新的数量"})#line:5117
			O00OO000O0OO0OO0O =O00OO000O0OO0OO0O .rename (columns ={"严重伤害待评价数":"新的严重的数量"})#line:5118
		return O00OO000O0OO0OO0O #line:5119
	def df_xinghao (O0O0O0OO00000000O ):#line:5121
		""#line:5122
		O00O00OO00000OO00 =O0O0O0OO00000000O .df .groupby (["上市许可持有人名称","产品类别","产品名称","注册证编号/曾用注册证编号","型号"]).agg (型号计数 =("报告编码","nunique"),批号个数 =("产品批号","nunique"),批号列表 =("产品批号",STAT_countx ),规格个数 =("规格","nunique"),规格列表 =("规格",STAT_countx ),).sort_values (by ="型号计数",ascending =[False ],na_position ="last").reset_index ()#line:5129
		O00O0OO00OO00O0OO =O0O0O0OO00000000O .df .drop_duplicates (["报告编码"]).groupby (["上市许可持有人名称","产品类别","产品名称","注册证编号/曾用注册证编号","型号"]).agg (严重伤害数 =("伤害",lambda OOOOOO00O0OOOOOOO :STAT_countpx (OOOOOO00O0OOOOOOO .values ,"严重伤害")),死亡数量 =("伤害",lambda OO0OOOO0OO0OO00OO :STAT_countpx (OO0OOOO0OO0OO00OO .values ,"死亡")),单位个数 =("单位名称","nunique"),单位列表 =("单位名称",STAT_countx ),待评价数 =("持有人报告状态",lambda OOOOO00OOOO00O0O0 :STAT_countpx (OOOOO00OOOO00O0O0 .values ,"待评价")),严重伤害待评价数 =("伤害与评价",lambda O0O00O00O0O0O0OOO :STAT_countpx (O0O00O00O0O0O0OOO .values ,"严重伤害待评价")),).reset_index ()#line:5138
		OO000OOO00OOOO000 =pd .merge (O00O00OO00000OO00 ,O00O0OO00OO00O0OO ,on =["上市许可持有人名称","产品类别","产品名称","注册证编号/曾用注册证编号","型号"],how ="left")#line:5140
		OO000OOO00OOOO000 ["报表类型"]="dfx_xinghao"#line:5143
		if ini ["模式"]=="药品":#line:5144
			OO000OOO00OOOO000 =OO000OOO00OOOO000 .rename (columns ={"待评价数":"新的数量"})#line:5145
			OO000OOO00OOOO000 =OO000OOO00OOOO000 .rename (columns ={"严重伤害待评价数":"新的严重的数量"})#line:5146
		return OO000OOO00OOOO000 #line:5148
	def df_guige (O00000OO00O0000O0 ):#line:5150
		""#line:5151
		OOOO0OO0O000000O0 =O00000OO00O0000O0 .df .groupby (["上市许可持有人名称","产品类别","产品名称","注册证编号/曾用注册证编号","规格"]).agg (规格计数 =("报告编码","nunique"),批号个数 =("产品批号","nunique"),批号列表 =("产品批号",STAT_countx ),型号个数 =("型号","nunique"),型号列表 =("型号",STAT_countx ),).sort_values (by ="规格计数",ascending =[False ],na_position ="last").reset_index ()#line:5158
		O00OO0O000OO0O00O =O00000OO00O0000O0 .df .drop_duplicates (["报告编码"]).groupby (["上市许可持有人名称","产品类别","产品名称","注册证编号/曾用注册证编号","规格"]).agg (严重伤害数 =("伤害",lambda O0O0O0OOO000O000O :STAT_countpx (O0O0O0OOO000O000O .values ,"严重伤害")),死亡数量 =("伤害",lambda OO000OO00OOO000O0 :STAT_countpx (OO000OO00OOO000O0 .values ,"死亡")),单位个数 =("单位名称","nunique"),单位列表 =("单位名称",STAT_countx ),待评价数 =("持有人报告状态",lambda O0O0OOOO0OO0O0O00 :STAT_countpx (O0O0OOOO0OO0O0O00 .values ,"待评价")),严重伤害待评价数 =("伤害与评价",lambda OO0O000O00OOOO0OO :STAT_countpx (OO0O000O00OOOO0OO .values ,"严重伤害待评价")),).reset_index ()#line:5167
		O0OO0OOOO00O000OO =pd .merge (OOOO0OO0O000000O0 ,O00OO0O000OO0O00O ,on =["上市许可持有人名称","产品类别","产品名称","注册证编号/曾用注册证编号","规格"],how ="left")#line:5169
		O0OO0OOOO00O000OO ["报表类型"]="dfx_guige"#line:5171
		if ini ["模式"]=="药品":#line:5172
			O0OO0OOOO00O000OO =O0OO0OOOO00O000OO .rename (columns ={"待评价数":"新的数量"})#line:5173
			O0OO0OOOO00O000OO =O0OO0OOOO00O000OO .rename (columns ={"严重伤害待评价数":"新的严重的数量"})#line:5174
		return O0OO0OOOO00O000OO #line:5176
	def df_findrisk (OOOOOOOOO0O00OOO0 ,OOOOOO0OO00OOOOOO ):#line:5178
		""#line:5179
		if OOOOOO0OO00OOOOOO =="产品批号":#line:5180
			return STAT_find_risk (OOOOOOOOO0O00OOO0 .df [(OOOOOOOOO0O00OOO0 .df ["产品类别"]!="有源")],["上市许可持有人名称","产品类别","产品名称","注册证编号/曾用注册证编号"],"注册证编号/曾用注册证编号",OOOOOO0OO00OOOOOO )#line:5181
		else :#line:5182
			return STAT_find_risk (OOOOOOOOO0O00OOO0 .df ,["上市许可持有人名称","产品类别","产品名称","注册证编号/曾用注册证编号"],"注册证编号/曾用注册证编号",OOOOOO0OO00OOOOOO )#line:5183
	def df_find_all_keword_risk (O0OO00000O0OOOO0O ,O000O0OOO00O0O000 ,*O0O0OOO0OO0O0OO00 ):#line:5185
		""#line:5186
		O000OOOOOOOO0O000 =O0OO00000O0OOOO0O .df .copy ()#line:5188
		O000OOOOOOOO0O000 =O000OOOOOOOO0O000 .drop_duplicates (["报告编码"]).reset_index (drop =True )#line:5189
		OO00O000OO00OO0OO =time .time ()#line:5190
		O0O0OO00O0000OOOO =peizhidir +"0（范例）比例失衡关键字库.xls"#line:5191
		if "报告类型-新的"in O000OOOOOOOO0O000 .columns :#line:5192
			O0O0O00000OO000OO ="药品"#line:5193
		else :#line:5194
			O0O0O00000OO000OO ="器械"#line:5195
		OO0O0OO0OOOO00O0O =pd .read_excel (O0O0OO00O0000OOOO ,header =0 ,sheet_name =O0O0O00000OO000OO ).reset_index (drop =True )#line:5196
		try :#line:5199
			if len (O0O0OOO0OO0O0OO00 [0 ])>0 :#line:5200
				OO0O0OO0OOOO00O0O =OO0O0OO0OOOO00O0O .loc [OO0O0OO0OOOO00O0O ["适用范围"].str .contains (O0O0OOO0OO0O0OO00 [0 ],na =False )].copy ().reset_index (drop =True )#line:5201
		except :#line:5202
			pass #line:5203
		O0OOO0000OOOOO000 =["上市许可持有人名称","产品类别","产品名称","注册证编号/曾用注册证编号"]#line:5205
		O0O00O000O0O0O0O0 =O0OOO0000OOOOO000 [-1 ]#line:5206
		O00OOO000O00OO0OO =O000OOOOOOOO0O000 .groupby (O0OOO0000OOOOO000 ).agg (总数量 =(O0O00O000O0O0O0O0 ,"count"),严重伤害数 =("伤害",lambda OOO0OO00OO0OOOO0O :STAT_countpx (OOO0OO00OO0OOOO0O .values ,"严重伤害")),死亡数量 =("伤害",lambda OO0O0O0O0OO0OO000 :STAT_countpx (OO0O0O0O0OO0OO000 .values ,"死亡")),)#line:5211
		O0O00O000O0O0O0O0 =O0OOO0000OOOOO000 [-1 ]#line:5212
		O0OOOO0O0O0OO00OO =O0OOO0000OOOOO000 .copy ()#line:5214
		O0OOOO0O0O0OO00OO .append (O000O0OOO00O0O000 )#line:5215
		O0OO000O00O0O00OO =O000OOOOOOOO0O000 .groupby (O0OOOO0O0O0OO00OO ).agg (该元素总数量 =(O0O00O000O0O0O0O0 ,"count"),).reset_index ()#line:5218
		O00OOO000O00OO0OO =O00OOO000O00OO0OO [(O00OOO000O00OO0OO ["总数量"]>=3 )].reset_index ()#line:5221
		O0O00O0O0OO00O00O =[]#line:5222
		OOO000OO0OO0OO0OO =0 #line:5226
		OO000OO0O00OOO000 =int (len (O00OOO000O00OO0OO ))#line:5227
		for OO0OO00O0O00OOO0O ,OOOO0O0OOOO0OOO0O ,O00O0OOOO0OO000O0 ,OOOOO00O00OOOOO0O in zip (O00OOO000O00OO0OO ["产品名称"].values ,O00OOO000O00OO0OO ["产品类别"].values ,O00OOO000O00OO0OO [O0O00O000O0O0O0O0 ].values ,O00OOO000O00OO0OO ["总数量"].values ):#line:5228
			OOO000OO0OO0OO0OO +=1 #line:5229
			if (time .time ()-OO00O000OO00OO0OO )>3 :#line:5231
				root .attributes ("-topmost",True )#line:5232
				PROGRAM_change_schedule (OOO000OO0OO0OO0OO ,OO000OO0O00OOO000 )#line:5233
				root .attributes ("-topmost",False )#line:5234
			O0OOO0OOO0OO000OO =O000OOOOOOOO0O000 [(O000OOOOOOOO0O000 [O0O00O000O0O0O0O0 ]==O00O0OOOO0OO000O0 )].copy ()#line:5235
			OO0O0OO0OOOO00O0O ["SELECT"]=OO0O0OO0OOOO00O0O .apply (lambda O000OO000O0O0000O :(O000OO000O0O0000O ["适用范围"]in OO0OO00O0O00OOO0O )or (O000OO000O0O0000O ["适用范围"]in OOOO0O0OOOO0OOO0O )or (O000OO000O0O0000O ["适用范围"]=="通用"),axis =1 )#line:5236
			O00OOOOOO0O0O0000 =OO0O0OO0OOOO00O0O [(OO0O0OO0OOOO00O0O ["SELECT"]==True )].reset_index ()#line:5237
			if len (O00OOOOOO0O0O0000 )>0 :#line:5238
				for OO0OO00OO0O0OOOO0 ,O0O00O000OO000O0O ,OOO0000OO0OOO0O00 in zip (O00OOOOOO0O0O0000 ["值"].values ,O00OOOOOO0O0O0000 ["查找位置"].values ,O00OOOOOO0O0O0000 ["排除值"].values ):#line:5240
					OO00OOOO00OO0O0O0 =O0OOO0OOO0OO000OO .copy ()#line:5241
					O0O0OOO0O000OOOO0 =TOOLS_get_list (OO0OO00OO0O0OOOO0 )[0 ]#line:5242
					OO00OOOO00OO0O0O0 ["关键字查找列"]=""#line:5244
					for O0O0O00000OO0O000 in TOOLS_get_list (O0O00O000OO000O0O ):#line:5245
						OO00OOOO00OO0O0O0 ["关键字查找列"]=OO00OOOO00OO0O0O0 ["关键字查找列"]+OO00OOOO00OO0O0O0 [O0O0O00000OO0O000 ].astype ("str")#line:5246
					OO00OOOO00OO0O0O0 .loc [OO00OOOO00OO0O0O0 ["关键字查找列"].str .contains (OO0OO00OO0O0OOOO0 ,na =False ),"关键字"]=O0O0OOO0O000OOOO0 #line:5248
					if str (OOO0000OO0OOO0O00 )!="nan":#line:5251
						OO00OOOO00OO0O0O0 =OO00OOOO00OO0O0O0 .loc [~OO00OOOO00OO0O0O0 ["关键字查找列"].str .contains (OOO0000OO0OOO0O00 ,na =False )].copy ()#line:5252
					if (len (OO00OOOO00OO0O0O0 ))<1 :#line:5254
						continue #line:5255
					O00OO00O00OO0OOO0 =STAT_find_keyword_risk (OO00OOOO00OO0O0O0 ,["上市许可持有人名称","产品类别","产品名称","注册证编号/曾用注册证编号","关键字"],"关键字",O000O0OOO00O0O000 ,int (OOOOO00O00OOOOO0O ))#line:5257
					if len (O00OO00O00OO0OOO0 )>0 :#line:5258
						O00OO00O00OO0OOO0 ["关键字组合"]=OO0OO00OO0O0OOOO0 #line:5259
						O00OO00O00OO0OOO0 ["排除值"]=OOO0000OO0OOO0O00 #line:5260
						O00OO00O00OO0OOO0 ["关键字查找列"]=O0O00O000OO000O0O #line:5261
						O0O00O0O0OO00O00O .append (O00OO00O00OO0OOO0 )#line:5262
		O0000O00OOO0O0O0O =pd .concat (O0O00O0O0OO00O00O )#line:5266
		O0000O00OOO0O0O0O =pd .merge (O0000O00OOO0O0O0O ,O0OO000O00O0O00OO ,on =O0OOOO0O0O0OO00OO ,how ="left")#line:5269
		O0000O00OOO0O0O0O ["关键字数量比例"]=round (O0000O00OOO0O0O0O ["计数"]/O0000O00OOO0O0O0O ["该元素总数量"],2 )#line:5270
		O0000O00OOO0O0O0O =O0000O00OOO0O0O0O .reset_index (drop =True )#line:5272
		if len (O0000O00OOO0O0O0O )>0 :#line:5273
			O0000O00OOO0O0O0O ["风险评分"]=0 #line:5274
			O0000O00OOO0O0O0O ["报表类型"]="keyword_findrisk"+O000O0OOO00O0O000 #line:5275
			O0000O00OOO0O0O0O .loc [(O0000O00OOO0O0O0O ["计数"]>=3 ),"风险评分"]=O0000O00OOO0O0O0O ["风险评分"]+3 #line:5276
			O0000O00OOO0O0O0O .loc [(O0000O00OOO0O0O0O ["计数"]>=(O0000O00OOO0O0O0O ["数量均值"]+O0000O00OOO0O0O0O ["数量标准差"])),"风险评分"]=O0000O00OOO0O0O0O ["风险评分"]+1 #line:5277
			O0000O00OOO0O0O0O .loc [(O0000O00OOO0O0O0O ["计数"]>=O0000O00OOO0O0O0O ["数量CI"]),"风险评分"]=O0000O00OOO0O0O0O ["风险评分"]+1 #line:5278
			O0000O00OOO0O0O0O .loc [(O0000O00OOO0O0O0O ["关键字数量比例"]>0.5 )&(O0000O00OOO0O0O0O ["计数"]>=3 ),"风险评分"]=O0000O00OOO0O0O0O ["风险评分"]+1 #line:5279
			O0000O00OOO0O0O0O .loc [(O0000O00OOO0O0O0O ["严重伤害数"]>=3 ),"风险评分"]=O0000O00OOO0O0O0O ["风险评分"]+1 #line:5280
			O0000O00OOO0O0O0O .loc [(O0000O00OOO0O0O0O ["单位个数"]>=3 ),"风险评分"]=O0000O00OOO0O0O0O ["风险评分"]+1 #line:5281
			O0000O00OOO0O0O0O .loc [(O0000O00OOO0O0O0O ["死亡数量"]>=1 ),"风险评分"]=O0000O00OOO0O0O0O ["风险评分"]+10 #line:5282
			O0000O00OOO0O0O0O ["风险评分"]=O0000O00OOO0O0O0O ["风险评分"]+O0000O00OOO0O0O0O ["单位个数"]/100 #line:5283
			O0000O00OOO0O0O0O =O0000O00OOO0O0O0O .sort_values (by ="风险评分",ascending =[False ],na_position ="last").reset_index (drop =True )#line:5284
		print ("耗时：",(time .time ()-OO00O000OO00OO0OO ))#line:5290
		return O0000O00OOO0O0O0O #line:5291
	def df_ror (OOO0OO0O000OOOOO0 ,OOO0000000OO0OO0O ,*O000OO000O0OO0OOO ):#line:5294
		""#line:5295
		O000OOO0O00OOOOOO =OOO0OO0O000OOOOO0 .df .copy ()#line:5297
		O000OO0O0O00OO0O0 =time .time ()#line:5298
		OO00OOO00OO00O0O0 =peizhidir +"0（范例）比例失衡关键字库.xls"#line:5299
		if "报告类型-新的"in O000OOO0O00OOOOOO .columns :#line:5300
			O000OOO000000OO00 ="药品"#line:5301
		else :#line:5303
			O000OOO000000OO00 ="器械"#line:5304
		O00000O0O00OO0O00 =pd .read_excel (OO00OOO00OO00O0O0 ,header =0 ,sheet_name =O000OOO000000OO00 ).reset_index (drop =True )#line:5305
		if "css"in O000OOO0O00OOOOOO .columns :#line:5308
			OO0OOO0OO00000000 =O000OOO0O00OOOOOO .copy ()#line:5309
			OO0OOO0OO00000000 ["器械故障表现"]=OO0OOO0OO00000000 ["器械故障表现"].fillna ("未填写")#line:5310
			OO0OOO0OO00000000 ["器械故障表现"]=OO0OOO0OO00000000 ["器械故障表现"].str .replace ("*","",regex =False )#line:5311
			OOO0O00O0O0OO00O0 ="use("+str ("器械故障表现")+").file"#line:5312
			O00000O00OOO0000O =str (Counter (TOOLS_get_list0 (OOO0O00O0O0OO00O0 ,OO0OOO0OO00000000 ,1000 ))).replace ("Counter({","{")#line:5313
			O00000O00OOO0000O =O00000O00OOO0000O .replace ("})","}")#line:5314
			O00000O00OOO0000O =ast .literal_eval (O00000O00OOO0000O )#line:5315
			O00000O0O00OO0O00 =pd .DataFrame .from_dict (O00000O00OOO0000O ,orient ="index",columns =["计数"]).reset_index ()#line:5316
			O00000O0O00OO0O00 ["适用范围列"]="产品类别"#line:5317
			O00000O0O00OO0O00 ["适用范围"]="无源"#line:5318
			O00000O0O00OO0O00 ["查找位置"]="伤害表现"#line:5319
			O00000O0O00OO0O00 ["值"]=O00000O0O00OO0O00 ["index"]#line:5320
			O00000O0O00OO0O00 ["排除值"]="-没有排除值-"#line:5321
			del O00000O0O00OO0O00 ["index"]#line:5322
		O000O0OO0000O0O0O =OOO0000000OO0OO0O [-2 ]#line:5325
		OO00O0OOOO0000O0O =OOO0000000OO0OO0O [-1 ]#line:5326
		O000OO0O0OO00O0O0 =OOO0000000OO0OO0O [:-1 ]#line:5327
		try :#line:5330
			if len (O000OO000O0OO0OOO [0 ])>0 :#line:5331
				O000O0OO0000O0O0O =OOO0000000OO0OO0O [-3 ]#line:5332
				O00000O0O00OO0O00 =O00000O0O00OO0O00 .loc [O00000O0O00OO0O00 ["适用范围"].str .contains (O000OO000O0OO0OOO [0 ],na =False )].copy ().reset_index (drop =True )#line:5333
				OOOO0O0O00OOO00O0 =O000OOO0O00OOOOOO .groupby (["产品类别","规整后品类","产品名称","注册证编号/曾用注册证编号"]).agg (该元素总数量 =(OO00O0OOOO0000O0O ,"count"),该元素严重伤害数 =("伤害",lambda OOOO000OOOO000000 :STAT_countpx (OOOO000OOOO000000 .values ,"严重伤害")),该元素死亡数量 =("伤害",lambda O0OOOOOOOO0O00000 :STAT_countpx (O0OOOOOOOO0O00000 .values ,"死亡")),该元素单位个数 =("单位名称","nunique"),该元素单位列表 =("单位名称",STAT_countx ),).reset_index ()#line:5340
				O0OO00O0OOO0OOO0O =O000OOO0O00OOOOOO .groupby (["产品类别","规整后品类"]).agg (所有元素总数量 =(O000O0OO0000O0O0O ,"count"),所有元素严重伤害数 =("伤害",lambda O0O0000O000O0OO00 :STAT_countpx (O0O0000O000O0OO00 .values ,"严重伤害")),所有元素死亡数量 =("伤害",lambda OO00O00OO00OO0OO0 :STAT_countpx (OO00O00OO00OO0OO0 .values ,"死亡")),)#line:5345
				if len (O0OO00O0OOO0OOO0O )>1 :#line:5346
					text .insert (END ,"注意，产品类别有两种，产品名称规整疑似不正确！")#line:5347
				OOOO0O0O00OOO00O0 =pd .merge (OOOO0O0O00OOO00O0 ,O0OO00O0OOO0OOO0O ,on =["产品类别","规整后品类"],how ="left").reset_index ()#line:5349
		except :#line:5351
			text .insert (END ,"\n目前结果为未进行名称规整的结果！\n")#line:5352
			OOOO0O0O00OOO00O0 =O000OOO0O00OOOOOO .groupby (OOO0000000OO0OO0O ).agg (该元素总数量 =(OO00O0OOOO0000O0O ,"count"),该元素严重伤害数 =("伤害",lambda O000OO00OOOO0O0OO :STAT_countpx (O000OO00OOOO0O0OO .values ,"严重伤害")),该元素死亡数量 =("伤害",lambda O0OO0OO0OOOO0OO0O :STAT_countpx (O0OO0OO0OOOO0OO0O .values ,"死亡")),该元素单位个数 =("单位名称","nunique"),该元素单位列表 =("单位名称",STAT_countx ),).reset_index ()#line:5359
			O0OO00O0OOO0OOO0O =O000OOO0O00OOOOOO .groupby (O000OO0O0OO00O0O0 ).agg (所有元素总数量 =(O000O0OO0000O0O0O ,"count"),所有元素严重伤害数 =("伤害",lambda O0OO000000OO000OO :STAT_countpx (O0OO000000OO000OO .values ,"严重伤害")),所有元素死亡数量 =("伤害",lambda O0OOOOOOO00O00000 :STAT_countpx (O0OOOOOOO00O00000 .values ,"死亡")),)#line:5365
			OOOO0O0O00OOO00O0 =pd .merge (OOOO0O0O00OOO00O0 ,O0OO00O0OOO0OOO0O ,on =O000OO0O0OO00O0O0 ,how ="left").reset_index ()#line:5369
		O0OO00O0OOO0OOO0O =O0OO00O0OOO0OOO0O [(O0OO00O0OOO0OOO0O ["所有元素总数量"]>=3 )].reset_index ()#line:5371
		O0OOO00OO0OOO000O =[]#line:5372
		if ("产品名称"not in O0OO00O0OOO0OOO0O .columns )and ("规整后品类"not in O0OO00O0OOO0OOO0O .columns ):#line:5374
			O0OO00O0OOO0OOO0O ["产品名称"]=O0OO00O0OOO0OOO0O ["产品类别"]#line:5375
		if "规整后品类"not in O0OO00O0OOO0OOO0O .columns :#line:5381
			O0OO00O0OOO0OOO0O ["规整后品类"]="不适用"#line:5382
		OO0OO00O000OO000O =0 #line:5385
		OO0OO0O0OO0O00000 =int (len (O0OO00O0OOO0OOO0O ))#line:5386
		for O000O00O0O0000OO0 ,O00OOO00O00OO0000 ,OOO0O00000O000OO0 ,OO0OOO00O0O0000OO in zip (O0OO00O0OOO0OOO0O ["规整后品类"],O0OO00O0OOO0OOO0O ["产品类别"],O0OO00O0OOO0OOO0O [O000O0OO0000O0O0O ],O0OO00O0OOO0OOO0O ["所有元素总数量"]):#line:5387
			OO0OO00O000OO000O +=1 #line:5388
			if (time .time ()-O000OO0O0O00OO0O0 )>3 :#line:5389
				root .attributes ("-topmost",True )#line:5390
				PROGRAM_change_schedule (OO0OO00O000OO000O ,OO0OO0O0OO0O00000 )#line:5391
				root .attributes ("-topmost",False )#line:5392
			OO0OOO0O0O0OOO000 =O000OOO0O00OOOOOO [(O000OOO0O00OOOOOO [O000O0OO0000O0O0O ]==OOO0O00000O000OO0 )].copy ()#line:5393
			O00000O0O00OO0O00 ["SELECT"]=O00000O0O00OO0O00 .apply (lambda OO0O0OOO0O00OOO00 :((O000O00O0O0000OO0 in OO0O0OOO0O00OOO00 ["适用范围"])or (OO0O0OOO0O00OOO00 ["适用范围"]in O00OOO00O00OO0000 )),axis =1 )#line:5394
			O0O0O0O0O0OO0O0OO =O00000O0O00OO0O00 [(O00000O0O00OO0O00 ["SELECT"]==True )].reset_index ()#line:5395
			if len (O0O0O0O0O0OO0O0OO )>0 :#line:5396
				for O00OOOOOOOOO00O0O ,OOO00O00OOOOOOOOO ,OOOOOO00O00OOOO00 in zip (O0O0O0O0O0OO0O0OO ["值"].values ,O0O0O0O0O0OO0O0OO ["查找位置"].values ,O0O0O0O0O0OO0O0OO ["排除值"].values ):#line:5398
					OOOOO0OOOOO0OO0O0 =OO0OOO0O0O0OOO000 .copy ()#line:5399
					OOO000OOO00O0O000 =TOOLS_get_list (O00OOOOOOOOO00O0O )[0 ]#line:5400
					O00OOOOOOO0O0O0OO ="关键字查找列"#line:5401
					OOOOO0OOOOO0OO0O0 [O00OOOOOOO0O0O0OO ]=""#line:5402
					for OO0OO0OOO0OOOOOOO in TOOLS_get_list (OOO00O00OOOOOOOOO ):#line:5403
						OOOOO0OOOOO0OO0O0 [O00OOOOOOO0O0O0OO ]=OOOOO0OOOOO0OO0O0 [O00OOOOOOO0O0O0OO ]+OOOOO0OOOOO0OO0O0 [OO0OO0OOO0OOOOOOO ].astype ("str")#line:5404
					OOOOO0OOOOO0OO0O0 .loc [OOOOO0OOOOO0OO0O0 [O00OOOOOOO0O0O0OO ].str .contains (O00OOOOOOOOO00O0O ,na =False ),"关键字"]=OOO000OOO00O0O000 #line:5406
					if str (OOOOOO00O00OOOO00 )!="nan":#line:5409
						OOOOO0OOOOO0OO0O0 =OOOOO0OOOOO0OO0O0 .loc [~OOOOO0OOOOO0OO0O0 ["关键字查找列"].str .contains (OOOOOO00O00OOOO00 ,na =False )].copy ()#line:5410
					if (len (OOOOO0OOOOO0OO0O0 ))<1 :#line:5413
						continue #line:5414
					for OOOOOOO00O000O0OO in zip (OOOOO0OOOOO0OO0O0 [OO00O0OOOO0000O0O ].drop_duplicates ()):#line:5416
						try :#line:5419
							if OOOOOOO00O000O0OO [0 ]!=O000OO000O0OO0OOO [1 ]:#line:5420
								continue #line:5421
						except :#line:5422
							pass #line:5423
						O0OOO0OO000O0O0OO ={"合并列":{O00OOOOOOO0O0O0OO :OOO00O00OOOOOOOOO },"等于":{O000O0OO0000O0O0O :OOO0O00000O000OO0 ,OO00O0OOOO0000O0O :OOOOOOO00O000O0OO [0 ]},"不等于":{},"包含":{O00OOOOOOO0O0O0OO :O00OOOOOOOOO00O0O },"不包含":{O00OOOOOOO0O0O0OO :OOOOOO00O00OOOO00 }}#line:5431
						O0O0O0OOO000O0OOO =STAT_PPR_ROR_1 (OO00O0OOOO0000O0O ,str (OOOOOOO00O000O0OO [0 ]),"关键字查找列",O00OOOOOOOOO00O0O ,OOOOO0OOOOO0OO0O0 )+(O00OOOOOOOOO00O0O ,OOOOOO00O00OOOO00 ,OOO00O00OOOOOOOOO ,OOO0O00000O000OO0 ,OOOOOOO00O000O0OO [0 ],str (O0OOO0OO000O0O0OO ))#line:5433
						if O0O0O0OOO000O0OOO [1 ]>0 :#line:5435
							OOOO0000000O0OOOO =pd .DataFrame (columns =["特定关键字","出现频次","占比","ROR值","ROR值的95%CI下限","PRR值","PRR值的95%CI下限","卡方值","四分表","关键字组合","排除值","关键字查找列",O000O0OO0000O0O0O ,OO00O0OOOO0000O0O ,"报表定位"])#line:5437
							OOOO0000000O0OOOO .loc [0 ]=O0O0O0OOO000O0OOO #line:5438
							O0OOO00OO0OOO000O .append (OOOO0000000O0OOOO )#line:5439
		OO00OOOO0O0OO0O0O =pd .concat (O0OOO00OO0OOO000O )#line:5443
		OO00OOOO0O0OO0O0O =pd .merge (OOOO0O0O00OOO00O0 ,OO00OOOO0O0OO0O0O ,on =[O000O0OO0000O0O0O ,OO00O0OOOO0000O0O ],how ="right")#line:5447
		OO00OOOO0O0OO0O0O =OO00OOOO0O0OO0O0O .reset_index (drop =True )#line:5448
		del OO00OOOO0O0OO0O0O ["index"]#line:5449
		if len (OO00OOOO0O0OO0O0O )>0 :#line:5450
			OO00OOOO0O0OO0O0O ["风险评分"]=0 #line:5451
			OO00OOOO0O0OO0O0O ["报表类型"]="ROR"#line:5452
			OO00OOOO0O0OO0O0O .loc [(OO00OOOO0O0OO0O0O ["出现频次"]>=3 ),"风险评分"]=OO00OOOO0O0OO0O0O ["风险评分"]+3 #line:5453
			OO00OOOO0O0OO0O0O .loc [(OO00OOOO0O0OO0O0O ["ROR值的95%CI下限"]>1 ),"风险评分"]=OO00OOOO0O0OO0O0O ["风险评分"]+1 #line:5454
			OO00OOOO0O0OO0O0O .loc [(OO00OOOO0O0OO0O0O ["PRR值的95%CI下限"]>1 ),"风险评分"]=OO00OOOO0O0OO0O0O ["风险评分"]+1 #line:5455
			OO00OOOO0O0OO0O0O ["风险评分"]=OO00OOOO0O0OO0O0O ["风险评分"]+OO00OOOO0O0OO0O0O ["该元素单位个数"]/100 #line:5456
			OO00OOOO0O0OO0O0O =OO00OOOO0O0OO0O0O .sort_values (by ="风险评分",ascending =[False ],na_position ="last").reset_index (drop =True )#line:5457
		print ("耗时：",(time .time ()-O000OO0O0O00OO0O0 ))#line:5463
		return OO00OOOO0O0OO0O0O #line:5464
	def df_chiyouren (OOO00O00O000O0OOO ):#line:5470
		""#line:5471
		OO0O0OO0OOOOOOOOO =OOO00O00O000O0OOO .df .copy ().reset_index (drop =True )#line:5472
		OO0O0OO0OOOOOOOOO ["总报告数"]=data ["报告编码"].copy ()#line:5473
		OO0O0OO0OOOOOOOOO .loc [(OO0O0OO0OOOOOOOOO ["持有人报告状态"]=="待评价"),"总待评价数量"]=data ["报告编码"]#line:5474
		OO0O0OO0OOOOOOOOO .loc [(OO0O0OO0OOOOOOOOO ["伤害"]=="严重伤害"),"严重伤害报告数"]=data ["报告编码"]#line:5475
		OO0O0OO0OOOOOOOOO .loc [(OO0O0OO0OOOOOOOOO ["持有人报告状态"]=="待评价")&(OO0O0OO0OOOOOOOOO ["伤害"]=="严重伤害"),"严重伤害待评价数量"]=data ["报告编码"]#line:5476
		OO0O0OO0OOOOOOOOO .loc [(OO0O0OO0OOOOOOOOO ["持有人报告状态"]=="待评价")&(OO0O0OO0OOOOOOOOO ["伤害"]=="其他"),"其他待评价数量"]=data ["报告编码"]#line:5477
		O00OO0OOO0OO0O0OO =OO0O0OO0OOOOOOOOO .groupby (["上市许可持有人名称"]).aggregate ({"总报告数":"nunique","总待评价数量":"nunique","严重伤害报告数":"nunique","严重伤害待评价数量":"nunique","其他待评价数量":"nunique"})#line:5480
		O00OO0OOO0OO0O0OO ["严重伤害待评价比例"]=round (O00OO0OOO0OO0O0OO ["严重伤害待评价数量"]/O00OO0OOO0OO0O0OO ["严重伤害报告数"]*100 ,2 )#line:5485
		O00OO0OOO0OO0O0OO ["总待评价比例"]=round (O00OO0OOO0OO0O0OO ["总待评价数量"]/O00OO0OOO0OO0O0OO ["总报告数"]*100 ,2 )#line:5488
		O00OO0OOO0OO0O0OO ["总报告数"]=O00OO0OOO0OO0O0OO ["总报告数"].fillna (0 )#line:5489
		O00OO0OOO0OO0O0OO ["总待评价比例"]=O00OO0OOO0OO0O0OO ["总待评价比例"].fillna (0 )#line:5490
		O00OO0OOO0OO0O0OO ["严重伤害报告数"]=O00OO0OOO0OO0O0OO ["严重伤害报告数"].fillna (0 )#line:5491
		O00OO0OOO0OO0O0OO ["严重伤害待评价比例"]=O00OO0OOO0OO0O0OO ["严重伤害待评价比例"].fillna (0 )#line:5492
		O00OO0OOO0OO0O0OO ["总报告数"]=O00OO0OOO0OO0O0OO ["总报告数"].astype (int )#line:5493
		O00OO0OOO0OO0O0OO ["总待评价比例"]=O00OO0OOO0OO0O0OO ["总待评价比例"].astype (int )#line:5494
		O00OO0OOO0OO0O0OO ["严重伤害报告数"]=O00OO0OOO0OO0O0OO ["严重伤害报告数"].astype (int )#line:5495
		O00OO0OOO0OO0O0OO ["严重伤害待评价比例"]=O00OO0OOO0OO0O0OO ["严重伤害待评价比例"].astype (int )#line:5496
		O00OO0OOO0OO0O0OO =O00OO0OOO0OO0O0OO .sort_values (by =["总报告数","总待评价比例"],ascending =[False ,False ],na_position ="last")#line:5499
		if "场所名称"in OO0O0OO0OOOOOOOOO .columns :#line:5501
			OO0O0OO0OOOOOOOOO .loc [(OO0O0OO0OOOOOOOOO ["审核日期"]=="未填写"),"审核日期"]=3000 -12 -12 #line:5502
			OO0O0OO0OOOOOOOOO ["报告时限"]=pd .Timestamp .today ()-pd .to_datetime (OO0O0OO0OOOOOOOOO ["审核日期"])#line:5503
			OO0O0OO0OOOOOOOOO ["报告时限2"]=45 -(pd .Timestamp .today ()-pd .to_datetime (OO0O0OO0OOOOOOOOO ["审核日期"])).dt .days #line:5504
			OO0O0OO0OOOOOOOOO ["报告时限"]=OO0O0OO0OOOOOOOOO ["报告时限"].dt .days #line:5505
			OO0O0OO0OOOOOOOOO .loc [(OO0O0OO0OOOOOOOOO ["报告时限"]>45 )&(OO0O0OO0OOOOOOOOO ["伤害"]=="严重伤害")&(OO0O0OO0OOOOOOOOO ["持有人报告状态"]=="待评价"),"待评价且超出当前日期45天（严重）"]=1 #line:5506
			OO0O0OO0OOOOOOOOO .loc [(OO0O0OO0OOOOOOOOO ["报告时限"]>45 )&(OO0O0OO0OOOOOOOOO ["伤害"]=="其他")&(OO0O0OO0OOOOOOOOO ["持有人报告状态"]=="待评价"),"待评价且超出当前日期45天（其他）"]=1 #line:5507
			OO0O0OO0OOOOOOOOO .loc [(OO0O0OO0OOOOOOOOO ["报告时限"]>30 )&(OO0O0OO0OOOOOOOOO ["伤害"]=="死亡")&(OO0O0OO0OOOOOOOOO ["持有人报告状态"]=="待评价"),"待评价且超出当前日期30天（死亡）"]=1 #line:5508
			OO0O0OO0OOOOOOOOO .loc [(OO0O0OO0OOOOOOOOO ["报告时限2"]<=1 )&(OO0O0OO0OOOOOOOOO ["伤害"]=="严重伤害")&(OO0O0OO0OOOOOOOOO ["报告时限2"]>0 )&(OO0O0OO0OOOOOOOOO ["持有人报告状态"]=="待评价"),"严重待评价且只剩1天"]=1 #line:5510
			OO0O0OO0OOOOOOOOO .loc [(OO0O0OO0OOOOOOOOO ["报告时限2"]>1 )&(OO0O0OO0OOOOOOOOO ["报告时限2"]<=3 )&(OO0O0OO0OOOOOOOOO ["伤害"]=="严重伤害")&(OO0O0OO0OOOOOOOOO ["持有人报告状态"]=="待评价"),"严重待评价且只剩1-3天"]=1 #line:5511
			OO0O0OO0OOOOOOOOO .loc [(OO0O0OO0OOOOOOOOO ["报告时限2"]>3 )&(OO0O0OO0OOOOOOOOO ["报告时限2"]<=5 )&(OO0O0OO0OOOOOOOOO ["伤害"]=="严重伤害")&(OO0O0OO0OOOOOOOOO ["持有人报告状态"]=="待评价"),"严重待评价且只剩3-5天"]=1 #line:5512
			OO0O0OO0OOOOOOOOO .loc [(OO0O0OO0OOOOOOOOO ["报告时限2"]>5 )&(OO0O0OO0OOOOOOOOO ["报告时限2"]<=10 )&(OO0O0OO0OOOOOOOOO ["伤害"]=="严重伤害")&(OO0O0OO0OOOOOOOOO ["持有人报告状态"]=="待评价"),"严重待评价且只剩5-10天"]=1 #line:5513
			OO0O0OO0OOOOOOOOO .loc [(OO0O0OO0OOOOOOOOO ["报告时限2"]>10 )&(OO0O0OO0OOOOOOOOO ["报告时限2"]<=20 )&(OO0O0OO0OOOOOOOOO ["伤害"]=="严重伤害")&(OO0O0OO0OOOOOOOOO ["持有人报告状态"]=="待评价"),"严重待评价且只剩10-20天"]=1 #line:5514
			OO0O0OO0OOOOOOOOO .loc [(OO0O0OO0OOOOOOOOO ["报告时限2"]>20 )&(OO0O0OO0OOOOOOOOO ["报告时限2"]<=30 )&(OO0O0OO0OOOOOOOOO ["伤害"]=="严重伤害")&(OO0O0OO0OOOOOOOOO ["持有人报告状态"]=="待评价"),"严重待评价且只剩20-30天"]=1 #line:5515
			OO0O0OO0OOOOOOOOO .loc [(OO0O0OO0OOOOOOOOO ["报告时限2"]>30 )&(OO0O0OO0OOOOOOOOO ["报告时限2"]<=45 )&(OO0O0OO0OOOOOOOOO ["伤害"]=="严重伤害")&(OO0O0OO0OOOOOOOOO ["持有人报告状态"]=="待评价"),"严重待评价且只剩30-45天"]=1 #line:5516
			del OO0O0OO0OOOOOOOOO ["报告时限2"]#line:5517
			OOOO0OO00O00000OO =(OO0O0OO0OOOOOOOOO .groupby (["上市许可持有人名称"]).aggregate ({"待评价且超出当前日期45天（严重）":"sum","待评价且超出当前日期45天（其他）":"sum","待评价且超出当前日期30天（死亡）":"sum","严重待评价且只剩1天":"sum","严重待评价且只剩1-3天":"sum","严重待评价且只剩3-5天":"sum","严重待评价且只剩5-10天":"sum","严重待评价且只剩10-20天":"sum","严重待评价且只剩20-30天":"sum","严重待评价且只剩30-45天":"sum"}).reset_index ())#line:5519
			O00OO0OOO0OO0O0OO =pd .merge (O00OO0OOO0OO0O0OO ,OOOO0OO00O00000OO ,on =["上市许可持有人名称"],how ="outer",)#line:5520
			O00OO0OOO0OO0O0OO ["待评价且超出当前日期45天（严重）"]=O00OO0OOO0OO0O0OO ["待评价且超出当前日期45天（严重）"].fillna (0 )#line:5521
			O00OO0OOO0OO0O0OO ["待评价且超出当前日期45天（严重）"]=O00OO0OOO0OO0O0OO ["待评价且超出当前日期45天（严重）"].astype (int )#line:5522
			O00OO0OOO0OO0O0OO ["待评价且超出当前日期45天（其他）"]=O00OO0OOO0OO0O0OO ["待评价且超出当前日期45天（其他）"].fillna (0 )#line:5523
			O00OO0OOO0OO0O0OO ["待评价且超出当前日期45天（其他）"]=O00OO0OOO0OO0O0OO ["待评价且超出当前日期45天（其他）"].astype (int )#line:5524
			O00OO0OOO0OO0O0OO ["待评价且超出当前日期30天（死亡）"]=O00OO0OOO0OO0O0OO ["待评价且超出当前日期30天（死亡）"].fillna (0 )#line:5525
			O00OO0OOO0OO0O0OO ["待评价且超出当前日期30天（死亡）"]=O00OO0OOO0OO0O0OO ["待评价且超出当前日期30天（死亡）"].astype (int )#line:5526
			O00OO0OOO0OO0O0OO ["严重待评价且只剩1天"]=O00OO0OOO0OO0O0OO ["严重待评价且只剩1天"].fillna (0 )#line:5528
			O00OO0OOO0OO0O0OO ["严重待评价且只剩1天"]=O00OO0OOO0OO0O0OO ["严重待评价且只剩1天"].astype (int )#line:5529
			O00OO0OOO0OO0O0OO ["严重待评价且只剩1-3天"]=O00OO0OOO0OO0O0OO ["严重待评价且只剩1-3天"].fillna (0 )#line:5530
			O00OO0OOO0OO0O0OO ["严重待评价且只剩1-3天"]=O00OO0OOO0OO0O0OO ["严重待评价且只剩1-3天"].astype (int )#line:5531
			O00OO0OOO0OO0O0OO ["严重待评价且只剩3-5天"]=O00OO0OOO0OO0O0OO ["严重待评价且只剩3-5天"].fillna (0 )#line:5532
			O00OO0OOO0OO0O0OO ["严重待评价且只剩3-5天"]=O00OO0OOO0OO0O0OO ["严重待评价且只剩3-5天"].astype (int )#line:5533
			O00OO0OOO0OO0O0OO ["严重待评价且只剩5-10天"]=O00OO0OOO0OO0O0OO ["严重待评价且只剩5-10天"].fillna (0 )#line:5534
			O00OO0OOO0OO0O0OO ["严重待评价且只剩5-10天"]=O00OO0OOO0OO0O0OO ["严重待评价且只剩5-10天"].astype (int )#line:5535
			O00OO0OOO0OO0O0OO ["严重待评价且只剩10-20天"]=O00OO0OOO0OO0O0OO ["严重待评价且只剩10-20天"].fillna (0 )#line:5536
			O00OO0OOO0OO0O0OO ["严重待评价且只剩10-20天"]=O00OO0OOO0OO0O0OO ["严重待评价且只剩10-20天"].astype (int )#line:5537
			O00OO0OOO0OO0O0OO ["严重待评价且只剩20-30天"]=O00OO0OOO0OO0O0OO ["严重待评价且只剩20-30天"].fillna (0 )#line:5538
			O00OO0OOO0OO0O0OO ["严重待评价且只剩20-30天"]=O00OO0OOO0OO0O0OO ["严重待评价且只剩20-30天"].astype (int )#line:5539
			O00OO0OOO0OO0O0OO ["严重待评价且只剩30-45天"]=O00OO0OOO0OO0O0OO ["严重待评价且只剩30-45天"].fillna (0 )#line:5540
			O00OO0OOO0OO0O0OO ["严重待评价且只剩30-45天"]=O00OO0OOO0OO0O0OO ["严重待评价且只剩30-45天"].astype (int )#line:5541
		O00OO0OOO0OO0O0OO ["总待评价数量"]=O00OO0OOO0OO0O0OO ["总待评价数量"].fillna (0 )#line:5543
		O00OO0OOO0OO0O0OO ["总待评价数量"]=O00OO0OOO0OO0O0OO ["总待评价数量"].astype (int )#line:5544
		O00OO0OOO0OO0O0OO ["严重伤害待评价数量"]=O00OO0OOO0OO0O0OO ["严重伤害待评价数量"].fillna (0 )#line:5545
		O00OO0OOO0OO0O0OO ["严重伤害待评价数量"]=O00OO0OOO0OO0O0OO ["严重伤害待评价数量"].astype (int )#line:5546
		O00OO0OOO0OO0O0OO ["其他待评价数量"]=O00OO0OOO0OO0O0OO ["其他待评价数量"].fillna (0 )#line:5547
		O00OO0OOO0OO0O0OO ["其他待评价数量"]=O00OO0OOO0OO0O0OO ["其他待评价数量"].astype (int )#line:5548
		O0O0O00OO00O00OOO =["总报告数","总待评价数量","严重伤害报告数","严重伤害待评价数量","其他待评价数量"]#line:5551
		O00OO0OOO0OO0O0OO .loc ["合计"]=O00OO0OOO0OO0O0OO [O0O0O00OO00O00OOO ].apply (lambda O0O0O00000O00OOO0 :O0O0O00000O00OOO0 .sum ())#line:5552
		O00OO0OOO0OO0O0OO [O0O0O00OO00O00OOO ]=O00OO0OOO0OO0O0OO [O0O0O00OO00O00OOO ].apply (lambda OOO0O00O00O0OOOOO :OOO0O00O00O0OOOOO .astype (int ))#line:5553
		O00OO0OOO0OO0O0OO .iloc [-1 ,0 ]="合计"#line:5554
		if "场所名称"in OO0O0OO0OOOOOOOOO .columns :#line:5556
			O00OO0OOO0OO0O0OO =O00OO0OOO0OO0O0OO .reset_index (drop =True )#line:5557
		else :#line:5558
			O00OO0OOO0OO0O0OO =O00OO0OOO0OO0O0OO .reset_index ()#line:5559
		if ini ["模式"]=="药品":#line:5561
			O00OO0OOO0OO0O0OO =O00OO0OOO0OO0O0OO .rename (columns ={"总待评价数量":"新的数量"})#line:5562
			O00OO0OOO0OO0O0OO =O00OO0OOO0OO0O0OO .rename (columns ={"严重伤害待评价数量":"新的严重的数量"})#line:5563
			O00OO0OOO0OO0O0OO =O00OO0OOO0OO0O0OO .rename (columns ={"严重伤害待评价比例":"新的严重的比例"})#line:5564
			O00OO0OOO0OO0O0OO =O00OO0OOO0OO0O0OO .rename (columns ={"总待评价比例":"新的比例"})#line:5565
			del O00OO0OOO0OO0O0OO ["其他待评价数量"]#line:5567
		O00OO0OOO0OO0O0OO ["报表类型"]="dfx_chiyouren"#line:5568
		return O00OO0OOO0OO0O0OO #line:5569
	def df_age (OOO0OO00OOOO0O00O ):#line:5571
		""#line:5572
		O00OOOO0OOOOO0O0O =OOO0OO00OOOO0O00O .df .copy ()#line:5573
		O00OOOO0OOOOO0O0O =O00OOOO0OOOOO0O0O .drop_duplicates ("报告编码").copy ()#line:5574
		O0OOO000000OOOO00 =pd .pivot_table (O00OOOO0OOOOO0O0O .drop_duplicates ("报告编码"),values =["报告编码"],index ="年龄段",columns ="性别",aggfunc ={"报告编码":"nunique"},fill_value ="0",margins =True ,dropna =False ,).rename (columns ={"报告编码":"数量"}).reset_index ()#line:5575
		O0OOO000000OOOO00 .columns =O0OOO000000OOOO00 .columns .droplevel (0 )#line:5576
		O0OOO000000OOOO00 ["构成比(%)"]=round (100 *O0OOO000000OOOO00 ["All"]/len (O00OOOO0OOOOO0O0O ),2 )#line:5577
		O0OOO000000OOOO00 ["累计构成比(%)"]=O0OOO000000OOOO00 ["构成比(%)"].cumsum ()#line:5578
		O0OOO000000OOOO00 ["报表类型"]="年龄性别表"#line:5579
		return O0OOO000000OOOO00 #line:5580
	def df_psur (OO00OO0O0O00O0O00 ,*OOOO0O00O0OO000O0 ):#line:5582
		""#line:5583
		OOOO0000O000OO0O0 =OO00OO0O0O00O0O00 .df .copy ()#line:5584
		O0O000O0O00O00OOO =peizhidir +"0（范例）比例失衡关键字库.xls"#line:5585
		O0000OO0O000000OO =len (OOOO0000O000OO0O0 .drop_duplicates ("报告编码"))#line:5586
		if "报告类型-新的"in OOOO0000O000OO0O0 .columns :#line:5590
			OO000OO00OO0OO00O ="药品"#line:5591
		elif "皮损形态"in OOOO0000O000OO0O0 .columns :#line:5592
			OO000OO00OO0OO00O ="化妆品"#line:5593
		else :#line:5594
			OO000OO00OO0OO00O ="器械"#line:5595
		O0O0OO00O0O00OOOO =pd .read_excel (O0O000O0O00O00OOO ,header =0 ,sheet_name =OO000OO00OO0OO00O )#line:5598
		O0O000OO0O000O00O =(O0O0OO00O0O00OOOO .loc [O0O0OO00O0O00OOOO ["适用范围"].str .contains ("通用监测关键字|无源|有源",na =False )].copy ().reset_index (drop =True ))#line:5601
		try :#line:5604
			if OOOO0O00O0OO000O0 [0 ]in ["特定品种","通用无源","通用有源"]:#line:5605
				O00O00OOO00OOO0O0 =""#line:5606
				if OOOO0O00O0OO000O0 [0 ]=="特定品种":#line:5607
					O00O00OOO00OOO0O0 =O0O0OO00O0O00OOOO .loc [O0O0OO00O0O00OOOO ["适用范围"].str .contains (OOOO0O00O0OO000O0 [1 ],na =False )].copy ().reset_index (drop =True )#line:5608
				if OOOO0O00O0OO000O0 [0 ]=="通用无源":#line:5610
					O00O00OOO00OOO0O0 =O0O0OO00O0O00OOOO .loc [O0O0OO00O0O00OOOO ["适用范围"].str .contains ("通用监测关键字|无源",na =False )].copy ().reset_index (drop =True )#line:5611
				if OOOO0O00O0OO000O0 [0 ]=="通用有源":#line:5612
					O00O00OOO00OOO0O0 =O0O0OO00O0O00OOOO .loc [O0O0OO00O0O00OOOO ["适用范围"].str .contains ("通用监测关键字|有源",na =False )].copy ().reset_index (drop =True )#line:5613
				if OOOO0O00O0OO000O0 [0 ]=="体外诊断试剂":#line:5614
					O00O00OOO00OOO0O0 =O0O0OO00O0O00OOOO .loc [O0O0OO00O0O00OOOO ["适用范围"].str .contains ("体外诊断试剂",na =False )].copy ().reset_index (drop =True )#line:5615
				if len (O00O00OOO00OOO0O0 )<1 :#line:5616
					showinfo (title ="提示",message ="未找到相应的自定义规则，任务结束。")#line:5617
					return 0 #line:5618
				else :#line:5619
					O0O000OO0O000O00O =O00O00OOO00OOO0O0 #line:5620
		except :#line:5622
			pass #line:5623
		try :#line:5627
			if OO000OO00OO0OO00O =="器械"and OOOO0O00O0OO000O0 [0 ]=="特定品种作为通用关键字":#line:5628
				O0O000OO0O000O00O =OOOO0O00O0OO000O0 [1 ]#line:5629
		except dddd :#line:5631
			pass #line:5632
		OO000O0OO0O0000OO =""#line:5635
		O00OOO000OOOO00OO ="-其他关键字-不含："#line:5636
		for OO0O0000O0000O000 ,OOO0O00O0O0O00O00 in O0O000OO0O000O00O .iterrows ():#line:5637
			O00OOO000OOOO00OO =O00OOO000OOOO00OO +"|"+str (OOO0O00O0O0O00O00 ["值"])#line:5638
			OOO0O0OO0O0O00OO0 =OOO0O00O0O0O00O00 #line:5639
		OOO0O0OO0O0O00OO0 [2 ]="通用监测关键字"#line:5640
		OOO0O0OO0O0O00OO0 [4 ]=O00OOO000OOOO00OO #line:5641
		O0O000OO0O000O00O .loc [len (O0O000OO0O000O00O )]=OOO0O0OO0O0O00OO0 #line:5642
		O0O000OO0O000O00O =O0O000OO0O000O00O .reset_index (drop =True )#line:5643
		if ini ["模式"]=="器械":#line:5647
			OOOO0000O000OO0O0 ["关键字查找列"]=OOOO0000O000OO0O0 ["器械故障表现"].astype (str )+OOOO0000O000OO0O0 ["伤害表现"].astype (str )+OOOO0000O000OO0O0 ["使用过程"].astype (str )+OOOO0000O000OO0O0 ["事件原因分析描述"].astype (str )+OOOO0000O000OO0O0 ["初步处置情况"].astype (str )#line:5648
		else :#line:5649
			OOOO0000O000OO0O0 ["关键字查找列"]=OOOO0000O000OO0O0 ["器械故障表现"]#line:5650
		text .insert (END ,"\n药品查找列默认为不良反应表现,药品规则默认为通用规则。\n器械默认查找列为器械故障表现+伤害表现+使用过程+事件原因分析描述+初步处置情况，器械默认规则为无源通用规则+有源通用规则。\n")#line:5651
		O0OOO0OO000OO0O00 =[]#line:5653
		for OO0O0000O0000O000 ,OOO0O00O0O0O00O00 in O0O000OO0O000O00O .iterrows ():#line:5655
			OOO0O00O00OO00000 =OOO0O00O0O0O00O00 ["值"]#line:5656
			if "-其他关键字-"not in OOO0O00O00OO00000 :#line:5658
				OOO0OOO0OO00OO0OO =OOOO0000O000OO0O0 .loc [OOOO0000O000OO0O0 ["关键字查找列"].str .contains (OOO0O00O00OO00000 ,na =False )].copy ()#line:5661
				if str (OOO0O00O0O0O00O00 ["排除值"])!="nan":#line:5662
					OOO0OOO0OO00OO0OO =OOO0OOO0OO00OO0OO .loc [~OOO0OOO0OO00OO0OO ["关键字查找列"].str .contains (str (OOO0O00O0O0O00O00 ["排除值"]),na =False )].copy ()#line:5664
			else :#line:5666
				OOO0OOO0OO00OO0OO =OOOO0000O000OO0O0 .loc [~OOOO0000O000OO0O0 ["关键字查找列"].str .contains (OOO0O00O00OO00000 ,na =False )].copy ()#line:5669
			OOO0OOO0OO00OO0OO ["关键字标记"]=str (OOO0O00O00OO00000 )#line:5670
			OOO0OOO0OO00OO0OO ["关键字计数"]=1 #line:5671
			if len (OOO0OOO0OO00OO0OO )>0 :#line:5677
				try :#line:5678
					O000OO0O000O00O0O =pd .pivot_table (OOO0OOO0OO00OO0OO .drop_duplicates ("报告编码"),values =["关键字计数"],index ="关键字标记",columns ="伤害PSUR",aggfunc ={"关键字计数":"count"},fill_value ="0",margins =True ,dropna =False ,)#line:5688
				except :#line:5690
					O000OO0O000O00O0O =pd .pivot_table (OOO0OOO0OO00OO0OO .drop_duplicates ("报告编码"),values =["关键字计数"],index ="关键字标记",columns ="伤害",aggfunc ={"关键字计数":"count"},fill_value ="0",margins =True ,dropna =False ,)#line:5700
				O000OO0O000O00O0O =O000OO0O000O00O0O [:-1 ]#line:5701
				O000OO0O000O00O0O .columns =O000OO0O000O00O0O .columns .droplevel (0 )#line:5702
				O000OO0O000O00O0O =O000OO0O000O00O0O .reset_index ()#line:5703
				if len (O000OO0O000O00O0O )>0 :#line:5706
					O000OOOO0O0OOOO00 =str (Counter (TOOLS_get_list0 ("use(器械故障表现).file",OOO0OOO0OO00OO0OO ,1000 ))).replace ("Counter({","{")#line:5707
					O000OOOO0O0OOOO00 =O000OOOO0O0OOOO00 .replace ("})","}")#line:5708
					O000OOOO0O0OOOO00 =ast .literal_eval (O000OOOO0O0OOOO00 )#line:5709
					O000OO0O000O00O0O .loc [0 ,"事件分类"]=str (TOOLS_get_list (O000OO0O000O00O0O .loc [0 ,"关键字标记"])[0 ])#line:5711
					O0OOOOOO00OO00000 ={O00OOO00OO0000O0O :OOO0OO0O0OOO000OO for O00OOO00OO0000O0O ,OOO0OO0O0OOO000OO in O000OOOO0O0OOOO00 .items ()if STAT_judge_x (str (O00OOO00OO0000O0O ),TOOLS_get_list (OOO0O00O00OO00000 ))==1 }#line:5712
					O000OO0O000O00O0O .loc [0 ,"该类别不良事件计数"]=str (O0OOOOOO00OO00000 )#line:5714
					O0OO00O0O000O0OOO ={O0O0OO0O00OOO0000 :O000OO0OOO0O00OOO for O0O0OO0O00OOO0000 ,O000OO0OOO0O00OOO in O000OOOO0O0OOOO00 .items ()if STAT_judge_x (str (O0O0OO0O00OOO0000 ),TOOLS_get_list (OOO0O00O00OO00000 ))!=1 }#line:5715
					O000OO0O000O00O0O .loc [0 ,"同时存在的其他类别不良事件计数"]=str (O0OO00O0O000O0OOO )#line:5716
					if "-其他关键字-"in str (OOO0O00O00OO00000 ):#line:5718
						O0OOOOOO00OO00000 =O0OO00O0O000O0OOO #line:5719
						O000OO0O000O00O0O .loc [0 ,"该类别不良事件计数"]=O000OO0O000O00O0O .loc [0 ,"同时存在的其他类别不良事件计数"]#line:5720
					O000OO0O000O00O0O .loc [0 ,"不良事件总例次"]=str (sum (O0OOOOOO00OO00000 .values ()))#line:5722
					if ini ["模式"]=="药品":#line:5732
						for O0O0OO0O00O00O0OO in ["SOC","HLGT","HLT","PT"]:#line:5733
							O000OO0O000O00O0O [O0O0OO0O00O00O0OO ]=OOO0O00O0O0O00O00 [O0O0OO0O00O00O0OO ]#line:5734
					if ini ["模式"]=="器械":#line:5735
						for O0O0OO0O00O00O0OO in ["国家故障术语集（大类）","国家故障术语集（小类）","IMDRF有关术语（故障）","国家伤害术语集（大类）","国家伤害术语集（小类）","IMDRF有关术语（伤害）"]:#line:5736
							O000OO0O000O00O0O [O0O0OO0O00O00O0OO ]=OOO0O00O0O0O00O00 [O0O0OO0O00O00O0OO ]#line:5737
					O0OOO0OO000OO0O00 .append (O000OO0O000O00O0O )#line:5740
		OO000O0OO0O0000OO =pd .concat (O0OOO0OO000OO0O00 )#line:5741
		OO000O0OO0O0000OO =OO000O0OO0O0000OO .sort_values (by =["All"],ascending =[False ],na_position ="last")#line:5746
		OO000O0OO0O0000OO =OO000O0OO0O0000OO .reset_index ()#line:5747
		OO000O0OO0O0000OO ["All占比"]=round (OO000O0OO0O0000OO ["All"]/O0000OO0O000000OO *100 ,2 )#line:5749
		OO000O0OO0O0000OO =OO000O0OO0O0000OO .rename (columns ={"All":"总数量","All占比":"总数量占比"})#line:5750
		try :#line:5751
			OO000O0OO0O0000OO =OO000O0OO0O0000OO .rename (columns ={"其他":"一般"})#line:5752
		except :#line:5753
			pass #line:5754
		try :#line:5756
			OO000O0OO0O0000OO =OO000O0OO0O0000OO .rename (columns ={" 一般":"一般"})#line:5757
		except :#line:5758
			pass #line:5759
		try :#line:5760
			OO000O0OO0O0000OO =OO000O0OO0O0000OO .rename (columns ={" 严重":"严重"})#line:5761
		except :#line:5762
			pass #line:5763
		try :#line:5764
			OO000O0OO0O0000OO =OO000O0OO0O0000OO .rename (columns ={"严重伤害":"严重"})#line:5765
		except :#line:5766
			pass #line:5767
		try :#line:5768
			OO000O0OO0O0000OO =OO000O0OO0O0000OO .rename (columns ={"死亡":"死亡(仅支持器械)"})#line:5769
		except :#line:5770
			pass #line:5771
		for O000O00OOO00OOOOO in ["一般","新的一般","严重","新的严重"]:#line:5774
			if O000O00OOO00OOOOO not in OO000O0OO0O0000OO .columns :#line:5775
				OO000O0OO0O0000OO [O000O00OOO00OOOOO ]=0 #line:5776
		try :#line:5778
			OO000O0OO0O0000OO ["严重比"]=round ((OO000O0OO0O0000OO ["严重"].fillna (0 )+OO000O0OO0O0000OO ["死亡(仅支持器械)"].fillna (0 ))/OO000O0OO0O0000OO ["总数量"]*100 ,2 )#line:5779
		except :#line:5780
			OO000O0OO0O0000OO ["严重比"]=round ((OO000O0OO0O0000OO ["严重"].fillna (0 )+OO000O0OO0O0000OO ["新的严重"].fillna (0 ))/OO000O0OO0O0000OO ["总数量"]*100 ,2 )#line:5781
		OO000O0OO0O0000OO ["构成比"]=round ((OO000O0OO0O0000OO ["不良事件总例次"].astype (float ).fillna (0 ))/OO000O0OO0O0000OO ["不良事件总例次"].astype (float ).sum ()*100 ,2 )#line:5783
		if ini ["模式"]=="药品":#line:5785
			try :#line:5786
				OO000O0OO0O0000OO =OO000O0OO0O0000OO [["关键字标记","一般","新的一般","严重","新的严重","总数量","总数量占比","严重比","事件分类","不良事件总例次","构成比","该类别不良事件计数","同时存在的其他类别不良事件计数","死亡(仅支持器械)","SOC","HLGT","HLT","PT"]]#line:5787
			except :#line:5788
				OO000O0OO0O0000OO =OO000O0OO0O0000OO [["关键字标记","一般","新的一般","严重","新的严重","总数量","总数量占比","严重比","事件分类","不良事件总例次","构成比","该类别不良事件计数","同时存在的其他类别不良事件计数","SOC","HLGT","HLT","PT"]]#line:5789
		elif ini ["模式"]=="器械":#line:5790
			try :#line:5791
				OO000O0OO0O0000OO =OO000O0OO0O0000OO [["关键字标记","一般","新的一般","严重","新的严重","总数量","总数量占比","严重比","事件分类","不良事件总例次","构成比","该类别不良事件计数","同时存在的其他类别不良事件计数","死亡(仅支持器械)","国家故障术语集（大类）","国家故障术语集（小类）","IMDRF有关术语（故障）","国家伤害术语集（大类）","国家伤害术语集（小类）","IMDRF有关术语（伤害）"]]#line:5792
			except :#line:5793
				OO000O0OO0O0000OO =OO000O0OO0O0000OO [["关键字标记","一般","新的一般","严重","新的严重","总数量","总数量占比","严重比","事件分类","不良事件总例次","构成比","该类别不良事件计数","同时存在的其他类别不良事件计数","国家故障术语集（大类）","国家故障术语集（小类）","IMDRF有关术语（故障）","国家伤害术语集（大类）","国家伤害术语集（小类）","IMDRF有关术语（伤害）"]]#line:5794
		else :#line:5796
			try :#line:5797
				OO000O0OO0O0000OO =OO000O0OO0O0000OO [["关键字标记","一般","新的一般","严重","新的严重","总数量","总数量占比","严重比","事件分类","不良事件总例次","构成比","该类别不良事件计数","同时存在的其他类别不良事件计数","死亡(仅支持器械)"]]#line:5798
			except :#line:5799
				OO000O0OO0O0000OO =OO000O0OO0O0000OO [["关键字标记","一般","新的一般","严重","新的严重","总数量","总数量占比","严重比","事件分类","不良事件总例次","构成比","该类别不良事件计数","同时存在的其他类别不良事件计数"]]#line:5800
		for OO000O00O0000OOO0 ,O00OO0O000O000O00 in O0O000OO0O000O00O .iterrows ():#line:5802
			OO000O0OO0O0000OO .loc [(OO000O0OO0O0000OO ["关键字标记"].astype (str )==str (O00OO0O000O000O00 ["值"])),"排除值"]=O00OO0O000O000O00 ["排除值"]#line:5803
		OO000O0OO0O0000OO ["排除值"]=OO000O0OO0O0000OO ["排除值"].fillna ("没有排除值")#line:5805
		for O00O0OO0OOOO00O0O in ["一般","新的一般","严重","新的严重","总数量","总数量占比","严重比"]:#line:5809
			OO000O0OO0O0000OO [O00O0OO0OOOO00O0O ]=OO000O0OO0O0000OO [O00O0OO0OOOO00O0O ].fillna (0 )#line:5810
		for O00O0OO0OOOO00O0O in ["一般","新的一般","严重","新的严重","总数量"]:#line:5812
			OO000O0OO0O0000OO [O00O0OO0OOOO00O0O ]=OO000O0OO0O0000OO [O00O0OO0OOOO00O0O ].astype (int )#line:5813
		OO000O0OO0O0000OO ["RPN"]="未定义"#line:5816
		OO000O0OO0O0000OO ["故障原因"]="未定义"#line:5817
		OO000O0OO0O0000OO ["可造成的伤害"]="未定义"#line:5818
		OO000O0OO0O0000OO ["应采取的措施"]="未定义"#line:5819
		OO000O0OO0O0000OO ["发生率"]="未定义"#line:5820
		OO000O0OO0O0000OO ["报表类型"]="PSUR"#line:5822
		return OO000O0OO0O0000OO #line:5823
def A0000_Main ():#line:5833
	print ("")#line:5834
if __name__ =='__main__':#line:5836
	root =Tk .Tk ()#line:5839
	root .title (title_all )#line:5840
	try :#line:5841
		root .iconphoto (True ,PhotoImage (file =peizhidir +"0（范例）ico.png"))#line:5842
	except :#line:5843
		pass #line:5844
	sw_root =root .winfo_screenwidth ()#line:5845
	sh_root =root .winfo_screenheight ()#line:5847
	ww_root =700 #line:5849
	wh_root =620 #line:5850
	x_root =(sw_root -ww_root )/2 #line:5852
	y_root =(sh_root -wh_root )/2 #line:5853
	root .geometry ("%dx%d+%d+%d"%(ww_root ,wh_root ,x_root ,y_root ))#line:5854
	framecanvas =Frame (root )#line:5859
	canvas =Canvas (framecanvas ,width =680 ,height =30 )#line:5860
	canvas .pack ()#line:5861
	x =StringVar ()#line:5862
	out_rec =canvas .create_rectangle (5 ,5 ,680 ,25 ,outline ="silver",width =1 )#line:5863
	fill_rec =canvas .create_rectangle (5 ,5 ,5 ,25 ,outline ="",width =0 ,fill ="silver")#line:5864
	canvas .create_text (350 ,15 ,text ="总执行进度")#line:5865
	framecanvas .pack ()#line:5866
	try :#line:5873
		frame0 =ttk .Frame (root ,width =90 ,height =20 )#line:5874
		frame0 .pack (side =LEFT )#line:5875
		B_open_files1 =Button (frame0 ,text ="导入数据",bg ="white",height =2 ,width =12 ,font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =TOOLS_allfileopen ,)#line:5886
		B_open_files1 .pack ()#line:5887
		B_open_files3 =Button (frame0 ,text ="数据查看",bg ="white",height =2 ,width =12 ,font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :TABLE_tree_Level_2 (ori ,0 ,ori ),)#line:5902
		B_open_files3 .pack ()#line:5903
	except KEY :#line:5906
		pass #line:5907
	text =ScrolledText (root ,height =400 ,width =400 ,bg ="#FFFFFF")#line:5911
	text .pack (padx =5 ,pady =5 )#line:5912
	text .insert (END ,"\n 本程序适用于整理和分析国家医疗器械不良事件信息系统、国家药品不良反应监测系统和国家化妆品不良反应监测系统中导出的监测数据。如您有改进建议，请点击其-意见反馈。\n")#line:5915
	text .insert (END ,"\n\n")#line:5916
	setting_cfg =read_setting_cfg ()#line:5919
	generate_random_file ()#line:5920
	setting_cfg =open_setting_cfg ()#line:5921
	if setting_cfg ["settingdir"]==0 :#line:5922
		showinfo (title ="提示",message ="未发现默认配置文件夹，请选择一个。如该配置文件夹中并无配置文件，将生成默认配置文件。")#line:5923
		filepathu =filedialog .askdirectory ()#line:5924
		path =get_directory_path (filepathu )#line:5925
		update_setting_cfg ("settingdir",path )#line:5926
	setting_cfg =open_setting_cfg ()#line:5927
	random_number =int (setting_cfg ["sidori"])#line:5928
	input_number =int (str (setting_cfg ["sidfinal"])[0 :6 ])#line:5929
	day_end =convert_and_compare_dates (str (setting_cfg ["sidfinal"])[6 :14 ])#line:5930
	sid =random_number *2 +183576 #line:5931
	if input_number ==sid and day_end =="未过期":#line:5932
		usergroup ="用户组=1"#line:5933
		text .insert (END ,usergroup +"   有效期至：")#line:5934
		text .insert (END ,datetime .strptime (str (int (int (str (setting_cfg ["sidfinal"])[6 :14 ])/4 )),"%Y%m%d"))#line:5935
	else :#line:5936
		text .insert (END ,usergroup )#line:5937
	text .insert (END ,"\n配置文件路径："+setting_cfg ["settingdir"]+"\n")#line:5938
	peizhidir =str (setting_cfg ["settingdir"])+csdir .split ("pinggutools")[0 ][-1 ]#line:5939
	roox =Toplevel ()#line:5943
	tMain =threading .Thread (target =PROGRAM_showWelcome )#line:5944
	tMain .start ()#line:5945
	t1 =threading .Thread (target =PROGRAM_closeWelcome )#line:5946
	t1 .start ()#line:5947
	root .lift ()#line:5949
	root .attributes ("-topmost",True )#line:5950
	root .attributes ("-topmost",False )#line:5951
	root .mainloop ()#line:5955
	print ("done.")#line:5956
