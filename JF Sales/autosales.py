import re
from datetime import datetime

def val_search(label, source):
	raw = re.search(label+' +(-)?\$?([0-9]+,)*[0-9]+\.[0-9]{2}', source)
	line = raw.group(0).strip()
	val = re.search('(-)?([0-9]+,)*[0-9]+\.[0-9]{2}', line)
	sales = val.group(0).strip()
	return float(sales.replace(",", "")) # Remove commas to convert to float

def main():
	days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

	dtmstart = None

	sales_calendar = {}
	for day in days:
		f = open(day+".txt", "r")
		s = f.read()

		if day not in s: # Preliminary search
			break

		m = re.search('\n.*'+day+'.*\n', s)
		strdate = m.group(0).strip() # Day of week with date

		dtmdate = datetime.strptime(strdate, "%A, %B %d, %Y")
		if day == "Monday":
			dtmstart = dtmdate # Benchmark date to compare

		if day == days[dtmdate.weekday()]:
			print("Parsing "+day)
		else:
			break

		timestamp = int(dtmdate.strftime("%Y%m%d"))
		datesales = dtmdate.strftime("%d")

		ccsales = val_search("Total Credit Cards:", s)
		deliverysales = val_search("Total In House Charges:", s)
		gratsales = val_search("TOTAL GRATUITIES:", s)
		cashsales = gratsales + val_search("Total Cash:", s)


		calculated_total_sales = round(ccsales + cashsales + deliverysales - gratsales, 2)

		# Below is the value we will use to verify the calculated sales
		totalsales = val_search("TOTAL PAYMENTS:", s)

		if abs(calculated_total_sales - totalsales) > 0.01:
			print("ERROR: Margin of error is greater than 0.01")

		sales_entry = [datesales,ccsales,cashsales,deliverysales,gratsales]
		sales_calendar[timestamp] = ",".join(["\""+str(x)+"\"" for x in sales_entry])

		#input()

	file = open("sales.csv","w")
	while len(sales_calendar) > 0:
		timekey = min(sales_calendar.keys())
		
		entry = sales_calendar[timekey]
		file.write(entry+"\n")

		del sales_calendar[timekey]

	file.close()

if __name__ == '__main__':
	main()