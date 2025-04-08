from pandas       import DataFrame
from data.manager import Manager

class Caching:

    def __init__(self, manager: Manager):        
        
        self.memory  = {}
        self.manager = manager

    def cache(self, table: str) -> DataFrame:

        if table not in self.memory:
            
            self.manager.exec(f"SELECT * FROM {table}")
            self.memory[table] = self.manager.fetch()
        
        return self.memory[table]