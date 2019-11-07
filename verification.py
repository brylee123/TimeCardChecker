import datetime

red = "\033[0;31m"
redb = "\033[1;31m"
green = "\033[0;32m"
greenb = "\033[1;32m"
yellow = "\033[0;33m"
cyan = "\033[0;36m"
cyanb = "\033[1;36m"
coff = "\033[0m" 

def dayofweekchk(date):
	month, day, year = (int(x) for x in date.split('/'))
	ans = datetime.date(year, month, day)
	return (ans.strftime("%A"), ans)

def timecheck(raw_tc_date):

	raw_date = raw_tc_date[5:]	# Removed "From "
	raw_date = raw_date.split(" To ") # Split " To "

	start_end_DAYS = [] # Check which day of weeks
	start_end_DATE = []
	for date in raw_date:
		days, dates = dayofweekchk(date)
		start_end_DAYS.append(days)
		start_end_DATE.append(dates)

	error = False
	if start_end_DAYS != ["Monday", "Sunday"]:
		if start_end_DAYS[0] != "Monday":
			print(red, "***** CHECK FAIL: Start date is NOT Monday!", coff)
			error = True
		if start_end_DAYS[1] != "Sunday":
			print(red, "***** CHECK FAIL: End date is NOT Sunday!", coff)
			error = True
		quit()

	else:
		print(green, "CHECK PASS: Start and end dates are Monday to Sunday", coff)

	delta_days = (start_end_DATE[1]-start_end_DATE[0]).days
	if delta_days == 6:
		print(green, "CHECK PASS: Start and end dates are a week apart", coff)
	else:
		print(red, "***** CHECK FAIL: Days are", delta_days, "apart", coff)
		quit()

