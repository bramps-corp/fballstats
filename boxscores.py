import requests, bs4, csv
from pprint import pprint
from pymongo import MongoClient

#connect('boxscores')
client = MongoClient()
db = client.boxscoresdb
boxscores = db.boxscores

list_of_boxscores = []
baseurl = 'http://www.pro-football-reference.com/years/2014/games.htm'
response = requests.get(baseurl)
print response.encoding
soup = bs4.BeautifulSoup(response.text, 'html.parser')

#print(soup)

#class Box(Document):
#	url = StringField(required=True)


table = soup.find('table', {'id': 'games'})
rows = table.findAll('tr')
print len(rows)
for row in rows[1:]:
	if 'thead' not in row['class']:
		cells = row.findAll('td')
		try:
			link = cells[3].find('a').get('href')
			#print link
			list_of_boxscores.append(link)
			#Box(url=link).save()
			box = {
				'link': link
			}
			boxscores.insert(box)
		except AttributeError:
			print 'error'
