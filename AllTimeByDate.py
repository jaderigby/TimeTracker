import json, helpers

import messages as msg

def execute():
	record = helpers.load_record()

	while True:
		projectSelection = msg.select_date_for_times(record)

		if projectSelection is 'x':
			break
		else:
			dates = helpers.compile_date_list(record)
			chosenDate = dates[int(projectSelection) - 1]
			newList = helpers.collect_projects_by_date(dates, record['projects'])

			msg.show_projects_for_date(newList, chosenDate)

	print('''
[Finished]
''')
