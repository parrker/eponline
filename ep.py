import scrapy

from scrapy.item import Item, Field
from scrapy.http import FormRequest
from scrapy.utils.response import open_in_browser
from bgcolors import bgcolors
from datetime import datetime

class EPSpider(scrapy.Spider):
    name = 'EP Online'
    allowed_domains = ['eponline.mom.gov.sg']
    start_urls = ['https://eponline.mom.gov.sg/epol/PEPOLENQM007DisplayAction.do']

    def parse(self, response):
        formdata = {
          'requesterNRICFIN': '',
          'requesterName': ''
        }

        yield FormRequest.from_response(response,
                                        formdata=formdata,
                                        clickdata={'name': 'commit'},
                                        callback=self.parse1)

    def parse1(self, response):
        formdata = {
            'travelDocNo': '',
            'trvDateBirth': ''
        }

        yield FormRequest.from_response(response,
                                        formdata=formdata,
                                        clickdata={'name': 'commit'},
                                        callback=self.parse2)

    def parse2(self, response):
        status = response.css('.outerBox tr:last-child td:last-child::text').extract_first()
        color = bgcolors.WARNING if status.find('Pending') != 0 else bgcolors.OKBLUE

        print(datetime.now())
        print('%sStatus%s%s' % (color, status, bgcolors.ENDC))
