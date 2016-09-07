#!/usr/bin/env python
import re
import datetime
from stage1 import calc_date, get_station_list, get_weather_report
from stage3 import draw_pic
from stage4 import get_arrival_time

ampm = ('AM', 'PM')
dates = ('Today', 'Tomorrow', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday')
stations = get_station_list()


def generate_label(text, newline):
	data = '<label>%s</label>' % text
	if newline:
		data += '<br>'
	return data


def generate_header(text):
	data = '<header><h3>%s<br></h3></header>' % text
	return data


def generate_station_dropdown(key):
	data = '<select name=%sstation>' % key

	for station in stations:
		data += '<option value="%s">%s</option>' % (station[0], str(station[1]).title())

	data += '</select>'
	return data


def generate_date_dropdown():
	data = '<select name=date>'

	for i in range(0, len(dates)):
		data += '<option value="%s">%s</option>' % (i, dates[i])

	data += '</select>'
	return data


def generate_time_dropdown():
	# Hours:
	data = '<select name=timehour>'
	for i in range(1, 13):
		data += '<option value="%s:00">%s:00</option>' % (i, i)
	data += '</select>'
	# AM/PM:
	data += '<select name=timeampm>'
	data += '<option value="0">AM</option>'
	data += '<option value="1">PM</option>'
	data += '</select>'

	return data


def generate_stage_2_3_page(location, date):
	# Initialisation:
	data = '<html>'
	data += '<head><title>Stage2 : s3529497</title></head>'
	data += '<body>'
	data += generate_header('Stage 2:')
	# Format report for HTML:
	data += re.sub("\n", "<br>", get_weather_report(location, date)) + '<br>'
	data += generate_header('Stage 3:')
	data += '<img src="metroModified.png" alt="assets/metro.png">'
	data += '</body></html>'

	return data


def generate_stage_4_page(start, end, date):

	arrival = get_arrival_time(start, end, date)

	# Initialisation:
	data = '<html>'
	data += '<head><title>Stage4 : s3529497</title></head>'
	data += '<body>'
	data += generate_header('Stage 4:')
	# Format report for HTML:
	data += 'Start time: %s<br>' % date
	data += 'EARLIEST ARRIVAL: %s<br>' % arrival
	data += '</body></html>'

	return data


def stage2webpage():
	# Initialisation:
	data = '<html>'
	data += '<head><title>Stage2 : s3529497</title></head>'
	data += '<body>'
	data += generate_header('Stage 2:')
	data += '<form action="http://127.0.0.1:34567/" method="POST"><br>'
	# Add labels:
	data += generate_label('Starting station: ', False)
	# Add station dropdown menu:
	data += generate_station_dropdown('start') + '<br><br>'
	# Add date dropdown menu:
	data += generate_label('Date: ', False)
	data += generate_date_dropdown() + '<br><br>'
	# Add time dropdown menu:
	data += generate_label('Time: ', False)
	data += generate_time_dropdown() + '<br><br>'
	# Add submit button:
	data += '<input name=submit type="submit" value="Stage 2/3"><br><br><br>'
	# data += generate_label('**************************************************', True)

	data += generate_header('Stage 4:')

	data += generate_label('End station: ', False)

	data += generate_station_dropdown('end') + '<br>'

	data += '<input name=submit type="submit" value="Stage 4"><br><br>'

	data += '</form></body></html>'

	print(data)

	return data


def respond2webpage(formdata):
	# Format date arg:
	date = [dates[int(formdata['date'])]]
	date = calc_date(date)

	# Format time arg:
	time = re.sub(':', '', formdata['timehour'])
	if len(time) < 4:
		time = '0' + time + ampm[int(formdata['timeampm'])]
	else:
		time += ampm[int(formdata['timeampm'])]

	# Format date for weather report call:
	date = datetime.datetime.strptime("%s%s" % (date, time), "%x%I%M%p")

	# Format station arg:
	location = ()

	for s in stations:
		if s[0] == str(formdata['startstation']):
			location = (s[1], s[2], s[3])
			break

	# Draw box around station name:
	draw_pic(formdata['startstation'])

	if formdata['submit'] == 'Stage 2/3':
		data = generate_stage_2_3_page(location, date)
	else:  # Stage 4:
		data = generate_stage_4_page(formdata['startstation'], formdata['endstation'], date)

	return data

def testfuck():
	print('wtf is happening')


#import Webserver
stage2webpage()
