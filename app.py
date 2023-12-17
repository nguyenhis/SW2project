import json
import os
import mysql.connector
from dotenv import load_dotenv
from flask import Flask, request
from flask_cors import CORS
import config
from game import Game

load_dotenv()

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# Database connection
config.conn = mysql.connector.connect(
    host=os.environ.get('127.0.0.1'),  # Use your actual host
    port=3306,
    database=os.environ.get('flight_game'),  # Use your actual database name
    user=os.environ.get('dbuser'),  # Use your actual database user
    password=os.environ.get('new_password'),  # Use your actual database password
    autocommit=True
)
cur = config.conn.cursor()

# Select the database
cur.execute("USE flight_game")

def fly(id, dest, consumption=0, player=None):
    if id == 0:
        game = Game(0, dest, consumption, player)
    else:
        game = Game(id, dest, consumption)
    game.location[0].fetchWeather(game)
    nearby = game.location[0].find_nearby_airports()
    for a in nearby:
        game.location.append(a)
    json_data = json.dumps(game, default=lambda o: o.__dict__, indent=4)
    return json_data

@app.route('/flyto')
def flyto():
    args = request.args
    id = args.get("game")
    dest = args.get("dest")
    consumption = args.get("consumption")
    json_data = fly(id, dest, consumption)
    print("*** Called flyto endpoint ***")
    return json_data

@app.route('/newgame')
def newgame():
    args = request.args
    player = args.get("player")
    dest = args.get("loc")
    json_data = fly(0, dest, 0, player)
    return json_data

if __name__ == '__main__':
    app.run(use_reloader=True, host='127.0.0.1', port=3000)
