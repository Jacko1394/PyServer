#!/usr/bin/env python
import sys
import datetime
import re
#from urllib2 import Request, urlopen
from urllib import request
import json

station_file = "google_transit/stops.txt"
min_argc = 3


def calc_date(date):
	days2add = 0

	# (N) DAYS FROM:
	if str(date[0]).isdigit():
		days2add = int(date[0])  # save (n) number of days
		del date[0:3]  # delete "(n) days from" args

	# DAY SPECIFIER: today/now, tomorrow, next week or weekday:
	date[0] = date[0].lower()  # convert to lowercase
	if date[0] == ('today' or 'now'):
		del date
	elif date[0] == 'tomorrow':
		days2add += 1
		del date
	elif date[0] == 'next':
		days2add += 7
		del date

	# DAYS OF THE WEEK:
	else:
		# Reference tuple of weekdays:
		days = ('sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday')
		date = str(date[0]).lower()  # convert to lowercase
		# Check weekday match:
		for d in days:
			if date in d:  # mon found in monday
				now = int(datetime.datetime.today().strftime("%w"))
				seeking = days.index(d)
				difference = abs(now - seeking)

				if seeking > now:
					days2add += difference
				else:
					days2add += (7 - difference)
				break

	new_date = datetime.datetime.today() + datetime.timedelta(days=int(days2add))
	return new_date.strftime("%x")


def get_station_list():
	try:
		stops = open(station_file, 'r')
	except IOError as e:
		print('ERROR: "stops.txt" file not found.')
		del e
		sys.exit()

	stations = []

	for l in stops:
		l = l.lower()  # convert to lowercase
		l = re.findall('"([^"]*)"', l)  # extract/separate info

		if not l:  # skip any blank lines (line 1)
			continue

		l[1] = re.sub('\(.*?\)', '', l[1])  # remove text in brackets
		stations.append(l)

	stops.close()

	return stations


def get_station_location(station):

	found = False
	location = ()
	stations = get_station_list()

	for s in stations:
		if station in s[1]:
			found = True
			location = (s[1], s[2], s[3])  # save name, lat, lon

	if not found:
		print("ERROR: Station not found.")
		sys.exit()
	else:
		return location


def get_weather_report(location, date):
	# Calculate number of hours from the current time, based on command arguments:
	hoursfromnow = int((date - datetime.datetime.now()).total_seconds() / 3600)
	# Limit to 168 hours (7 days):
	if hoursfromnow > 168:
		hoursfromnow = 168

	# Forcast API call (% lat, lon):
	weatherapi = request.Request("https://api.forecast.io/forecast/e24dac09f9fd8317208be7bc7504d270/"
		"%s,%s?units=si&extend=hourly&exclude=currently,minutely,daily,alerts,flags"
		% (location[1], location[2]))

	# Extract JSON into data structure:
	weatherdata = json.loads(request.urlopen(weatherapi).read())["hourly"]["data"][hoursfromnow]

	# Report string generation:
	report = "***********WEATHER REPORT***********\n" \
		"Location: %s\nLatitude: %s\nLongitude: %s\n" \
		"" % (str(location[0]).title(), location[1], location[2])

	report += "Time: %s\n" \
		"" % date.strftime("%A %b %d, %Y, %I:%M%p")

	report += "Summary: %s\n" \
		"" % weatherdata["summary"]

	report += "Temp: %s degrees celcius\n" \
		"" % weatherdata["temperature"]

	report += "Rain probability: %s%%\nRain quantity: %s mm/hour\n" \
		"" % (weatherdata["precipProbability"] * 100, weatherdata["precipIntensity"])

	report += "Wind speed: %s km/h\nWind direction: %s degrees\n" \
		"" % (weatherdata["windSpeed"], weatherdata["windBearing"])

	report += "************************************"
	return report


def main():
	if len(sys.argv) < min_argc:
		print("ERROR: Incorrect number of arguments.")
		sys.exit()
	else:
		argc = len(sys.argv)  # save number of arguments
	try:
		# Variables (arguments converted to lowercase):
		location = get_station_location(str(sys.argv[1]).lower())

		# If date specified, calc the number of days from today's date:
		if argc > min_argc:
			date = calc_date(sys.argv[2:argc - 1])
		else:
			date = datetime.datetime.today().strftime("%x")

		# Time extracted from last argument (ARGC - 1):
		time = re.sub(":", "", str(sys.argv[argc - 1]).lower())
		# Add '0' to start of time string if needed (for formatting):
		if len(re.sub("\D", "", time)) < 4:
			time = '0' + time

		# Generate date and time object based on analysed arguments:
		if time.isdigit():
			date = datetime.datetime.strptime("%s%s" % (date, time), "%x%H%M")
		else:  # if time.isdigit is not true, am/pm formatting dealt with:
			date = datetime.datetime.strptime("%s%s" % (date, time), "%x%I%M%p")

		print(get_weather_report(location, date))

	except Exception as e:
		print("ERROR: %s" % e.message)
		sys.exit()


# ------------------------------- END MAIN ------------------------------- #

if __name__ == "__main__":
	main()
