import csv
from bs4 import BeautifulSoup
import urllib2
import socket
import time

result_team_link = list()
result_player_link = list()
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

def wanted_player_table(tag):
    return tag.get('width')=="690" and tag.get('cellspacing')=="0" and \
        tag.get('cellpadding')=="0" and tag.get('border')=="0" and \
        tag.get('bgcolor')=="#FFFFFF"

def scrape_all_links(links, result_list, f_wanted_table, team_or_play):
    i = 1
    for link in links:
        time.sleep(4)
        try:
            file_open = urllib2.urlopen(link, timeout=100)
        except urllib2.URLError:
            print "Bad URL or timeout"
        except socket.timeout:
            print "socket timeout"
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

                result_list.append([link, wanted_link])

        print " ".join((team_or_play, "done", str(i)))
        i += 1
        if i % 40 == 0:
            time.sleep(150)

scrape_all_links(year_links, result_team_link, wanted_team_table, "team")
print "Done with team link"
file_team_link = open("result_team_link.csv", "wb")
wr_team = csv.writer(file_team_link)
for i in range(len(result_team_link)):
    wr_team.writerow(result_team_link[i])

file_team_link2 = open("result_team_link.txt", "wb")
for item in result_team_link:
    file_team_link2.write("%s\n" %item)
file_team_link2.close()

team_links = list()
for i in range(len(result_team_link)):
    team_links.append(result_team_link[i][1])

scrape_all_links(team_links, result_player_link, wanted_player_table, "footballer")
print "Done with player link"
file_player_link = open("result_player_link.csv", "wb")
wr_player = csv.writer(file_player_link)
for i in range(len(result_player_link)):
    wr_player.writerow(result_player_link[i])
file_player_link.close()

file_player_link2 = open("result_player_link.txt", "wb")
for item in result_player_link:
    file_player_link2.write("%s\n" %item)
file_player_link2.close()


print "Start writing result all"
file_all = open("result_all.csv", "wb")
wr_all = csv.writer(file_all)
for i in range(len(result_player_link)):
    team = result_player_link[i][1]
    for j in range(len(result_team_link)):
        if result_team_link[j][1] == team:
            year = result_team_link[j][0]
    result = [year] + result_player_link[0].split("/")[4] + result_player_link[1]
    wr_all.writerow(result)

#file_all = open("result_all.csv", "wb")
#wr_all = csv.writer(file_all)
#for i in range(len(year_links)):
    #for j in range(len(result_team_link)):
        #for k in range(len(result_player_link)):
            #wr_all.writerow([start_year[i],
                            #result_team_link[j].split("/")[5],
                            #result_player_link[k]])
