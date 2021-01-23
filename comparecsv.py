import csv
import numpy as np
import shutil

def compare2(download_place):
    shutil.copyfile(download_place+"\\query.csv",'wiki.csv')
    with open('wiki.csv', newline='', encoding='utf-8') as csvfile:
        reader_Ds  = csv.reader(csvfile) #將內容全轉成字典
        wiki_list = list(reader_Ds)  #將A表存進矩陣

    shutil.copyfile(download_place+"\\interpreter",'OSM')
    with open('OSM', newline='',encoding='utf-8') as csvfile:
        reader_Ms = csv.reader(csvfile) #將內容全轉成字典
        osm_list = list(reader_Ms)  #將B表存進矩陣

    wiki_col = len(wiki_list)
    wiki_row = len(wiki_list[0])
    osm_col = len(osm_list)
    osm_row = len(osm_list[0])

    #利用雙回圈比對兩個表格全部的資料

    for i in range(1, wiki_col):
        str = ""
        s0 = wiki_list[i][0]
        wiki_list[i][0] = s0[31:45]

    com_list=['wikidata id','osm id']
    already_list=['wikidata id','osm id']

    for m in range(1,osm_col):
        if osm_list[m][2]=="":
            for i in range(1, wiki_col):
                if osm_list[m][1]==wiki_list[i][1]:
                    arr = [wiki_list[i][0],osm_list[m][0]]
                    com_list = np.vstack((com_list,arr))
                else:
                    sa = wiki_list[i][3]
                    l = 0
                    for j in range(0, len(sa)):
                        if sa[j] == ",":
                            if sa[l:j]==osm_list[m][1]:
                                arr = [wiki_list[i][0], osm_list[m][0]]
                                com_list = np.vstack((com_list,arr))
                                break
                            else:
                                l = j + 1
                        if j == len(sa) - 1:
                            if sa[l:j + 1]==osm_list[m][1]:
                                arr = [wiki_list[i][0], osm_list[m][0]]
                                com_list = np.vstack((com_list,arr))
                                break
                            else:
                                l = j + 1

        else:
            arr = [osm_list[m][2], osm_list[m][0]]
            already_list = np.vstack((already_list,arr))

    with open('already.csv', 'w', newline='') as csvfile:
      writer = csv.writer(csvfile)
      writer.writerows(already_list)     # 資料回寫表格

    with open('compare.csv', 'w', newline='') as csvfile:
      writer = csv.writer(csvfile)
      writer.writerows(com_list)     # 資料回寫表格
