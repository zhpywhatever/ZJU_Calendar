import scrapy


class YunfengSpider(scrapy.Spider):
    name = "yunfeng"
    allowed_domains = ["yunfeng.zju.edu.cn"]
    start_urls = ["http://yunfeng.zju.edu.cn/"]

    def parse(self, response):
        pass
