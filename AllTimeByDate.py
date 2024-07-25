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
		projectSelection = helpers.user_selection("Select: ", datesListedOrderedAndFormatted)

		if projectSelection == 'exit':
			break
		else:
			chosenDate = datesListedOrdered[int(projectSelection) - 1]
			entries = helpers.get_chronological_entries(chosenDate, record['projects'])

			msg.chrono_breakdown(chosenDate, entries)
			break

	msg.done()
