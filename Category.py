import messages as msg
import helpers

# settings = helpers.get_settings()

def execute():
	record = helpers.load_record()

	category_times = {}

	for project in record["projects"].values():
		category = project["category"]
		time_entries = project["time"]
		
		for entry in time_entries:
			if entry["spent"] == '':
				recordedTime = helpers.time_stamp()
				entry["spent"] = helpers.time_spent(entry['start'], recordedTime)
		total_minutes = sum(
			int(entry["spent"].split(":")[0]) * 60 + int(entry["spent"].split(":")[1])
			for entry in time_entries
		)
		
		hours = total_minutes // 60
		minutes = total_minutes % 60
		
		if category in category_times:
			category_times[category][0] += hours
			category_times[category][1] += minutes
		else:
			category_times[category] = [hours, minutes]

	# Convert any excess minutes to hours if it exceeds 60
	for category, (hours, minutes) in category_times.items():
		category_times[category][0] += minutes // 60
		category_times[category][1] = minutes % 60

	# Format the total time as hours and minutes
	formatted_category_times = {
		category: f"{hours}:{str(minutes).zfill(2)}"
		for category, (hours, minutes) in category_times.items()
	}

	grandTotalHrs = 0
	grandTotalMins = 0
	
	for category, total_time in formatted_category_times.items():
		grandTotalHrs += int(total_time.split(':')[0])
		grandTotalMins += int(total_time.split(':')[1])
		if category:
			print('''
Category:   {}
Total:      {}

'''.format(helpers.decorate('bold', category), total_time))
		else:
			print('''
Category:   {}
Total:      {}

'''.format(helpers.decorate('yellow', 'No Category'), total_time))

	minsToHrs = grandTotalMins // 60
	grandTotalHrs += minsToHrs
	grandTotalMins = grandTotalMins % 60
	if grandTotalMins < 10:
		grandTotalMins = '0' + str(grandTotalMins)
	print()
	print(helpers.decorate('bold', 'Grand Total: {}:{}'.format(grandTotalHrs, grandTotalMins)))
	print()
	msg.done()