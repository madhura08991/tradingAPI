import csv
import sys
#Creating dummy functions for buy and sell 

def dummyBuy(stockCode, position, strike_price):
    print "Dummy Buy of " + stockCode + " of position: " + position + " at strike price of: " + strike_price
    
def dummySell(stockCode, position, strike_price):
    print "Dummy Sell of " + stockCode + " of position: " + position + " at strike price of: " + strike_price




sys.stdout = open("output.txt", 'wb')

print "Trading Simulation"

stockCode = raw_input("Enter Stock Code: ")
stockCode = stockCode + ".csv"
lot_size = int(raw_input("Enter the lot size of Stock: "))
#Each file will have the stock code as name (use sample for now, later on we will rename files to their stock codes)
#Since Baba wants the first action to be manual
first_position = raw_input("Enter the first position(CE/PE): ")
second_position = raw_input("Enter the second position(CE/PE): ")
#hid the auto position gen as per baba's instructions

"""if (first_position == "CE"):
    second_position = "PE"
else:
    second_position = "CE" """
    
print first_position + " " + second_position
#Just checking if it gave the right positions
strike_first = raw_input("Enter first position strike price: ")
strike_second = raw_input("Enter second position strike price: ")
#Enter the strike prices at which PE and CE will be taken from
first_position_action = raw_input("Enter the first position action: ")
second_position_action = raw_input("Enter the second position action: ")
#Decide which action for PE and which for CE in the beginning
print "First Position: " + first_position + " " + first_position_action + " at " + strike_first
print "Second Position: " + second_position + " " + second_position_action + " at " + strike_second
#confirmation to the actions we decided

#Initialization of needed variables

iteration = 0
pre_total_CEPE = 0
total_CEPE = 0

profit_first = 0    #Gives profits for each completed transaction
profit_second = 0
total_profit = 0    #Gives total profit after end of simulation
buy_first = 0         #First position buy and sell prices
sell_first = 0
buy_second = 0        #second position buy and sell prices
sell_second = 0

transaction_first = 0    #To understand whether a transaction pair has completed or not 0=no action done, 1= only one actio done 2=transaction pair complete
transaction_second = 0

#Open the file (use the name of the file without extension)
with open(stockCode, 'rb') as stockData:
    for row in stockData:

        print "Iteration: " + str(iteration)

        #Split each row in the file with comma and store in a list called 'columns'

        columns = row.split(",")
        
        #EQ_PROCE is the 3rd column so extract element at index 2 (n-1)
        #Similarly you can extract other column details

        EQ_PROCE = columns[2]
        CORRECTED_500_CE_PRICE = columns[9]
        CORRECTED_500_PE_PRICE = columns[15]
        CORRECTED_500_PE_PRICE = CORRECTED_500_PE_PRICE.replace("'","").replace("\n","")    
        CORRECTED_500_CE_PRICE = CORRECTED_500_CE_PRICE.replace("'","").replace("\n","")

        try:
            total_CEPE = float(CORRECTED_500_PE_PRICE) + float(CORRECTED_500_CE_PRICE)
        except ValueError, e:
            print "value error detected"

        #Getting Value Error : Cannot convert str into float
      
        #On first iteration no pre_total_CEPE value available so use default value    
      
        if(iteration == 0):
            difference = 0.7
        elif(iteration == 1):
            difference = total_CEPE - pre_total_CEPE        #On second iteration new difference is calculated
            print "Value changed from: " + str(pre_total_CEPE) + "->" + str(total_CEPE)
        else:
            difference = difference + (total_CEPE - pre_total_CEPE)    #total difference is now calculated from third iteration onwards
            print "Value changed from: " + str(pre_total_CEPE) + "->" + str(total_CEPE)
        
        #As per baba's instruction transaction occurs only after sufficient differnce (for now 0.5)
        if(difference > 0.5 or difference < (-0.5)):        
            if (first_position_action == "Buy"):
                dummyBuy(stockCode, first_position, strike_first)
                buyFlag_first = 1 #set the buy flag
                transaction_first = transaction_first+1  #Iterate transaction pair counter
                if(transaction_first == 1):
                    if(first_position == "CE"):
                        buy_first = CORRECTED_500_CE_PRICE   #if first transaction then get price and store
                        profit_first = 0                            #since transaction pair is not complete reset profit
                    else:
                        buy_first = CORRECTED_500_PE_PRICE
                        profit_first = 0
                else:
                    try:
                        profit_first = float(sell_first) - float(buy_first) #if second transaction then calculate profit(in units)
                    except ValueError ,e:
                        print "Value Error detected again....."
            else:
                dummySell(stockCode, first_position, strike_first)
                sellFlag_first = 1 #set the sell flag
                transaction_first = transaction_first+1
                if(transaction_first == 1):
                    if(first_position == "CE"):
                        sell_first = CORRECTED_500_CE_PRICE
                        profit_first = 0
                    else:
                        sell_first = CORRECTED_500_PE_PRICE
                        profit_first =0
                else:
                    try:
                        profit_first = float(sell_first) - float(buy_first)
                    except ValueError ,e:
                        print "Value Error detected again....."
                        
            if (second_position_action == "Buy"):
                dummyBuy(stockCode, second_position, strike_second)
                buyFlag_second = 1 #set the buy flag
                transaction_second = transaction_second+1
                if(transaction_second == 1):
                    if(second_position == "CE"):
                        buy_second = CORRECTED_500_CE_PRICE
                        profit_second = 0
                    else:
                        buy_second = CORRECTED_500_PE_PRICE
                        profit_second = 0
                else:
                    try:
                        profit_second = float(sell_second) - float(buy_second)
                    except ValueError ,e:
                        print "ValueError Detected again....."

            else:
                dummySell(stockCode,second_position,strike_second)
                sellFlag_second=1 #set the sell flag
                transaction_second = transaction_second+1 
                if(transaction_second == 1):
                    if(second_position == "CE"):
                        sell_second = CORRECTED_500_CE_PRICE     
                        profit_second = 0
                    else:
                        sell_second = CORRECTED_500_PE_PRICE
                        profit_second = 0
                else:
                    try:
                        profit_second = float(sell_second) - float(buy_second)        
                    except ValueError, e:
                        print "Value Error detected again......"
        else:
            print "Not enough difference no action"
            
        if (transaction_first == 1 and first_position_action == "Buy"):
            first_position_action = "Sell"     #Since only first action of transaction is done next action is opposite
        elif(transaction_first == 1 and first_position_action == "Sell"):
            first_position_action = "Buy"  
        else:
            transaction_first = 0               #after a transaction pair is completed clear counter
            buyFlag_first = 0
            sellFlag_first = 0
            difference = 0            #needs a new difference now
            
            
            
        if (transaction_second == 1 and second_position_action == "Buy"):
            second_position_action = "Sell"     #Since only first action of transaction is done next action is opposite
        elif(transaction_second == 1 and second_position_action == "Sell"):
            second_position_action = "Buy"
        else:
            transaction_second = 0     #after a transaction pair is completed clear counter
            buyFlag_second = 0
            sellFlag_second = 0
            difference = 0
      
        #Set current values as previous and change current values in next iteration    
            
        pre_EQ = columns[2]
        pre_CE_PRICE = columns[9]
        pre_PE_PRICE = columns[15]
        pre_PE_PRICE = pre_PE_PRICE.replace("'","").replace("\n","")
        pre_CE_PRICE = pre_CE_PRICE.replace("'","").replace("\n","")
        try:        
            pre_total_CEPE = float(pre_CE_PRICE) + float(pre_PE_PRICE)
        except ValueError , e :
            print "Value error detected"
        
        iteration = iteration + 1
        total_profit = float(total_profit) + float(profit_first) + float(profit_second)
        
        #print EQ_PROCE + "    |    " + CORRECTED_500_CE_PRICE + "   |   " + CORRECTED_500_PE_PRICE
		#commented the print details becauseof use of dummy functions to emulate buying and seelling
total_profit = float(total_profit)*lot_size
print "Ending Simulator"
print "Total Profit Acquired: " + str(total_profit)
