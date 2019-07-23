import re
import csv
import datetime

class employee():
	def __init__(self, eid, account_name, work_hrs, ot_hrs, split_hrs, shifts, dual_acct):
		self.eid = eid
		self.account_name = account_name
		self.work_hrs = work_hrs
		self.ot_hrs = ot_hrs
		self.split_hrs = split_hrs
		self.shifts = shifts
		self.dual_acct = dual_acct

red = "\033[0;31m"
redb = "\033[1;31m"
green = "\033[0;32m"
greenb = "\033[1;32m"
yellow = "\033[0;33m"
cyan = "\033[0;36m"
cyanb = "\033[1;36m"
coff = "\033[0m" 

raw_timecard = []

####################################################
filename = 'tc7.23'
####################################################

openfile = filename + '.csv'
outputfile = filename + '_output.csv'

with open(openfile, newline='') as csvfile:
	raw_csv = csv.reader(csvfile, delimiter=' ', quotechar='|')
	date_is_found = False
	for row in raw_csv:

		row_str = ' '.join(row)

		if row_str == ",,,,,": # Remove empty lines
			continue

		if row_str[:5] == "=====": # Remove line break
			continue

		if row_str[0] == ",": # Remove empty first cell
			row_str = row_str[1:]
		
		if row_str[len(row_str)-5:] == ",,,,,": # Remove empty trailing cells
			row_str = row_str[:-5]

		if row_str == "*** NO INFORMATION TO REPORT ***": # Remove inactive employee
			raw_timecard.pop()
			continue

		if date_is_found:
			if row_str[-1] == ",":
				row_str = row_str[:-1]
			raw_timecard.append(row_str)
		
		# Regex for date
		if re.search("From (([0-9]+)/([0-9]+)/[0-9]+) To (([0-9]+)/([0-9]+)/[0-9]+)", row_str):
			raw_tc_date = row_str
			date_is_found = True

	# Print to check final list
	for row in raw_timecard:
		#print(row)
		pass


# Time Check BEGIN
def timecheck():
	def dayofweekchk(date):
		month, day, year = (int(x) for x in date.split('/'))
		ans = datetime.date(year, month, day)
		return (ans.strftime("%A"), ans)

	raw_date = raw_tc_date[5:]	# Removed "From "
	raw_date = raw_date.split(" To ") # Split " To "

	start_end_DAYS = [] # Check which day of weeks
	start_end_DATE = []
	for date in raw_date:
		days, dates = dayofweekchk(date)
		start_end_DAYS.append(days)
		start_end_DATE.append(dates)

	if start_end_DAYS != ["Monday", "Sunday"]:
		if start_end_DAYS[0] != "Monday":
			print(red, "***** CHECK FAIL: Start date is NOT Monday!", coff)
		if start_end_DAYS[1] != "Sunday":
			print(red, "***** CHECK FAIL: End date is NOT Sunday!", coff)
	else:
		print(green, "CHECK PASS: Start and end dates are Monday to Sunday", coff)

	delta_days = (start_end_DATE[1]-start_end_DATE[0]).days
	if delta_days == 6:
		print(green, "CHECK PASS: Start and end dates are a week apart", coff)
	else:
		print(red, "***** CHECK FAIL: Days are", delta_days, "apart", coff)
timecheck()
# Time Check END
