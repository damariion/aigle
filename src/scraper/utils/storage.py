from data.template   import Template
from sqlite3         import connect, Row
from os.path         import dirname, \
                            abspath, \
                            join as pjoin
from os              import listdir
from datetime        import datetime
from .serialise      import Serialise
from pandas          import DataFrame

class Storage:

    def __init__(self):
        
        # database dynamic path detection
        root = dirname(dirname(abspath(__file__)))
        
        # initialisation
        self.database = connect(pjoin(root, "data", "base.db"), 
                                check_same_thread=False)
        self.database.row_factory = Row 
        self.cursor = self.database.cursor()
        self.cache  = {}

        for table in listdir(pjoin(root, "spiders")):
            
            if '_' in table:
                continue
            table = table[:-3]

            self.cursor.execute(
                f"""
                CREATE TABLE IF NOT EXISTS {table}
                (
                    date     TEXT,
                    name     TEXT,
                    brand    TEXT,
                    price    REAL,
                    reviews  INTEGER,
                    likeness INTEGER,
                    supplier TEXT
                )
                """
            )

            # temporary cache
            self.cache[table] = DataFrame(self.read(table))

    def serialise(self, template: Template):

        for key in template.__dict__.keys():
           
            serialiser = getattr(Serialise, key)
            setattr(template, key, serialiser(getattr(template, key)))

        return template.__dict__

    def write(self, table: str, template: Template):
        
        # date insertion
        data = {"date": datetime.now().isoformat()}
        data.update(self.serialise(template))
        
        self.cursor.execute(
            f"""
            INSERT INTO {table} 
            (name, brand, price, reviews, likeness, supplier, date)
            VALUES 
            (:name, :brand, :price, :reviews, :likeness, :supplier, :date)
            """, data
        )

    def read(self, table: str):

        response = []
        self.cursor.execute(f"SELECT * FROM {table}")

        for entry in self.cursor.fetchall():
            response.append(dict(entry))

        return response
    
    # micros
    describe = lambda self, table:    self.cache[table].describe().to_dict()
    memory   = lambda self, table:    self.cache[table].memory_usage().to_dict()
    head     = lambda self, table, n: self.cache[table].head(n).to_dict()
    tail     = lambda self, table, n: self.cache[table].tail(n).to_dict()
    index    = lambda self, table, n: self.cache[table].iloc[n].to_dict()    
    sample   = lambda self, table, n: self.cache[table].sample(n).to_dict()
    column   = lambda self, table, c: self.cache[table][c].to_dict()
    query    = lambda self, table, q: self.cache[table].query(q).to_dict()


    def __del__(self):

        # EOF commit
        self.database.commit()

        # termination
        self.cursor.close()
        self.database.close()