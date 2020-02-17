# kg-weather-reporter
A weather reporter for Krace Gennedy (an evaluation project for Particular Presence Technologies)
Flask was considered to be used as it is easy to deploy and I started learning it recently

Resources:
https://github.com/uwi-info3180/flask-db-demo
https://flask-sqlalchemy.palletsprojects.com/
https://github.com/sagunsh/weather-app
https://pythonhosted.org/
https://gist.github.com/keeguon/2310008
https://www.twilio.com/blog
https://github.com/theskumar/python-dotenv
https://openweathermap.org/
https://www.twilio.com/blog/2018/03/send-email-programmatically-with-gmail-python-and-flask.html

It is necessary to create the .env file so it can be functional on one's system. Linux was used to create this project. Hence, 
some features may encounter an issue
#####################.env file format:#######################
export TESTENV="HELLOWORD"#for tesing purposes
export SECRET_KEY='some random string'
export MAIL_USERNAME='my email address'
export MAIL_PASSWORD='my email address password'
export WEATHER_API_KEY='my openweathermap.org/api api key'
#############################################################
