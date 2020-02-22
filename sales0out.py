import openpyxl
import csv
from datetime import datetime
from datetime import timedelta
import bisect
#toplam 3.000.000

# Store id ve product id ve date al

#test.xlsxde o id ve o urun icin datete  +5 -5 gunleri al

#secilen gunlerde eger 0sa > zeroLess'in sales_quantitysinin %95ini ekle


#secilen gunler eger 0 degilse > averageFormul yap onu ekle


# toplam - average + first one


saleData = open('saleZeroless.csv')
saleDataReader = csv.reader(saleData, delimiter=';')
saleDataArray = list(saleDataReader)
saleData.close()

testData = open('testnewnew.csv')
testDataReader = csv.reader(testData, delimiter=';')
testDataArray = list(testDataReader)
for row in testDataArray:
    row.append([0,0])
testData.close()

def averageUp(sales,data):
    sales[0]*= sales[1]
    sales[0]+=data
    sales[1]+=1
    sales[0]/=sales[1]
    return sales


def possibleDateGen(date):
    i = 0
    dates = []
    normal_date = datetime.strptime(date, "%Y-%m-%d")
    while i < 5:
        i += 1
        lowDate = normal_date + timedelta(days=-i)
        lowDate = lowDate.strftime("%Y-%m-%d")
        highDate = normal_date + timedelta(days=+i)
        highDate = highDate.strftime("%Y-%m-%d")

        dates.append(lowDate)
        dates.append(highDate)
    return dates

def findAllDates(currentDate):
    possibleDates = possibleDateGen(currentDate)
    return possibleDates

total = 3000000


def findProductInDates(allDates,currentStore,currentProduct,currentSales):
    global total
    for date in allDates:
        for row in testDataArray:
            if row[2] == date and currentStore == row[0] and currentProduct == row[1]:
                first = row[4][0]
                row[4] = averageUp(row[4],int(currentSales))
                total -= row[4][0] - first
                print(currentSales)
                print(row)
                print(total)

for i in saleDataArray[1:]:
    currentStore = i[0]
    currentProduct = i[1]
    currentDate = i[2]
    currentSales = i[3]
    currentValue = i[5]

    allDates = findAllDates(currentDate)
    print("Date alindi")
    findProductInDates(allDates,currentStore,currentProduct,currentSales)

