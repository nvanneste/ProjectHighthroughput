import urllib.request as ur
import csv

username = []
download = []

with open ('GenomeProject.csv') as csvfile:
	reader = csv.DictReader(csvfile)
	for row in reader:
	   download.append(row['downloadurl'])
	   username.append(row['username'])

f = open('vcffiles.csv', 'a')

for i in range(0, len(download),1):
	username[i]
	download[i]
	f.write("{},{}".format(username,download)) 
#ur.urlurlopen(download[i])
#	print(u)

#	import urllib

#testfile = urllib.URLopener()
#testfile.retrieve("http://randomsite.com/file.gz", "file.gz")