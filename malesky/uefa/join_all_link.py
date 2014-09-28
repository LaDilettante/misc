import csv
import pickle
# from unicode_csv import UnicodeWriter

result_team_link = pickle.load(open("result_team_link2"))
result_player_link = pickle.load(open("result_player_link2"))

fileoutput = open("clean_result_player_link.csv", "w")
wr_fileoutput = csv.writer(fileoutput, lineterminator="\n")
clean_result_player_link = list()
for i in range(len(result_player_link)):
	if i % 2 == 0:
		clean_result_player_link.append(result_player_link[i])
		wr_fileoutput.writerow(result_player_link[i])
		
fileoutput.close()
pickle.dump(clean_result_player_link, open("clean_result_player_link2", "wb"))

print "Start writing result all"
file_all = open("result_all_link.csv", "wb")
wr_all = csv.writer(file_all)

for i in range(len(clean_result_player_link)):
	team = clean_result_player_link[i][0].split("/")[4]

	for j in range(len(result_team_link)):
		if result_team_link[j][1] == clean_result_player_link[i][0]:
			year = result_team_link[j][0].split("/")[4].split("_")[2]
			
			result = [year] + [team] + result_team_link[j] + [clean_result_player_link[i][1]]

			wr_all.writerow(result)
file_all.close()
