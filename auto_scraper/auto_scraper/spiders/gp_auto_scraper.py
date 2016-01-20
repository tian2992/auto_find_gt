# -*- coding: utf-8 -*-
import scrapy

from auto_scraper.items import AutoItem


class GpAutoScraperSpider(scrapy.Spider):
    """Scraper for a website."""
    name = "gp_auto_scraper"
    allowed_domains = ["gpautos.net"]
    start_urls = "http://gpautos.net"

    def __init__(self):
        super(GpAutoScraperSpider, self).__init__()

    def start_requests(self, min_cost=1, max_cost=45000):
        #return [scrapy.FormRequest(gp_domain_base + "/GP/carros/filtro",
        #TODO: loop pages
        return [scrapy.FormRequest(self.start_urls + "/GP/carros/pagina/",
                formdata={"pagina": "1",
                          "AnioMinimo": unicode(1916),
                          "AnioMaximo": unicode(2017),
                          "Marca": "todos",
                          "Linea": 'todos',
                          "Combustible": "todos",
                          "Origen": "todos",
                          "Transmision": "todos",
                          "Moneda": "Q",
                          "Departamento": "todos",
                          "Tipo": "usado",
                          "TipoVehiculo": "automovil",
                           "RangoMinimo": unicode(min_cost),
                          "RangoMaximo": unicode(max_cost),
                          },
                callback=self.scrape_search_page)]

    def scrape_search_page(self, response):
        extracted_cars = response.xpath('//*[@id="formPag"]/div')
        for car in extracted_cars:
            link = response.urljoin(car.xpath("a/@href").extract()[0])
            yield scrapy.Request(link, callback=self.parse_car_page)
            ### div.cdata:nth-child(1) > span:nth-child(2)
            ### model div.cdata:nth-child(3) > span:nth-child(2)
        #print extracted_cars
        #yield

    def parse_car_page(self, response):
        auto = AutoItem()
        auto["gp_id"] = response.xpath('//*[@id="carroCabecera"]/h1').extract()
        #TODO: fix xpaths...
        auto["brand"] = response.xpath('/html/body/div/section/div[1]/div[4]/div[1]/span/text()').extract()
        auto["model"] = response.xpath('/html/body/div/section/div[1]/div[4]/div[3]/span/text()').extract()
        auto["color"] = response.xpath('/html/body/div/section/div[1]/div[4]/div[4]/span/text()').extract()
        auto["kms"] = response.xpath('/html/body/div/section/div[1]/div[4]/div[9]/span/text()').extract()
        auto["ccs"] = response.xpath('/html/body/div/section/div[1]/div[4]/div[6]/span/text()').extract()
        auto["year"] = response.xpath('/html/body/div/section/div[1]/div[4]/div[8]/span/text()').extract()
        return auto
