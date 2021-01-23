# 雙邊進行爬蟲，將原始資料下載    資料比對      加上Pid(OSM辨識碼)  上傳
# queryOSM.py,querywiki.py->comparecsv.py->(WIKI)add PID->upload
#                                           回到OSM找原始OSM檔  將要增加的wikidata Qid加入  osm->osc    上傳
#                                        ->(OSM)backfindosm-.py>inputwiki2osm.py->osm2change.py->upload.py
from queryOSM  import query_osm
from querywiki import query_wiki
from comparecsv import compare2
from backfindosm import back_finding_osm
from inputwiki2osm import inputwiki2osm_osc
import sys
# query_osm(south,west,north,east)
query_osm(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4])
# query_wiki(place_Qid,country_Qid)
query_wiki("\""+sys.argv[5]+"\"","\""+sys.argv[6]+"\"")
# 下載位置
compare2("\""+sys.argv[7]+"\"")
back_finding_osm()
# 下載位置
inputwiki2osm_osc("\""+sys.argv[7]+"\"")

# ./linkallpy.py 22 120 25 122 Q3914 Q865 C:\\Users\\USER\\Downloads