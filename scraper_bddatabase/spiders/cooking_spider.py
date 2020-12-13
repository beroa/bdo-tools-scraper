#
# This scraper will look at all cooking recipes, and extract all the materials as well as the products.
#

import scrapy
import json
import re

class CookingSpider(scrapy.Spider):
    name = "cooking"

    def start_requests(self):
        urls = [
            "https://bddatabase.net/query.php?a=recipes&type=culinary&id=1&l=us"
        ]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    # parse() will grab just item-ids from all cooking recipes
    def parse(self, response):
        results = json.loads(response.body)

        unique_items = set()

        for recipe in results["aaData"]:
            # materials = recipe[6] # will link to itemgroups
            products = recipe[7]
            products = re.findall('data-id="(.*?)(?=")', products)
            for item in products:
                unique_items.add(item)

            raw_materials = recipe[8] # will contain all relevant item-ids
            raw_materials = raw_materials.strip('][').split(',') 
            for item in raw_materials:
                unique_items.add("item--{}".format(item))

        for item in unique_items:
            url = "https://bddatabase.net/tip.php?id={}&enchant=0&caphrasenhancement=&l=us&nf=on".format(item)
            yield scrapy.Request(url=url, callback=self.parse_item) # lookup item tooltip to get the name
            # break
        
    # parse_items() will take item-ids and get item names
    def parse_item(self, response):
        response = response.body.decode("utf-8")

        grade = re.findall('class="item_title item_grade_(.*?)(?=")', response)
        grade = grade[0]

        name = re.findall('<h1>(.*?)(?=<\/h1>)', response)
        name = name[0]

        id = re.findall('>ID: (.*?)(?=<)', response)
        id = id[0]

        yield {"name": name, "id": id, "grade": grade}

    def parse_item_group(self, response):
        return