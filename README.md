### Automatic Data Completion Integration Between Open-Source Database OpenStreetMap and Wikidata 
**Ching-Ting Chia**

**2020-12-22**

Wikidata and OpenStreetMap are widely used open databases that leverage the power of crowdsourcing to expand their datasets. However, there are limitations within each platform. In Wikidata, while it contains information about many prominent landmarks and geographic locations, these places are often represented by a single point. From a geographic information system perspective, this representation is insufficient.

On the other hand, OpenStreetMap provides more comprehensive layers of geographical data, including points, lines, and polygons. However, the attribute data within these layers is still relatively sparse compared to Wikidata. Two main reasons contribute to the incompleteness of data in both Wikidata and OpenStreetMap.

Firstly, different individuals or communities contribute to the development of these databases, resulting in varying levels of progress. For instance, OpenStreetMap may prioritize geographic features (points, lines, areas, and relations), while Wikidata focuses on data sources and interconnections between data.

Secondly, Wikidata's representation of geographic information is limited to node coordinates, and nodes cannot be overlaid to depict relationships. In contrast, OpenStreetMap's Attribute Table is relatively basic, with connectivity based primarily on geographic coordinates. As a solution to these limitations, integrating these two databases and subsequent data enhancement can significantly contribute to open data resources.

#### Preparatory for Wikidata and OpenStreetMap Integration

Before proceeding with the integration, it's essential to have a few critical understandings about Wikidata and OpenStreetMap:

Data Identification: In both databases, data is identified with a unique identifier: the data's ID. In Wikidata, this identifier is known as a 'Qid,' while in OpenStreetMap, it is referred to as the (Node/Polyline/Polygon/Relation) id.
Linking Mechanism: Wikidata connects to OpenStreetMap using the OSM Relation ID, and OpenStreetMap links to Wikidata using a 'wikidata' tag in the Attribute Table associated with a Qid.
Data Rigidity: Wikidata has stricter data standards and guidelines, whereas OpenStreetMap allows easier creation of new data. Consequently, OpenStreetMap contains a significant amount of data created by individual users for personal use, which may not be intended for public use.
Batch Data Upload: Regarding batch data upload, Wikidata provides an accessible tool called Quickstatements, which allows direct data uploads. Users can copy and paste data into desired fields, making it user-friendly and intuitive. In contrast, OpenStreetMap requires users to modify and convert original, complete data into change files before performing batch uploads. It's akin to pulling data, making necessary changes, and pushing it back, much like Git's principles. Consequently, batch data uploads in OpenStreetMap are more complex and involve multiple steps."



#### Steps of the integration

1. =Collecting Data in both Wikidata and OpenStreetMap

Wikidata: Data collection is performed using Wikidata Query.
The following collects all the schools' data throughout Taiwan as an example for integration.
	
	SPARQL=  
	SELECT ?item ?itemLabel ?itemDescription (GROUP_CONCAT(DISTINCT(?altLabel); separator = ", ") AS ?altLabel_list)  
	WHERE  
	{  
	?item wdt:P31/wdt:P279* wd:Q3914;  
		wdt:P17 wd:Q865.  
	OPTIONAL { ?item skos:altLabel ?altLabel . FILTER (lang(?altLabel) in ("zh","zh-tw","en","zh-hant")) }  
	SERVICE wikibase:label { bd:serviceParam wikibase:language "zh","zh-tw","en","zh-hant". }  
	}  
	GROUP BY ?item ?itemLabel ?itemDescription  

  - OpenStreetMap:Using [Overpass Turbo](https://overpass-turbo.eu/) to search for all relation data
	
	[out:csv(  
	::"id",name,wikidata;  
	true; ","  
	)];  
	relation  
	({{bbox:22,120,25,122}});  
	/*added by auto repair*/  
	(._;>;);  
	/*end of auto repair*/  
	out;  

2. Both datasets are compared by matching each field individually based on name and alias, and the corresponding linking code is added to create a new table. If a link already exists, no further output is generated.

As an example, a CSV comparison is used (matching label names with alias/label to find the corresponding Oid):
	- A data has labels without Qid (from OpenStreetMap Query).
	- B data has labels, aliases, and Qid (from Wikidata Query).
 
	IFNA(INDEX(B-Qid,match(A-label,B-label或B-alias,0)),0)  

    if it matches, then return Qid; if not, then return 0 
    
3. Update Wikidata and OpenStreetMap
  - Wikidata
    - Add Pid to Wikidata(In Wikidata, Pid is the id for OpenStreetMap)
    - Upload on [Quickstatements](https://quickstatements.toolforge.org/#/)
  - OpenStreetMap
    - Download the original OpenStreetMap file(.osm) from JOSM, which is in XML format.
    - Add Wikidata Qid
    - Transfer osm to osc file in [osm2change.py](https://github.com/grigory-rechistov/osm-bulk-upload/blob/master/osm2change.py). In OpenStreetMap, osm and osc are both in XML format. However, the difference is that osm is the storage file, including the data and its attributes; the osc is for the updating file, including the data's adding, deleting, correcting, and so on.
	
	./osm2change.py file.osm  

    - Upload the file by [upload.py](https://github.com/grigory-rechistov/osm-bulk-upload/blob/master/upload.py)
	
	./upload.py -u username -p password -c yes -m 'add wikidata' file.osc  

#### Wikidata與OSM的自動化串聯

此次研究中，因為步驟十分繁瑣，因此我自行寫了數個程式，配合原有的upload.py，將整個串連動作進行自動化的串聯，讓非Wikidata專業與OpenStreetMap的使用者皆可以進行資料串連，並且可以針對不同地區、不同對象進行串聯。
以下程式皆可於此下載:[自動化串聯](https://github.com/ting20314/WikiOSM)

1. 雙邊進行爬蟲，將原始資料下載
  - OpenStreetMap:queryOSM.py
  - Wikidata:querywiki.py
    皆是以selenium的webdriver模擬滑鼠及虛擬鍵盤，進行模擬滑鼠及虛擬鍵盤，進行資料的收集下載。
2. 資料比對:comparecsv.py
    將xml轉為動態陣列後，使其重複比對，直到比對成功時，將兩者所對應之Wikidata Qid與OpenStreetMap Relation id進行配對，輸出為新檔案compare.csv，且輸出一個已完成串連的檔案already.csv。
3. 資料的回傳
  - Wikidata
      - 加上Pid(OSM辨識碼):P402
      - [Quickstatements](https://quickstatements.toolforge.org/#/)進行上傳
      在Wikidata中，Upload資料較為簡單，只需要在compare.csv中，將表格改為column=1為wikidata Qid,column=2為P402,column=3為OpenStreetMap Relation id，在全部複製貼上，即可上傳更新。
  - OpenStreetMap
    - 回到OSM找原始OSM檔:backfindosm.py
    因為要再次開啟JOSM的軟體，重畫範圍等太過麻煩，因此我使用類似queryOSM.py的方法，以要更正的Relation id做搜尋，將每個要更新的Relation id進行搜尋，並下載其osm檔案，即會獲得原始的osm檔案。
    - 將要增加的wikidata Qid加入:inputwiki2osm.py
    將所有要加上去的<tags:wikidata=Qid>批次加入每一項Relation中。
    - osm->osc:osc.py
    將osm的資料轉為osc資料格式，使其OpenStreetMap系統了解使用者是為了更正原始資料。
    - 上傳:upload.py
    使用OpenStreetMap原有的開元Uploading檔案，以
	
	./upload.py -u username -p password -c yes -m 'add wikidata' file.osc  

執行檔案
 **可直接執行linkallpy.py，以連動所有步驟程式，再以upload.py進行上傳**

並未將upload.py加入串聯是因為要提醒使用者再將大量資料上傳前，需要先進行確認才能上傳。
將資料進行匯入，連動後，以串聯範圍(south,west,north,east)、串聯對象(place_Qid)、串聯國家(country_Qid)、下載路徑作為參數輸入:
	
	./linkallpy.py south west north east place_Qid country_Qid 下載路徑  

執行檔案。
舉例而言，若要串聯台灣地區學校的Wikidata與OpenStreetMap，則學校Qid=Q3914、中華民國Qid=Q865、台灣本島範圍(south,west,north,east)=(22,120,25,122)，如下
	
	./linkallpy.py 22 120 25 122 Q3914 Q865 C:\\Users\\USER\\Downloads  

### 遇到的困難及可以改進的地方

從串聯的過程中，雖然容易對Wikidata進行串聯，然而在Wikiata資料庫的呈現上仍只有一組識別碼，並非展現出OpenStreetMap的圖層，然而這個部分可能就要與Wikidata的社群討論，是否以OpenStreetMap圖台呈現圖層，更能夠展現出地理特性，畢竟並非所有人都會點入識別碼，連到OpenStreetMap中看地理範圍的。
而在OpenStreetMap中，Relation的數量極少，因此能夠串連的地物不多，且建立Relation的標準不明確，如以中正紀念堂為例，中正紀念堂的Relation範圍在建築物周圍，還是Relation範圍在整個圍牆周圍，這也是需要討論的問題。此外，OpenStreetMap本身在Query時，在bbox的範圍選擇上也容易系統出錯，導致可能查找的範圍並非所求範圍。
另外OpenStreetMap中name的規定有較為不嚴謹，同樣的地物於Wikidata中為全名，在OpenStreetMap中卻為簡稱，因此導致OpenStreetMap中常有名字重複的問題，因此可以以Relation中的Node點座標，對於Wikidata中的點位做距離的比較，即可解決重複問題，然而因為會更為複雜，因此做為之後發展的目標。
除此之外，OpenStreetMap的社群中，對於資料的串聯意見不一，因為有些使用者使用OpenStreetMap不是未開放資料，而是為了個人作業，因此常常會搜尋到很多錯誤的資訊或錯誤的位置，且在於資料補齊上比較無法進行，因為無法確切資訊或錯誤的位置，且在於資料補齊上比較無法進行，因為確定使用者是否接受將資料作為Wikidata的補齊，因此這是兩個社群須溝通的部分。





# Wikidata與OSM的串聯及補齊 Automated Integration and Augmentation of Wikidata with OpenStreetMap 
**Ching-Ting Chia**

**2020-12-22**

### 對於Wikidata與OpenStreetMap的了解與前置作業

在進行串聯前，我們需要先對於Wikidata與OpenStreetMap有幾個認識:

1. 資料庫中，資料的識別碼可謂資料的身分證字號，在Wikidata中稱為Qid，而在OpenStreetMap中則稱為(Node/Polyline/Polygon/Relation) id。
2. 連接方式:Wikidata是以OSM Relation id(OSM關聯碼)對OpenStreetMap進行連接，而OpenStreetMap則是以在Attribute Table中新增一tags稱為wikidata，為Qid為連接方式
3. Wikidata中資料庫建立較為嚴格，而在OpenStreetMap中建立一新資料較容易，因此在OpenStreetMap中有許多資料為使用者個人使用，非提供與大眾使用。
4. 以資料的批次上傳而言，Wikidata有可以直接使用的Quickstatements來上傳資料，並且只要將想增加的欄位複製貼上即可，非榮直觀、容易；然而在OpenStreetMap中，需要以原始的完整資料進行修改，並且轉換為更正檔，才能進行批次上傳，類似於git中，需要上傳資料前，需要先將資料pull out，將所要增加或刪減的資料修正後，才能夠push回去，是類似的原理，因此愛批次上傳下資料修正後，才能夠push回去，是類似的原理，因此在OpenStreetMap的批次上傳是較為複雜、多程序的。

### 步驟

1. 同時在Wikidata與OpenStreetMap中進行資料的採集
  - Wikidata:使用[Wikidata Query](https://query.wikidata.org/)進行資料的收集
  (然而若收集全台灣的所有資料會太過龐大，因此以下為全台灣之學校作為串聯對象)
	
	SPARQL=  
	SELECT ?item ?itemLabel ?itemDescription (GROUP_CONCAT(DISTINCT(?altLabel); separator = ", ") AS ?altLabel_list)  
	WHERE  
	{  
	?item wdt:P31/wdt:P279* wd:Q3914;  
		wdt:P17 wd:Q865.  
	OPTIONAL { ?item skos:altLabel ?altLabel . FILTER (lang(?altLabel) in ("zh","zh-tw","en","zh-hant")) }  
	SERVICE wikibase:label { bd:serviceParam wikibase:language "zh","zh-tw","en","zh-hant". }  
	}  
	GROUP BY ?item ?itemLabel ?itemDescription  

  - OpenStreetMap:使用[Overpass Turbo](https://overpass-turbo.eu/)搜尋所有的Relation搜尋所有的Relation
	
	[out:csv(  
	::"id",name,wikidata;  
	true; ","  
	)];  
	relation  
	({{bbox:22,120,25,122}});  
	/*added by auto repair*/  
	(._;>;);  
	/*end of auto repair*/  
	out;  

2. 兩邊資料進行比對，以name,alias進行純文字資料集每個欄位一一的比對，對應即補上其串聯碼，並匯出新表格資料。若已有串聯，則不進行輸出。
  - 以csv對照(以label名稱對應alias/label來找到對應Oid)為例
    - 以A資料有label無Qid(來自OSM Query)
    - B資料有label,alias,Qid(來自Wikidata Query)
	
	IFNA(INDEX(B-Qid,match(A-label,B-label或B-alias,0)),0)  

    有對應則回傳Qid，沒有則回傳0 
3. 將Wikidata與OpenStreetMap進行回傳Upload
  - Wikidata
    - Wikidata加上Pid(Pid為Value的屬性，因此此資料集中Pid為OSM識別碼)
    - 於[Quickstatements](https://quickstatements.toolforge.org/#/)進行上傳
  - OpenStreetMap
    - 使用JOSM將原始OSM檔(.osm)下載後，會得到一xml格式之檔案
    - 將要增加的wikidata Qid加入
    - 使用[osm2change.py](https://github.com/grigory-rechistov/osm-bulk-upload/blob/master/osm2change.py)將osm轉換為osc，在OpenStreetMap中，osm與osc皆為xml的資料格式，不同在於osm為資料庫中處存之資料格式，而osc則為告訴資料庫要增加、刪改、更正等資料庫變化檔案
	
	./osm2change.py file.osm  

    - 利用[upload.py](https://github.com/grigory-rechistov/osm-bulk-upload/blob/master/upload.py)將資料進行上傳
	
	./upload.py -u username -p password -c yes -m 'add wikidata' file.osc  

### Wikidata與OSM的自動化串聯

此次研究中，因為步驟十分繁瑣，因此我自行寫了數個程式，配合原有的upload.py，將整個串連動作進行自動化的串聯，讓非Wikidata專業與OpenStreetMap的使用者皆可以進行資料串連，並且可以針對不同地區、不同對象進行串聯。
以下程式皆可於此下載:[自動化串聯](https://github.com/ting20314/WikiOSM)

1. 雙邊進行爬蟲，將原始資料下載
  - OpenStreetMap:queryOSM.py
  - Wikidata:querywiki.py
    皆是以selenium的webdriver模擬滑鼠及虛擬鍵盤，進行模擬滑鼠及虛擬鍵盤，進行資料的收集下載。
2. 資料比對:comparecsv.py
    將xml轉為動態陣列後，使其重複比對，直到比對成功時，將兩者所對應之Wikidata Qid與OpenStreetMap Relation id進行配對，輸出為新檔案compare.csv，且輸出一個已完成串連的檔案already.csv。
3. 資料的回傳
  - Wikidata
      - 加上Pid(OSM辨識碼):P402
      - [Quickstatements](https://quickstatements.toolforge.org/#/)進行上傳
      在Wikidata中，Upload資料較為簡單，只需要在compare.csv中，將表格改為column=1為wikidata Qid,column=2為P402,column=3為OpenStreetMap Relation id，在全部複製貼上，即可上傳更新。
  - OpenStreetMap
    - 回到OSM找原始OSM檔:backfindosm.py
    因為要再次開啟JOSM的軟體，重畫範圍等太過麻煩，因此我使用類似queryOSM.py的方法，以要更正的Relation id做搜尋，將每個要更新的Relation id進行搜尋，並下載其osm檔案，即會獲得原始的osm檔案。
    - 將要增加的wikidata Qid加入:inputwiki2osm.py
    將所有要加上去的<tags:wikidata=Qid>批次加入每一項Relation中。
    - osm->osc:osc.py
    將osm的資料轉為osc資料格式，使其OpenStreetMap系統了解使用者是為了更正原始資料。
    - 上傳:upload.py
    使用OpenStreetMap原有的開元Uploading檔案，以
	
	./upload.py -u username -p password -c yes -m 'add wikidata' file.osc  

執行檔案
 **可直接執行linkallpy.py，以連動所有步驟程式，再以upload.py進行上傳**

並未將upload.py加入串聯是因為要提醒使用者再將大量資料上傳前，需要先進行確認才能上傳。
將資料進行匯入，連動後，以串聯範圍(south,west,north,east)、串聯對象(place_Qid)、串聯國家(country_Qid)、下載路徑作為參數輸入:
	
	./linkallpy.py south west north east place_Qid country_Qid 下載路徑  

執行檔案。
舉例而言，若要串聯台灣地區學校的Wikidata與OpenStreetMap，則學校Qid=Q3914、中華民國Qid=Q865、台灣本島範圍(south,west,north,east)=(22,120,25,122)，如下
	
	./linkallpy.py 22 120 25 122 Q3914 Q865 C:\\Users\\USER\\Downloads  

### 遇到的困難及可以改進的地方

從串聯的過程中，雖然容易對Wikidata進行串聯，然而在Wikiata資料庫的呈現上仍只有一組識別碼，並非展現出OpenStreetMap的圖層，然而這個部分可能就要與Wikidata的社群討論，是否以OpenStreetMap圖台呈現圖層，更能夠展現出地理特性，畢竟並非所有人都會點入識別碼，連到OpenStreetMap中看地理範圍的。
而在OpenStreetMap中，Relation的數量極少，因此能夠串連的地物不多，且建立Relation的標準不明確，如以中正紀念堂為例，中正紀念堂的Relation範圍在建築物周圍，還是Relation範圍在整個圍牆周圍，這也是需要討論的問題。此外，OpenStreetMap本身在Query時，在bbox的範圍選擇上也容易系統出錯，導致可能查找的範圍並非所求範圍。
另外OpenStreetMap中name的規定有較為不嚴謹，同樣的地物於Wikidata中為全名，在OpenStreetMap中卻為簡稱，因此導致OpenStreetMap中常有名字重複的問題，因此可以以Relation中的Node點座標，對於Wikidata中的點位做距離的比較，即可解決重複問題，然而因為會更為複雜，因此做為之後發展的目標。
除此之外，OpenStreetMap的社群中，對於資料的串聯意見不一，因為有些使用者使用OpenStreetMap不是未開放資料，而是為了個人作業，因此常常會搜尋到很多錯誤的資訊或錯誤的位置，且在於資料補齊上比較無法進行，因為無法確切資訊或錯誤的位置，且在於資料補齊上比較無法進行，因為確定使用者是否接受將資料作為Wikidata的補齊，因此這是兩個社群須溝通的部分。
