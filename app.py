from flask import Flask, render_template
import requests
import json
import pymongo
import dns
import scrap
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

@app.route('/squad/<int:team>/<int:matchId>')
def squad(team,matchId):
    squad = requests.get('https://cricapi.com/api/fantasySquad?apikey=boIC5DMYOVTMW5JVb4yS1qILyaw2&unique_id='+str(matchId))
    squad = squad.json()
    return render_template("squad.html",squad = squad['squad'][team])

@app.route('/player/<int:pId>')
def player(pId):
    player = requests.get('https://cricapi.com/api/playerStats?apikey=boIC5DMYOVTMW5JVb4yS1qILyaw2&pid='+str(pId))
    player = player.json()
    return render_template("player.html",player=player)

@app.route('/livescore/<int:unique_id>')
def livescore(unique_id):
    x = mycol.find({'unique_id':unique_id})
    match = requests.get("https://cricapi.com/api/fantasySummary?apikey=boIC5DMYOVTMW5JVb4yS1qILyaw2&unique_id="+str(unique_id))
    match = match.json()
    if 'matchStarted' not in match['data']:
        return render_template('livescore.html',started = False)
    for i in x:
        url = i['url']
    livescore,comment = scrap.getLiveScore(url)
    return render_template('livescore.html',started = True,livescore=livescore,comment = comment)


@app.errorhandler(404)
def notfound(e):
    return render_template('404.html')



if __name__ =="__main__":
    app.run(port=5000,debug=True)