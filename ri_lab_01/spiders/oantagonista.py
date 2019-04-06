# -*- coding: utf-8 -*-
import scrapy
import json
from datetime import datetime

from ri_lab_01.items import RiLab01Item
from ri_lab_01.items import RiLab01CommentItem

class OantagonistaSpider(scrapy.Spider):
    name = 'oantagonista'
    allowed_domains = ['oantagonista.com']
    start_urls = []

    data_limite = datetime.strptime('01/01/2018', '%d/%m/%Y')

    def __init__(self, *a, **kw):
        super(OantagonistaSpider, self).__init__(*a, **kw)
        with open('seeds/oantagonista.json') as json_file:
                data = json.load(json_file)
        self.start_urls = list(data.values())


    def parse(self, response):
        for art in response.css('div.collect article'):
            data = art.css('a.article_link span.postmeta time::attr(datetime)').get()
            data = datetime.strptime(data, '%Y-%m-%d %H:%M:%S')
            
            if (self.data_limite <= data):
                titulo = art.css('a.article_link::attr(title)').get()
                data_noticia = data.strftime("%d/%m/%Y %H:%M:%S")
                secao = art.css('a.article_link span.postmeta span.categoria::text').get()
                texto = art.css('a.article_link p').get()
                url = art.css('a.article_link::attr(href)').get()

                yield {
                    'titulo': titulo,
                    'subtitulo': '-',
                    'autor': '-',
                    'data': data_noticia,
                    'secao': secao,
                    'texto': texto,
                    'url': url
                }
            else:
                quit()                
                
        listUrl = response.url.split('/')
        
        if len(listUrl) == 6:
            newPage = listUrl[0] + '//' + listUrl[2] + '/' + listUrl[3] + '/' + str(int(listUrl[4]) + 1) + '/'
        else:
            newPage = listUrl[0] + '//' + listUrl[2] + '/' + 'pagina' + '/' + '2' + '/'
                                          
        yield scrapy.Request(url=newPage, callback=self.parse)
