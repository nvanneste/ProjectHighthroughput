import json
import urllib.request as ur
from pprint import pprint
from urllib.request import urlopen

list_terms = ['Have you ever been diagnosed with one of the following conditions?']#lijst van vragen

url= "https://www.openhumans.org/api/public-data/?source=pgp"
site = ur.urlopen(url).read() #de site openen die gegeven werd
data = json.loads(site.decode()) #moet gedecode worden door anaconda die url niet normaal kan openen

header = ("userid;username;url;basename;") #definieer je titels zodat je de terms kan eraan plakken door +=

output_file = open('Harvard.csv', mode = 'a')#append aan de file anders rewrite het

for terms in list_terms:
    header += (terms + ";")
output_file.write(header + "\n")

#als de next niet niets is dan gaat de loop eeuwig verder zo itereer je over heel de site
while data['next'] or data['next'] == 'null':
    #limit is lengte van de data+ sprongen van 1 om geen gegevens over te slaan
    for i in range(0,len(data["results"]),1):
        #zoekt naar metadata.json files en gaat deze dan de gegevens ophalen
        if 'surveys' and '.json' in data["results"][i]["basename"]:
            userid = data["results"][i]["user"]["id"]
            username = data["results"][i]["user"]["name"]
            downloadurl = data["results"][i]["download_url"]
            basename = data["results"][i]["basename"]
            print_out = (" {};{};{};{};".format(userid,username, downloadurl, basename))
            
            #open de json file en zoek daarin de bepaalde ziekten en rapporteer ze
            link_data = (ur.urlopen(downloadurl).read())
            link = json.loads(link_data.decode())
            for j in range(0, len(link)):
                responses = link[j]["responses"]
                for response in responses:
                    nextquery = response["query"] #de vraag van de json zoeken
                    responsevalue = response["response"]#antwoord van de json zoeken
                    if nextquery in list_terms: #als de vraag in je lijst staat van vragen dan moet hij het antwoord geven
                        print_out += (responsevalue + "|")
            print_out += ("\n")
            output_file.write(print_out)
            
    #open de volgende url en laat deze draaien als er over de 100 range is gepasseerd zodat de 2de link kan gestart 
    #worden
    url = data['next']
    site = ur.urlopen(url).read()
    data = json.loads(site.decode())

output_file.close()