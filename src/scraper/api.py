from flask          import Flask, request
from utils.storage  import Storage
from os             import listdir
from scrapy.crawler import CrawlerProcess
from os.path        import dirname, abspath, join as pjoin

# spiders
from spiders.bol    import Bol

# globals
storage = Storage()
flask   = Flask(__name__)

@flask.route("/scraper/refresh", methods=["POST"])
def refresh():
    
    # overwrite with new instance
    global storage 
    del storage
    
    # reinitialise
    storage = Storage()
    return {200: "refreshed"}, 200

@flask.route("/scraper/<spider>/scrape", methods=["POST"])
def scrape(spider: str):
    
    spiders = {
        "bol": (Bol, "https://www.bol.com/nl/nl/l/keukengerei/11"
                     "785/?12194=2-100&rating=5&availability=non")
    }

    crawler = CrawlerProcess({'RANDOMIZE_DOWNLOAD_DELAY': True})
    crawler.crawl(
        spiders[spider][0],
        storage = storage,
        url     = spiders[spider][1])
    crawler.start()

    storage.database.commit()
    return {200:f"{spider} scraped"}, 200

# micros
def template(spider: str, delegate: callable, letters: list = []):
    
    # dynamic path detection
    root    = dirname(abspath(__file__))
    spiders = listdir(pjoin(root, "spiders"))

    # spider validation
    if (f"{spider}.py" not in spiders):
        return {404:"invalid spider"}, 404
    
    # argument validation
    for letter in letters:
        if (letter not in request.args.keys()):
            return {404:"invalid arguments"}, 404
    
    return delegate(), 200

@flask.route("/scraper/<spider>")
def read(spider: str): 
    return template(spider, lambda: storage.read(spider))

@flask.route("/scraper/<spider>/describe")
def describe(spider: str): return template(
    spider, lambda: storage.describe(spider))

@flask.route("/scraper/<spider>/memory")
def memory(spider: str): return template(
    spider, lambda: storage.memory(spider))

@flask.route("/scraper/<spider>/head")
def head(spider: str): return template(
        spider, lambda: storage.head(spider, int(request.args['n'])), ['n'])

@flask.route("/scraper/<spider>/index")
def index(spider: str): return template(
        spider, lambda: storage.index(spider, int(request.args['n'])), ['n'])

@flask.route("/scraper/<spider>/tail")
def tail(spider: str): return template(
    spider, lambda: storage.tail(spider, int(request.args['n'])), ['n'])

@flask.route("/scraper/<spider>/sample")
def sample(spider: str): return template(
    spider, lambda: storage.sample(spider, int(request.args['n'])), ['n'])

@flask.route("/scraper/<spider>/column")
def column(spider: str): return template(
    spider, lambda: storage.column(spider, request.args['c']), ['c'])

@flask.route("/scraper/<spider>/query")
def query(spider: str): return template(
    spider, lambda: storage.query(spider, int(request.args['q'])), ['q'])

if __name__ == "__main__": 
    
    flask.run(debug=True)
    del storage