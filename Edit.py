import json, helpers
import messages as msg
from datetime import datetime

def execute():
	record = helpers.load_record()
	datesListRaw = []

	for item in record['projects']:
		for time in record['projects'][item]['time']:
			newDate = time['spent_date']
			datesListRaw.append(newDate)
	
	datesList = list(set(datesListRaw))

	while("" in datesList):
		datesList.remove("")
	
	dateObjects = [datetime.strptime(date, '%Y-%m-%d') for date in datesList]
	sortedDates = sorted(dateObjects)
	datesListedOrdered = [date.strftime('%Y-%m-%d') for date in sortedDates]

	while True:
		datesListedOrderedAndFormatted = [helpers.format_date_w_day(date) for date in datesListedOrdered]
		projectSelection = helpers.detailed_user_selection("Select: ", datesListedOrderedAndFormatted)

		if projectSelection == 'exit':
			break
		else:
			chosenDate = datesListedOrdered[projectSelection['index']]
			entries = helpers.get_chronological_entries(chosenDate, record['projects'])

			timeObj = helpers.chrono_selection(chosenDate, entries)

			for i, item in enumerate(record['projects'][timeObj['project']]['time']):
				if item['start'] == timeObj['old']['start'] and item['end'] == timeObj['old']['end']:
					record['projects'][timeObj['project']]['time'][i]['start'] = timeObj['new']['start']
					record['projects'][timeObj['project']]['time'][i]['end'] = timeObj['new']['end']
					record['projects'][timeObj['project']]['time'][i]['spent'] = timeObj['spent']
					record['projects'][timeObj['project']]['time'][i]['spent_date'] = timeObj['spent_date']

			# print(record['projects'][timeObj['project']])

			helpers.write_file(helpers.recordPath, 'const data = ' + json.dumps(record, sort_keys=True, indent=4))

			break

	msg.done()
