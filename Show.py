import messages as msg
import helpers

from time import gmtime, strftime

# settings = helpers.get_settings()

def execute():
	record = helpers.load_record()
	
	current = record['current']
	if current == "":
		msg.no_current_project()
	else:
		description = record['projects'][current]['description']
		today = helpers.date_stamp()
		current_time = helpers.time_stamp()
		tt = '00:00'

		tracking = False
		for i in record['projects'][current]['time']:
			if i['end'] == '':
				tracking = True
			if i['start'][:-6] == today:
				s = i['spent']
				if s == '':
					s = helpers.time_spent(i['start'], current_time)
				tt = helpers.calculate_time(tt, s)

		totalTime = helpers.calculate_total_time(record['projects'][current]['time'])

		msg.currentProject(current, description, totalTime, tt, tracking)