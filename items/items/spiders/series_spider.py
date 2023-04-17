import scrapy

class SerieSpider(scrapy.Spider):
    name = 'serie'
    start_urls = ['https://www.imdb.com/chart/toptv/']

    def parse(self, response):
        series = response.css('.lister-list tr')
        for serie in series:
            title = serie.css('.titleColumn a::text').get()
            original_title = serie.css('.titleColumn span::text').get()
            score = serie.css('.ratingColumn strong::text').get()
            genre = serie.css('.genre::text').get()
            year = serie.css('.secondaryInfo span:first-child::text').get()
            duration = serie.css('.runtime::text').get()
            description = serie.css('.ratings-bar+ .text-muted::text').get()
            actors = serie.css('.rating-list .ghost~ a::text').getall()
            public = serie.css('.certificate::text').get()
            country = serie.css('.secondaryInfo span:last-child::text').get()
            language = serie.css('.see-more.inline a[href^="/language"]::text').get()

            yield {
                'title': title,
                'original_title': original_title,
                'score': score,
                'genre': genre,
                'year': year,
                'duration': duration,
                'description': description,
                'actors': actors,
                'public': public,
                'country': country,
                'language': language
            }