#
# This scraper will look at all cooking recipes, and extract all the materials as well as the products.
#

import scrapy
import json
import re

class CookingSpider(scrapy.Spider):
    name = "cooking_box"

    ranks = ["apprentices", "skilled", "professionals", "artisans", "masters", "gurus"]

    def start_requests(self):
        urls = [
            "https://bdo.altarofgaming.com/item/apprentices-cooking-box/",
            "https://bdo.altarofgaming.com/item/skilled-cooks-cooking-box/",
            "https://bdo.altarofgaming.com/item/professionals-cooking-box/",
            "https://bdo.altarofgaming.com/item/artisans-cooking-box/",
            "https://bdo.altarofgaming.com/item/masters-cooking-box/",
            "https://bdo.altarofgaming.com/item/gurus-cooking-box/"
        ]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)


    def parse(self, response):
        url = response.request.url
        rank = ""
        for i in self.ranks:
            if i in url:
                rank = i
                break

        rows = response.css('tr.bdo_table_recipe_calculator_row_ingredient')
        for row in rows:
            quantity = row.css('.recipe_ingredient_quantity::text').get()
            name = row.css('.tooltip::text').get()
            id = row.css('.tooltip').attrib['data-tooltip-content']
            id = id.split("-",1)[1]

            yield({"rank": rank, "name": name, "quantity": quantity, "id": id})