from flask import Flask

from ..utils.micros  import Micros
from ..utils.caching import Manager
from ..utils.visuals import Visuals

# definition
flask   = Flask(__name__)
manager = Manager()
micros  = Micros(manager)
visuals = Visuals(manager)

class Micros:

    @staticmethod
    @flask.route("<table>/summarise")
    def summarise(table: str):
        return micros.summarise(table).to_json()

class Visuals:

    @staticmethod
    @flask.route("<table>/best_brands")
    def best_brands(table: str):
        return {200:visuals.best_brands(table)}

if __name__ == "__main__":
    flask.run(debug=1)