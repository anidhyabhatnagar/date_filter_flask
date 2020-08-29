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
from werkzeug.utils import secure_filename
import os
import functools
import flask 
from db import generate_data, get_all_jobs, get_jobs_for_date, get_jobs_for_date_range, get_job, add_job

DATE_FORMAT = '%Y-%m-%d'

from db import *
from flask.helpers import flash


UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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
        fdate = datetime.strptime(from_date, DATE_FORMAT)
        tdate = datetime.strptime(to_date, DATE_FORMAT)
        jobs = get_jobs_for_date_range(fdate, tdate)
    else:
        jobs = get_all_jobs()
    return render_template('jobsreport.html', jobs=jobs)

@app.route("/daywisejobs", methods=["GET", "POST"])
def daywisejobs():
    if request.method == "POST":
        day = request.form['date']
        date = datetime.strptime(day, DATE_FORMAT)
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
        fdate = datetime.strptime(date, DATE_FORMAT)
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

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/uploadimage', methods=["GET", "POST"])
def uploadimage():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'uploadimage' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['uploadimage']
        image_title = request.form['name']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            insert_uploaded_image_to_db(file, image_title)
            return render_template('uploadimage.html', filename=filename)
    return render_template('uploadimage.html')

if __name__ == "__main__":
    serve(app, host='0.0.0.0', port=5000)
    app.secret_key = 'c4d26589e751e52f639b5bf64390a30a'
    app.run(host='0.0.0.0')
