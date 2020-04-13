# -*- coding: utf-8 -*-
import scrapy


class BooksSpider(scrapy.Spider):
    name = "books"
    allowed_domains = ["wedmegood.com/vendors/all/wedding-photographers"]
    start_urls = [
        'https://www.wedmegood.com/vendors/all/wedding-photographers/',
    ]

    def parse(self, response):
        for book_url in response.css("article.product_pod > h3 > a ::attr(href)").extract():
            yield scrapy.Request(response.urljoin(book_url), callback=self.parse_book_page)
        next_page = response.css("li.next > a ::attr(href)").extract_first()
        if next_page:
            yield scrapy.Request(response.urljoin(next_page), callback=self.parse)

    def parse_book_page(self, response):
        item = {}
        product = response.css("div.product_main")
        item["title"] = product.css("h1 ::text").extract_first()
        item['category'] = response.xpath(
            "//*[@id="react-view"]/div/div/div[3]/div[3]/div[1]/div/div/div[1]/div[1]/div/div/h1"
        ).extract_first()
        item['description'] = response.xpath(
            "//*[@id="card0"]/div/div[3]/div[2]/div[1]/div[1]/div[1]/a"
        ).extract_first()
        item['price'] = response.css('p.price_color ::text').extract_first()
        yield item
