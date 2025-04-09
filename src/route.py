from flask import Flask, jsonify

from utils.micros  import Micros
from data.manager  import Manager
from utils.visuals import Visuals

# definition
flask   = Flask(__name__)
manager = Manager()
micros  = Micros(manager)
visuals = Visuals(manager)

# utils
json = lambda df: jsonify(df.to_dict())

class Micros:

    @staticmethod
    @flask.route("/<table>/summarise")
    def summarise(table: str):
        return json(micros.summarise(table))

class Visuals:

    @staticmethod
    @flask.route("/<table>/best_brands")
    def best_brands(table: str):
        return {200:visuals.best_brands(table)}

if __name__ == "__main__":
    flask.run(debug=1)