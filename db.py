import pymongo
import glob
from pymongo import MongoClient
from datetime import datetime
from datetime import timedelta
from random import randint
from bson.binary import Binary
from bson.objectid import ObjectId
import base64


client = MongoClient('localhost', 27017)
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

    image_list = glob.glob1("img/","*.jpg")
    if db.images.find().count() == 0:
        print("Image Data Not Found! Generating Image Data with {} images.".format(len(image_list)))
        for img_name in image_list:
            with open('img/' + img_name, 'rb') as f:
                byte_im = f.read()

            binary_image = Binary(byte_im)
            name = img_name.split('.')[0].strip().capitalize()
            db.images.insert_one({'name': name, 'image': binary_image})
    else:
        print("Image Data exists in databse. Skipping Images data generation.")


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

def get_image_from_db():
    record = db.images.find_one()
    img = record['image']
    name = record['name']
    dbid = record['_id']
    imgbase = base64.b64encode(img)
    imgbase = imgbase.decode("utf-8")
    return dbid, imgbase, name

def get_next_image_from_db(id):
    img = name = dbid = ''
    oid = ObjectId(id)
    records = db.images.find({'_id': {'$gt': oid}}).sort([('_id', pymongo.ASCENDING)]).limit(1)
    for record in records:
        img = record['image']
        name = record['name']
        dbid = record['_id']
        imgbase = base64.b64encode(img)
        imgbase = imgbase.decode("utf-8")
        return dbid, imgbase, name, True
    else:
        record = db.images.find_one({'_id': oid})
        id = record['_id']
        name = record['name']
        img = record['image']
        imgbase = base64.b64encode(img)
        imgbase = imgbase.decode("utf-8")
    return id, imgbase, name, False

def get_previous_image_from_db(id):
    img = name = dbid = ''
    oid = ObjectId(id)
    records = db.images.find({'_id': {'$lt': oid}}).sort([('_id', pymongo.DESCENDING)]).limit(1)
    for record in records:
        img = record['image']
        name = record['name']
        dbid = record['_id']
        imgbase = base64.b64encode(img)
        imgbase = imgbase.decode("utf-8")
        return dbid, imgbase, name, True
    else:
        record = db.images.find_one({'_id': oid})
        id = record['_id']
        name = record['name']
        img = record['image']
        imgbase = base64.b64encode(img)
        imgbase = imgbase.decode("utf-8")
    return id, imgbase, name, False

def insert_uploaded_image_to_db(image, image_title):
    byte_im = image.read()
    binary_image = Binary(byte_im)
    name = image_title
    db.images.insert_one({'name': name, 'image': binary_image})