import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from ..items import ItemsItem

    
class MoviesCrawlerSpider(CrawlSpider):
    name = 'movies'
    allowed_domains = ['imdb.com']

    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'

    def start_requests(self):
            yield scrapy.Request(url='https://www.imdb.com/chart/top/?ref_=nv_mv_250', headers={
                'User-Agent': self.user_agent
            })
   
    movie_details = LinkExtractor(restrict_xpaths='//div[@class="lister"]//table//td[@class="titleColumn"]//a')
    rule_movie_details = Rule(movie_details, callback='parse_item', follow=False)
    rules = (rule_movie_details, )
    
    
    def parse_item(self, movie):
        title = movie.xpath('//h1//span//text()').get()
        # original_title = movie.xpath('//div[@class="sc-afe43def-3 EpHJp"]//text()').get()
        score = movie.xpath('//span[@class="sc-bde20123-1 iZlgcd"]//text()').get()
        genre = movie.xpath('//a[@class="ipc-chip ipc-chip--on-baseAlt"]//text()').get()
        year = movie.xpath('//ul[@class="ipc-inline-list ipc-inline-list--show-dividers sc-afe43def-4 kdXikI baseAlt"]//li[1]').get()
        duration = movie.xpath('//ul[@class="ipc-inline-list ipc-inline-list--show-dividers sc-afe43def-4 kdXikI baseAlt"]//li[3]//text()').get()
        description = movie.xpath('//p[@class="sc-5f699a2-3 lopbTB"]//text()').get()
        year = movie.xpath('//ul[@class="ipc-inline-list ipc-inline-list--show-dividers sc-afe43def-4 kdXikI baseAlt"]/li[1]/ a /text()').get()
        public = movie.xpath('//ul[@class="ipc-inline-list ipc-inline-list--show-dividers sc-afe43def-4 kdXikI baseAlt"]/li[2]/ a /text()').get()
        actors = movie.xpath('//div[@class="ipc-avatar ipc-avatar--base ipc-avatar--dynamic-width"] /a/@aria-label').getall()
        country = movie.xpath('(//ul[@class="ipc-metadata-list ipc-metadata-list--dividers-all ipc-metadata-list--base"]//li[@class="ipc-metadata-list__item"]//div[@class="ipc-metadata-list-item__content-container"])[1]//text()').get()
        language = movie.xpath('(//ul[@class="ipc-metadata-list ipc-metadata-list--dividers-all ipc-metadata-list--base"]//li[@class="ipc-metadata-list__item"]//div[@class="ipc-metadata-list-item__content-container"])[3]//text()').get()
        yield {
            'title': title,
            # 'original_title': original_title,
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
