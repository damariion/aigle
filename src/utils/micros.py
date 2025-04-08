from data.manager import Manager
from caching      import Caching

class Micros:

    def __init__(self, manager: Manager):        
        self.caching = Caching(manager)
    
    # basic stats (min, max, mean, etc)
    summarise = lambda self, table: \
        self.caching.cache(table).describe()
    
    # specific row on index
    index = lambda self, table, a, b = -1, c = 1: \
        self.caching.cache(table).iloc[a:b+1|a+1:c]