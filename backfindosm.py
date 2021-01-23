from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import csv
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import selenium.webdriver.support.ui as ui
import time

def back_finding_osm():
    with open('compare.csv', newline='', encoding='utf-8') as csvfile:
        reader_Ds  = csv.reader(csvfile) #將內容全轉成字典
        compare_list = list(reader_Ds)  #將表存進矩陣

    if __name__ == "__main__":
        options = Options()
        options.binary_location = "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"
        driver = webdriver.Chrome('C:/Program Files (x86)/Google/Chrome/Application/chromedriver', options=options)
        driver.set_window_size(1024, 960)
        # 使用 driver 開起 https://tw.yahoo.com
        driver.get("https://overpass-turbo.eu/")
        # 使用 xpath 找到搜尋欄並填入 hello world

        sid="id"
        soo="\""

        wait = ui.WebDriverWait(driver, 10)
        wait.until(lambda driver: driver.find_element_by_xpath("//div[@style='']/pre[1]"))
        # inputs = driver.find_element_by_xpath("//div[@class='CodeMirror-lines']/div[1]/div[3]")

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
        sfront = "[out:xml];\n("
        ActionChains(driver).send_keys(sfront).perform()
        for i in range(1,len(compare_list)):
            sin = "rel(" +compare_list[i][1]+ ");\n"
            ActionChains(driver).send_keys(sin).perform()
        send = ");\n/*added by auto repair*/\n(._;>;);\n/*end of auto repair*/\nout meta;"
        ActionChains(driver).send_keys(send).perform()
        # driver.close()

        # 找到送出鍵並點擊
        # driver.find_element_by_id('a.t.button').click()
        button_play = driver.find_element_by_xpath("//a[@class='t button'][1]")
        ActionChains(driver).move_to_element(button_play).click().perform()

        #
        # try:
        #     element = WebDriverWait(driver, 20).until(
        #         EC.presence_of_element_located((By.XPATH, "//div[@style=''][2]/pre"))
        #     )
        # finally:
        time.sleep(30)
        button_get = driver.find_element_by_xpath("//button[@class='ui-button ui-corner-all ui-widget'][2]")
        ActionChains(driver).move_to_element(button_get).click().perform()
        button_download = driver.find_element_by_xpath("//a[@class='t button'][3]")
        ActionChains(driver).move_to_element(button_download).click().perform()
        button_overapi = driver.find_element_by_xpath("//p[@class='t'][4]/a[@class='export']")
        ActionChains(driver).move_to_element(button_overapi).click().perform()
        time.sleep(20)
        driver.close()
