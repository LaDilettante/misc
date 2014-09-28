from unicode_csv import UnicodeWriter

outputfile = open("test_csv_writer.csv", "w")
wr = UnicodeWriter(outputfile)
for i in range(10):
	wr.writerow([str(i), str(i+2)])
	
outputfile.close()
	
