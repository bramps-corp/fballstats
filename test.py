from pymongo import MongoClient
import re

ty = 't.y. hilton'
heybey = 'darius heyward-bey'
play1 = 'Aaron Rodgers pass complete short left to Jordy Nelson for 15 yards (tackle by Earl Thomas)'
play2 = 'Andrew Luck pass complete deep middle to T.Y. Hilton for 50 yards (tackle by Some Guy-Dude)'
play3 = 'Robert Griffin pass complete short right to Pierre Garcon for -2 yards (tackle by Robert Griffin somehow)'
play4 = 'Marshawn Lynch right tackle for 10 yards (tackle by Tramon Williams)'
play5 = 'Alfred Morris left end for 99 yards, touchdown'
play6 = 'DeMarco Murray up the middle for -99 yards (tackle by Jason Hatcher)'
play7 = 'T.Y. Hilton up the middle for no gain (tackle by Jason Hatcher)'
play8 = 'Darius Heyward-Bey right end for -1 yards (tackle by J.J. Watt)'
play9 = 'Eri-c Rei-d left tackle for 1 yard (tackle by Jadaveon Clowney)'
play10 = 'Eric Reid runs right for 0 yards (tackle by J.J. Watt)'

lines = ['left end', 'left tackle', 'left guard', 'up the middle', 'right guard', 'right tackle', 'right end']

if any(l in play10 for l in lines):
	print play10