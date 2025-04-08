from scrapy               import Spider
from data.template        import Template
from scrapy.http.response import Response

class Bol(Spider):

    def __init__(self, manager, url, pages = 1, **kwargs):
        
        super().__init__("bol", **kwargs)
        self.manager    = manager
        self.start_urls = [url]

        # depth management
        self.pages   = pages
        self.page    = 0

    def parse(self, response: Response):
        
        selectors = \
        {
            "name"     : "div.product-title--inline a::text",
            "brand"    : "ul.product-creator li a::text",
            "price"    : (".promo-price::text", ".promo-price__fraction::text"),
            "reviews"  : ".u-mb--xs::attr(aria-label)",
            "likeness" : "div.star-rating span::attr(style)",
            "supplier" : "span.product-seller__name::text",
        }

        for item in response.css("li.product-item--row"):

            self.manager.insert(self.name, Template(
                name     = Serialise.name(item.css(selectors["name"]).get()),
                brand    = Serialise.brand(item.css(selectors["brand"]).get()),
                price    = Serialise.price(f"{item.css(selectors["price"][0]).get()},"
                                           f"{item.css(selectors["price"][1]).get()}"),
                reviews  = Serialise.reviews(item.css(selectors["reviews"]).get()),
                likeness = Serialise.likeness(item.css(selectors["likeness"]).get()),
                supplier = Serialise.supplier(item.css(selectors["supplier"]).get()),
            ))

        # page limiter
        if (self.page >= self.pages):
            return None
        self.page += 1

        # recursion
        selector = "a.ui-btn[aria-label=volgende]::attr(href)"
        yield response.follow(
            url      = response.css(selector).get(),
            callback = self.parse,  
        )

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