import requests
from bs4 import BeautifulSoup
from selenium import webdriver

참고
# 동적 웹 크롤링(1) https://liveyourit.tistory.com/14
# 멜론 차트 크롤링하기(1) https://velog.io/@kjh107704/K-POP-%EC%97%AD%EC%82%AC%EA%B4%80-%EB%A9%9C%EB%A1%A0-%EC%B0%A8%ED%8A%B8-%ED%81%AC%EB%A1%A4%EB%A7%81%ED%95%98%EA%B8%B0-1
 

driver = webdriver.Chrome("chromedriver.exe")
if __name__ == "__main__":
    RANK = 100 ## 멜론 차트 순위가 1 ~ 100위까지 있음
 
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko'}
    req = requests.get('https://www.melon.com/chart/week/index.htm', headers = header) ## 주간 차트를 크롤링 할 것임
    html = req.text
    parse = BeautifulSoup(html, 'html.parser')
 
    titles = parse.find_all("div", {"class": "ellipsis rank01"}) 
    singers = parse.find_all("div", {"class": "ellipsis rank02"}) 
    albums = parse.find_all("div",{"class": "ellipsis rank03"})
 
    title = []
    singer = []
    album = []
 
    for t in titles:
        title.append(t.find('a').text)
 
    for s in singers:
        singer.append(s.find('span', {"class": "checkEllipsis"}).text)

    for a in albums:
        album.append(a.find('a').text)
 
    for i in range(RANK):
        print('%3d위: %s [ %s ] - %s'%(i+1, title[i], album[i], singer[i]))