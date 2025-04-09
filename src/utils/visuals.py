from os.path             import dirname, join
from datetime            import datetime
from matplotlib          import use
from data.manager        import Manager
from utils.caching       import Caching
import matplotlib.pyplot as plt

class Visuals:

    def __init__(self, manager: Manager):                
        
        self.root    = dirname(dirname(__file__))
        self.caching = Caching(manager)
        
        # configuration
        use('Agg')

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
        _, ax = plt.subplots()  # this is key for safety
        
        ax.set_title  ("best performing brands")
        ax.set_xlabel ("brand")
        ax.set_ylabel ("5 star reviews")
        plt.xticks    (rotation = 45)

        # creation & storage
        plt.bar(data["brand"], data["reviews"])
        return self.save("best-performing-brands")
        
        