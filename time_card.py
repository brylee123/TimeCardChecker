import re
import csv
import datetime

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
filename = 'tc8.6'
####################################################

openfile = filename + '.csv'
outputfile = filename + '_output.csv'

print(openfile)

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

# Employee Data Entry
employees = {}
delta_t = 0
total_shift_h = 0
employee_name = ""
split_hr = 0

dual_accounts = {}
dual_employee = False

# Employee ID = (Date, Hours)
dual_accounts[2] = ([],[])
dual_accounts[3] = ([],[])
dual_accounts[4] = ([],[])
dual_accounts[5] = ([],[])
dual_accounts[9] = ([],[])
dual_accounts[11] = ([],[])
dual_accounts[14] = ([],[])
dual_accounts[16] = ([],[])
dual_accounts[24] = ([],[])
dual_accounts[25] = ([],[])
dual_accounts[29] = ([],[])
dual_accounts[31] = ([],[])

dual_account_hldr = ["Zheng (Bar), Jason", "Zheng (Expo), Jason",
					 "Wu (Runner), Jonathan", "Wu (Expo), Jonathan",
					 "Huang (Runner), Jay", "Huang (Expo), Jay",
					 "Xiao (Server), Danny","Xiao (Expo), Danny",
					 "Huang (Runner), Joanne", "Huang (Hostess), Joanne",
					 "Chiu (Bar), Kenny", "Chiu (Server), Kenny",
					 "Wu (Runner), Raymond", "Wu (Expo), Raymond",
					 "Lee, Barry", "Lee (Bar), Barry",
					 "Chen (Busser), Kelly", "Chen (Expo), Kelly",
					 "Lau (Bar), Stanley", "Lau (Host), Stanley",
					 "Li, Nick1", "Li, Nick2", 
					 "Cao (Busser), David", "Cao (Delivery), David"]
dual_id = 0

for line in raw_timecard:
	total_hours = 0
	
	if re.search("\"([A-Z]|[a-z]|[0-9]| |\,|\(|\)|)+\"", line):
		#print(line) # All active employees
		employee_name = line[1:-1]
		employees[employee_name] = []
		print("\n*********************************************************")
		print(employee_name)
		if employee_name in dual_account_hldr:
			print("This is a dual employee")
			if employee_name in ["Zheng (Bar), Jason","Zheng (Expo), Jason"]:
				dual_id = 2
			elif employee_name in ["Wu (Runner), Jonathan","Wu (Expo), Jonathan"]:
				dual_id = 3
			elif employee_name in ["Huang (Runner), Jay", "Huang (Expo), Jay"]:
				dual_id = 4			
			elif employee_name in ["Xiao (Server), Danny","Xiao (Expo), Danny"]:
				dual_id = 5
			elif employee_name in ["Huang (Runner), Joanne","Huang (Hostess), Joanne"]:
				dual_id = 9
			elif employee_name in ["Chiu (Bar), Kenny","Chiu (Server), Kenny"]:
				dual_id = 11
			elif employee_name in ["Wu (Runner), Raymond","Wu (Expo), Raymond"]:
				dual_id = 14
			elif employee_name in ["Lee, Barry","Lee (Bar), Barry"]:
				dual_id = 16
			elif employee_name in ["Chen (Busser), Kelly", "Chen (Expo), Kelly"]:
				dual_id = 24
			elif employee_name in ["Lau (Bar), Stanley", "Lau (Host), Stanley"]:
				dual_id = 25
			elif employee_name in ["Li, Nick1", "Li, Nick2"]:
				dual_id = 29
			elif employee_name in ["Cao (Busser), David", "Cao (Delivery), David"]:
				dual_id = 31
			dual_employee = True
		continue

	elif re.search("CLOCK IN DATE/TIME .+", line) or re.search("-{18}.*", line):
		continue
	
	elif re.search("  Break .*", line):
		line = line[11:]
		break_start, break_end = line.split(" - ")
		print("\tBreak Time:", break_start, "to", break_end)

		# Format - "  Break 1: 04:36 PM - 05:04 PM"
		def PM_check(break_time):
			PM = False
			if break_time[-2:] == "PM":
				PM = True
			btime = break_time[:-3] # Remove " PM"
			bhour, bmin = btime.split(":")
			bhour, bmin = int(bhour), int(bmin)
			if PM:
				bhour+=12 # Change to 24-hour format
			return bhour+(bmin/60) # Minutes as decimals

		bstart = PM_check(break_start)
		bend = PM_check(break_end)

		total_btime = bend - bstart
		print("\tTotal Duration:", round(total_btime,2), "hours")

		if abs(delta_t-float(total_shift_h)-total_btime) < 0.05:
			print(green, "CHECK PASS: Ignore last CHECK WARNING", coff)
		continue
	
	elif re.search(">{16}.*", line):
		total_hours = float(line[41:-7])

		print("")

		ot_hours = 0
		if total_hours > 40:
			print(red+"Total Hours: 40", coff)
			print(redb+"Total OT Hours:", round(total_hours-40,2), coff)
			ot_hours = round(total_hours-40,2)
			total_hours = 40

		else:
			print(greenb+"Total Hours:", total_hours, coff)

		print(cyanb+"Total Split Hours:", split_hr, coff)
		
		print("*********************************************************\n")

		if total_hours > 0:
			employees[employee_name].append(total_hours)
			employees[employee_name].append(ot_hours)
			employees[employee_name].append(split_hr)

		# Reset
		dual_employee = False
		total_hours = 0
		ot_hours = 0
		split_hr = 0
		dual_id = 0

	elif re.search(".*Still Clocked In.*", line):
		print(red, "***** CHECK FAIL: Still clocked in.", coff)
	
	else: # Per shift check
		print("--------------------------------------")
		shft = line[:-7]
		shift = shft.split(",")

		print(shift)

		shift_date = []
		shift_time = []

		for clock in shift[:-1]: # Iterate through clock in and out
			clock = clock.split(' ')
			shift_date.append(clock[0])
			shift_time.append(clock[1])

		if shift_date[0] != shift_date[1]:
			print(red, "***** CHECK FAIL: Possible missed clock out! Clock in/out on different dates.", coff)

		else:
			hour1, minute1 = shift_time[0].split(":")
			hour1, minute1 = int(hour1), int(minute1)
			hour2, minute2 = shift_time[1].split(":")
			hour2, minute2 = int(hour2), int(minute2)

			t1 = hour1 + (minute1/60)
			t2 = hour2 + (minute2/60)
			delta_t = t2-t1

			#print("Delta t:", delta_t)
			#print("Documented t:", shift[-1])

			total_shift_h = float(shift[-1])
		

			if abs(delta_t-total_shift_h) < 0.1:
				if total_shift_h > 13:
					print(red, "***** CHECK FAIL: Abnormally long shift!", total_shift_h, "hour long shift", coff)
				elif total_shift_h == 0:
					print(yellow, "***** CHECK WARNING: Zero Time", coff)
				elif total_shift_h < 4:
					print(yellow, "***** CHECK WARNING: Abnormally short shift!", total_shift_h, "hour long shift", coff)
				else:
					if dual_employee:
						print(shift_date[0], total_shift_h)
						dual_accounts[dual_id][0].append(shift_date[0])
						dual_accounts[dual_id][1].append(total_shift_h)
					print(green, "CHECK PASS: Good shift", coff)
				
			else:
				print(yellow, "***** CHECK WARNING: Is there a break?", coff)

			if total_shift_h > 8:
				split_hr += 1
				print(cyan, "\t+1 Split Hour", coff, coff)

print("==== Checking Dual Account Employees for Split Hours ====\n")

# Dual account split hour
for employee in dual_accounts:
	if len(dual_accounts[employee][0]) == len(set(dual_accounts[employee][0])):
		#print("**",dual_accounts[employee][0])
		# If no duplicate dates, no extra split hours for this employee
		continue

	for i, shift in enumerate(dual_accounts[employee][0]): # Date list
		for j, other_shifts in enumerate(dual_accounts[employee][0][i+1:]):
			if shift == other_shifts:
				if dual_accounts[employee][1][i]+dual_accounts[employee][1][j+i+1] > 8: # Use index to find total hours
					#print(dual_accounts[employee][1][i], "+",dual_accounts[employee][1][j+i+1], "SPLIT HOUR")
					if employee == 2:
						employee_name = "Zheng (Bar), Jason"
					elif employee == 3:
						employee_name = "Wu (Runner), Jonathan"
					elif employee == 4:
						employee_name = "Huang (Runner), Jay"
					elif employee == 5:
						employee_name = "Xiao (Server), Danny"
					elif employee == 9:
						employee_name = "Huang (Hostess), Joanne"
					elif employee == 11:
						employee_name = "Chiu (Server), Kenny"
					elif employee == 14:
						employee_name = "Wu (Runner), Raymond"
					elif employee == 16:
						employee_name = "Lee (Bar), Barry"
					elif employee == 24:
						employee_name = "Chen (Busser), Kelly"
					elif employee == 25:
						employee_name = "Lau (Host), Stanley"
					elif employee == 29:
						employee_name = "Li, Nick1"
					elif employee == 31:
						employee_name = "Cao (Busser), David"

					employees[employee_name][2]+=1

					print(cyanb+employee_name, "accrued an additional split hour.", coff)

print("\n=========================================================\n")

empty_tc = []
for em_k in employees.keys():
	if employees[em_k] == []:
		empty_tc.append(em_k)
		continue
	print(em_k+": ", employees[em_k])

for eid in empty_tc:
	del employees[eid]
	print("Popped", eid, "for not having a clock in.")

file = open(outputfile,"w")
#file.write("")
payroll_order =["Rowley, Theresa", 
				"Zheng (Expo), Jason",
				"Zheng (Bar), Jason",
				"Wu (Runner), Jonathan",
				"Wu (Expo), Jonathan",
				"Huang (Runner), Jay",
				"Huang (Expo), Jay",
				"Xiao (Expo), Danny",
				"Xiao (Server), Danny",
				"Ho, Calvin",
				"Huang, William",
				"Huang (Hostess), Joanne",
				"Huang (Runner), Joanne",
				"Chiu (Bar), Kenny",
				"Chiu (Server), Kenny",
				"Loh, Ngan",
				"Tse, Tony",
				"Wu (Runner), Raymond",
				"Wu (Expo), Raymond",
				"Lee, Barry",
				"Lee (Bar), Barry",
				"Fong (Host), Ben",
				"Fong (Runner), Ben",
				"Chen, Yu",
				"Jyoti, Annie",
				"Lam, Sanhoi",
				"Ming, William",
				"Chin, Peter",
				"Chow, Joe",
				"Chen (Busser), Kelly",
				"Chen (Expo), Kelly",
				"Lau (Bar), Stanley",
				"Lau (Host), Stanley",
				"Wang, Liz",
				"Sak, Jeff",
				"Ruan, Sam",
				"Li, Nick1",
				"Yeh, Raymond",
				"Cao (Busser), David", 
				"Cao (Delivery), David",
				"Ming, Mui Chuen",
				"Li, Nick2",
				"Choi, Joseph",
				"Chen, Johnny"]

print("\n==================================")
print("Employee,Hours,OT Hours,Split Hour")
print("==================================")
file.write("Employee,Hours,OT Hours,Split Hour\n")
for employee in payroll_order:
	if employee in employees.keys():
		string = "\""+employee+"\","+str(employees[employee][0])+","+str(employees[employee][1])+","+str(employees[employee][2])+"\n"
		print(string[:-1])
		file.write(string)
