# %%
# Nicholas J Uhlhorn
# Sumerian Social Network Research Project
# July 2022

import mysql.connector as connection
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys


# %%

# Suppress warning that sql connector is not compatible with our database (seems to work fine so far)
import warnings
warnings.simplefilter(action='ignore', category=UserWarning)

# Database password
pwd_token_file = open("dbtoken.txt", 'r')
pwd_token = pwd_token_file.readline()

# Get names to lookup
names = ['sza3-gu4', 'ur-x', 'inim-{d}szara2', 'e2-masz-ta']

queryDFs = []

# Open connection to database
database = connection.connect(
	host = "sumerian-social-network.clzdkdgg3zul.us-west-2.rds.amazonaws.com",
	database = "sumerianDB",
	user = "root",
	password = pwd_token
)

# Get tablets
# ASSUMPTION: since using distinct, assuming that multiple occurrences of a name on a tablet is the same person
# SELECT DISTINCT rawnames.tabid, yearsequence.year, yearsequence.sequence, proveniences.provenience
# 	FROM rawnames INNER JOIN bestyears 
# 		ON rawnames.tabid = bestyears.tabid 
# 	INNER JOIN yearsequence
# 		ON bestyears.year = yearsequence.year
# 	INNER JOIN proveniences
# 		ON rawnames.tabid = proveniences.tabid
# 	WHERE rawnames.name = "<name>";

name_count = len(names)
progress = 0

print("Querying database:")
for name in names:
	# Set query to search for name
	query = f"SELECT DISTINCT rawnames.tabid, yearsequence.year, yearsequence.sequence, proveniences.provenience FROM rawnames INNER JOIN bestyears ON rawnames.tabid = bestyears.tabid INNER JOIN yearsequence ON bestyears.year = yearsequence.year INNER JOIN proveniences ON rawnames.tabid = proveniences.tabid WHERE rawnames.name = '{name}';"
	# Query the database
	queryDFs.append(pd.read_sql(query, database))
	progress += 1
	print(f"{progress}/{name_count}", end="\r")
print(f"{progress}/{name_count}")

# Close database as we are done with it
database.close()


# %%
from datetime import date
import os
import shutil

try:
	os.mkdir("output")
except:
	print()
try:
	os.mkdir("output/img")
except:
	print()

# Start html file
html_log = open("output/output.html", "w")

todays_date = date.today()

html_log.write(f"<html>\n<head>\n<title>{todays_date}</title>\n <link rel=\"stylesheet\" href=\"style.css\">\n</head>\n<body>\n")

# Generate bar graphs
for i in range(name_count):

	# Start row
	html_log.write("<div class=\"row\">")

	# Get instance of data
	data_name = names[i]
	data = queryDFs[i]

	data = data.astype({'sequence': int})
	data['provenience'] = data['provenience'].str.split(' ').str[0]

	# Extract data
	count_data = data.groupby(['sequence'], as_index=False).agg({'sequence': 'first', 'year': ['first', 'count']})
	years = count_data['sequence']['first']
	counts = count_data['year']['count']
	
	plt.rcParams["figure.figsize"] = (20,12)
	fig, bar_plt = plt.subplots(1,1)

	bars = bar_plt.bar(years, counts)

	bar_plt.set_title(f"Occurrence of \"{data_name}\"")
	bar_plt.set_xlabel("Sequential Date")
	bar_plt.set_ylabel("Tablet Count")
	
	bar_plt.set_xticks(years)
	bar_plt.set_xticklabels(count_data['year']['first'], rotation=90)

	bar_plt.bar_label(bars, padding=3)

	# Save plot
	image_file_name = f"occurrence_of_{data_name}.png"
	plt.savefig(f"output\img\{image_file_name}", bbox_inches="tight")

	# Save plot to html file
	html_log.write(f"<h1>{data_name}</h1>\n")
	html_log.write(f"<div class=\"column\"><img src=\"img\{image_file_name}\"></div>\n")

	##### Generate Bar Plot based on provenience #####
	# '...' = tablet missing from database, '___' = tablet has no known provenience

	data = queryDFs[i]
	data_name = names[i]

	data = data.astype({'sequence': int})
	data['provenience'] = data['provenience'].str.split(' ').str[0]

	count_data = data.groupby(['sequence', 'provenience'], as_index=False).agg({'sequence': 'first', 'year': ['first', 'count'], 'provenience': 'first'})


	unique_proveniences = list(count_data['provenience'].drop_duplicates().iloc[:,0])
	column_names = ['sequence', 'year'] + unique_proveniences

	sequence_occurances = list(count_data['sequence'].drop_duplicates().iloc[:,0])

	plot_data = pd.DataFrame(columns=column_names) 

	for seq in range(min(sequence_occurances), max(sequence_occurances)):
		# Add blank rows
		if seq not in sequence_occurances:
			append_data = [seq, ""] + [0 for c in range(len(unique_proveniences))] 
			plot_data.loc[len(plot_data.index)] = append_data
			continue


		seq_data = count_data[count_data['sequence']['first'] == seq]
		seq_year = seq_data['year']['first'].iloc[0]
		
		counts = []
		for prov in unique_proveniences:
			prov_data = seq_data[seq_data['provenience']['first'] == prov]
			if(len(prov_data) > 0):
				counts.append(prov_data['year']['count'].iloc[0])
			else:
				counts.append(0)
		append_data = [seq, seq_year] + counts
		plot_data.loc[len(plot_data.index)] = append_data

	plt.rcParams["figure.figsize"] = (20,12)
	provenience_bar_plt = plot_data.plot.bar(x='sequence', stacked=True, )

	provenience_bar_plt.set_title(f"Occurrence of \"{data_name}\" split by provenience")
	provenience_bar_plt.set_xlabel("Sequential Date")
	provenience_bar_plt.set_ylabel("Tablet Count")


	provenience_bar_plt.set_xticklabels(plot_data['year'], rotation=90)

	for c in provenience_bar_plt.containers:
		# Optional: if the segment is small or 0, customize the labels
		labels = [int(v.get_height()) if v.get_height() > 0 else '' for v in c]
		
		# remove the labels parameter if it's not needed for customized labels
		provenience_bar_plt.bar_label(c, labels=labels, label_type='center')

	# Save plot
	image_file_name = f"occurrence_of_{data_name}_prov.png"
	plt.savefig(f"output\img\{image_file_name}", bbox_inches="tight")

	# Save plot to html file
	html_log.write(f"<div class=\"column\"><img src=\"img\{image_file_name}\"></div>\n")
	html_log.write(f"</div>")



##### Generate career tracker #####
minYear = np.min(data['sequence'].astype('int'))
maxYear = np.max(data['sequence'].astype('int'))
maxCount = 0

for data in queryDFs:
	count_data = data.groupby(['sequence', 'year']).size().reset_index().rename(columns={0:''})
	counts = count_data.iloc[:,2].to_numpy()
	maxCount = max(maxCount, np.max(counts))

ticks = pd.DataFrame()

fig, careerPlot = plt.subplots(1,1)
for i in range(name_count):
	# Get instance of data
	data_name = names[i]
	data = queryDFs[i]

	data = data.astype({'sequence': int})

	# Extract data
	count_data = data.groupby(['sequence'], as_index=False).agg({'sequence': 'first', 'year': ['first', 'count']})
	years = count_data['sequence']['first']
	counts = count_data['year']['count']

	# Get Scales for points
	scales = [20 + (20*c) for c in counts]

	minYear = min(minYear, np.min(years))
	maxYear = max(maxYear, np.max(years))

	careerPlot.plot(years, np.ones(len(years)) * i, label=names[i])
	careerPlot.scatter(years, np.ones(len(years)) * i, label=names[i], marker=2, s=scales)

	ticks = pd.concat((ticks, count_data))

	# for j in range(len(years)):
	# 	careerPlot.annotate(counts[j], (years[j], i), xytext=(years[j], i+0.03))

ticks = ticks.drop_duplicates()

careerPlot.set_title('Career Tracking of Same Name on Nearby Tablets')
careerPlot.set_ylabel("Name")
careerPlot.set_xlabel("Sequential Date")

careerPlot.set_yticks(np.arange(0,len(names)), names)
careerPlot.set_xticks(np.arange(minYear, maxYear+1), np.arange(minYear, maxYear+1))

careerPlot.set_xticks(ticks['sequence']['first'])
careerPlot.set_xticklabels(ticks['year']['first'], rotation=90)

# Save plot
image_file_name = "careers.png"
plt.savefig(f"output\img\{image_file_name}", bbox_inches="tight")

# Save plot to html file
html_log.write(f"<h1>Careers</h1>\n")
html_log.write(f"<img src=\"img\{image_file_name}\">")

html_log.write("</body>\n</html>")
html_log.close()


