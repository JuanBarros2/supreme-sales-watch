import scrapy
import re


class PelandoSpider(scrapy.Spider):
    name = "pelando"
    start_urls = ['https://www.pelando.com.br/recentes']

    def parse(self, response):
        for quote in response.css('article'):
            yield {
                'temp': " ".join(quote.css('span.cept-vote-temp::text').re(r'\d+')),
                'product': " ".join(quote.css('a.cept-tt::text').re(r'\w+')),
                'price': quote.css('span.thread-price::text').get(),
                'merchant': quote.css('span.cept-merchant-name::text').get()
            }
