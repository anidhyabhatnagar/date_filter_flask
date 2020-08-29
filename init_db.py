from pymongo import MongoClient
from datetime import datetime
from datetime import timedelta
from random import randint

import configparser

config = configparser.ConfigParser()
config.read('.ini')

username = config['DEV']['UserName']
password = config['DEV']['Password']
host = config['DEV']['Host']

client = MongoClient('mongodb://%s:%s@%s/jobtest?authSource=jobtest' % (username, password, host))
db = client['jobtest']

def generate_data(records=20):
    if db.jobtest.find().count() == 0:
        print("Data Not Found! Generating Data with {} records.".format(records))
        uname = [
            'Anidhya Bhatnagar',
            'Nishanth Chandrasekar',
            'Yashwant Chouhan',
            'Manikandan P'
            ]
        date = [
            "2020-03-01 22:10:57",
            "2020-03-09 01:45:21",
            "2020-03-12 05:06:09",
            "2020-03-15 12:16:40",
            "2020-03-25 00:00:00",
            "2020-04-02 00:00:01",
            "2020-04-05 23:59:59"
            ]
        data = {}
        job_id_list = []
        user_name_list = []
        date_time_list = []
        for i in range(records):
            db.jobs.insert_one({ 
                'job_id': i + 1,
                'user_name': uname[randint(0, 3)],
                'time': datetime.strptime(date[randint(0, 6)], '%Y-%m-%d %H:%M:%S')
            })
    else:
        print("Data exists in database. Skipping data generation.")
