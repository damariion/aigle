from flask         import Flask, jsonify, request
from utils.storage import Storage

# globals
storage = Storage()
flask   = Flask(__name__)

def validate(spider):
    return spider == "bol"

@flask.route("/scraper/<spider>")
def read(spider: str):
    
    if (not validate(spider)):
        return {}, 404
    
    return storage.read(spider), 200

@flask.route("/scraper/<spider>/head")
def head(spider: str):
    
    if (not validate(spider)):
        return {}, 404
    
    return storage.head(spider), 200

@flask.route("/scraper/<spider>/tail")
def tail(spider: str):
    
    if (not validate(spider)):
        return {}, 404
    
    return storage.tail(spider), 200

@flask.route("/scraper/<spider>/describe")
def describe(spider: str):
    
    if (not validate(spider)):
        return {}, 404
    
    return storage.describe(spider), 200

@flask.route("/scraper/<spider>/sample")
def sample(spider: str):
    
    if (not validate(spider) or "n" not in request.args):
        return {}, 404
    
    return storage.sample(spider, int(request.args["n"])), 200

@flask.route("/scraper/<spider>/column")
def column(spider: str):
    
    if (not validate(spider) or "c" not in request.args):
        return {}, 404
    
    return storage.column(spider, request.args["c"]), 200

@flask.route("/scraper/<spider>/query")
def query(spider: str):
    
    if (not validate(spider) or "q" not in request.args):
        return {}, 404

    return storage.query(spider, request.args["q"]), 200

if __name__ == "__main__": 
    flask.run(debug=True)