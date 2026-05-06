import scrapy

class MarketSpider(scrapy.Spider):
    # El nombre que usaremos para ejecutarla
    name = 'market_crawler'
    
    # La URL inicial
    start_urls = ['https://quotes.toscrape.com']

    def parse(self, response):
        # Recorremos cada contenedor de información
        for item in response.css('div.quote'):
            yield {
                'texto': item.css('span.text::text').get(),
                'autor': item.css('small.author::text').get(),
                'tags': item.css('div.tags a.tag::text').getall(),
            }

        # Buscamos el botón de "Siguiente" para paginar
        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)