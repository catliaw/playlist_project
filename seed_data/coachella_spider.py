import scrapy


class QuotesSpider(scrapy.Spider):
    name = "coachella_artists"
    start_urls = ['https://www.coachella.com/lineup/']

    def parse(self, response):
        for coachella_artist in response.css('div.in'):
            yield {
                'artist': coachella_artist.xpath('div[@class="artist-info"]/h1/text()').extract_first(),
                'website_url': coachella_artist.xpath('div[@class="artist-info"]/ul/li/a/@href').extract_first(),
                'image_url': coachella_artist.xpath('div[@class="artist-img"]/@data-img').extract_first(),
                'day1': coachella_artist.xpath('div[@class="artist-info"]/ul[@class="event-list"]/li[@data-weekend="1"]/div[@class="perf-date"]/text()').extract_first(),
                'day2': coachella_artist.xpath('div[@class="artist-info"]/ul[@class="event-list"]/li[@data-weekend="1"][2]/div[@class="perf-date"]/text()').extract_first(),
                'stage': coachella_artist.xpath('div[@class="artist-info"]/ul[@class="event-list"]/li[@data-weekend="1"]/div[@class="perf-time-loc"]/span[@class="sep"]/following-sibling::text()').extract_first()
            }