import os
import requests
from selenium import webdriver
import chromedriver_autoinstaller
from selenium.webdriver.support.ui import Select
import time

#참고
# 동적 웹 크롤링(1) https://liveyourit.tistory.com/14
# 동적 웹 크롤링(2) https://liveyourit.tistory.com/15
# 셀레니움 설치와 크롬 드라이버 자동 처리 https://pythondocs.net/selenium/%EC%85%80%EB%A0%88%EB%8B%88%EC%9B%80-%EC%84%A4%EC%B9%98%EC%99%80-%ED%81%AC%EB%A1%AC-%EB%93%9C%EB%9D%BC%EC%9D%B4%EB%B2%84-%EC%9E%90%EB%8F%99-%EC%B2%98%EB%A6%AC/
# 파이썬 자동화 https://wikidocs.net/73539


driver = webdriver.Chrome(chromedriver_autoinstaller.install())

driver.implicitly_wait(10)
URL = "https://www.melon.com/artistplus/finder/index.htm"
driver.get(URL)
driver.find_element_by_id("GN0300").click()

for i in range(1, 16):
    xpath = "//*[@id='conts']/div[1]/dl/dd/div[1]/button["+ str(i) +"]"
    print(xpath)
    driver.find_element_by_xpath(xpath).click()
for i in range(1, 26):
    xpath = "//*[@id='conts']/div[1]/dl/dd/div[2]/button["+ str(i) +"]"
    print(xpath)
    driver.find_element_by_xpath(xpath).click()

time.sleep(100)

#xpath = '//*[@id="GN0300"]'
#select = Select(driver.find_element_by_xpath(xpath))
#select.select_by_value('GN0300')
