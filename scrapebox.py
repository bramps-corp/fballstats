import requests, bs4, csv, re
from pprint import pprint
from pymongo import MongoClient

stats_client = MongoClient()
stats_db = stats_client.statsdb
stats_col = stats_db.stats
stats_col.drop()

box_client = MongoClient()
box_db = box_client.boxscoresdb
box_col = box_db.boxscores 

baseurl = 'http://www.pro-football-reference.com'

#print box_col.count()


# this bit is used to iterate over the table data simultaneously
# making filling up the json objects a bit easier
keys = ('pass_cmp', 'pass_att', 'pass_yds', 'pass_tds', 
		'ints', 'pass_lng', 'rush_att', 'rush_yds', 'rush_tds',
		'rush_lng', 'rec_recs', 'rec_yds', 'rec_tds', 'rec_lng')
ints = (2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15)

stats = {}
list_of_stats = []


for box in box_col.find():
	#game = '/boxscores/201409040sea.htm'
	game = box['link']
	print baseurl + game
	response = requests.get(baseurl + game)
	soup = bs4.BeautifulSoup(response.text, 'html.parser')


	# the first table i want had id div_skill_stats
	# this table contains the traditional box score stats
	# rushing passing receiving etc
	week_table = soup.find('table', {'class': 'stats_table'})
	week_table_rows = week_table.findAll('tr')
	week_table_cells = week_table_rows[0].findAll('td')
	week_table_text = week_table_cells[0].text
	#print week_table_text
	week = re.search('(Week\s)(\d+)(20\d+)(20\d+)', week_table_text).group(2)
	#print week


	table = soup.find('table', {'id': 'skill_stats'})
	rows = table.findAll('tr')
	for row in rows[2:]:
		stats = {}
		if 'thead' not in row['class'] and 'over_header' not in row['class']:
			cells = row.findAll('td')
			#print cells[0].text
			stats['name'] = cells[0].text
			stats['week'] = week
			for k, i in zip(keys, ints):
				#print k + ': ' + str(i)
				if cells[i].string is not None:
					stats[k] = int(cells[i].text)
				else:
					stats[k] = 0
			list_of_stats.append(stats)


#print list_of_stats

stats_col.insert(list_of_stats)
#print stats_col.count()