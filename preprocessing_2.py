# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
import mojimoji

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

root_path_dataset = "./test.csv"
df = pd.read_csv(root_path_dataset)

#columns = ['最寄駅：距離（分）', '最寄駅：名称', '建築年', '取引時点']
df_kyori = df['最寄駅：距離（分）']

#print "csv 行数 before: ", len(df)
kyori_vec = []

for i in range(0,len(df_kyori)):
    kyori = df_kyori.iloc[i]
    if "分" in kyori:
        cat_kyori = '0'
    elif "?" in kyori:
        cat_kyori = '0'
    else:
        kyori = int(kyori)
        if kyori >=0 and kyori <=3:
            cat_kyori = "1"
        elif kyori>=4 and kyori <=6:
            cat_kyori= "2"
        elif kyori>=7 and kyori <=10:
            cat_kyori = "3"
        else:
            cat_kyori = "4"
    kyori_vec.append(cat_kyori)

# dataframe(もとのCSV file）に対して, 'category_kyori'という名の変数を追加する
# その変数の中身，つまり行の値がkyori_vecに相当するため，それを代入
df['category_kyori'] = kyori_vec
#print df

# 追加されたところから、cat_kyori == '0'のもの，つまり30分以上のものは除外したい
# それを新しいdataframe2として定義する
df2 = df[df['category_kyori'] != '0']

#print "csv 行数 after: ", len(df2)


#平成や昭和を西暦に直す
df_kenchiku = df['建築年']
kenchiku_vec = []
#"平成"="1988+" "昭和"="1925+"

for i in range(0,len(df2)):

	kenchiku = df_kenchiku.iloc[i]
	kenchiku = mojimoji.han_to_zen(unicode(kenchiku))
	kenchiku = kenchiku.replace('年','')
	if "元" in kenchiku:
		kenchiku = kenchiku.replace('元','1')
	else:
		pass
	if "平成" in kenchiku:
		kenchiku = kenchiku.replace('平成','1988')
	elif "昭和" in kenchiku:
		kenchiku = kenchiku.replace('昭和','1925')
	else:
		kenchiku = "-1"

	if kenchiku == "-1":
		kenchiku = -1
	else:
		kenchiku = mojimoji.zen_to_han(unicode(kenchiku))
		kenchiku = 2017 - int(kenchiku[0:4]) - int(kenchiku[4:])
	kenchiku_vec.append(kenchiku)

df2['建築年'] = kenchiku_vec
df3 = df2[df2['建築年'] != -1]
#print df3


#新たに、築20年以上の場合[0]それより下[1]の列を作成

df_kenchiku20 = df3['建築年']
kenchiku20_vec = []

for i in range(0,len(df_kenchiku20)):
	kenchiku20 = df_kenchiku20.iloc[i]
	if kenchiku20 >= 20:
		kenchiku20 = 0
	else:
		kenchiku20 = 1
	kenchiku20_vec.append(kenchiku20)

df3['築20年以下'] = kenchiku20_vec
#print df3, len(df3)


#columns = [Unnamed: 0 最寄駅：距離（分）  最寄駅：名称  建築年        取引時点 category_kyori  築20年以下]

#取引時点の種類の確認


#取引時点を0~11まででラベリング
#平成年第四半期を消す
#前から2文字をx、３文字目を1文字を
#(x-27)*4+(y-1)

df_torihiki = df3["取引時点"]
torihiki_vec = []
for i in range(0,len(df3)):
	torihiki = df_torihiki.iloc[i]
	torihiki = mojimoji.han_to_zen(unicode(torihiki))
	torihiki = torihiki.replace("平成","").replace("年第","").replace("四半期","")
	torihiki = mojimoji.zen_to_han(unicode(torihiki))	
	torihiki_x =  int(torihiki[:2])-27
	torihiki = torihiki_x * 4 + int(torihiki[2:])-1
	torihiki_vec.append(torihiki)

df3["取引時点"] = torihiki_vec

#print df3['取引時点'].value_counts(), df3
#0~9まで振り分けられた

#リーマン2009,2010[-28~-21]は[0]、以外は[1]
#df_lehman = df3["取引時点"]
#lehman_vec = []
#for i in range(0,len(df_lehman)):
	#lehman = df_lehman.iloc[i]
	#if lehman >= -28 and lehman <= -21:
		#lehman = 0
	#else:
		#lehman = 1
	#lehman_vec.append(lehman)
#df3["リーマン以外"] = lehman_vec
#print df3

#徒歩距離のダミー変数化0~3=>1,4~6=>2,7~10=>3,10~=>4をそれぞれ
df_kyori_d = pd.get_dummies(df3["category_kyori"])
#確認のため
#print df_kyori_d
#元のデータとダミー変数化したものと結合
df4 = pd.concat([df3, df_kyori_d], axis=1)

#最寄駅のダミー変数化
df_sta = pd.get_dummies(df3["最寄駅：名称"])
#以下は確認のため
#print df_sta["氷川台"].value_counts()
#元データとと最寄駅をダミー変数化したものと結合
df5 = pd.concat([df4, df_sta], axis=1)

#ダミー変数化をcsvで確認
#df5.to_csv("test2.csv",encoding="SHIFT-JIS")
