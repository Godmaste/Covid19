from bs4 import BeautifulSoup
import requests
import json
import country_converter as coco


data = {'country':[],
        'location': [],
        'name': [],
        'code': []}

URL = "https://en.wikipedia.org/wiki/List_of_international_airports_by_country"

page = requests.get(URL)
soup = BeautifulSoup(page.text, 'lxml')

tables = soup.findAll('table')[1:]

for table in tables:
    country = table.find_previous('span', {'class':'mw-headline'})
    if country.text.endswith('Europe'):
        country = country.find_next('b').text
    else:
        country = country.text
        if country in ['England and Wales', 'Scotland', 'Northern Ireland']:
            country = 'United Kingdom'
        if country in ['Easter Island']:
            country = 'Chile'

    airports = table.findAll('tr')[1:]
    for airport in airports:
        content = airport.findAll('td')

        location = content[0].text.strip()
        name = content[1].text.strip()
        code = content[2].text.strip()

        row = [('country', country),
               ('location', location),
               ('name', name),
               ('code', code)]

        for col, val in row:
            data[col].append(val)

data['country'] = coco.convert(names=data['country'], to='short_name', not_found=None)

with open('airport.json', 'w') as file:
    json.dump(data, file)
