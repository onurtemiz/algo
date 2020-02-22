def dateToInt_(datestr, monthvalue = {1:0, 2:31, 3:59, 4:90, 5:120, 6:151, 7:181, 8:212, 9:243, 10:273, 11:304, 12:334}):
	year, month, day = [int(i) for i in datestr.split("-")]
	return (year-2017)*365 + monthvalue[month] + day

def dateToInt(dataframe): #USE THIS
	dataframe["date"] = dataframe["date"].apply(dateToInt_)