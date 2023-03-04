import random
from flask import Flask, Response, redirect, render_template, request, session
from twilio.rest import Client
# import json
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from pytz import timezone

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')


if __name__ == '__main__':
    app.secret_key = 'mysecretkey'
    app.run()
    
    
