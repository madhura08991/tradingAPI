import csv
import sys
#Creating dummy functions for buy and sell 

def dummyBuy(stockCode, position, strike_price):
    print "Dummy Buy of " + stockCode + "of position: " + position + "at strike price of: " + strike_price
    
def dummySell(stockCode, position, strike_price):
    print "Dummy Sell of " + stockCode + "of position: " + position + "at strike price of: " + strike_price




sys.stdout = open("output.txt", 'wb')

print "Trading Simulation"

stockCode = raw_input("Enter Stock Code: ")
stockCode = stockCode + ".csv"
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
strike_second =raw_input("Enter second position strike price: ")
#Enter the strike prices at which PE and CE will be taken from
first_position_action = raw_input("Enter the first position action: ")
second_position_action = raw_input("Enter the second position action: ")
#Decide which action for PE and which for CE in the beginning
print "First Position" + first_position + first_position_action + " at " + strike_first
print "Second Position" + second_position + second_position_action + " at " + strike_second
#confirmation to the actions we decided

#Initialization of needed variables

iteration = 0
pre_total_CEPE = 0
total_CEPE = 0

#Open the file (use the name of the file without extension)
with open(stockCode, 'rb') as stockData:
    for row in stockData:

        print "Iteration: " + str(iteration)

        #Split each row in the file with comma and store in a list called 'columns'

        columns = row.split(",")
        
        #EQ_PROCE is the 3rd column so extract element at index 2 (n-1)
        #Similarly you can extract other column details

        EQ_PROCE = columns[2]
        CORRECTED_500_CE_PRICE=columns[9]
        CORRECTED_500_PE_PRICE=columns[15]
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
        else:
            difference = total_CEPE - pre_total_CEPE
            print "Value changed from: " + str(pre_total_CEPE) + "->" + str(total_CEPE)
        
        
        if(difference > 0.5 or difference < (-0.5)):
            if (first_position_action == "Buy"):
                dummyBuy(stockCode, first_position, strike_first)
                buyFlag_first=1
                
            else:
                dummySell(stockCode, first_position, strike_first)
                sellFlag_first=1
                
            if (second_position_action == "Buy"):
                dummyBuy(stockCode, second_position, strike_second)
                buyFlag_second=1        
            
            else:
                dummySell(stockCode,second_position,strike_second)
                sellFlag_second=1
        
        else:
            print "Not enough difference no action"
      
        #Set current values as previous and change current values in next iteration    
            
        pre_EQ = columns[2]
        pre_CE_PRICE=columns[9]
        pre_PE_PRICE=columns[15]
        pre_PE_PRICE = pre_PE_PRICE.replace("'","").replace("\n","")
        pre_CE_PRICE = pre_CE_PRICE.replace("'","").replace("\n","")
        try:        
            pre_total_CEPE = float(pre_CE_PRICE) + float(pre_PE_PRICE)
        except ValueError , e :
            print "Value error detected"
        
        iteration = iteration + 1
        
        #print EQ_PROCE + "    |    " + CORRECTED_500_CE_PRICE + "   |   " + CORRECTED_500_PE_PRICE
		#commented the print details becauseof use of dummy functions to emulate buying and seelling

print "Ending Simulator"
