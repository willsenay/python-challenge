#import necessary packages
import csv
import os

#specify locations to read from and write to
file_to_load = os.path.join("Resources", "election_data.csv")
file_to_output = os.path.join("analysis", "election_analysis.txt")

#initialize variables############
vote_count = 0
khan_percent = 0
khan_votes = 0
correy_percent = 0
correy_votes = 0
li_percent = 0
li_votes = 0
tool_percent = 0
tool_votes = 0
winner = ''

#################################

#read from designated location
with open(file_to_load) as election_data:
    
    #set variable to csv shortcut
    reader = csv.reader(election_data)

    #save and skip header
    header = next(reader)

    #loop through rows in data
    for row in reader:

        #add 1 to vote count for each row of data
        vote_count += 1

        #count the khan votes
        if row[2] == 'Khan':
            khan_votes += 1
        
        #count the correy votes
        elif row[2] == 'Correy':
            correy_votes += 1

        #count the li votes
        elif row[2] == 'Li':
            li_votes += 1

        #count the o'tooley votes
        elif row[2] == "O'Tooley":
            tool_votes += 1
    
    #calculate percentages
    khan_percent = khan_votes / vote_count * 100
    correy_percent = correy_votes / vote_count * 100
    li_percent = li_votes / vote_count * 100
    tool_percent = tool_votes / vote_count * 100

#check for highest vote percent and designate winner
if max([khan_percent, correy_percent, li_percent, tool_percent]) == khan_percent:
    winner = 'Khan'
elif max([khan_percent, correy_percent, li_percent, tool_percent]) == correy_percent:
    winner = 'Correy'
elif max([khan_percent, correy_percent, li_percent, tool_percent]) == li_percent:
    winner = 'Li'
elif max([khan_percent, correy_percent, li_percent, tool_percent]) == tool_percent:
    winner = "O'Tooley"

#write analysis in text file in specified location (create file if it doesn't already exist)
with open(file_to_output, 'w+') as analysis_file:
    analysis_file.write("Election Results")
    analysis_file.write("\n--------------------------")
    analysis_file.write(f"\nTotal votes: {vote_count}")
    analysis_file.write("\n--------------------------")
    analysis_file.write(f"\nKhan: {round(khan_percent, 3)}% ({khan_votes})")
    analysis_file.write(f"\nCorrey: {round(correy_percent, 3)}% ({correy_votes})")
    analysis_file.write(f"\nLi: {round(li_percent, 3)}% ({li_votes})")
    analysis_file.write(f"\nO'Tooley: {round(tool_percent, 3)}% ({tool_votes})")
    analysis_file.write("\n--------------------------")
    analysis_file.write(f"\nWinner: {winner}")
    analysis_file.write("\n--------------------------")

#print the text file to the terminal
with open(file_to_output, 'r') as analysis_file:
    print_statement = analysis_file.read()
    print(print_statement)


