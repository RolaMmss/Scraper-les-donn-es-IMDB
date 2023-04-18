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
    # def start_requests(self):
    #         url = 'https://www.imdb.com/chart/top/'
    #         headers = {
    #             'User-Agent': self.settings.get('USER_AGENT')
    #         }
    #         yield scrapy.Request(url, headers=headers, callback=self.parse_item)
            
    movie_details = LinkExtractor(restrict_xpaths='//div[@class="lister"]//table//td[@class="titleColumn"]//a')
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
        title = movie.xpath('//h1//span//text()').get()
        original_title = movie.xpath('//div[@class="sc-afe43def-3 EpHJp"]//text()').get()
        score = movie.xpath('//span[@class="sc-bde20123-1 iZlgcd"]//text()').get()
        genre = movie.xpath('//a[@class="ipc-chip ipc-chip--on-baseAlt"]//text()').get()
        year = movie.xpath('//ul[@class="ipc-inline-list ipc-inline-list--show-dividers sc-afe43def-4 kdXikI baseAlt"]//li[1]').get()
        duration = movie.xpath('//ul[@class="ipc-inline-list ipc-inline-list--show-dividers sc-afe43def-4 kdXikI baseAlt"]//li[3]').get()
        description = movie.xpath('//p[@class="sc-5f699a2-3 lopbTB"]').get()
        
        year = movie.xpath('//ul[@class="ipc-inline-list ipc-inline-list--show-dividers sc-afe43def-4 kdXikI baseAlt"]/li[1]/ a /text()').get()
        public = movie.xpath('//ul[@class="ipc-inline-list ipc-inline-list--show-dividers sc-afe43def-4 kdXikI baseAlt"]/li[2]/ a /text()').get()
        duration = movie.xpath('//ul[@class="ipc-inline-list ipc-inline-list--show-dividers sc-afe43def-4 kdXikI baseAlt"]/li[3]/ a /text()').get()
        actors = movie.xpath('//div[@class="ipc-avatar ipc-avatar--base ipc-avatar--dynamic-width"] /a/@aria-label').getall()
        country = movie.xpath('/html/body/div[2]/main/div/section[1]/div/section/div/div[1]/section[12]/div[2]/ul/li[2]/div/ul/li/a').get()
        language = movie.xpath('/html/body/div[2]/main/div/section[1]/div/section/div/div[1]/section[12]/div[2]/ul/li[4]/div/ul/li/a').get()
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
