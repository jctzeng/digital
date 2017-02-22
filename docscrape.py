import scrapy


class AuthorSpider(scrapy.Spider):
    name = 'doctor'
    start_urls = ['https://www4.mdanderson.org/peoplefinder/index.cfm?q=.*']

    def parse(self, response):
        # follow links to author pages
        for href in response.css('.an12b a::attr(href)').extract():
            yield scrapy.Request(response.urljoin(href),
                                 callback=self.parse_author)

        # follow pagination links
        next_page = response.css('li.next a::attr(href)').extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)

    def parse_author(self, response):
        def extract_with_css(query):
            return response.css(query).extract_first().strip()

        yield {
            'name': extract_with_css('h1 span ::text'),
            'title': extract_with_css('h3 span ::text'),
            #'degree': extract_with_css('div.degree span.degree-list ::text'),
            'organization-unit': extract_with_css('h3 span.organization-unit ::text'),
            #'address_1': extract_with_css('div.adr div.street-address ::text'),
            #'address_2': extract_with_css('div.adr div.extended-address ::text'),
            #'city': extract_with_css('div.adr div.locality ::text'),
            #'region': extract_with_css('div.adr div.region ::text'),
            #'zip_code': extract_with_css('div.adr div.postal-code ::text'),

        }