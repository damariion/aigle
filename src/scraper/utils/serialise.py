class Serialise:

    # micro serialization
    @staticmethod
    def name(value: str):

        if len(value) > 60:
            value = f"{value[:60-3]}..."
        
        return value
        
    @staticmethod
    def brand(value: str):
        
        return value

    @staticmethod
    def price(value: str):

        # conversion
        i, y = value.split(',')
        i, y = i.strip(), y.strip()
        
        y = '0' if y == '-' else y
        map(int, [i, y])

        return float(f"{i}.{y}")

    @staticmethod
    def reviews(value: str): 
        
        if not value:
            return None

        value = value.split()
        return int(value[-2])

    @staticmethod
    def likeness(value: str):
        
        if not value:
            return None

        value = value.split()
        return int(value[-1][:-1])

    @staticmethod
    def supplier(value: str):
    
        if not value:
            value = "bol"

        return value