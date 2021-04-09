from flask import Flask, render_template
import requests
import json
import pymongo
import dns

client = pymongo.MongoClient("mongodb+srv://jai:123@cluster0.ztbk2.mongodb.net")
db = client.stagging
mycol = db['timetable']

app = Flask(__name__)

@app.route('/health')
def health():
    return "Health OK!"

@app.route('/')
def home():
    matches = mycol.find()
    carousel = []
    for i in range(2,8):
        carousel.append('/static/img/ipl'+str(i)+'.jpg')
    images = {"Chennai Super Kings":"/static/img/csk.jpg","Mumbai Indians":"/static/img/mi.jpg","Royal Challengers Bangalore":"/static/img/rcb.jpeg","Delhi Capitals":"/static/img/dc.jpeg","Sunrisers Hyderabad":"/static/img/srh.jpeg","Kolkata Knight Riders":"/static/img/kkr.jpeg","Rajasthan Royals":"/static/img/rr.jpg","Punjab Kings":"/static/img/pk.jpeg"}
    return render_template('home.html',matches = matches,images=images,carousel=carousel)

# @app.route('/match/:matchId')
# def match(matchId):

# @app.route('/player/:pId')
# def player(pId):

@app.errorhandler(404)
def notfound(e):
    return render_template('404.html')



if __name__ =="__main__":
    app.run(debug=True)