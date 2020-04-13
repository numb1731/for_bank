from urllib import request
from bs4 import BeautifulSoup
import re, os
import time
import connect_to_Mongo
useragent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'
headers = {'User-Agent': useragent}


def find_values(lists, placetag):
    for link in lists:
        url = os.path.join('https:' + link)
        print(url)
        req = request.Request(url, headers=headers)
        res = request.urlopen(req)
        soup = BeautifulSoup(res, 'html.parser')

        house_info = soup.find('div', {'class': 'main_house_info clearfix'})
        # 標題
        name = house_info.find('span', {'class': 'houseInfoTitle'}).text
        time.sleep(2)
        # 出租者
        try:
            owner_des = house_info.find('div', {'class': 'avatarRight'}).text
            owner_des = owner_des.replace('）', '')
            owner_des = owner_des.replace(')', '')
            owner_des = owner_des.replace('（', ',')
            owner_des = owner_des.replace('(', ',')
            owner_des = owner_des.split(',')
            owner = owner_des[0].replace('\n', '')
            time.sleep(2)
            # 出租者身分
            if re.search('^屋主', owner_des[1]):
                owner_id = '屋主'
            elif re.search('^仲介', owner_des[1]):
                owner_id = '仲介'
            else:
                owner_id = owner_des[1].replace('\n', '')
            time.sleep(2)
            # 電話號碼 #圖片
            phone_span = house_info.find('span', {'class': 'dialPhoneNum'})
            phone_num = phone_span['data-value']
            time.sleep(2)

            # 型態
            house = house_info.find('ul', {'class': 'attr'})
            house = house.find_all('li')
            for tmp in house:
                if re.search('型態', tmp.text):
                    house_type = tmp.text
                    house_type = house_type.split(':')[1].replace('\xa0', '')
                    break
                else:
                    house_type = 'None'
            time.sleep(2)

            # 現況
            for tmp in house:
                if re.search('現況', tmp.text):
                    status = tmp.text
                    status = status.split(':')[1].replace('\xa0', '')
                    break
                else:
                    status = 'None'
            time.sleep(2)

            # 性別要求
            cond = []
            for page in house_info.find_all('div', {'class': 'leftBox'}):
                page_ul = page.find('ul', {'class': 'clearfix labelList labelList-1'})
                page_em = page_ul.find_all('em')
                for tmp in page_em:
                    cond.append(tmp.text)
            for tmp in cond:
                if re.search('男', tmp) or re.search('女', tmp):
                    sex_limit = tmp
                    break
                else:
                    sex_limit = 'None'
            time.sleep(3)

            # 價格
            price = house_info.find('div', {'class': 'price clearfix'})
            price = price.text.replace('\n', '')

            #地區
            if placetag == 1:
                place = '臺北'
            else:
                place = '新北'

            house_dict = {
                '標題': name,
                '出租者': owner,
                '出租者身分': owner_id,
                '聯絡電話': phone_num,
                '型態': house_type,
                '現況': status,
                '性別要求': sex_limit,
                '價格': price,
                '地區': place
            }
            print(house_dict)
            connect_to_Mongo.send_to_Mongo(house_dict)
        except AttributeError as err:
            print(name, err)
