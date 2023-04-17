import scrapy

class MovieSpider(scrapy.Spider):
    name = 'movies'
    start_urls = ['https://www.imdb.com/chart/top/']

    def parse(self, response):
        movies = response.css('.lister-list tr')
        for movie in movies:
            title = movie.css('.titleColumn a::text').get()
            original_title = movie.css('.titleColumn span::text').get()
            score = movie.css('.ratingColumn strong::text').get()
            genre = movie.css('.genre::text').get()
            year = movie.css('.secondaryInfo span:first-child::text').get()
            duration = movie.css('.runtime::text').get()
            description = movie.css('.ratings-bar+ .text-muted::text').get()
            actors = movie.css('.rating-list .ghost~ a::text').getall()
            public = movie.css('.certificate::text').get()
            country = movie.css('.secondaryInfo span:last-child::text').get()
            language = movie.css('.see-more.inline a[href^="/language"]::text').get()

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