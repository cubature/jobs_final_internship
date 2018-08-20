# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader import ItemLoader
from frenchcorpus.items import FrenchcorpusItem

import pprint


class Voxforge(scrapy.Spider):
    name = "voxforge"

    allowed_domains = ["www.repository.voxforge1.org"]
    start_urls = [
        "http://www.repository.voxforge1.org/downloads/fr/Trunk/Audio/Main/16kHz_16bit/"
    ]

    def parse(self, response):
        tgz_files = []
        for f in response.xpath('//pre/a[position()>4]/@href'):
            tgz_files.append(self.start_urls[0] + f.extract())

        item_loader = ItemLoader(item=FrenchcorpusItem(), response=response)
        item_loader.add_value('file_urls', tgz_files)

        yield item_loader.load_item()