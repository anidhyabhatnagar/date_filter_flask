from pymongo import MongoClient
from datetime import datetime
from datetime import timedelta
from random import randint
from app_configurations import AppConfigurations

app_conf = AppConfigurations('.ini')
username = app_conf.get_value('DEV', 'UserName')
password = app_conf.get_value('DEV', 'Password')
host = app_conf.get_value('DEV', 'Host')

client = MongoClient('mongodb://%s:%s@%s/jobtest?authSource=jobtest' % (username, password, host))
db = client['jobtest']

def generate_data(records=20):
    if db.jobs.find().count() == 0:
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
            "2020-04-02 16:12:20",
            "2020-04-05 23:59:59",
            "2020-04-18 17:45:18",
            "2020-04-20 09:35:26"
            ]
        data = {}
        job_id_list = []
        user_name_list = []
        date_time_list = []
        for i in range(records):
            db.jobs.insert_one({ 
                'job_id': i + 1,
                'user_name': uname[randint(0, 3)],
                'time': datetime.strptime(date[randint(0, 9)], '%Y-%m-%d %H:%M:%S')
            })
    else:
        print("Data exists in database. Skipping data generation.")


def get_job(jobid):
    job = db.jobs.find_one({'job_id' : jobid})
    return job

def add_job(jobid, name, date):
    status = db.jobs.insert_one({'job_id': jobid, 'user_name': name, 'time': date})
    return status

def get_all_jobs():
    jobs = db.jobs.find({}, {'_id': 0})
    return jobs

def get_jobs_for_date(from_date):
    to_date = from_date + timedelta(hours=23,minutes=59,seconds=59)
    jobs = db.jobs.find(
        {'$and': [
            {'time': {'$gte': from_date}},
            {'time': {'$lt': to_date}}
        ]}, 
        {'_id': 0})
    return jobs

def get_jobs_for_date_range(from_date, to_date):
    t_date = to_date + timedelta(hours=23,minutes=59,seconds=59)
    jobs = db.jobs.find(
        {'$and': [
            {'time': {'$gte': from_date}},
            {'time': {'$lt': t_date}}
        ]}, 
        {'_id': 0})
    return jobs
