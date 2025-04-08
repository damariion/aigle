from data.manager        import Manager
from utils.caching       import Caching
import matplotlib.pyplot as plt
from os.path             import dirname, join
from datetime            import datetime

class Visuals:

    def __init__(self, manager: Manager):                
        
        self.root    = dirname(dirname(__file__))
        self.caching = Caching(manager)

    def save(self, name):

        date = datetime.now().isoformat()
        date = date.replace(':', '.')[:-10]

        name = join(self.root, "media", f"{name}-{date}.png")
        plt.savefig(name)

        return name

    def best_brands(self, table, n = 5):
        
        # processing
        data = self.caching.cache(table)
        data = data.groupby("brand", as_index=0)["reviews"].sum()
        data = data.sort_values("reviews", ascending=0)
        data = data.head(n) # limit
        
        # configuration
        plt.style.use("ggplot")
        plt.title  ("best performing brands")
        plt.xlabel ("brand")
        plt.ylabel ("5 star reviews")
        plt.xticks (rotation = 45)

        # creation & storage
        plt.bar(data["brand"], data["reviews"])
        plt.tight_layout()
        return self.save("best-performing-brands")
        
        