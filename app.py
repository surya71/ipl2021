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

# @app.route('/match/:matchId')
# def match(matchId):
@app.route('/squad/<int:team>/<int:matchId>')
def squad(team,matchId):
    squad = requests.get('https://cricapi.com/api/fantasySquad?apikey=boIC5DMYOVTMW5JVb4yS1qILyaw2&unique_id='+str(matchId))
    squad = squad.json()
    return render_template("squad.html",squad = squad['squad'][team])

@app.route('/player/<int:pId>')
def player(pId):
    player = requests.get('https://cricapi.com/api/playerStats?apikey=boIC5DMYOVTMW5JVb4yS1qILyaw2&pid='+str(pId))
    player = player.json()
    print(player)
    # player ={'pid': 625383, 'country': 'India', 'profile': "\n\nJasprit Bumrah grabbed eyeballs first with his unorthodox action, and then his bowling skills. Armed with an anomalous, sling-arm action and natural pace, the peculiar release point of Bumrah's deliveries makes it hard for batsmen to pick him.  \n\n", 'imageURL': 'https://www.cricapi.com/playerpic/625383.jpg', 'battingStyle': 'Right-hand bat', 'bowlingStyle': 'Right-arm fast', 'majorTeams': 'India,Gujarat,India A,India Under-23s,Mumbai Indians', 'currentAge': '25 years 327 days', 'born': 'December 6, 1993, Ahmedabad', 'fullName': 'Jasprit Jasbirsingh Bumrah', 'name': 'Jasprit Bumrah', 'playingRole': 'Bowler', 'v': '2', 'data': {'bowling': {'listA': {'10': '0', '5w': '2', '4w': '8', 'SR': '28.1', 'Econ': '4.33', 'Ave': '20.35', 'BBM': '5/27', 'BBI': '5/27', 'Wkts': '155', 'Runs': '3155', 'Balls': '4364', 'Inns': '83', 'Mat': '83'}, 'firstClass': {'10': '0', '5w': '11', '4w': '3', 'SR': '51.1', 'Econ': '2.67', 'Ave': '22.83', 'BBM': '9/86', 'BBI': '6/27', 'Wkts': '151', 'Runs': '3448', 'Balls': '7725', 'Inns': '66', 'Mat': '38'}, 'T20Is': {'10': '0', '5w': '0', '4w': '0', 'SR': '18.0', 'Econ': '6.71', 'Ave': '20.17', 'BBM': '3/11', 'BBI': '3/11', 'Wkts': '51', 'Runs': '1029', 'Balls': '919', 'Inns': '42', 'Mat': '42'}, 'ODIs': {'10': '0', '5w': '1', '4w': '5', 'SR': '29.2', 'Econ': '4.49', 'Ave': '21.88', 'BBM': '5/27', 'BBI': '5/27', 'Wkts': '103', 'Runs': '2254', 'Balls': '3009', 'Inns': '58', 'Mat': '58'}, 'tests': {'10': '0', '5w': '5', '4w': '0', 'SR': '43.7', 'Econ': '2.64', 'Ave': '19.24', 'BBM': '9/86', 'BBI': '6/27', 'Wkts': '62', 'Runs': '1193', 'Balls': '2711', 'Inns': '24', 'Mat': '12'}}, 'batting': {'listA': {'50': '0', '100': '0', 'St': '0', 'Ct': '25', '6s': '4', '4s': '7', 'SR': '81.18', 'BF': '101', 'Ave': '7.45', 'HS': '42*', 'Runs': '82', 'NO': '15', 'Inns': '26', 'Mat': '83'}, 'firstClass': {'50': '0', '100': '0', 'St': '0', 'Ct': '12', '6s': '0', '4s': '16', 'SR': '23.27', 'BF': '593', 'Ave': '7.66', 'HS': '16*', 'Runs': '138', 'NO': '27', 'Inns': '45', 'Mat': '38'}, 'T20Is': {'50': '0', '100': '0', 'St': '0', 'Ct': '6', '6s': '0', '4s': '1', 'SR': '61.53', 'BF': '13', 'Ave': '4.00', 'HS': '7', 'Runs': '8', 'NO': '4', 'Inns': '6', 'Mat': '42'}, 'ODIs': {'50': '0', '100': '0', 'St': '0', 'Ct': '17', '6s': '1', '4s': '2', 'SR': '44.18', 'BF': '43', 'Ave': '3.80', 'HS': '10*', 'Runs': '19', 'NO': '8', 'Inns': '13', 'Mat': '58'}, 'tests': {'50': '0', '100': '0', 'St': '0', 'Ct': '3', '6s': '0', '4s': '1', 'SR': '14.87', 'BF': '121', 'Ave': '2.00', 'HS': '6', 'Runs': '18', 'NO': '8', 'Inns': '17', 'Mat': '12'}}}, 'ttl': 1, 'provider': {'source': 'Various', 'url': 'https://cricapi.com/', 'pubDate': '2021-04-10T08:35:47.413Z'}, 'creditsLeft': 250}
    return render_template("player.html",player=player)

@app.route('/check')
def check():
    return render_template('sample.html',data=scrap.getLiveScore(5))
@app.errorhandler(404)
def notfound(e):
    return render_template('404.html')



if __name__ =="__main__":
    app.run(debug=True)