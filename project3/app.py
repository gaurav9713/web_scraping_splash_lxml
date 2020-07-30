import requests
from fake_useragent import UserAgent
import pprint
import json
import sqlite3

all_products = []

def scraper(pageNumber=1):
  url = "https://www.walgreens.com/productsearch/v1/products/search"
  ua = UserAgent()
  payload = {"p":pageNumber,"s":24,"view":"allView","geoTargetEnabled":False,"abtest":["tier2","showNewCategories"],"deviceType":"desktop","q":"undefined","id":["350006"],"requestType":"tier3","sort":"Top Sellers","couponStoreId":"15196"}
  headers = {
    'Content-Type': 'application/json',
    'User_Agent': ua.random
  }

  response = requests.request("POST", url, headers=headers, data=json.dumps(payload))

  # pprint.pprint(response.json())
  # print(response.text.encode('utf8'))

  product_info = response.json()['products']
  # pprint.pprint(product_info)

  '''
  #imgUrl,price,id,name[productdisplay],size[productsize],url
'''
  try:
    for product in product_info:
      p = {
        'img': product['productInfo']['imageUrl'],
        'price': product['productInfo']['priceInfo']['regularPrice'],
        'id': product['productInfo']['prodId'],
        'name': product['productInfo']['productDisplayName'],
        'size': product['productInfo']['productSize'],
        'url': f"'https://walgreens.com{product['productInfo']['productURL']}'"
      }
      all_products.append(p)

    pageNumber += 1
    print(pageNumber)
    scraper(pageNumber)
  except KeyError:
    return



scraper()

print(len(all_products))

connection = sqlite3.connect("walgreens.db")
c = connection.cursor()
try:
    c.execute('''
        CREATE TABLE products (
            id TEXT PRIMARY KEY,
            name TEXT,
            url TEXT,
            size TEXT,
            price TEXT,
            image TEXT
        )

    ''')

    connection.commit()
except sqlite3.OperationalError as e:
    print(e)

for product in all_products:
    try:
        c.execute('''
            INSERT INTO products (id, name, url, size, price, image) VALUES (
                ?,?,?,?,?,?
            )
        ''', (
            product['id'],
            product['name'],
            product['url'],
            product['size'],
            product['price'],
            product['img']
        ))
    except sqlite3.IntegrityError:
        pass

connection.commit()
connection.close()


