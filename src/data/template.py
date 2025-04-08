from dataclasses import dataclass

@dataclass
class Template:

    # unique
    name     : str
    brand    : str
    price    : float
    reviews  : int
    likeness : int
    supplier : str