from urllib import request
from bs4 import BeautifulSoup
#import re
import time, os
import from591_find_values
from selenium import webdriver
chromedriver = './chromedriver'
driver = webdriver.Chrome(chromedriver)


url = os.path.join('https://rent.591.com.tw/?kind=0&region=3')
useragent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'
cookie = 'webp=1; PHPSESSID=b9lbhu6fciq49dv70lr8dd7b61; urlJumpIp=1; urlJumpIpByTxt=%E5%8F%B0%E5%8C%97%E5%B8%82; new_rent_list_kind_test=1; T591_TOKEN=b9lbhu6fciq49dv70lr8dd7b61; c10f3143a018a0513ebe1e8d27b5391c=1; _ga=GA1.3.557136261.1586498565; _gid=GA1.3.959731503.1586498565; _ga=GA1.4.557136261.1586498565; _gid=GA1.4.959731503.1586498565; tw591__privacy_agree=0; XSRF-TOKEN=eyJpdiI6IkErQnJvSHFEclZtTG5Sck9TTytQVlE9PSIsInZhbHVlIjoiaXRZY3M1ZTFuS09jZU9tS08xeHkxZ3hGVDZlQ2lLa09iY1poYWlPdVZiZ3AyYk5zdWpKZndwRzk4eDVoK2MyR1wvdEJGcEFuNUpPYStTVVNEQ0VjcTZnPT0iLCJtYWMiOiI3OTc3NjkzOTRlMWM0MTJmOTU4YTY0MmFkMmZkMjFmZjA5NTA3ZWY1YWVjNjE0ZmIxMGYyZTY5NzEwZjVmZDk4In0%3D; 591_new_session=eyJpdiI6IkpMOHI1d0trVDcyWjZwSE5IaEpUb0E9PSIsInZhbHVlIjoiYlhvZng5ZDBvcTR5Q3JtdTNtMjVCajF0blpLZWdLb2RDeTB0K3I2OEVmY0JhaGhMR09XaEpPWW9wVFwvcmw5SUw0SDVQbXJWTWhKUjBwWDVTMGh0RkRRPT0iLCJtYWMiOiJjMzBlMTgzMWFiYmVhNWE5YmVhZmY3Mjc4MGQyYWViYzBhYjQ2MWEzMTM5YTdkMjU5OWJhNjc5MzQ4N2ZiMWZjIn0%3D'
headers = {'User-Agent': useragent, 'Cookie': cookie}
driver.get(url)
driver.find_element_by_xpath("// *[ @ id = 'area-box-close']").click()
driver.find_element_by_xpath("//*[@id='search-location']/span[1]").click()
driver.find_element_by_xpath("//*[@id='optionBox']/dl[1]/ul/li[2]/a").click()
req = request.Request(url, headers=headers)
res = request.urlopen(req)
soup = BeautifulSoup(res, 'html.parser')

pages = soup.find_all('a', {'class': 'pageNum-form'})
final_page = pages[-1].text
print('total page: ', final_page)

p = 0
while p < int(final_page):
    req = request.Request(url, headers=headers)
    res = request.urlopen(req)
    soup = BeautifulSoup(res, 'html.parser') 
    tmp_list = []
    for count in range(30):
        pl = driver.find_element_by_xpath(os.path.join('//*[@id="content"]/ul['+str(count + 1)+']/li[2]/h3/a')).get_attribute('href')
        pl = pl.replace('https:', '')
        tmp_list.append(pl)
    
    page_link_list = tmp_list
    print(page_link_list)
    
    from591_find_values.find_values(page_link_list, 3)
    
    time.sleep(5)
    driver.find_element_by_xpath("//a[@class='pageNext']").click()
    time.sleep(5)
    p = p + 1



    
