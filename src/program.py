from utils.micros import Micros
from data.manager import Manager
from pprint import pp

class Program:

    def __init__(self):
        
        self.manager = Manager()
        self.micros  = Micros(self.manager)

    def main(self):
        
        pp(self.micros.most_reviews("bol"))

    def __del__(self):

        ...

if __name__ == "__main__":
    (_ := Program()).main(); del _