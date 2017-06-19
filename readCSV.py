import csv


with open('sample.csv', 'rb') as stockData:
    for row in stockData:
        #Split each row in the file with comma and store in a list called 'columns'
        columns = row.split(",")
        #EQ_PROCE is the 3rd column so extract element at index 2 (n-1)
        #Similarly you can extract other column details
        EQ_PROCE = columns[2]
        CORRECTED_500_CE_PRICE=columns[9]
        CORRECTED_500_PE_PRICE=columns[15]
        print EQ_PROCE 
        print CORRECTED_500_CE_PRICE
        print CORRECTED_500_PE_PRICE
        
