import datetime
import re

def date2str(dtmobj):
	return "" if not dtmobj else str(dtmobj.month)+"/"+str(dtmobj.day)+"/"+str(dtmobj.year) 	# Convert datetime object back to string

def str2date(strdate):
	m, d, y = strdate.split("/") # "06/24/2020" ["6","24","2020"]
	return datetime.date(int(y), int(m), int(d))

def str2time(strtime):
	h, m, ampm = re.split(":| ", strtime) # "04:15 PM" ["04","15","PM"]
	h, m = int(h), int(m)
	if ampm == "PM" and h != 12:
		h += 12
	elif ampm == "AM" and h == 12:
		h = 0
	return datetime.time(h, m)

def time2str(timeobj):
	return int(timeobj.strftime("%H")), int(timeobj.strftime("%M"))

def datetime2dtm(dateobj, timeobj):
	return datetime.datetime.combine(dateobj, timeobj)

def timedelta2minutes(tdduration):
	days, seconds = tdduration.days, tdduration.seconds
	hours   = days * 24 + seconds // 3600
	minutes = (seconds % 3600) // 60
	seconds = (seconds % 60)
	return (hours*60)+minutes

def re_exist(r, s):
	return True if re.search(r, s) else False

def inputyn(s):
	yn = ""
	while yn != "y" and yn != "n":
		yn = input(s).lower()
		if not yn:
			pass
		else:
			yn = yn[0]
	return yn == "y" # True if "y", false if "n"
