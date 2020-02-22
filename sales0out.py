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

total = 500

def getDiffDate(currentDate,testDate):
    date_format = "%Y-%m-%d"
    a = datetime.strptime(currentDate, date_format)
    b = datetime.strptime(testDate, date_format)
    delta = abs(b - a)
    return delta.days

def getExplosion(diff,sales):
    current = 0
    if diff == 0:
        current = int(sales)
    elif diff == 1:
        current = float((sales/100)*95)
    elif diff == 2:
        current = float((sales/100)*90)
    elif diff == 3:
        current = float((sales/100)*85)
    elif diff == 4:
        current = float((sales/100)*80)
    elif diff == 5:
        current = float((sales/100)*75)
    return round(current)

def findProductInDates(allDates,currentStore,currentProduct,currentSales,currentDate):
    global total



    for date in allDates:
        if total == 0:
            break
        for row in testDataArray:

            if row[2] == date and currentStore == row[0] and currentProduct == row[1] :
                first = row[4][0]
                diffDate = getDiffDate(currentDate,row[2])
                print("Diff: " + str(diffDate) + " CurrentSale: " + str(currentSales))
                explosion = getExplosion(diffDate,int(currentSales))
                if (total < explosion or explosion == 0):
                    continue
                row[4] = averageUp(row[4],explosion)
                total -= row[4][0] - first
                outputWriter.writerow([row[0],row[1],row[2],row[3],row[4][0]])
                print("Kaydedildi: " + str(row) + " Total:" + str(total) + " Explosion: " + str(explosion))

outputFile = open('outputZevk.csv', 'w', newline='')
outputWriter = csv.writer(outputFile)
k = 0
for i in saleDataArray[1:]:
    if total == 0:
        break
    k +=1
    currentStore = i[0]
    currentProduct = i[1]
    currentDate = i[2]
    currentSales = i[3]
    currentValue = i[5]
    print(str(k) + ": Date alindi")
    currentSales = float(currentSales.replace(',', '.'))
    if int((currentSales)*100)/75 > float(total):
        continue
    allDates = findAllDates(currentDate)
    findProductInDates(allDates,currentStore,currentProduct,currentSales,currentDate)


outputFile.close()
