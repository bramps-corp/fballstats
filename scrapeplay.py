import requests, bs4, csv, re
from pprint import pprint
from pymongo import MongoClient

client = MongoClient()
db = client.passingdb
passplays = db.passplays
passplays.drop()
list_of_pass_plays = []

runclient = MongoClient()
rundb = client.rundb
runplays = rundb.runplays
runplays.drop()
list_of_run_plays = []

boxclient = MongoClient()
boxdb = client.boxscoresdb
boxcol = boxdb.boxscores

i = 1
line_positions = ['left end', 'left tackle', 'left guard', 'up the middle', 'right guard', 'right tackle', 'right end']


for box in boxcol.find():
	baseurl = 'http://www.pro-football-reference.com'
	game = box['link']
	#game = '/boxscores/201409040sea.htm'

	print baseurl + game + ' - ' + str(i)
	i = i + 1
	response = requests.get(baseurl + game)
	soup = bs4.BeautifulSoup(response.text, 'html.parser')

	pbp_table = soup.find('table', {'id': 'pbp_data'})
	pbp_rows = pbp_table.findAll('tr')

	for row in pbp_rows[1:]:
		pass_play = {}
		run_play = {}
		if 'thead' not in row['class']:
			cells = row.findAll('td')
			# 6th cell is the play
			play_string = str(cells[5].text)
			play_string = play_string.lower()
			printstring = ''
			if 'no play' not in play_string:
				if 'penalty' in play_string and 'declined' not in play_string:
					printstring = 'penalty'
				elif 'pass' in play_string:
					#passing play
					# get passer, distance, side, receiver, yards?
					if 'incomplete' not in play_string:
						if 'conversion' in play_string:
							prinstring = 'conversion'
						else:
							play_details = re.search('.+\s(-*\d+).+', play_string)
							atags = cells[5].findAll('a')
							passer = atags[1].text.lower()
							target = atags[2].text.lower()
							if 'no gain' in play_string:
								yards = 0
							else: 
								# will fix shortly
								yards = play_details.group(1)
							if ' short left ' in play_string:
								depth = 'short'
								area = 'left'
							elif ' short middle ' in play_string:
								depth = 'short'
								area = 'middle'
							elif ' short right ' in play_string:
								depth = 'short'
								area = 'right'
							elif ' deep left ' in play_string:
								depth = 'deep'
								area = 'left'
							elif ' deep middle ' in play_string:
								depth = 'deep'
								area = 'middle'
							else:
								depth = 'deep'
								area = 'right'
							pass_play['passer'] = passer
							pass_play['target'] = target
							pass_play['depth'] = depth
							pass_play['area'] = area
							pass_play['yards'] = yards
							list_of_pass_plays.append(pass_play)
					else:
						if 'intended for' not in play_string:
							printstring = 'incomplete'
						elif 'conversion' in play_string:
							printstring = 'conversion'
						else:
							atags = cells[5].findAll('a')
							passer = atags[1].text.lower()
							target = atags[2].text.lower()
							comp = 'incomplete'
							if ' short ' in play_string:
								depth = 'short'
							else:
								depth = 'long'
							if ' left ' in play_string:
								area = 'left'
							elif ' right ' in play_string:
								area = 'right'
							else:
								area = 'middle'

							pass_play['passer'] = passer
							pass_play['comp'] = comp
							pass_play['depth'] = depth
							pass_play['area'] = area
							pass_play['target'] = target
							pass_play['yards'] = 0
							list_of_pass_plays.append(pass_play)
				elif ' punts' in play_string:
					#get idk..nothing for now? punts aren't interesting yet
					printstring = 'punt'
				elif 'timeout ' in play_string:
					# i think do nothing this doesn't matter to me right now
					printstring = 'timeout'
				elif ' sacked' in play_string:
					# record sack data maybe?
					printstring = 'sack'
				elif ' kicks off' in play_string:
					# kickoff probably don't record anything
					printstring = 'kickoff'
				elif ' field goal' in play_string:
					printstring = 'field goal'
				elif ' kicks extra point' in play_string:
					printstring = 'extra point'
				elif ' spiked' in play_string:
					printstring = 'spike'
				elif ' kneels' in play_string:
					printstring = 'kneel'
				elif 'two point attempt' in play_string:
					printstring = 'conversion attempt'
				elif play_string is '':
					printstring = 'no play, formatting stuff'
				elif any(l in play_string for l in line_positions):
					# HOPEFULLY A RUN IF I COVERED EVERY OTHER DAMN CASE
					atags = cells[5].findAll('a')
					runner = atags[1].text.lower()
					if ' left end ' in play_string:
						area = 'left'
						line = 'tackle'
					elif ' left tackle ' in play_string:
						area = 'left'
						line = 'tackle'
					elif ' left guard ' in play_string:
						area = 'left'
						line = 'guard'
					elif ' up the middle ' in play_string:
						area = 'middle'
						line = 'center'
					elif ' right guard ' in play_string:
						area = 'right'
						line = 'guard'
					elif ' right tackle ' in play_string:
						area = 'right'
						line = 'tackle'
					elif ' right end ' in play_string:
						area = 'right'
						line = 'tackle'
					else:
						playstring = 'error'
					if 'no gain' in play_string:
						yards = 0
					else:
						yards = re.search('.+\s(-*\d+).+', play_string).group(1)
					run_play['runner'] = runner
					run_play['area'] = area
					run_play['line'] = line
					run_play['yards'] = yards
					list_of_run_plays.append(run_play)
				else:
					printstring = 'error'
			else:
				# there was no play so record nothing
				# or maybe the penalty
				printstring = 'accepted penalty'

passplays.insert(list_of_pass_plays)
runplays.insert(list_of_run_plays)

print passplays.count()
print runplays.count()
