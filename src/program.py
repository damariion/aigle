from pprint import pp
from utils.visuals import Visuals
from data.manager  import Manager

class Program:

    def __init__(self):
        
        self.manager = Manager()
        self.micros  = Visuals(self.manager)

    def main(self):
        
        pp(self.micros.best_brands("bol", 10))

    def __del__(self):

        ...

if __name__ == "__main__":
    (_ := Program()).main(); del _