# -*- coding: utf-8 -*-
import scrapy
import BathSim.items as items
import re

class BathharvestSpider(scrapy.Spider):
    name = "BathHarvest"
    allowed_domains = ["opus.bath.ac.uk"]
    start_urls = [
        'http://opus.bath.ac.uk/view/divisions/dept=5Fchem.html',
        'http://opus.bath.ac.uk/view/divisions/dept=5Fbio.html',
        'http://opus.bath.ac.uk/view/divisions/dept=5Fpharm.html'
    ]

    def parse(self, response):
        recs = response.xpath('//body/div[1]/div[2]/div[2]/div[1]/div[4]/div[@class="ep_view_citation_row"]')
        for rec in recs:
            item = items.BathHarvestItem()
            author_list = rec.xpath('./div[1]/span/text()').extract()
            punct_filter = dict((ord(char), u'') for char in ' "#$%&\'()*+,./-:;<=>?@[\\]^_`{|}')   
            fin=[]
            for i in author_list:
	        l,f =i.split(',')
	        f = f.translate(punct_filter)
	        fin.append(f+' '+ l)
            item['authors'] = fin
            item['title'] = rec.xpath('string(div[1]/a)').extract()[0]
            item['free_text'] = rec.xpath('string(div[1])').extract()[0]
            try:
	        item['publication'] = rec.xpath('div[1]/em/text()').extract()[0]
	    except:
	        item['publication'] = u'other'
            link = rec.xpath('div[1]/a/@href').extract()[0]
            try:
	        for stri in rec.xpath('div[1]/text()').extract():
                    s = re.sub("\D", "", stri)
                    if (len(s)==4):
                        item['year'] = s
            except:
	        item['year'] = u'0000'
            yield scrapy.Request(link,callback=self.parse_individual,meta={'item':item})
         

    def parse_individual(self,response):
        item = response.meta['item']
        try:
            item['doi']=response.xpath('//body/div[1]/div[2]/div[2]/div[1]/div[2]/div[4]/table[1]/tbody/tr[3]/td[2]/a/text()').extract()[0]
        except:
	    item['doi']= u'NOT FOUND'
        try:
	    ps = response.xpath('//body/div[1]/div[2]/div[2]/div[1]/div[2]/div[4]/h3/text()').extract()
            abs_ind = ps.index(u'Abstract')
            item['abstract']=response.xpath('//body/div[1]/div[2]/div[2]/div[1]/div[2]/div[4]/p['+str(abs_ind)+']/text()').extract()[0]
        except:
	    item['abstract']=None
        return item