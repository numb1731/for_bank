from urllib import request
from bs4 import BeautifulSoup
import re, time, os
import from591_find_values
from selenium import webdriver
chromedriver = './chromedriver'
driver = webdriver.Chrome(chromedriver)

place_num = [1, 3]

for num in place_num:
    url = os.path.join('https://rent.591.com.tw/?kind=0&region='+ str(num))
    useragent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'
    cookie = 'webp=1; PHPSESSID=b9lbhu6fciq49dv70lr8dd7b61; urlJumpIp=1; urlJumpIpByTxt=%E5%8F%B0%E5%8C%97%E5%B8%82; new_rent_list_kind_test=1; T591_TOKEN=b9lbhu6fciq49dv70lr8dd7b61; c10f3143a018a0513ebe1e8d27b5391c=1; _ga=GA1.3.557136261.1586498565; _gid=GA1.3.959731503.1586498565; _ga=GA1.4.557136261.1586498565; _gid=GA1.4.959731503.1586498565; tw591__privacy_agree=0; XSRF-TOKEN=eyJpdiI6IkErQnJvSHFEclZtTG5Sck9TTytQVlE9PSIsInZhbHVlIjoiaXRZY3M1ZTFuS09jZU9tS08xeHkxZ3hGVDZlQ2lLa09iY1poYWlPdVZiZ3AyYk5zdWpKZndwRzk4eDVoK2MyR1wvdEJGcEFuNUpPYStTVVNEQ0VjcTZnPT0iLCJtYWMiOiI3OTc3NjkzOTRlMWM0MTJmOTU4YTY0MmFkMmZkMjFmZjA5NTA3ZWY1YWVjNjE0ZmIxMGYyZTY5NzEwZjVmZDk4In0%3D; 591_new_session=eyJpdiI6IkpMOHI1d0trVDcyWjZwSE5IaEpUb0E9PSIsInZhbHVlIjoiYlhvZng5ZDBvcTR5Q3JtdTNtMjVCajF0blpLZWdLb2RDeTB0K3I2OEVmY0JhaGhMR09XaEpPWW9wVFwvcmw5SUw0SDVQbXJWTWhKUjBwWDVTMGh0RkRRPT0iLCJtYWMiOiJjMzBlMTgzMWFiYmVhNWE5YmVhZmY3Mjc4MGQyYWViYzBhYjQ2MWEzMTM5YTdkMjU5OWJhNjc5MzQ4N2ZiMWZjIn0%3D'
    headers = {'User-Agent': useragent, 'Cookie': cookie}
    req = request.Request(url, headers=headers)
    res = request.urlopen(req)
    soup = BeautifulSoup(res, 'html.parser')
    driver.get(url)

    pages = soup.find_all('a', {'class': 'pageNum-form'})
    final_page = pages[-1].text
    print('total page: ', final_page)

    p = 0
    while p < int(final_page):
        req = request.Request(url, headers=headers)
        res = request.urlopen(req)
        soup = BeautifulSoup(res, 'html.parser')

        page_link_list = []
        for page in soup.find_all('ul', {'class': 'listInfo clearfix'}):
            for page_li in page.find_all('li', {'class': 'pull-left infoContent'}):
                for page_a in page_li.find_all('a'):
                    page_link_list.append(page_a['href'])

        tmp_list = []
        page_link_list = list(set(page_link_list))
        for page_link in page_link_list:
            if re.search('rent-detail', page_link):
                tmp_list.append(page_link)

        page_link_list = tmp_list

        from591_find_values.find_values(page_link_list, num)
        if p == 0:
            driver.find_element_by_xpath("// *[ @ id = 'area-box-close']").click()
        time.sleep(5)
        driver.find_element_by_xpath("//a[@class='pageNext']").click()
        time.sleep(5)
        p = p + 1