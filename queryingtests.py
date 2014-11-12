from pymongo import MongoClient
from pprint import pprint

client = MongoClient()
db = client.passingdb
passplays = db.passplays

print 'most deep targets'
depth = 'deep'
sides = ['left', 'middle', 'right']

key = ['target']


group = passplays.aggregate([
	{'$group': {'_id': '$target', 'count': {'$sum': 1}}},
	{'$sort': {'count': -1}}
	])

pprint(group['result'])
