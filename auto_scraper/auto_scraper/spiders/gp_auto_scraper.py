# -*- coding: utf-8 -*-
import re
import scrapy

from auto_scraper.items import AutoItem


class GpAutoScraperSpider(scrapy.Spider):
    """Scraper for a website."""
    name = "gp_auto_scraper"
    allowed_domains = ["gpautos.net"]
    start_urls = "http://gpautos.net"
    __num_regex = re.compile(r"""(\d+)""")

    def __init__(self):
        super(GpAutoScraperSpider, self).__init__()

    def start_requests(self, min_cost=1, max_cost=60000):
            #return [scrapy.FormRequest(gp_domain_base + "/GP/carros/filtro",
            #for i in range(35):
            i = 1
            pags = 70
            request_list = []
            for i in range(pags):
                request_list.append(scrapy.FormRequest(self.start_urls + "/GP/carros/pagina/",
                formdata={"Pagina": unicode(i),
                          "Paginas": unicode(pags),
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
                callback=self.scrape_search_page))

            return request_list

    def scrape_search_page(self, response):
        extracted_cars = response.xpath('//*[@id="formPag"]/div')
        for car in extracted_cars:
            link = response.urljoin(car.xpath("a/@href").extract_first())
            yield scrapy.Request(link, callback=self.parse_car_page)
            ### div.cdata:nth-child(1) > span:nth-child(2)
            ### model div.cdata:nth-child(3) > span:nth-child(2)
        #print extracted_cars
        #yield

    def parse_car_page(self, response):
        auto = AutoItem()
        auto["gp_id"] = response.xpath('//*[@id="carroCabecera"]/h1').extract_first()
        #TODO: fix xpaths...
        auto["brand"] = response.xpath('/html/body/div/section/div[1]/div[4]/div[1]/span/text()').extract_first()
        auto["model"] = response.xpath('/html/body/div/section/div[1]/div[4]/div[3]/span/text()').extract_first()
        auto["color"] = response.xpath('/html/body/div/section/div[1]/div[4]/div[4]/span/text()').extract_first()
        auto["kms"] = response.xpath('/html/body/div/section/div[1]/div[4]/div[9]/span/text()').extract_first()
        auto["ccs"] = response.xpath('/html/body/div/section/div[1]/div[4]/div[6]/span/text()').extract_first()
        auto["year"] = response.xpath('/html/body/div/section/div[1]/div[4]/div[8]/span/text()').extract_first()
        auto["contact_string"] = response.xpath('//*[@id="carroContacto"]').extract_first()
        precio_string = response.xpath('/html/body/div/section/div[1]/div[4]/div[26]/h1').extract_first()
        # precio_l = self.__num_regex.findall(precio_string)[:2:]
        # print(precio_l)
        auto["price_string"] = precio_string
        return auto
