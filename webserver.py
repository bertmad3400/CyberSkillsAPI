#!/usr/bin/python3
from flask import Flask, Response, redirect, url_for

import json
import os

from datetime import datetime

app = Flask(__name__)

def listAllowedDates():
    allowedDates = []
    for fileName in os.listdir("./events"):
        year = fileName.split(";")[0]
        month = fileName.split(";")[1].split(".")[0]
        allowedDates.append({ "year" : year, "month" : month })
    return allowedDates

@app.route("/allowedDates/")
def showAllowedDates():
    return Response(json.dumps(listAllowedDates()), mimetype="application/json")

@app.route("/<string:year>/<string:month>/")
def sendEventsJSON(year, month):
    if { "year" : year, "month" : month } in listAllowedDates():
        with open(f"./events/{year};{month}.json") as eventFile:
            return Response(json.dumps(json.load(eventFile)), mimetype="application/json")
    else:
        return "Didn't recognize either year or month", 422

@app.route("/currentEvents/")
def listCurrentEvents():
    return redirect(url_for("sendEventsJSON", year=str(datetime.now().year), month=str(datetime.now().strftime("%B"))))

@app.route("/allEvents/")
def listAllEvents():
    with open("./allEvents.json") as eventFile:
        return Response(json.dumps(json.load(eventFile)), mimetype="application/json")

@app.route("/nextEvents/<int:numberOfEvents>/")
def listNextEvents(numberOfEvents):
    with open("./allEvents.json") as eventFile:
        allEvents = json.load(eventFile)

    nextEvents = sorted([ event for event in allEvents if datetime.strptime(event['date'], '%d %b %Y') > datetime.now() ], key = lambda event : datetime.strptime(event['date'], '%d %b %Y'))[:numberOfEvents]


    return Response(json.dumps(nextEvents), mimetype="application/json")

if __name__ == '__main__':
    app.run(debug=True)
