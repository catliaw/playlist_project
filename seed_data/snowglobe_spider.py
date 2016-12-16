import scrapy


class QuotesSpider(scrapy.Spider):
    name = "snowglobe_artists"
    start_urls = ['http://snowglobemusicfestival.com/artists']

    def parse(self, response):
            for snowglobe_artists in response.xpath('//span[@class="column-view-container"]'):
                yield {
                    'artist': snowglobe_artists.xpath('.//p[@class="fs-20"]/span/text()|.//p[@class="fs-20"]/span/span/text()').extract_first(),
                    'playing_at': snowglobe_artists.xpath('.//p[@class="fs-15"]/text()|.//p[@class="fs-15"]/span/text()|.//p[@class="fs-15"]/span/span/text()|.//p[@class="fs-15"]/span[3]/span/text()|.//p[@class="fs-20"][2]/span/text()').extract_first()
                    # 'image_url': snowglobe_artists.xpath('.//div[@class="focus-img-wrapper"]/div/img[@class="static-img"]/@src').extract_first()
                }