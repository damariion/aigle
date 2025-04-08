from data.manager import Manager
from pandas       import DataFrame

class Caching:

    def __init__(self, manager: Manager):        
        
        self.memory  = {}
        self.manager = manager

    def cache(self, table: str) -> DataFrame:

        if table not in self.cache:
            
            self.manager.exec(f"SELECT * FROM {table}")
            self.memory[table] = self.manager.fetch()
        
        return self.memory[table]