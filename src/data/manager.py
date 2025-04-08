from sqlite3       import connect, Row
from os.path       import dirname, join as pathify
from os            import listdir
from pandas        import DataFrame
from datetime      import datetime
from importlib     import import_module
from data.template import Template

class Manager:

    def __init__(self):
        
        # initialisation
        self.root     = dirname(dirname(__file__))
        self.database = connect(pathify(self.root, "data", "base.db"))
        self.cursor   = self.database.cursor()
        
        # configuration
        self.cursor.row_factory = Row
        
        # correction
        self.__fix_missing()

    def __fix_missing(self):

        mods = []
        for _ in listdir(pathify(self.root, "mods")):
            
            # ignore
            mod = _[:-3]
            if '_' in mod:
                continue

            file = import_module(f"mods.{mod}")
            mods.append(getattr(file, mod.capitalize()))

        # initialisation
        for mod in mods:

            name   = mod.__name__.lower()
            query  = f"CREATE TABLE IF NOT EXISTS {name}" \
                      "(date TEXT," # autonomous date handling
            
            for idx, (key, val) in enumerate(
                _ := Template.__annotations__.items()):

                query += key + ' ' + {

                    "None"            : "NULL",
                    "<class 'str'>"   : "TEXT",
                    "<class 'int'>"   : "INTEGER",
                    "<class 'float'>" : "REAL",

                }[str(val)] + (',' if idx < len(_) - 1 else '')

            self.exec(f"{query})")


    def exec(self, query, *args):

        # immediate
        self.cursor.execute(query, *args)
        self.database.commit()

    def fetch(self, one = False) -> DataFrame:

        # dynamic
        data = [self.cursor.fetchone()] \
        if one else self.cursor.fetchall()

        # conversion
        return DataFrame(map(dict, data))
    
    def insert(self, table: str, model: object):

        # consistent
        attributes = ["date"] + list(model.__annotations__.keys())
        model.date = datetime.now().isoformat()

        # construction
        query  = f"INSERT INTO {table}"
        query += f"({','.join(attributes)}) VALUES"
        query += f"({','.join(map(lambda _: f":{_}", attributes))})"

        # execution
        self.exec(query, model.__dict__)

    def __del__(self):

        # termination
        self.cursor.close()
        self.database.close()