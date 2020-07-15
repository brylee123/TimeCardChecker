import re
import datetime
import helper
import os
import shutil

filename = tc+
openfile = "timecard.txt"
outputfile = filename + '_output.csv'

with open(openfile, 'r') as file:
	data = file.read()
	datalist = data.split("\n")

	emp = {}
	error_log = []
	emp_name = ""
	multi_job = False
	for i, row in enumerate(datalist):
		row = row.replace("$0.00", "") # Remove TIPS REPORTED; makes searching for floats easier
		shift = {}
		if "Break" in row:
			# Check if break time is 30 minutes +/- 5 minutes

		if "," in row:
			multi_job = ("(" in row) and (")" in row)
			emp_name = re.sub(r" \(\w+\)", "", row.strip()) # Remove job description
			emp[emp_name] = {}
		elif "*** NO INFORMATION TO REPORT ***" in row and not emp[emp_name]: # If no data and employee name has no data, delete.
			del emp[emp_name]
			emp_name = ""

		elif re_exist(r"20\d{2}\-\d{2}\-\d{2} \d{2}:\d{2} [AP]M", row):
			def shift(strdatetime):



			strshiftstart, strshiftend = re.findall(r"20\d{2}\-\d{2}\-\d{2} \d{2}:\d{2} [AP]M", row)
			
			dtmshiftstart, tshiftstart = shift(strshiftstart)
			dtmshiftend, tshiftend =



		elif "From" in row and "To" in row: # Date Check
			strstart, strend = re.findall(r"\d+/\d+/\d+", row) # Find all dates (might break if there are more than two arguments, but unlikely in this case)
			dtmstart, dtmend = str2dtm(strstart), str2dtm(strend)
			
			if "Monday" != dtmstart.strftime("%A") or "Sunday" != dtmend.strftime("%A"):
				e = "***** CHECK FAIL: Day range is not Monday to Sunday"
				error_log.append(e)
				print(e)
			else:
				print("CHECK PASS: Day range is Monday to Sunday")

			delta_days = abs(dtmstart-dtmend)
			if delta_days != 6:
				e = "***** CHECK FAIL: Day are only "+str(delta_days)+" apart."
				error_log.append(e)
				print(e)
			else:
				print("CHECK PASS: Days are a week apart")
		else: # Skips blank lines, headers, and line separators
			continue
