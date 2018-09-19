#import necessary packages
import csv
import os

#specify locations to read from and write to
file_to_load = os.path.join("Resources", "budget_data.csv")
file_to_output = os.path.join("analysis", "budget_analysis.txt")

#initialize variables###########################

months_count = 0
sum_total = 0
avg_change = 0
inc_profits = 0
dec_profits = 0
inc_month = ''
dec_month = ''
total_change = 0
avg_change = 0
last_change = 0
profits = []
months = []
index_counter = -1

#################################################

#read from designated file
with open(file_to_load) as financial_data:
    
    #set variable to csv shortcut
    reader = csv.reader(financial_data)

    #save header and skip
    header = next(reader)
    
    #loop through each row in the dataset
    for row in reader:

        #sum the total profits of every month
        sum_total += int(row[1])

        #add each profit to list
        profits.append(int(row[1]))

        #add each month to list
        months.append(row[0])

#add number of months in list of months to variable
months_count = len(months)

#initialize starting profit for use when calculating profit changes
last_profit = profits[0]

#loop through each profit in list of profits    
for profit in profits:
    
    #increase 1 to index counter to use for months list
    index_counter += 1

    #calculate change between profits and save as last change
    last_change = profit - last_profit

    #check if last change in profits is greater than current greatest increase in profits
    if last_change > inc_profits:

        #change greatest increase to values for current month and profit change
        inc_month = months[index_counter]
        inc_profits = last_change

    #check if last change in profits is less than current greatest decrease in profits
    if last_change < dec_profits:

        #change greatest decrease to values for current month and profit change
        dec_month = months[index_counter]
        dec_profits = last_change

    #add last change to total in order to eventually find average change
    total_change += last_change
    
    #change current profit to last profit variable so that we can calculate change at the start of the loop
    last_profit = profit

#calculate average change (months_count - 1 instead of months_count because there is one less CHANGE in profits than there are profits)
avg_change = total_change / (months_count - 1)




#write in the analysis file (create if it doesn't exist)
with open(file_to_output, 'w+') as analysis_file:
    analysis_file.write("Financial Analysis")
    analysis_file.write("\n--------------------")
    analysis_file.write(f"\nTotal Months: {months_count}")
    analysis_file.write(f"\nTotal: ${sum_total}")
    analysis_file.write(f"\nAverage Change: ${round(avg_change, 2)}")
    analysis_file.write(f"\nGreatest Increase in Profits: {inc_month} (${inc_profits})")
    analysis_file.write(f"\nGreatest Decrease in Profits: {dec_month} (${dec_profits})")

#read the text file and output its contents in the terminal
with open(file_to_output, 'r') as analysis_file:
    print_statement = analysis_file.read()
    print(print_statement)



