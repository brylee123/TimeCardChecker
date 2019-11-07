import re
import csv
import datetime
import glob
import os
import shutil
import verification


class employee():
	def __init__(self, eid, account_name, work_hrs, ot_hrs, split_hrs, shifts, dual_acct):
		self.eid = eid
		self.account_name = account_name
		self.work_hrs1 = work_hrs1 # Max 40 total
		self.work_hrs2 = work_hrs2
		self.work_hrs3 = work_hrs3
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

list_of_files = glob.glob('Specific*.xls')
latest_file = max(list_of_files, key=os.path.getctime)

base_file_name = latest_file.replace("Specific Employee Time Cards Report ", "")
base_file_name = base_file_name.replace(".xls", "")

filename = "tc"+base_file_name[:-7]

shutil.copy(latest_file, filename+".txt")
print("XLS to TXT Converted!")

####################################################

openfile = filename + '.txt'
outputfile = filename + '_output.csv'

with open(openfile, newline='') as csvfile:
	raw_csv = csv.reader(csvfile, delimiter=' ', quotechar='|')
	date_is_found = False
	for row in raw_csv:

		row_str = ' '.join(row)

		if row_str == "": # Remove empty lines
			continue

		if row_str[:5] == "=====": # Remove line break
			continue

		if row_str[0] == "\t":
			row_str = row_str[1:]

		if row_str[:6] == "*** NO": # Remove inactive employee
			raw_timecard.pop()
			continue

		if date_is_found:
			if row_str[:5] != "CLOCK" and row_str[:5] != "-----":
				raw_timecard.append(row_str) # Begin parsing data
		
		# Regex for date
		if re.search("From (([0-9]+)/([0-9]+)/[0-9]+) To (([0-9]+)/([0-9]+)/[0-9]+)", row_str):
			verification.timecheck(row_str)
			date_is_found = True

	# Print to check final list
	for row in raw_timecard:
		print(row)
		#pass


