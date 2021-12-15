import os
import csv
import requests
import numpy as np
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

link_datas = []
rf = open('movie_link.csv', 'r', encoding='utf-8')
wf = open('movie_score.csv', 'a',newline='', encoding='utf-8')
rdr = csv.reader(rf)
wtr = csv.writer(wf)
for i in rdr:
    link_datas.append(i)

head = ['영화 이름', '개봉년도', '관람객 평점', '평론가 평점', '네티즌 평점', '평가한 관람객 수', '평가한 평론가 수', '평가한 네티즌 수']
wtr.writerow(head)
movie_data = []
year = 1999
for link_data in link_datas:
    year += 1
    for movie_link in link_data:
        URL = movie_link
        driver.implicitly_wait(10)
        
        driver.get(URL)
        time.sleep(0.3)
        try:#연령제한 영화는 넘어감(로그인)
            movie_name_el = driver.find_element(By.XPATH, "//*[@id='content']/div[1]/div[2]/div[1]/h3/a")
            movie_name = movie_name_el.text
        except:
            continue
        
        driver.implicitly_wait(0.1)
        try:#관람객 평점 있음
            audience = driver.find_element(By.XPATH, '//*[@id="actualPointPersentBasic"]/div')
            test = audience.find_element(By.TAG_NAME, "em") #점수가 없으면 오류남
            audience_depth1 = audience.find_elements(By.TAG_NAME, "em")
            temp = ""
            for i in audience_depth1:
                temp += i.text
            audience_score = float(temp)
        except:#관람객 평점 없음
            audience_score = np.NaN

        try:#평론가 평점 있음
            critic = driver.find_element(By.XPATH, '//*[@id="content"]/div[1]/div[2]/div[1]/div[1]/div[2]/div/a/div')
            test = critic.find_element(By.TAG_NAME, "em") #점수가 없으면 오류남
            critic_depth1 = critic.find_elements(By.TAG_NAME, "em")
            temp = ""
            for i in critic_depth1:
                temp += i.text
            critic_score = float(temp)
        except:#평론가 평점 없음
            critic_score = np.NaN
            
        try:#네티즌 평점 있음
            netizens = driver.find_element(By.XPATH, '//*[@id="pointNetizenPersentBasic"]')
            test = netizens.find_element(By.TAG_NAME, "em") #점수가 없으면 오류남
            netizens_depth1 = netizens.find_elements(By.TAG_NAME, "em")
            temp = ""
            for i in netizens_depth1:
                temp += i.text
            netizens_score = float(temp)
        except:#네티즌 평점 없음
            netizens_score = np.NaN
            
        # 관람객 참여 수
        try:
            a_count = driver.find_element(By.XPATH, '//*[@id="actualPointCountBasic"]')
            driver.execute_script("arguments[0].style.display = 'block';", a_count)
            audience_count = driver.find_element(By.XPATH, '//*[@id="actualPointCountBasic"]/em').text
            audience_count = int(audience_count.replace(',',''))
        except:
            audience_count = 0

        # 평론가 참여 수
        try:
            critic_count = driver.find_element(By.XPATH, '//*[@id="content"]/div[1]/div[4]/div[5]/div[2]/div[2]/div[2]/div/span/em').text
            critic_count = int(critic_count.replace(',',''))
        except:
            critic_count = 0

        # 네티즌 참여 수
        try:
            n_count = driver.find_element(By.XPATH, '//*[@id="pointNetizenCountBasic"]')
            driver.execute_script("arguments[0].style.display = 'block';", n_count)
            netizens_count = driver.find_element(By.XPATH, '//*[@id="pointNetizenCountBasic"]/em').text
            netizens_count = int(netizens_count.replace(',',''))
        except:
            netizens_count = 0
        
        try:
            movie_temp = [movie_name,  year, audience_score, critic_score, netizens_score, audience_count, critic_count, netizens_count]
            print(movie_temp)
            
            if movie_temp not in movie_data:
                movie_data.append(movie_temp)
                wtr.writerow(movie_temp)
        except:
            pass

rf.close()
wf.close()
print('-----------end-------------')