import csv
from bs4 import BeautifulSoup
import urllib2
import time
import pickle

result_team_link = list()
year_links = list()

# pdb.set_trace()

start_year = range(2001, 2014, 1)
end_year =  range(2002, 2015, 1)
for i in range(len(start_year)):
    if start_year[i] != 2004:
        year = '-'.join(( str(start_year[i]), str(end_year[i])) )
    else:
        year = '_'.join(( str(start_year[i]), str(end_year[i])) )

    link = "".join((
            "http://www.football-lineups.com/tourn/Champions_League_",
            year, "/Stats/Players_Used/"
        ))
    year_links.append(link)

def wanted_team_table(tag):
    return tag.get('width')=="80%" and tag.get('cellspacing')=="0" and \
        tag.get('cellpadding')=="0" and tag.get('border')=="0" and \
        tag.get('bgcolor')=="#f0f0f0"

def scrape_all_links(links, result_list, f_wanted_table, team_or_play, sleep, filenamecsv, filenametxt):
	outputfile = open(filenamecsv, "wb")
	wr_outputfile = csv.writer(outputfile)
	
	i = 0
    
	for link in links:
		time.sleep(sleep)
		
		while True:
			try:
				file_open = urllib2.urlopen(link, timeout=100)
			except urllib2.URLError:
				print "Bad URL or timeout. Put to sleep now"
				time.sleep(150)
				continue
			break
		
		html = file_open.read()
		file_open.close()
		soup = BeautifulSoup(html)

		that_table = soup.find(f_wanted_table)
		for child in that_table.descendants:
			if (child.name == "a") and (child.has_attr("href")) and \
			(team_or_play in child["href"]):
				wanted_link = "".join((
					"http://www.football-lineups.com", child.get("href")
				))
				
				wr_outputfile.writerow([link, wanted_link])
				result_list.append([link, wanted_link])

		print " ".join((team_or_play, "done", str(i)))
		i += 1
		#if i % 40 == 0:
			#time.sleep(150)
			
	outputfile.close()

	outputfile2 = open(filenametxt, "wb") 
	pickle.dump(result_list, outputfile2)
	outputfile2.close()


if __name__ == "__main__":
    scrape_all_links(year_links, result_team_link, wanted_team_table, "team", 0, "result_team_link.csv", "result_team_link2")
    print "Done with team link"
    
