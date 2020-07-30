import requests
from lxml import html
from urllib.parse import urljoin
from pymongo import MongoClient

def insert_into_db(list_currencies):
    client = MongoClient('''<connection_string>''')
    db = client["currencies"]
    collection = db["prices"]
    for currency in list_currencies:
        exists = collection.find_one({'_id': currency['_id']})
        if exists:
            if exists['name'] == currency['name'] and exists['price']!=currency['price'] or exists['market_cap']!=currency['market_cap'] or exists['change']!=currency['change']:
                collection.replace_one({'_id': exists['_id']},currency)
                print(f'Old item: {exists} New Item: {currency}')
        else:
            collection.insert_one(currency)
    client.close()


all_currencies = []


def scrape(url):
    #print(url)
    resp = requests.get(url=url,
                        headers={
                            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'})

    tree = html.fromstring(html=resp.text)
    currencies = tree.xpath("//tbody/tr")
    for i in currencies:
        c = {
            '_id': int(i.xpath(".//td[contains(@class,'rank')]/div/text()")[0]),
            'name': i.xpath(".//td[contains(@class,'sort-by__name')]/div/a/text()")[0],
            'market_cap': i.xpath(".//td[contains(@class,'sort-by__market-cap')]/div/text()")[0],
            'price': i.xpath(".//td[contains(@class,'sort-by__price')]/a/text()")[0],
            'change': i.xpath(".//td[contains(@class,'sort-by__percent')]/div/text()")[0]
        }
        all_currencies.append(c)

    #print(all_currencies)

    next_page = tree.xpath("//div/div/div[contains(@class,'tabs-w')]/div[contains(@class,'pa')]/div[contains(@class,'pa')]/a[contains(@data-qa-id,'button-next')]/@href")
    #print(next_page)
    if len(next_page)!= 0:
        next_url = urljoin(base=url, url=next_page[0])
        scrape(url=next_url)

scrape(url='https://coinmarketcap.com')
#print(all_currencies)
#print(len(all_currencies))
insert_into_db(all_currencies)

#print(currencies)
#print(c)
#print(len(currencies))
