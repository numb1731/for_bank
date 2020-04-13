import pymongo

def send_to_Mongo(house_dict):
    client = pymongo.MongoClient("mongodb+srv://user:password@cluster0-7dgxh.mongodb.net/test?retryWrites=true&w=majority")
    # db = client.test
    database = client['from591']
    collection =  database['deals_taipei_newtaipei']

    collection.insert_one(house_dict)
