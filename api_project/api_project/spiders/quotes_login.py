import scrapy
from scrapy import FormRequest


class QuotesLoginSpider(scrapy.Spider):
    name = "quotes_login"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["https://quotes.toscrape.com/login"]

    def parse(self, response):
        csrf_token = response.xpath('//input[@name="csrf_token"]/@value').get()
        yield FormRequest.from_response(
            response,
            formxpath="//form",
            formdata={
                'csrf_token': csrf_token,
                'username': 'admin',
                'password': 'admin'
            },
            callback=self.after_login
        )
    

    def after_login(self, response):
        logout_button = response.xpath('//a[@href="/logout"]/text()').get()

        if logout_button == 'Logout':
            print('Successfully logged in!')



