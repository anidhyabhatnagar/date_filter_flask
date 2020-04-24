from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import session
from flask import url_for
from flask import g
from flask import current_app
from datetime import datetime
from waitress import serve
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
    else:
        pass
    return render_template('addjob.html')

@app.route("/viewimage", methods=["GET", "POST"])
def viewimage():
    dbid, img, name = get_image_from_db()
    return render_template('viewimage.html', image=img, id=dbid, name=name, isprev=False, isnext=True)

@app.route('/next/', methods=["POST"])
def next():
    if request.method == "POST":
        id = request.form['id']
        dbid, img, name, isnext = get_next_image_from_db(id)
    return render_template('viewimage.html', id=dbid, image=img, name=name, isnext=isnext, isprev=True)

@app.route('/previous/', methods=["POST"])
def previous():
    if request.method == "POST":
        id = request.form['id']
        dbid, img, name, isprev = get_previous_image_from_db(id)
    return render_template('viewimage.html', id=dbid, image=img, name=name, isprev=isprev, isnext=True)

if __name__ == "__main__":
    #app.run(host='0.0.0.0')
    serve(app, host='0.0.0.0', port=5000)
