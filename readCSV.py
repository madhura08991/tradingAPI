import csv
import sys
#Creating dummy functions for buy and sell 

def dummyBuy(stockCode, position, strike_price):
    print "Dummy Buy of " + stockCode + " of position: " + position + " at strike price of: " + strike_price
    
def dummySell(stockCode, position, strike_price):
    print "Dummy Sell of " + stockCode + " of position: " + position + " at strike price of: " + strike_price

#sys.stdout = open("output.txt", 'wb')

#Initialization of needed variables

iteration = 0
pre_total_CEPE = 0
total_CEPE = 0

no_transactions = 0     #number of transactions completed

profit_first = 0    #Gives profits for each completed transaction
profit_second = 0
total_profit = 0    #Gives total profit after end of simulation
buy_first = 0         #First position buy and sell prices
sell_first = 0
buy_second = 0        #second position buy and sell prices
sell_second = 0

transaction_first = 0    #To understand whether a transaction pair has completed or not 0=no action done, 1= only one actio done 2=transaction pair complete
transaction_second = 0


print "Trading Simulation"

stockCode = raw_input("Enter Stock Code: ")
stockCode = stockCode + ".csv"
lot_size = int(raw_input("Enter the lot size of Stock: "))

diff_check = float(raw_input("Enter the range of difference: "))
diff_check_neg = -diff_check

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

#Decide which action for PE and which for CE in the beginning
first_position_action = raw_input("Enter the first position action: ")
second_position_action = raw_input("Enter the second position action: ")
#Set the flags according to user input

#these flags tells the algo whether or not these actions are already done or not
buyFlag_first = sellFlag_first = buyFlag_second = sellFlag_second = 0
if(first_position_action == "Buy"):
    sellFlag_first = 1      #block sell position
else:
    buyFlag_first = 1       #block buy position
    
if(second_position_action == "Buy"):
    sellFlag_second = 1     #block sell position
else:
    buyFlag_second = 1      #block buy position

print "First Position: " + first_position + " " + first_position_action + " at " + strike_first
print "Second Position: " + second_position + " " + second_position_action + " at " + strike_second
#confirmation to the actions we decided


#First orders: -> choice to be user inputted
choice_flag = 0
choice = raw_input("Do you want to enter order details(Y/N)? ")
if(choice == "Y"):
    if(first_position_action == "Buy"):
        buy_first = float(raw_input("First Position Buy Price: "))
        dummyBuy(stockCode, first_position, strike_first)
        buyFlag_first = 1
        sellFlag_first = 0
    else:
        sell_first = float(raw_input("First Position Sell Price: "))
        dummySell(stockCode, first_position, strike_first)
        sellFlag_first = 1
        buyFlag_first = 0
    transaction_first = 1
    print "Type of transaction: " + str(transaction_first)
    no_transctions = no_transactions + 1
    if(second_position_action == "Buy"):
        buy_second = float(raw_input("Second Position Buy Price: "))
        dummyBuy(stockCode, second_position, strike_second)
        buyFlag_second = 1
        sellFlag_second = 0
    else:
        sell_second = float(raw_input("Second Position Sell Price: "))
        dummySell(stockCode, second_position, strike_second)
        sellFlag_second = 1
        buyFlag_second = 0
    transaction_second = 1
    print "Type of trnasaction: " + str(transaction_second)
    no_transctions = no_transactions + 1
    pre_total_CEPE = buy_first + sell_first + buy_second + sell_second
    iteration = 1
else:
    iteration = 0


#Open the file (use the name of the file without extension)
with open(stockCode, 'rb') as stockData:
    for row in stockData:

        #Split each row in the file with comma and store in a list called 'columns'
        columns = row.split(",")
        if(iteration > 0):
            print "Iteration: " + str(iteration)

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
            if(total_CEPE == 0):
                continue
            #Getting Value Error : Cannot convert str into float

##################################### Algorithm part ########################################################################################          
            #On first iteration no pre_total_CEPE value available so use default value    
          
            if(iteration == 1):
                difference = diff_check
            elif(iteration == 2):
                difference = total_CEPE - pre_total_CEPE        #On second iteration new difference is calculated
                print "Value changed from: " + str(pre_total_CEPE) + "->" + str(total_CEPE)
            else:
                difference = difference + (total_CEPE - pre_total_CEPE)    #total difference is now calculated from third iteration onwards
                print "Value changed from: " + str(pre_total_CEPE) + "->" + str(total_CEPE)
            print "But actual difference from ordered CEPE is: " + str(difference)

############################# SELL ALGORITHM CODE ##################################################################################
            
            #As per baba's instruction transaction occurs only after sufficient difference (now a variable)
            if((difference >= diff_check) and ((sellFlag_first == 0) or (sellFlag_second == 0))):        
                
################################ FIRST POSITION ##########################################################################################
            
                if(sellFlag_first == 0):    
                    dummySell(stockCode, first_position, strike_first)
                    sellFlag_first = 1 #set the sell flag
                    transaction_first = transaction_first + 1
                    no_transactions = no_transactions + 1
                    print "Type of transaction: " + str(transaction_first)
                    if(first_position == "CE"):
                        sell_first = CORRECTED_500_CE_PRICE
                    else:
                        sell_first = CORRECTED_500_PE_PRICE
    
                    if(transaction_first == 1):
                        buyFlag_first = 0 #reset the buy flag
    
                    else:
                        try:
                            profit_first = float(sell_first) - float(buy_first)
                            total_profit = total_profit + profit_first
                            difference = 0  #reset the difference
                            print "Profit from this transaction: " + str(profit_first)
                            dummySell(stockCode, first_position, strike_first)
                            sellFlag_first = 1
                            transaction_first = 1
                            no_transactions += 1
                            buyFlag_first = 0
                            print "Type of transaction: " + str(transaction_first)
                            if(first_position == "CE"):
                                sell_first = CORRECTED_500_CE_PRICE
                            else:
                                sell_first = CORRECTED_500_PE_PRICE
                        except ValueError, e:
                            print "Value Error detected"
        
########################################### SECOND POSITION ###############################################################################    
                
                if(sellFlag_second == 0):
                    dummySell(stockCode,second_position,strike_second)
                    sellFlag_second=1 #set the sell flag
                    transaction_second = transaction_second + 1 
                    no_transactions = no_transactions + 1
                    print "Type of transaction: " + str(transaction_second)
                    if(second_position == "CE"):
                        sell_second = CORRECTED_500_CE_PRICE     
                    else:
                        sell_second = CORRECTED_500_PE_PRICE
    
                    if(transaction_second == 1):
                        buyFlag_second = 0 #reset the buy flag
    
                    else:
                        try:
                            profit_second = float(sell_second) - float(buy_second)        
                            total_profit = total_profit + profit_second
                            difference = 0
                            print "Profit from this transaction: " + str(profit_second)
                            dummySell(stockCode,second_position,strike_second)
                            sellFlag_second = 1 #set the sell flag
                            buyFlag_second = 0
                            transaction_second = 1 
                            no_transactions = no_transactions + 1
                            print "Type of transaction: " + str(transaction_second)
                            if(second_position == "CE"):
                                sell_second = CORRECTED_500_CE_PRICE     
                            else:
                                sell_second = CORRECTED_500_PE_PRICE
                        
                        except ValueError, e:
                            print "Value Error detected again......"
                            difference = 0

##################################### BUY ALORTIHM CODE #######################################################################################
                        
            elif((difference <= diff_check_neg) and ((buyFlag_first == 0) or (buyFlag_second == 0))):

####################################### FIRST POSITION #####################################################################################    
                if(buyFlag_first == 0):
                    dummyBuy(stockCode, first_position, strike_first)
                    buyFlag_first = 1 #set the buy flag
                    transaction_first = transaction_first+1  #Iterate transaction pair counter
                    no_transactions = no_transactions + 1
                    print "Type of transaction: " + str(transaction_first)
                    if(first_position == "CE"):
                        buy_first = CORRECTED_500_CE_PRICE   #if first transaction then get price and store
                    else:
                        buy_first = CORRECTED_500_PE_PRICE
    
                    if(transaction_first == 1):
                        sellFlag_first = 0 #reset the sell flags
    
                    else:
                            try:
                                profit_first = float(sell_first) - float(buy_first) #if second transaction then calculate profit(in units)
                                difference = 0
                                total_profit = total_profit + profit_first
                                print "Profit from this transaction: " + str(profit_first)
                                dummyBuy(stockCode, first_position, strike_first)
                                buyFlag_first = 1 #set the buy flag
                                sellFlag_first = 0
                                transaction_first = 1  #Iterate transaction pair counter
                                no_transactions = no_transactions + 1
                                print "Type of transaction: " + str(transaction_first)
                                if(first_position == "CE"):
                                    buy_first = CORRECTED_500_CE_PRICE   #if first transaction then get price and store
                                else:
                                    buy_first = CORRECTED_500_PE_PRICE
                            
                            except ValueError ,e:
                                print "Value Error detected again....."
                                difference = 0
                                
################################### SECOND POSITION #######################################################################################
                if(buyFlag_second == 0):        
                    dummyBuy(stockCode, second_position, strike_second)
                    buyFlag_second = 1 #set the buy flag
                    transaction_second = transaction_second + 1
                    no_transactions = no_transactions + 1
                    print "Type of transaction: " + str(transaction_second)
    
                    if(second_position == "CE"):
                        buy_second = CORRECTED_500_CE_PRICE
                    else:
                        buy_second = CORRECTED_500_PE_PRICE
    
                    if(transaction_second == 1):
                        sellFlag_second = 0#reset the sell flag
    
                    else:
                        try:
                            profit_second = float(sell_second) - float(buy_second)
                            difference = 0    #reset the difference
                            total_profit = total_profit + profit_second
                            print "Profit from this transaction: " + str(profit_second)
                            dummyBuy(stockCode, second_position, strike_second)
                            buyFlag_second = 1 #set the buy flag
                            sellFlag_second = 0
                            transaction_second = 1
                            no_transactions = no_transactions + 1
                            print "Type of transaction: " + str(transaction_second)
                            if(second_position == "CE"):
                                buy_second = CORRECTED_500_CE_PRICE
                            else:
                                buy_second = CORRECTED_500_PE_PRICE
    
                        except ValueError ,e:
                            print "ValueError Detected again....."
                            difference = 0
                            
                        
######################### NO ACTION HANDLING CODE ###########################################################################################   
            else:
                print "Not enough difference, or invalid decision averted. No action"
           
           
#######################Undergoing experimental algorithm that replaces this##################################################################           
            #if(transaction_first == 2):
             #   transaction_first = 0               #after a transaction pair is completed clear counter
              #  buyFlag_first = 0
               # sellFlag_first = 0
                #difference = 0            #needs a new difference now
                
            #if(transaction_second == 2):
             #   transaction_second = 0     #after a transaction pair is completed clear counter
              #  buyFlag_second = 0
               # sellFlag_second = 0
                #difference = 0
            
###########################################################################################################################################          
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

        else:
            iteration = 1
        
        #print EQ_PROCE + "    |    " + CORRECTED_500_CE_PRICE + "   |   " + CORRECTED_500_PE_PRICE
		#commented the print details becauseof use of dummy functions to emulate buying and seelling

################################### END OF ALGORITHM CODE ##################################################################################		

print "Total Profit Acquired(in points): " + str(total_profit)
total_profit = float(total_profit)*lot_size
print "Ending Simulator"
print "Total Profit Acquired(in Rs.): " + str(total_profit)
print "No of transactions done: " + str(no_transactions)

#################################### END OF CODE ############################################################################################
