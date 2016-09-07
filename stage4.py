#!/usr/bin/env python
import sys
import re


def get_arrival_time(start, end, date):
	try:
		trips = open('google_transit/stop_times.txt', 'r')
	except IOError as e:
		print('ERROR: "stops.txt" file not found.')
		del e
		sys.exit()

	# Extract/separate info from each line of file, into array:
	lines = []
	for l in trips:
		lines.append(re.findall('"([^"]*)"', l))
	del trips

	# Format start time to be same as file:
	time = date.strftime("%H:%M:00")

	# Extract trips from desired station:
	times = []
	for l in lines:
		if not l:  # skip any blank lines
			continue

		# Extract trips with start station:
		if l[3] == start:
			# Exclude trip of 0 length:
			if l[8] != '0':
				times.append(l)

	# Sort trips into order by time for searching:
	times.sort(key=lambda x: x[2])

	# Extracts trips after desired time:
	trips = []
	for l in times:
		if l[2] > time:
			trips.append(l)

	# Generates list of trips that will arrive at desired end station:
	new_trips = []
	for l in lines:
		if not l:  # skip any blank lines
			continue

		for t in trips:
			if l[0] == t[0] and l[3] == end:
				if l[1] > time:
					new_trips.append(l)

	# Sorts to find earliest arrival:
	new_trips.sort(key=lambda x: x[1])
	arrive_time = False

	# Find arrival time (that is after departure time):
	for n in new_trips:
		if n[1] > trips[0][2]:
			arrive_time = n[1]
			break

	# Sends error if it sadly did not work :(
	if not arrive_time:
		print('ERROR: Unable to find valid trip. :(')
		arrive_time = '00:00:00'

	return arrive_time
