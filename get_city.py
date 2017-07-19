import requests
# from scrapy import Selector
from lxml import etree
url = 'https://baike.baidu.com/item/%E5%9C%B0%E7%BA%A7%E5%B8%82'
headers = {
	'host': 'baike.baidu.com',
	'user-agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)',
	'X-Requested-With': 'XMLHttpRequest'
}
res = requests.get(url, headers=headers)
res.encoding = 'utf-8'

citys = etree.HTML(res.content).xpath('//table[@class="table-view log-set-param"]//div[@class="para"]/a//text()')
# city = Selector(response=res).xpath('//table[@class="table-view log-set-param"]//div[@class="para"]/a//text()').extract()

# print(city)
# print(len(city))
city = [x.replace('市', '') for x in citys]
# print(city)
# print(len(city))
