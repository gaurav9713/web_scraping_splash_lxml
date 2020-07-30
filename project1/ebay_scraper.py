from lxml import html
import requests
import json

def write_to_json(filename,data):
    with open(filename,'w') as f:
        f.write(json.dumps(data))


resp = requests.get(url='https://www.ebay.com/globaldeals',
                    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'})

#print(resp.text)
tree = html.fromstring(resp.text)
#product_main = tree.xpath("")
item_url = tree.xpath("//div[contains(@class,'ebayui-dne-item-featured-card')]/div[@class='row']/div/div/div[@class='dne-itemtile-detail']/a/@href")
#print(item_url)
title = tree.xpath("//div[contains(@class,'ebayui-dne-item-featured-card')]/div[@class='row']/div/div/div[@class='dne-itemtile-detail']/a/h3/span/span/text()")
#print(len(title))
price = tree.xpath("//div[contains(@class,'ebayui-dne-item-featured-card')]/div[@class='row']/div/div/div[@class='dne-itemtile-detail']/a/div/div/span/text()")
#print(len(price))

items = []
for i in range(len(item_url)):
    data = {'Url': item_url[i],
            'Title':title[i],
            'Prices':price[i]}
    items.append(data)
    write_to_json('ebay.json',items)
    #print(data)
    #print(f'Url: {item_url[i]} \nTitle: {title[i]} \nPrice: {price[i]} \n')
