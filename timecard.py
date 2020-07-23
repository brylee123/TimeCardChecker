import re
import datetime
import helper
import os
import shutil

filename = ""
openfile = "timecard.txt"
outputfile = filename + '_output.csv'

def shift2dtm(strdatetime):
	#"2020-07-07 04:30 PM"
	date = re.findall(r"\d{4}\-\d{2}\-\d{2}", strdatetime)[0] # Should only be one result
	y, m, d = date.split("-")
	date = m+"/"+d+"/"+y
	date = helper.str2date(date)
	time = helper.str2time(re.findall(r"\d{2}:\d{2} [AP]M", strdatetime)[0]) # Should only be one result
	return helper.datetime2dtm(date, time), date

with open(openfile, 'r') as file:
	data = file.read()
	datalist = data.split("\n")

	emp = {}
	error_log = []
	emp_name = ""
	multi_job = False
	for i, row in enumerate(datalist):
		row = row.replace("$0.00", "") # Remove TIPS REPORTED; makes searching for floats easier
		if "Break" in row:
			# Check if break time is 30 minutes +/- 5 minutes
			pass

		if "," in row:
			emp_name = row.strip()
			emp[emp_name] = {}

		elif "*** NO INFORMATION TO REPORT ***" in row and emp_name and not emp[emp_name]: # If no data and employee name has no data, delete.
			del emp[emp_name]

		elif helper.re_exist(r"\d{4}\-\d{2}\-\d{2} \d{2}:\d{2} [AP]M", row): # Valid Shift
			shift = {}
			strshiftstart, strshiftend = re.findall(r"\d{4}\-\d{2}\-\d{2} \d{2}:\d{2} [AP]M", row)

			dtmshiftstart, dateshiftstart = shift2dtm(strshiftstart)
			dtmshiftend,   dateshiftend   = shift2dtm(strshiftend)

			if dateshiftstart != dateshiftend:
				e = "***** CHECK FAIL: Shift does not start and end on the same date."
				erec = "\t"+emp_name+": "+row
				error_log.append(e)
				error_log.append(erec)
				print(e)
				print(erec)

				if helper.inputyn("\tValid error? Usually yes. (y/n): "):
					continue # Remove record
				else:
					pass # Accept as not an error

			hours_worked = re.findall(r"\d+\.\d{2}", row)[0]
			hours_worked = float(hours_worked)

			split_hour = 0
			if not hours_worked: # hours = 0
				continue
			elif hours_worked >= 8: # hours >= 8, grant a split hour
				split_hour = 1

			if "Shifts" not in emp[emp_name]:
				emp[emp_name]["Shifts"] = {
					dateshiftstart: hours_worked
				}
			else:
				if dateshiftstart in emp[emp_name]["Shifts"]: # If clocked in twice in once day
					print("**** Caution: Two separate clock-ins in one day.")
					emp[emp_name]["Shifts"][dateshiftstart] += hours_worked
				else:
					emp[emp_name]["Shifts"][dateshiftstart] = hours_worked

			if "Split" not in emp[emp_name] and split_hour:
				emp[emp_name]["Split"] = {
					dateshiftstart: split_hour
				}
			elif "Split" in emp[emp_name] and split_hour:
				emp[emp_name]["Split"][dateshiftstart] = split_hour

			# Check Break Time
			if "Break" in datalist[i+1]:
				breakrow = datalist[i+1]
				strbreakstart, strbreakend = re.findall(r"\d{2}:\d{2} [AP]M", breakrow)
				timebreakstart, timebreakend = helper.str2time(strbreakstart), helper.str2time(strbreakend)

				duration = datetime.datetime.combine(dateshiftstart, timebreakend) - datetime.datetime.combine(dateshiftstart, timebreakstart)
				timeduration = helper.timedelta2minutes(duration) # In units of minutes

				h0, m0 = helper.time2str(timebreakstart)
				h1, m1 = helper.time2str(timebreakend)

		elif "From" in row and "To" in row: # One Time Date Range Check
			strstart, strend = re.findall(r"\d+/\d+/\d+", row) # Find all dates (might break if there are more than two arguments, but unlikely in this case)
			dtmstart, dtmend = helper.str2date(strstart), helper.str2date(strend)
			
			if "Monday" != dtmstart.strftime("%A") or "Sunday" != dtmend.strftime("%A"):
				e = "***** CHECK FAIL: Day range is not Monday to Sunday"
				erec = "\t"+strstart+" - "+strend
				error_log.append(e)
				error_log.append(erec)
				print(e)
				print(erec)
			else:
				print("CHECK PASS: Day range is Monday to Sunday")

			delta_days = abs(dtmstart-dtmend).days #datetime.timedelta.days produces number of days
			if delta_days != 6:
				e = "***** CHECK FAIL: Day are only "+str(delta_days)+" apart."
				erec = "\t"+str(delta_days)
				error_log.append(e)
				error_log.append(erec)
				print(e)
				print(erec)
			else:
				print("CHECK PASS: Days are a week apart")

		else: # Skips blank lines, headers, and line separators
			continue

	#print(emp)
	for staff in emp:
		print(staff, emp[staff])