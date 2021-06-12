from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import pandas as pd

from selenium.webdriver.common.keys import Keys

options = Options()
options.add_argument("--start-maximized")
options.add_argument("--incognito")
options.add_argument('headless')
driver = webdriver.Chrome(options=options,
                          executable_path='C:/Users/User/PycharmProjects/zimer_grab/chromedriver.exe')

'''
scroll the page down:
https://stackoverflow.com/questions/20986631/how-can-i-scroll-a-web-page-using-selenium-webdriver-in-python
'''


def main():
    results = []

    def go_to_page():
        driver.get("https:/www.rrr.co.il")

    def go_north_zimmer():
        elem = driver.find_element_by_xpath('// *[ @ id = "56"] / div / a')
        elem.click()

    def go_south_zimmer():
        driver.back()
        time.sleep()
        elem = driver.find_element_by_xpath('//*[@id="84"]/div/a')
        elem.click()

    def go_center_zimmer():
        driver.back()
        time.sleep(5)
        elem = driver.find_element_by_xpath('// *[ @ id = "58"] / div / a')
        elem.click()

    def get_data():
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        time.sleep(5)
        zimmers = driver.find_elements_by_class_name("zleft")
        print(len(zimmers))
        for i in zimmers:
            res = {}
            name = i.find_element_by_tag_name("h3").get_attribute("innerText")
            location = i.find_element_by_class_name("in").get_attribute("innerText")
            units = i.find_elements_by_class_name("in")[1].get_attribute("innerText")
            cords = i.find_element_by_class_name("bottom_btn a").get_attribute("data-cord")
            try:
                weekdays_price = i.find_elements_by_class_name("theprice h4")[0].get_attribute("innerText")
                weekend_price = i.find_elements_by_class_name("theprice h4")[1].get_attribute("innerText")

            except:
                weekdays_price = 0
                weekend_price = 0

            res["zimmer_name"] = name
            res["zimmer_location"] = location
            res["num_and_type"] = units
            res["day_price"] = weekdays_price
            res["end_price"] = weekend_price
            res["coordinate"] = cords
            results.append(res)

    def data_frame_create():
        pd1 = pd.DataFrame(results)
        print(pd1)
        pd1.to_excel('output.xlsx')

    go_to_page()
    go_north_zimmer()
    get_data()
    go_south_zimmer()
    get_data()
    go_center_zimmer()
    get_data()
    data_frame_create()


if __name__ == "__main__":
    main()
