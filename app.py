from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import session
from flask import url_for
from flask import g
from flask import current_app
from datetime import datetime
import functools
import flask 
from db import *


app = Flask(__name__)

@app.route("/")
def index():
    generate_data(25)
    return render_template('index.html')

@app.route("/jobsreport", methods=["GET", "POST"])
def jobsreport():
    jobs = {}
    if request.method == "POST":
        from_date = request.form['fromdate']
        to_date = request.form['todate']
        fdate = datetime.strptime(from_date, '%Y-%m-%d')
        tdate = datetime.strptime(to_date, '%Y-%m-%d')
        #jobs = get_jobs_for_date(fdate)
        jobs = get_jobs_for_date_range(fdate, tdate)
    else:
        jobs = get_all_jobs()
    return render_template('jobsreport.html', jobs=jobs)

@app.route("/daywisejobs", methods=["GET", "POST"])
def daywisejobs():
    if request.method == "POST":
        day = request.form['date']
        date = datetime.strptime(day, '%Y-%m-%d')
        jobs = get_jobs_for_date(date)
    else:
        jobs = get_all_jobs()
    return render_template('daywisejobs.html', jobs=jobs)

@app.route("/addjob", methods=["GET", "POST"])
def addjob():
    if request.method == "POST":
        job_id = int(request.form['jobid'])
        name = request.form['name']
        date = request.form['date']
        fdate = datetime.strptime(date, '%Y-%m-%d')
        status = add_job(job_id, name, fdate)
        print("Job ID: {} \t Name: {} \t Date: {} \t Status: {}".format(job_id, name, date, status))
    else:
        print("Inside Else")
    return render_template('addjob.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0')
