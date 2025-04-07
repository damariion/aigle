from scrapy                  import Spider
from ..data.template         import Template
from scrapy.http.response    import Response

class Bol(Spider):

    def __init__(self, url, storage, pages = 1, **kwargs):
        
        super().__init__("bol", **kwargs)
        self.storage    = storage
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

            self.storage.write(self.name, Template(
                name     = item.css(selectors["name"]).get(),
                brand    = item.css(selectors["brand"]).get(),
                price    = 
                    f"{item.css(selectors["price"][0]).get()},"
                    f"{item.css(selectors["price"][1]).get()}",
                reviews  = item.css(selectors["reviews"]).get(),
                likeness = item.css(selectors["likeness"]).get(),
                supplier = item.css(selectors["supplier"]).get(),
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