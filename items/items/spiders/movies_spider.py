import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
# class MovieSpider(scrapy.Spider):
#     name = 'movies'
#     start_urls = ['https://www.imdb.com/chart/top/']

#     def parse(self, response):
#         movies = response.css('.lister-list tr')
#         for movie in movies:
#             title = movie.css('.titleColumn a::text').get()
#             original_title = movie.css('.titleColumn span::text').get()
#             score = movie.css('.ratingColumn strong::text').get()
#             genre = movie.css('.genre::text').get()
#             year = movie.css('.secondaryInfo span:first-child::text').get()
#             duration = movie.css('.runtime::text').get()
#             description = movie.css('.ratings-bar+ .text-muted::text').get()
#             actors = movie.css('.rating-list .ghost~ a::text').getall()
#             public = movie.css('.certificate::text').get()
#             country = movie.css('.secondaryInfo span:last-child::text').get()
#             language = movie.css('.see-more.inline a[href^="/language"]::text').get()

#             yield {
#                 'title': title,
#                 'original_title': original_title,
#                 'score': score,
#                 'genre': genre,
#                 'year': year,
#                 'duration': duration,
#                 'description': description,
#                 'actors': actors,
#                 'public': public,
#                 'country': country,
#                 'language': language
#             }
####################################################################
# class MovieSpider(scrapy.Spider):
#     name = 'movies'
#     start_urls = [  'https://www.imdb.com/chart/top/']
    
class MoviesCrawlerSpider(CrawlSpider):
    name = 'movies'
    allowed_domains = ['imdb.com']

    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'

    def start_requests(self):
            yield scrapy.Request(url='https://www.imdb.com/chart/top/?ref_=nv_mv_250', headers={
                'User-Agent': self.user_agent
            })

    movie_details = LinkExtractor(restrict_xpaths=['//div[@class="lister"]//table//td[@class="titleColumn"]//a'])
    rule_movie_details = Rule(movie_details, callback='parse_item', follow=False)
    rules = (rule_movie_details, )
        # Extract links matching 'category.php' (but not matching 'subsection.php')
        # and follow links from them (since no callback means follow=True by default).
      
    #     Rule(LinkExtractor(
    #         # allow=('category\.php', ), 
    #         # deny=('subsection\.php', ), 
    #         restrict_xpath=('//div[@class="lister"]//table//td[@class="titleColumn"]//a')),
    #         callback='parse_item', 
    #         follow=False),

    #     # # Extract links matching 'item.php' and parse them with the spider's method parse_item
    #     # Rule(LinkExtractor(allow=('item\.php', )), callback='parse_item'),
    # )

    
    def parse_item(self, movie):
        item={}
        # movies = movie.css('.lister-list tr')
        # for movie in movies:
        # title = movie.css('.titleColumn a::text').get()
        title = movie.xpath('//h1//span//text()').get()
        original_title = movie.xpath('//div[@class="sc-afe43def-3 EpHJp"]//text()').get()
        score = movie.css('.ratingColumn strong::text').get()
        genre = movie.css('.genre::text').get()
        year = movie.css('.secondaryInfo span:first-child::text').get()
        # duration = movie.css('.runtime::text').get()
        # //div[@class='sc-52d569c6-0 kNzJA-D']//ul//li[3]//text()
        
        # duration = response.xpath("//div[@class='sc-52d569c6-0 kNzJA-D']//ul//li[3]//text()").get().strip()
        duration = movie.css('div.sc-52d569c6-0.kNzJA-D ul li:nth-child(3)::text').get()

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
        next_page = movie.css('.lister-page-next a::attr(href)').get()
        if next_page:
            yield movie.follow(next_page, self.parse)
##########################################################
# class MovieSpider(scrapy.Spider):
#     name = 'movies'
#     start_urls = ['https://www.imdb.com/chart/top/']
#     download_delay = 1.0
#     custom_settings = {
#         'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
#     }

#     def parse(self, response):
#         movies = response.css('.lister-list tr')
#         for movie in movies:
#             title = movie.css('.titleColumn a::text').get()
#             movie_url = movie.css('.titleColumn a::attr(href)').get()
#             yield response.follow(movie_url, self.parse_movie, meta={'title': title})

#         next_page = response.css('.lister-page-next a::attr(href)').get()
#         if next_page:
#             yield response.follow(next_page, self.parse)

#     def parse_movie(self, response):
#         title = response.request.meta['title']
#         duration = response.css('.subtext time::text').get()
#         public = response.css('.subtext span:first-child::text').get().strip()
#         if public is not None:
#             public = public.strip()
#         yield {
#             'title': title,
#             'duration': duration,
#             'public': public
#         }
