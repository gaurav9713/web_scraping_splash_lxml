import requests
from lxml import html
import json

all_products = []
script = '''
  headers = {
    ['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
    ['cookie'] = 'AKAM_CLIENTID=bc9d67fa2ea0ff0acf7b0ff8db5a1706; gb_lang=en; gb_pipeline=GB; aff_mss_info_bak={"bak":"bak"}; reffer_channel=; landingUrl=https://www.gearbest.com/flash-sale.html; gb_countryCode=IN; gb_currencyCode=USD; gb_vsign=5e5336fc6390d956d37d2b2b0fec91bacaef6d3b; cdn_countryCode=IN; _gcl_au=1.1.698584194.1594886767; _uetsid=979e0632-e692-0660-c1ab-8331e4e47563; _uetvid=ae931966-9cde-326f-f347-82b974cef543; _ga=GA1.2.747840102.1594886768; _gid=GA1.2.709063414.1594886768; _fbp=fb.1.1594886767970.751286273; globalegrow_user_id=d2d3a9dd-c373-ad98-992a-e57a6d4f0ef0; gb_pf=%7B%22rp%22%3A%22originalurl%22%2C%22lp%22%3A%22https%3A%2F%2Fwww.gearbest.com%2Fflash-sale.html%22%2C%22wt%22%3A1594886768784%7D; od=pydgxkwxumkk1594886771242; osr_referrer=originalurl; osr_landing=https%3A%2F%2Fwww.gearbest.com%2Fflash-sale.html; gb_fcm=0; gb_fcmPipeLine=GB; gb_soa_www_session=eyJpdiI6ImtVQ2hSODNtd3dYcndXQ01QTnBzREE9PSIsInZhbHVlIjoiM0psMytOYTZ6bCtkM2thSkFna21JUTFoTGxRR2JrU1o3cXg2b2IxUWcyd0JhMnpRTW84QkMrcnZ2dXRRZDN1dHJDNmVuekZXamZLNWdTR3NMWGtaY3c9PSIsIm1hYyI6IjBkZGYzNjRkMzk3N2YyZWFmM2IyOWM2ZDRhZGIwMWI0NDBhODdjZTY5NDhjYjdkODI1Njg4NTAyZmJmMGYyOTgifQ%3D%3D'
  }
  splash:set_custom_headers(headers)
  splash.private_mode_enabled = false
  splash.images_enabled = false
  assert(splash:go(args.url))
  assert(splash:wait(1))
  return splash:html()    
'''

resp = requests.post(url='http://192.168.99.100:8050/run',
                     json={'lua_source': script,
                           'url': 'https://www.gearbest.com/flash-sale.html'}
                     )

#print(resp.content)
tree = html.fromstring(resp.content)

products = tree.xpath("//div[@id='siteWrap']/div/section/div[2]/ul[2]/li/div")

#name,url,orignal_price,discounted_price

try:
    for product in products:
        p = {
            'name': product.xpath(".//div[contains(@class,'title')]/a/text()")[0].strip(),
            'url': product.xpath(".//div[contains(@class,'title')]/a/@href")[0],
            'orignal_price': product.xpath(".//div[contains(@class,'delete')]/del/@data-currency")[0],
            'discounted_price': product.xpath(".//div[contains(@class,'detail')]/span/@data-currency")[0]
        }
        all_products.append(p)
except IndexError:
    print('price missing')

def write_to_json(filename,data):
    with open(filename,'w') as f:
        f.write(json.dumps(data))


write_to_json('products.json',all_products)
print(all_products)

