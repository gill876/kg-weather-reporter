from app import app
from flask import render_template, request, redirect, url_for, flash
from app.models import Worker
from . import db
from .forms import WorkerF
from app import mail
from flask_mail import Message
import requests
import json
import os
from dotenv import load_dotenv
from datetime import datetime
load_dotenv(verbose=True)

@app.route('/')
def home():
    """Render website's home page."""
    #db.create_all()
    #test1 = type(os.getenv("TESTENV")) 
    now = datetime.now()
    hour_start = 2
    """test1 = "failed"
    if request.method == 'GET':
        test1 = request.form['submitb']
        flash('Successful!', 'success')"""
    time = now.strftime("%H:%M")
    greeting_time = "Good afternoon" if (int(now.strftime("%H")) >= 12) else "Good morning"

    boss = Worker.query.filter_by(role='Manager').first()
    city = boss.city
    state = boss.state
    country = boss.country
    loadDays = getDays()
    forecasts = forecaster(city, state, country, hour_start)
    outputs = zip(forecasts, loadDays)
    return render_template('home.html', time=time, greeting_time=greeting_time, outputs= outputs)

@app.route('/addworker', methods=['GET', 'POST'])
def addWorker():
    workerF = WorkerF()
    if request.method == 'POST':
        if workerF.validate_on_submit():
            fname = workerF.fname.data
            lname = workerF.lname.data
            address1 = workerF.address1.data
            city = workerF.city.data
            state = workerF.state.data
            country = workerF.country.data
            telephone = workerF.telephone.data
            role = workerF.role.data
            email = workerF.email.data

            worker = Worker(fname, lname, address1, city, state, country, telephone, role, email)
            db.session.add(worker)
            db.session.commit()
            
            flash('Worker successfully added!', 'success')
            return redirect(url_for('home'))

        flash_errors(worker)
    return render_template('addworker.html', form=workerF)

@app.route('/viewworkers')
def viewWorkers():
    workers = Worker.query.all()
    return render_template('viewworkers.html', workers=workers)

@app.route('/etest')
def send_email():
    with app.app_context():
        msg = Message(subject="Email test",
                      sender=app.config.get("MAIL_USERNAME"),
                      recipients=["microcargill@hotmail.com"],
                      body="This is a test email I sent with Gmail and Python!")
        mail.send(msg)
    return 'email sent'

@app.route('/wtest')
#@app.route('/wtest/<city>')
def search_city(city='Duncans', state='Trelawny', country='Jamaica'):
    API_KEY = os.getenv("WEATHER_API_KEY")  # initialize your key here
    jsonccode = None 
    ccode = None
    #return app.send_static_file(url_for('static', filename='/json/countries.json'))
    with open(os.path.dirname(os.path.abspath(__file__)) + '/static/json/countries.json') as f: #this file directory format might not work in Windows
        jsonccode = json.load(f)
    for c_dict in jsonccode:
        if c_dict.get('name') == country:
            ccode = c_dict.get('code')

    # call API and convert response into Python dictionary
    url = f'http://api.openweathermap.org/data/2.5/forecast?q={city},{state},{ccode}&appid={API_KEY}'
    response = requests.get(url).json()

    #return response

    # error like unknown city name, inavalid api key
    if response.get("cod") != "200":
        message = response.get('message', '')
        return f'Error getting weather information for {city.title()}. Error message = {message}'

    forecast = []
    for i in range(2,40,8): #retrieves weather for five days at 6AM
	    forecast+= [response.get('list')[i].get('weather')[0].get('main')]
    
    return render_template('home.html', test1 = forecast)

def forecaster(city, state, country, hour_start):#Documentation for this function is in search_city()
    API_KEY = os.getenv("WEATHER_API_KEY")
    jsonccode = None 
    ccode = None

    with open(os.path.dirname(os.path.abspath(__file__)) + '/static/json/countries.json') as f: #this file directory format might not work in Windows
        jsonccode = json.load(f)
    for c_dict in jsonccode:
        if c_dict.get('name') == country:
            ccode = c_dict.get('code')

    url = f'http://api.openweathermap.org/data/2.5/forecast?q={city},{state},{ccode}&appid={API_KEY}'
    response = requests.get(url).json()

    if response.get("cod") != "200":
        message = response.get('message', '')
        return f'Error getting weather information for {city.title()}. Error message = {message}'

    forecasts = []
    for i in range(hour_start,40,8): #retrieves weather for the given hour period of the day eg: 0 => 00:00 - 02:59, 2 => 06:00-08:59
	    forecasts+= [response.get('list')[i].get('weather')[0].get('main')]
    
    return forecasts

def getDays():
    day = datetime.today().weekday()
    loadDays = []
    day_lst = ['Mon', 'Tue', 'Wed', 'Thur', 'Fri', 'Sat', 'Sun']

    for i in range(0,5):
        #loadDays+= [day_lst[day]]
        if day > 6:
            day = 0
            loadDays+= [day_lst[day]]
            day+=1
        else:
            loadDays+=[day_lst[day]]
            day+=1
    return loadDays

@app.route('/tomorrow')
def sendTomorrow():
    workers = Worker.query.all()
    boss = Worker.query.filter_by(role='Manager').first()
    hour_start = 2 #time for 06:00-08:59
    with mail.connect() as conn:
        for worker in workers:
            
            tomorrow_forecast = forecaster(worker.city, worker.state, worker.country, hour_start)

            if tomorrow_forecast[1] == 'Rain': #forecast for tomorrow
                if worker.role == "IT":
                    message = "Do not go on the road tomorrow\n\n\n\nRegards, {} {}".format(boss.fname, boss.lname)
                else:
                    message = "You are going to work for 4 hours tomorrow instead of 8 hours\n\n\n\nRegards, {} {}".format(boss.fname, boss.lname)
            else:
                if worker.role == "IT":
                    message = "Have fun at work tomorrow!\n\n\n\nRegards, {} {}".format(boss.fname, boss.lname)
                else:
                    message = "You will be working for 8 hours tomorrow\n\n\n\nRegards, {} {}".format(boss.fname, boss.lname)

            subject = "Work for tomorrow, Mr.%s" % worker.lname
            msg = Message(recipients=[worker.email],
                        sender=app.config.get("MAIL_USERNAME"),
                        body=message,
                        subject=subject)

            conn.send(msg)
    flash('Email notification sent to all workers!', 'success')
    return redirect(url_for('home'))

###
# The functions below should be applicable to all Flask apps.
###

@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404

# Flash errors from the form if validation fails
def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ), 'danger')

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port="8080")
