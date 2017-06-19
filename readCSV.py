import csv

print "Trading Simulation"
stockCode = raw_input("Enter Stock Code: ")
stockCode = stockCode + ".csv"
#Each file will have the stock code as name (use sample for now, later on we will rename files to their stock codes)
#Since Baba wants the first action to be manual
first_position = raw_input("Enter the first position(CE/PE): ")
if (first_position == "CE"):
    second_position = "PE"
else:
    second_position = "CE"
#If we re gonna have both PE and CE first position will be decided by us    
print first_position + second_position
#Just checking if it gave the right positions
strike_first = raw_input("Enter first position strike price: ")
strike_second =raw_input("Enter second position strike price: ")
#Enter the strike prices at which PE and CE will be taken from
first_position_action = raw_input("Enter the first position action: ")
second_position_action = raw_input("Enter the second position action: ")
#Decide which action for PE and which for CE in the beginning
print "First Position" + first_position + first_position_action + " at " + strike_first
print "Second Position" + second_position + second_position_action + " at " + strike_second
#confirmation to the actions we decided
#Open that file (use the name of the file without extension)
with open(stockCode, 'rb') as stockData:
    for row in stockData:
        #Split each row in the file with comma and store in a list called 'columns'
        columns = row.split(",")
        #EQ_PROCE is the 3rd column so extract element at index 2 (n-1)
        #Similarly you can extract other column details
        EQ_PROCE = columns[2]
        CORRECTED_500_CE_PRICE=columns[9]
        CORRECTED_500_PE_PRICE=columns[15]
        print EQ_PROCE + "    |    " + CORRECTED_500_CE_PRICE + "   |   " + CORRECTED_500_PE_PRICE
		#for now print the deatils
