from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
import selenium.webdriver.support.ui as ui
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

def query_osm(south,west,north,east):
    if __name__ == "__main__":
        options = Options()
        options.binary_location = "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"
        driver = webdriver.Chrome('C:/Program Files (x86)/Google/Chrome/Application/chromedriver', options=options)
        driver.set_window_size(1024, 960)
        # 使用 driver 開起 https://overpass-turbo.eu/
        driver.get("https://overpass-turbo.eu/")
        soo="\""
        s="[out:csv(\n::"+soo+"id"+soo+",name,wikidata;\ntrue; "+soo+","+soo+"\n)];\nrelation\n({{bbox:"+south+","+west+","+north+","+east+"}});\n/*added by auto repair*/\n(._;>;);\n/*end of auto repair*/\nout;"

        wait = ui.WebDriverWait(driver, 10)
        wait.until(lambda driver: driver.find_element_by_xpath("//div[@style='']/pre[1]"))

        # move_to  移動
        # 定位到元素的源位置
        ele = driver.find_element_by_xpath("//div[@style='']/pre[1]")
        # 滑鼠拖放操作：drag_and_drop(source, target)
        # source: 滑鼠拖動的源元素。
        # target: 滑鼠釋放的目標元素。
        # 定位元素的源位置
        element1 = driver.find_element_by_xpath("//div[@style='']/pre[1]")
        element9 = driver.find_element_by_xpath("//div[@style='']/pre[9]")
        # 定位元素要移動到的目標位置
        # target = driver.find_element_by_xpath("//div[@style='']/pre[9]")
        # 執行元素的拖放操作
        ActionChains(driver).move_to_element(element9).click().perform()
        for i in range(200):
            ActionChains(driver).send_keys(Keys.BACK_SPACE).perform()

        # ActionChains(driver).send_keys(Keys.DELETE).perform()
        ActionChains(driver).send_keys(s).perform()
        # driver.close()

        # 找到送出鍵並點擊
        # driver.find_element_by_id('a.t.button').click()
        button_play = driver.find_element_by_xpath("//a[@class='t button'][1]")
        ActionChains(driver).move_to_element(button_play).click().perform()


        try:
            element = WebDriverWait(driver, 45).until(
                EC.presence_of_element_located((By.XPATH, "//div[@style=''][2]/pre"))
            )
        finally:
            button_download = driver.find_element_by_xpath("//a[@class='t button'][3]")
            ActionChains(driver).move_to_element(button_download).click().perform()

            button_overapi = driver.find_element_by_xpath("//a[@id='export-overpass-api']")
            ActionChains(driver).move_to_element(button_overapi).click().perform()
            time.sleep(20)
            driver.close()
