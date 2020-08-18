import scrapy
import logging

class CountriesSpider(scrapy.Spider):
    name = 'countries'
    allowed_domains = ['www.worldometers.info']
    start_urls = ['https://www.worldometers.info/world-population/population-by-country/']

    def parse(self, response):
        countries = response.xpath('//td/a') 
        for country in countries:
            name = country.xpath('.//text()').get() 
            link = country.xpath('.//@href').get() 

        # absoulute_url = response.urljoin(link) 
            yield response.follow(url=link, callback=self.parse_country, meta={'country_name': name})

  
    def parse_country(self, response):
        name = response.request.meta['country_name'] 
        rows = response.xpath('(//table[@class="table table-striped table-bordered table-hover table-condensed table-list"])[1]/tbody/tr') 
        for row in rows:
            year = row.xpath('.//td[1]/text()').get() 
            population = row.xpath('.//td[2]/strong/text()').get() 
            yearly_percentage_change = row.xpath('.//td[3]/text()').get() 
            median_age = row.xpath('.//td[6]/text()').get() 
            fertilaity_rate = row.xpath('.//td[7]/text()').get() 
            
            yield {
                'country_name': name, 
                'year': year,
                'population': population,
                'yearly_%_change': yearly_percentage_change,
                'median_age': median_age,
                'fertilaity_rate': fertilaity_rate
                }