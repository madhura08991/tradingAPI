import csv
import sys
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import style
import datetime as dt
import pandas as pd
import pandas_datareader.data as web

style.use('fivethirtyeight')


#Creating dummy functions for buy and sell 

def dummyBuy(stockCode, position, buy_price):
    print ("Dummy Buy of " + stockCode + " of position: " + position + " at strike price of: " + str(buy_price))
    #plt.plot(buy_price)
    #plt.show()
    
def dummySell(stockCode, position, sell_price):
    print ("Dummy Sell of " + stockCode + " of position: " + position + " at strike price of: " + str(sell_price))
    #plt.plot(sell_price)
    #plt.show()
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


print ("Trading Simulation")

stockCode = input("Enter Stock Code: ")
stockCode = stockCode + ".csv"
lot_size = int(input("Enter the lot size of Stock: "))

diff_check = float(input("Enter the range of difference: "))
diff_check_neg = -diff_check

#Each file will have the stock code as name (use sample for now, later on we will rename files to their stock codes)
#Since Baba wants the first action to be manual
first_position = input("Enter the first position(CE/PE): ")
second_position = input("Enter the second position(CE/PE): ")
#hid the auto position gen as per baba's instructions
   
print (first_position + " " + second_position)
#Just checking if it gave the right positions
strike_first = input("Enter first position strike price: ")
strike_second = input("Enter second position strike price: ")
#Enter the strike prices at which PE and CE will be taken from

#Decide which action for PE and which for CE in the beginning
first_position_action = input("Enter the first position action: ")
second_position_action = input("Enter the second position action: ")
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

print ("First Position: " + first_position + " " + first_position_action + " at " + strike_first)
print ("Second Position: " + second_position + " " + second_position_action + " at " + strike_second)
#confirmation to the actions we decided


#First orders: -> choice to be user inputted
choice_flag = 0
choice = input("Do you want to enter order details(Y/N)? ")
if(choice == "Y"):
    if(first_position_action == "Buy"):
        buy_first = float(input("First Position Buy Price: "))
        dummyBuy(stockCode, first_position, buy_first)
        buyFlag_first = 1
        sellFlag_first = 0
    else:
        sell_first = float(input("First Position Sell Price: "))
        dummySell(stockCode, first_position, sell_first)
        sellFlag_first = 1
        buyFlag_first = 0
    transaction_first = 1
    print ("Type of transaction: " + str(transaction_first))
    no_transctions = no_transactions + 1
    if(second_position_action == "Buy"):
        buy_second = float(input("Second Position Buy Price: "))
        dummyBuy(stockCode, second_position, buy_second)
        buyFlag_second = 1
        sellFlag_second = 0
    else:
        sell_second = float(input("Second Position Sell Price: "))
        dummySell(stockCode, second_position, sell_second)
        sellFlag_second = 1
        buyFlag_second = 0
    transaction_second = 1
    print ("Type of trnasaction: " + str(transaction_second))
    no_transctions = no_transactions + 1
    pre_total_CEPE = buy_first + sell_first + buy_second + sell_second
    iteration = 2
else:
    iteration = 0

df = pd.read_csv(stockCode, parse_dates = True, index_col = 0)

#Open the file (use the name of the file without extension)
for iteration in range(0,(len(df))):
#Split each row in the file with comma and store in a list called 'columns'
#columns = row.split(",")
    if(iteration > 0):
        print ("Iteration: " + str(iteration))
         #EQ_PROCE is the 3rd column so extract element at index 2 (n-1)
        #Similarly you can extract other column details

        CORRECTED_500_CE_PRICE = df.ix[iteration,0]
        CORRECTED_500_PE_PRICE = df.ix[iteration,1]
        #total_CEPE = df.ix[iteration,3]
        total_CEPE = CORRECTED_500_CE_PRICE + CORRECTED_500_PE_PRICE
        if(total_CEPE == 0):
            continue
        #Getting Value Error : Cannot convert str into float
        
        #plt.plot(total_CEPE)
        #plt.plot(CORRECTED_500_CE_PRICE)
        #plt.plot(CORRECTED_500_PE_PRICE)
################################## Algorithm part ####################################################################################
        #On first iteration no pre_total_CEPE value available so use default value    
      
        if(iteration == 1):
            difference = diff_check
        elif(iteration == 2):
            difference = total_CEPE - pre_total_CEPE        #On second iteration new difference is calculated
            print ("Value changed from: " + str(pre_total_CEPE) + "->" + str(total_CEPE))
        else:
            difference = difference + (total_CEPE - pre_total_CEPE)    #total difference is now calculated from third iteration onwards
            print ("Value changed from: " + str(pre_total_CEPE) + "->" + str(total_CEPE))
        print ("But actual difference from ordered CEPE is: " + str(difference))
########################## SELL ALGORITHM CODE ##################################################################################
        
        #As per baba's instruction transaction occurs only after sufficient difference (now a variable)
        if((difference >= diff_check) and ((sellFlag_first == 0) or (sellFlag_second == 0))):        
            
############################ FIRST POSITION ##########################################################################################
        
            if(sellFlag_first == 0):    
                sellFlag_first = 1 #set the sell flag
                transaction_first = transaction_first + 1
                no_transactions = no_transactions + 1
                print ("Type of transaction: " + str(transaction_first))
                if(first_position == "CE"):
                    sell_first = CORRECTED_500_CE_PRICE
                else:
                    sell_first = CORRECTED_500_PE_PRICE
                
                dummySell(stockCode, first_position, sell_first)
                
                if(transaction_first == 1):
                    buyFlag_first = 0 #reset the buy flag

                else:
                    try:
                        profit_first = sell_first - buy_first
                        total_profit = total_profit + profit_first
                        difference = 0  #reset the difference
                        print ("Profit from this transaction: " + str(profit_first))
                        sellFlag_first = 1
                        transaction_first = 1
                        no_transactions += 1
                        buyFlag_first = 0
                        
                        #reorder at same spot
                        print ("Type of transaction: " + str(transaction_first))
                        
                        dummySell(stockCode, first_position, sell_first)   #double sell is a feature 
                    
                    except ValueError as e:
                        print ("Value Error detected")
    
####################################### SECOND POSITION ###############################################################################
            if(sellFlag_second == 0):
                sellFlag_second=1 #set the sell flag
                transaction_second = transaction_second + 1 
                no_transactions = no_transactions + 1
                print ("Type of transaction: " + str(transaction_second))
                if(second_position == "CE"):
                    sell_second = CORRECTED_500_CE_PRICE     
                else:
                    sell_second = CORRECTED_500_PE_PRICE
                    
                dummySell(stockCode,second_position,sell_second)
                    
                if(transaction_second == 1):
                    buyFlag_second = 0 #reset the buy flag

                else:
                    try:
                        profit_second = sell_second - buy_second        
                        total_profit = total_profit + profit_second
                        difference = 0
                        print ("Profit from this transaction: " + str(profit_second))
                        sellFlag_second = 1 #set the sell flag
                        buyFlag_second = 0
                        transaction_second = 1 
                        no_transactions = no_transactions + 1
                        
                        print ("Type of transaction: " + str(transaction_second))
                        
                        dummySell(stockCode,second_position,sell_second)
                    
                    except ValueError as e:
                        print ("Value Error detected again......")
                        difference = 0

##################################BUY ALGORTIHM CODE #######################################################################################
        elif((difference <= diff_check_neg) and ((buyFlag_first == 0) or (buyFlag_second == 0))):
#################################### FIRST POSITION #####################################################################################
            if(buyFlag_first == 0):
                buyFlag_first = 1 #set the buy flag
                transaction_first = transaction_first+1  #Iterate transaction pair
                no_transactions = no_transactions + 1                 
                print ("Type of transaction: " + str(transaction_first))
                if(first_position == "CE"):                     
                    buy_first = CORRECTED_500_CE_PRICE   #get price and store
                else:
                    buy_first = CORRECTED_500_PE_PRICE
                    
                dummyBuy(stockCode, first_position, buy_first)
                    
                if(transaction_first == 1):
                    sellFlag_first = 0 #reset the sell flags
                    
                else:
                    try:
                        profit_first = sell_first - buy_first #if second transaction then calculate profit(in units)
                        difference = 0
                        total_profit = total_profit + profit_first
                        print ("Profit from this transaction: " + str(profit_first))
                        buyFlag_first = 1 #set the buy flag
                        sellFlag_first = 0
                        transaction_first = 1  #Iterate transaction pair counter
                        no_transactions = no_transactions + 1
                            
                        print ("Type of transaction: " + str(transaction_first))
                            
                        dummyBuy(stockCode, first_position, buy_first)
                        
                    except ValueError as e:
                        print ("Value Error detected again.....")
                        difference = 0
                            
############################### SECOND POSITION #######################################################################################
            if(buyFlag_second == 0):        
                buyFlag_second = 1 #set the buy flag
                transaction_second = transaction_second + 1
                no_transactions = no_transactions + 1
                print ("Type of transaction: " + str(transaction_second))
                if(second_position == "CE"):
                    buy_second = CORRECTED_500_CE_PRICE
                else:
                    buy_second = CORRECTED_500_PE_PRICE
                
                dummyBuy(stockCode, second_position, buy_second)
                    
                if(transaction_second == 1):
                    sellFlag_second = 0#reset the sell flag

                else:
                    try:
                        profit_second = sell_second - buy_second
                        difference = 0    #reset the difference
                        total_profit = total_profit + profit_second
                        print ("Profit from this transaction: " + str(profit_second))
                        buyFlag_second = 1 #set the buy flag
                        sellFlag_second = 0
                        transaction_second = 1
                        no_transactions = no_transactions + 1
                        
                        print ("Type of transaction: " + str(transaction_second))
                        
                        dummyBuy(stockCode, second_position, buy_second)
                    
                    except ValueError as e:
                        print ("ValueError Detected again.....")
                        difference = 0
                        
                    
##################### NO ACTION HANDLING CODE ###########################################################################################
        else:
            print ("Not enough difference, or invalid decision averted. No action")
                   
#######################################################################################################################################               #Set current values as previous and change current values in next iteration    
                
        pre_CE_PRICE = CORRECTED_500_CE_PRICE
        pre_PE_PRICE = CORRECTED_500_PE_PRICE
        pre_total_CEPE = total_CEPE
        
        #iteration = iteration + 1
    else:
        iteration = 1
    
    #print EQ_PROCE + "    |    " + CORRECTED_500_CE_PRICE + "   |   " + CORRECTED_500_PE_PRICE
    #commented the print details becauseof use of dummy functions to emulate buying and seelling
################################ END OF ALGORITHM CODE ##############################################################################        

print ("Total Profit Acquired(in points): " + str(total_profit))
total_profit = total_profit * lot_size
print ("Ending Simulator")
print ("Total Profit Acquired(in Rs.): " + str(total_profit))
print ("No of transactions done: " + str(no_transactions))

print ("Print Graph? (Y/N) : ")
graph_in = input()



if(graph_in == "Y"):
    plt.plot(df)
    plt.show()
    

#################################### END OF CODE ############################################################################################
