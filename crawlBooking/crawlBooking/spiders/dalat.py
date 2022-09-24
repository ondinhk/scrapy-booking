import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes"

    def start_requests(self):
        urls = [
            'https://www.booking.com/searchresults.en-gb.html?label=gen173nr-1DCAEoggI46AdIM1gEaPQBiAEBmAEJuAEZyAEM2AED6AEBiAIBqAIDuAKn0ryZBsACAdICJDFjN2ZiNTNlLTkyYzYtNDdjOS05NTg3LTEyMGFmZjZlMjM0NtgCBOACAQ&sid=87b657754f8327f14759b75311b5a649&dest_id=-3712045&dest_type=city&'
            # 'https://quotes.toscrape.com/page/2/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for item in response.css('.div.fcab3ed991'):
            name = item.get()
            print(dict(name=name))
