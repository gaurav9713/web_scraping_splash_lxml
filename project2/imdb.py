import requests
from lxml import html
import re


all_movies = []

'''def scrape(url):
    resp = requests.get(
        url=url,
        headers={
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'})
    # print(resp.text)
    tree = html.fromstring(resp.text)

    movies = tree.xpath("//div[@id='wrapper']/div/div/div[contains(@id,'content-2')]/div/div/div[3]/div/div")

    # print(len(movies))

    for movie in movies:
        m = {
            'title': movie.xpath(".//div[3]/h3/a/text()")[0],
            'year': re.findall(r'\d+', movie.xpath(".//div[3]/h3/span[2]/text()")[0])[0],
            'runtime': re.findall(r'\d+', movie.xpath(".//div[3]/p/span[@class='runtime']/text()")[0])[0],
            'rating': movie.xpath(".//div[3]/div/div[contains(@class,'ratings-imdb')]/@data-value")[0]
        }

        all_movies.append(m)

    next_page = tree.xpath("//div[@id='wrapper']/div/div[2]/div[3]/div[1]/div/div[@class='nav']/div[2]/a[contains(@class,'next-page')]/@href")
    if len(next_page)!=0:
        #print(str(f'https://imdb.com{next_page[0]}'))
        scrape(str(f'https://imdb.com{next_page[0]}'))


scrape('https://www.imdb.com/search/title/?genres=drama&groups=top_250&sort=user_rating,desc&ref_=adv_prv')
print(all_movies)
print(len(all_movies))'''


resp = requests.get(
        url='https://www.imdb.com/search/title/?genres=drama&groups=top_250&sort=user_rating,desc&ref_=adv_prv',
        headers={
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'})
    # print(resp.text)
tree = html.fromstring(resp.text)

movies = tree.xpath("//div[@id='wrapper']/div/div/div[contains(@id,'content-2')]/div/div/div[3]/div/div")
for movie in movies:
        m = {
            'title': movie.xpath(".//div[3]/h3/a/text()")[0],
            'year': re.findall(r'\d+', movie.xpath(".//div[3]/h3/span[2]/text()")[0])[0],
            'runtime': re.findall(r'\d+', movie.xpath(".//div[3]/p/span[@class='runtime']/text()")[0])[0],
            'rating': movie.xpath(".//div[3]/div/div[contains(@class,'ratings-imdb')]/@data-value")[0]
        }

        all_movies.append(m)
print(all_movies)