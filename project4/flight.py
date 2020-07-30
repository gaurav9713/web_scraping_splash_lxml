import requests
from lxml import html
import pprint
script = '''
  headers = {['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'}
  splash:set_custom_headers(headers)
  splash.private_mode_enabled = false
  splash.images_enabled = false
  assert(splash:go(args.url))
  assert(splash:wait(1))
  return splash:html()
'''

resp = requests.post(url='http://192.168.99.100:8050/run',
                         json={
                             'lua_source': script,
                             'url': 'https://uk.flightaware.com/live/flight/HOP1319'
                         })

print(resp.content)
tree = html.fromstring(resp.content)
pprint.pprint(tree[0])
flight_info = tree.xpath("//div[@id='slideOutPanel']/div[1]/div[2]/div[contains(@class,'Log')]/div[1]/div[1]")

print(flight_info)