import json
import urllib.request as ur
from pprint import pprint
from urllib.request import urlopen

#alles wat ik wil opvragen + de mogelijke antwoorden
list_terms = ['diabetes', 'alzheimers','autoimmune','chickenpox', 'age_years', 'weight_kg', 'height_cm' ]
neg_answers = ['I do not have this condition', 'No']
dnk_answers = ['Unknown', 'Unspecified']
pos_answers = ['yes', 'Yes']

url= "https://www.openhumans.org/api/public-data/?source=american_gut"
site = ur.urlopen(url).read()
data = json.loads(site.decode()) #decode de json want anaconda heeft problemen ermee om het gewoon te loaden

#append want met w wordt dit constant overschreven
outfile = open('AmericanGut.csv', mode = 'a')

#header info opmaken username, url,... ter navigatie
header = ("username ; url ; basename ;")

#laten loopen zodat er een bepaalde header iedere keer terug komt en de info er rechtstreeks onder komt
for terms in list_terms:
    header += (terms + ";")
outfile.write(header + "\n")
    
#als de next niet niets is dan gaat de loop eeuwig verder zo itereer je over heel de site
while data['next'] != None:
    for i in range(0,len(data["results"]),1):
        #zoekt naar metadata.json files en gaat deze dan de gegevens ophalen
        if 'metadata.json' in data["results"][i]["basename"]:
            username = data["results"][i]["user"]["name"]
            downloadurl = data["results"][i]["download_url"]
            basename = data["results"][i]["basename"]
            print_out = ("{}; {}; {};".format(username, downloadurl, basename))
            
            #open de json file en zoek daarin de bepaalde ziekten en rapporteer ze
            link_data = (ur.urlopen(downloadurl).read())
            link = json.loads(link_data.decode())
            for terms in list_terms:
                if link: #in de downloadjson kijken naar de antwoorden van de vermelde ziekten en omvormen naar binair
                    ans = link[terms]
                    if ans in neg_answers: #antwoorden binair omzetten
                        print_out +=("0 ;")
                    elif ans in dnk_answers:
                        print_out += ("NA ;")
                    elif ans in pos_answers:
                        print_out += ("1 ;")
                    elif link:
                        print_out += (ans + ";") 
                    #als het antwoord niet in de lijst staat gewoon antwoord geven zodat script kan aangepast worden
                else:
                    print_out += ("Not Found ;")
            print_out += ("\n")
            outfile.write(print_out)
            
    #open de volgende url en laat deze draaien als er over de len(data) range is gepasseerd zodat de volgende link 
    #kan gestart worden
    url = data['next']
    site = ur.urlopen(url).read()
    data = json.loads(site.decode())

outfile.close()
