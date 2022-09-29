# Nicholas J Uhlhorn
# Sumerian Social Network Research Project
# September 2022

import mysql.connector as connection
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys
import os

# Suppress warning that sql connector is not compatible with our database (seems to work fine so far) TODO: See what is up with this...
import warnings
warnings.simplefilter(action='ignore', category=UserWarning)

def generateCareerGraph(extraCallFunc):
    ##### CONNECT TO DATABASE #####
    # Database password
    pwd_token_file = open("dbtoken.txt", 'r')
    pwd_token = pwd_token_file.readline()

    if (len(sys.argv) < 2):
        print("Incorrect number of arguments, see usage:\npython career_name_info.py <name_of_interest> <name_of_interest> ...")
        exit()

    # Get names to lookup
    names = sys.argv[1:]

    queryDFs = []

    # Open connection to database
    database = connection.connect(
        host = "sumerian-social-network.clzdkdgg3zul.us-west-2.rds.amazonaws.com",
        database = "sumerianDB",
        user = "root",
        password = pwd_token
    )

    ##### GRAB DATA FROM DB #####
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
        query = f"SELECT DISTINCT rawnames.tabid, yearsequence.year, yearsequence.sequence, proveniences.provenience FROM rawnames INNER JOIN bestyears ON rawnames.tabid = bestyears.tabid INNER JOIN yearsequence ON bestyears.year = yearsequence.year INNER JOIN proveniences ON rawnames.tabid = proveniences.tabid WHERE rawnames.name = \'{name}\';"
        # Query the database
        queryDFs.append(pd.read_sql(query, database))
        progress += 1
        print(f"{progress}/{name_count}", end="\r")
    print(f"{progress}/{name_count}")

    # Close database as we are done with it
    database.close()

    ##### FILE STRUCTURE CHECKS #####
    try:
        os.mkdir("output")
    except:
        print()
    try:
        os.mkdir("output/img")
    except:
        print()

    ##### GENERATE CAREER GRAPH #####
    minYear = -1000
    maxYear = 1000
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
    plt.savefig(f"output/img/{image_file_name}", bbox_inches="tight")

    # Call extra function
    extraCallFunc()