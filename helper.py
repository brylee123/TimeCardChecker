import datetime
import re

def dtm2str(dtmobj):
	return "" if not dtmobj else str(dtmobj.month)+"/"+str(dtmobj.day)+"/"+str(dtmobj.year) 	# Convert datetime object back to string

def str2dtm(strdate):
	m, d, y = strdate.split("/") # "06/24/2020" ["6","24","2020"]
	return datetime.datetime(int(y), int(m), int(d))

def str2time(strtime):
	h, m, ampm = re.split(":| ", strtime) # "04:15 PM" ["04","15","PM"]
	h, m = int(h), int(m)
	if ampm == "PM":
		h += 12
	elif ampm == "AM" and h == 12:
		h = 
	return datetime.time(h, m)

def re_exist(r, s):
	return True if re.search(r, s) else False
