# Nicholas J Uhlhorn
# February 2022
# A helper program to find and list all tablets that have "..." tagged as a PN and
# save those tablet ids in a text file

import os

# Get CWD
path = os.getcwd()

# Open new file to write to
output = open("dotdotdotTablets.txt", "w")

# Find Tablets with "..." assigned as PN
tablets = os.listdir(path + '/Translated')
total_tablets = len(tablets)
current_tablet = 0
for tablet in tablets:
    current_tablet += 1
    print("%s/%s" % (current_tablet, total_tablets), end='\r')

    tablet_file = open(path + '/Translated/' + tablet, "r")
    current_line = tablet_file.readline()
    tablet_id = current_line[-8:-1]
    tablet_has_dot = False
    tablet_dot_count = 0

    while current_line != '':
        if(current_line.find("[place]") == -1 and current_line.find("\tPN\n") != -1 and current_line.find("...") != -1):
            # Found "..." categorized as a PN thats not a place
            tablet_has_dot = True
            tablet_dot_count += 1
        current_line = tablet_file.readline()

    if tablet_has_dot:
        output.write("%s\t%i\n" % (tablet_id, tablet_dot_count))

print("%s/%s" % (current_tablet, total_tablets))
        
