from scrape_team_link import scrape_all_links
import csv
import pickle

file_team_link2 = open("result_team_link2")
result_team_link = pickle.load(file_team_link2)

team_links = list()
for i in range(len(result_team_link)):
    team_links.append(result_team_link[i][1])

def wanted_player_table(tag):
    return tag.get('width')=="690" and tag.get('cellspacing')=="0" and \
        tag.get('cellpadding')=="0" and tag.get('border')=="0" and \
        tag.get('bgcolor')=="#FFFFFF"

result_player_link = list()
if __name__ == "__main__":
    scrape_all_links(team_links, result_player_link, wanted_player_table, "footballer", 4, "result_player_link.csv", "result_player_link2")
    print "Done with player link"

