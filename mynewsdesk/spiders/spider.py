import scrapy

from scrapy.loader import ItemLoader
from ..items import MynewsdeskItem
from itemloaders.processors import TakeFirst


class MynewsdeskSpider(scrapy.Spider):
	name = 'mynewsdesk'
	start_urls = ['https://www.mynewsdesk.com/no/bmw-no']

	def parse(self, response):
		post_links = response.xpath('//div[@class="grid js-material-grid"]//a[@class="panel"]/@href')
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):
		title = response.xpath('//h1/text()').get()
		description = response.xpath('//div[@class="panel__text"]//text()[normalize-space()]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description)
		date = response.xpath('//p[@class="type__date"]/time/text()').get()

		item = ItemLoader(item=MynewsdeskItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
