import messages as msg
import helpers

# settings = helpers.get_settings()

def execute():
	record = helpers.load_record()

	while True:
		projectSelection = msg.select_project_for_times(record)

		if projectSelection is 'x':
			break

		projectName = helpers.retrieve_project_name(projectSelection, helpers.project_list(record))

		totalTimeDict = helpers.calculate_total_time_daily(record['projects'][projectName]['time'])
		totalTime = helpers.calculate_total_time(record['projects'][projectName]['time'])

		print '''
===========================================

{title} ({total})
Description: {description}

Breakdown by Day:
-----------------'''.format(title=projectName, description=record['projects'][projectName]['description'], total=totalTime)
		i = 0
		for item in totalTimeDict:
			if item['date'] == '':
				item['date'] = "-- {} --".format(helpers.date_stamp())
				item['spent'] = "currently tracking"
			i += 1
			print '''
{itemNumber}.  Date:{date}
    Spent: {spent}

===========================================
'''.format(itemNumber=i, date=item['date'], spent=item['spent'])
	print
	print '[Finished]'
	print
