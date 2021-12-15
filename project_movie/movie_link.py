import os
import csv
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import chromedriver_autoinstaller
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
import time

#참고
# 동적 웹 크롤링(1) https://liveyourit.tistory.com/14
# 동적 웹 크롤링(2) https://liveyourit.tistory.com/15
# 셀레니움 설치와 크롬 드라이버 자동 처리 https://pythondocs.net/selenium/%EC%85%80%EB%A0%88%EB%8B%88%EC%9B%80-%EC%84%A4%EC%B9%98%EC%99%80-%ED%81%AC%EB%A1%AC-%EB%93%9C%EB%9D%BC%EC%9D%B4%EB%B2%84-%EC%9E%90%EB%8F%99-%EC%B2%98%EB%A6%AC/
# 파이썬 자동화 https://wikidocs.net/73539
# 페이지 이동 https://steadiness-193.tistory.com/118
# Selenium에서 요소의 속성을 얻는 방법은 무엇입니까? https://stackoverflow.com/questions/30324760/how-to-get-attribute-of-element-from-selenium
# find_element By 사용 https://pythonblog.co.kr/coding/23/
# 커뮤니티 게시물 크롤러 https://projectlog-eraser.tistory.com/12

driver = webdriver.Chrome(chromedriver_autoinstaller.install())
driver.implicitly_wait(10)

def next_page(driver):
    #페이지 이동
    page_bar = driver.find_element(By.CLASS_NAME, 'pagenavigation')
    try:
        nextpage = page_bar.find_element(By.LINK_TEXT, '다음')
        nextpage.send_keys("\n")
        time.sleep(0.5)
        return False
    except:
        return True

    
def get_movie_link(driver):
    movie_list = driver.find_element(By.CLASS_NAME, 'directory_list')
    link_info = movie_list.find_elements(By.XPATH, '//*[@id="old_content"]/ul/li[*]/a')
    
    for id in link_info:
        temp_list.append(id.get_attribute("href"))
        print(id.get_attribute("href"))
    
    

movie_link = []
for year in range(2000,2022):
    temp_list = []
    URL = f"https://movie.naver.com/movie/sdb/browsing/bmovie.naver?open={year}"
    driver.get(URL)

    is_done = False
    while(not is_done):
        get_movie_link(driver)
        is_done = next_page(driver)
    
    movie_link.append(temp_list)


#중복 제거
for i in range(0,22):
    temp = set(movie_link[i])
    movie_link[i] = list(temp)

#csv파일로 저장
with open('movie_link.csv', 'w',newline='') as f:
    write = csv.writer(f)
    for i in range(0,22):
        write.writerow(movie_link[i])