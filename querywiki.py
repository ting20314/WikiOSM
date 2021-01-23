from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import selenium.webdriver.support.ui as ui
import time

def query_wiki(place_Qid,country_Qid):
    if __name__ == "__main__":
        options = Options()
        options.binary_location = "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"
        driver = webdriver.Chrome('C:/Program Files (x86)/Google/Chrome/Application/chromedriver', options=options)
        driver.set_window_size(1024, 960)
        # 使用 driver 開起 https://tw.yahoo.com
        driver.get("https://query.wikidata.org/")
        # 使用 xpath 找到搜尋欄並填入 hello world
        soo="\""
        s="SELECT ?item ?itemLabel ?itemDescription (GROUP_CONCAT(DISTINCT(?altLabel); separator = "+soo+","+soo+") AS ?altLabel_list)\nWHERE\n{\n?item wdt:P31/wdt:P279* wd:"+place_Qid+";\nwdt:P17 wd:"+country_Qid+".\nOPTIONAL { ?item skos:altLabel ?altLabel . FILTER (lang(?altLabel) in ("+soo+"zh"+soo+","+soo+"zh-tw"+soo+","+soo+"en"+soo+","+soo+"zh-hant"+soo+")) }\nSERVICE wikibase:label { bd:serviceParam wikibase:language "+soo+"zh"+soo+","+soo+"zh-tw"+soo+","+soo+"en"+soo+","+soo+"zh-hant"+soo+". }\n}\nGROUP BY ?item ?itemLabel ?itemDescription"

        wait = ui.WebDriverWait(driver, 10)
        wait.until(lambda driver: driver.find_element_by_xpath("//span[@cm-text]"))
        # inputs = driver.find_element_by_xpath("//div[@class='CodeMirror-lines']/div[1]/div[3]")

        # move_to  移動
        # 定位到元素的源位置
        ele = driver.find_element_by_xpath("//span[@cm-text]")
        # 滑鼠拖放操作：drag_and_drop(source, target)
        # source: 滑鼠拖動的源元素。
        # target: 滑鼠釋放的目標元素。
        # 定位元素的源位置
        element = driver.find_element_by_xpath("//span[@cm-text]")
        # 定位元素要移動到的目標位置
        # target = driver.find_element_by_xpath("//div[@style='']/pre[9]")
        # 執行元素的拖放操作
        ActionChains(driver).move_to_element(element).click().perform()

        # ActionChains(driver).send_keys(Keys.DELETE).perform()
        ActionChains(driver).send_keys(s).perform()
        # driver.close()

        # 找到送出鍵並點擊
        # driver.find_element_by_id('a.t.button').click()
        button_play = driver.find_element_by_xpath("//span[@class='fa fa-play']")
        ActionChains(driver).move_to_element(button_play).click().perform()


        time.sleep(60)
        button_download = driver.find_element_by_xpath("//a[@id='download-button']")
        ActionChains(driver).move_to_element(button_download).click().perform()
        button_download = driver.find_element_by_xpath("//a[@id='downloadCSV']")
        ActionChains(driver).move_to_element(button_download).click().perform()

            # button_overapi = driver.find_element_by_xpath("//a[@id='export-overpass-api']")
            # ActionChains(driver).move_to_element(button_overapi).click().perform()
        time.sleep(20)
        driver.close()
