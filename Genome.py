import json
import urllib.request as ur
from pprint import pprint
from urllib.request import urlopen
import csv

idlist = []
idlist2 = []

url= "https://www.openhumans.org/api/public-data/?source=vcf_data"
site = ur.urlopen(url).read()
data = json.loads(site.decode())

with open ('AmericanGut.csv') as csvfile:
	reader = csv.DictReader(csvfile)
	for row in reader:
	   idlist.append(row['userid']) #lijst maken van alle id's die aanwezig zijn in americangut

with open ('Harvard.csv') as Harvardfile:
	reader = csv.DictReader(Harvardfile)
	for row in reader:
	   idlist2.append(row['userid'])

uniek = list(set(idlist)) #zorgen dat overlappende ids worden verworpen zodat er niet meerdere keren hetzelfde gegeven wordt
uniek2 = list(set(idlist2)) 

for i in range(0, len(uniek), 1): #de lengte van de idlist wordt er naar overeenkomende gezocht
	for j in range(0, len(data["results"]), 1): #de lengte van de api wordt ook gebruikt om te zoeken naar de ids anders is er overlap heb je 
	#id uit de lijst die nooit ook op de eerste plaats zal komen als in de api
		userid = data["results"][j]["user"]["id"] #userids bekijken van de api
		if uniek[i] == userid and uniek[i] == userid and 'vcf.gz' in data["results"][j]["basename"]: # zoeken naar vcf.gz en dezelfde userid als in de uniek lijst
			userid = data["results"][j]["user"]["id"]
			username = data["results"][j]["user"]["name"]
			downloadurl = data["results"][j]["download_url"]
			basename = data["results"][j]["basename"]
			print("{}, {}, {}, {}".format(userid, username, downloadurl, basename))
