# -*- coding: utf-8 -*-
"""
Created on Sat Apr 11 19:50:11 2020

@author: 旬
"""

from flask import Flask
from flask import jsonify
from flask import request
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient("mongodb+srv://user:password@cluster0-7dgxh.mongodb.net/test?retryWrites=true&w=majority")
mydb = client['from591']

@app.route('/deals_taipei_newtaipei', methods=['GET'])
def get_all_deals():
    deal = mydb.deals_taipei_newtaipei
    output = []
    for d in deal.find():
        output.append({'標題': d['標題'], '出租者': d['出租者'], '出租者身分': d['出租者身分'], '聯絡電話': d['聯絡電話'], '型態': d['型態'], \
                       '現況': d['現況'], '性別要求': d['性別要求'], '價格': d['價格'], '地區': d['地區']})
    return jsonify({"result": output})

@app.route('/deals_taipei_newtaipei/', methods=['GET'])
def get_deals_by_gender_place():
    sex_limit = request.args.get('性別要求')
    place = request.args.get('地區')
    phone = request.args.get('聯絡電話')
    owner = request.args.get('出租者')
    owner_id = request.args.get('出租者身分')
    owner_gender = request.args.get('出租者性別')
    female_gender_type = ['媽媽', '小姐', '太太', '女士']
    male_gender_type = ['先生']
    deal = mydb.deals_taipei_newtaipei
    output = []

    for d in deal.find({"$and": [{'性別要求' : sex_limit}, {'地區': place}]}):
        output.append({'標題': d['標題'], '出租者': d['出租者'], '出租者身分': d['出租者身分'], '聯絡電話': d['聯絡電話'], '型態': d['型態'], \
                       '現況': d['現況'], '性別要求': d['性別要求'], '價格': d['價格'], '地區': d['地區']})
            
    for d in deal.find({'聯絡電話' : phone}):
        output.append({'標題': d['標題'], '出租者': d['出租者'], '出租者身分': d['出租者身分'], '聯絡電話': d['聯絡電話'], '型態': d['型態'], \
                       '現況': d['現況'], '性別要求': d['性別要求'], '價格': d['價格'], '地區': d['地區']})
            
    if owner_id == '非屋主':
        for d in deal.find({'出租者身分' : {"$in": ["仲介", "代理人"]}}):
            output.append({'標題': d['標題'], '出租者': d['出租者'], '出租者身分': d['出租者身分'], '聯絡電話': d['聯絡電話'], '型態': d['型態'], \
                            '現況': d['現況'], '性別要求': d['性別要求'], '價格': d['價格'], '地區': d['地區']})
            
    if owner_gender == '女':
        for count in female_gender_type:
            for d in deal.find({"$and": [{'地區': place}, \
                {"$and": [{'出租者': {'$regex':count}}, {'出租者': {'$regex': owner}}]}, {'出租者身分': owner_id}]}):
                output.append({'標題': d['標題'], '出租者': d['出租者'], '出租者身分': d['出租者身分'], '聯絡電話': d['聯絡電話'], \
                               '型態': d['型態'], '現況': d['現況'], '性別要求': d['性別要求'], '價格': d['價格'], '地區': d['地區']})
    else:
        for d in deal.find({"$and": [{'地區': place}, \
           {"$and": [{'出租者': {'$regex':male_gender_type[0]}}, {'出租者': {'$regex': owner}}]}, {'出租者身分': owner_id}]}):
                output.append({'標題': d['標題'], '出租者': d['出租者'], '出租者身分': d['出租者身分'], '聯絡電話': d['聯絡電話'], \
                               '型態': d['型態'], '現況': d['現況'], '性別要求': d['性別要求'], '價格': d['價格'], '地區': d['地區']})
    
            
    return jsonify({"result": output})


@app.route('/')
def test():
    return "this is a test message"

if __name__ == '__main__':
    app.run(debug=True)
