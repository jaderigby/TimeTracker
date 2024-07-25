import messages as msg
import helpers, json

from time import gmtime, strftime

# settings = helpers.get_settings()

def execute():
	record = helpers.load_record()
	current = record['current']

	selection = helpers.select_project(record)

	if selection != 'x':

		#= First check if there is an open item being tracked, if so, close it
		#=====================================================================

		#= Is there a current project? This check covers the case where it's the first time a project has been created.
		if current == '':
			msg.no_current_project()

		else:
			markedTime = helpers.time_stamp()
			markedDate = helpers.date_stamp()
			tempObj = {}
			openTracking = False

			#= find if current project has an unclosed time, ie, it's still tracking
			for item in record['projects'][current]['time']:
				if item['end'] == '':
					openTracking = True
					tempObj = item
			
			if openTracking:
				# #= close out open project
				tempObj['end'] = markedTime
				tempObj['spent'] = helpers.time_spent(tempObj['start'], tempObj['end'])
				tempObj['spent_date'] = markedDate

				# record['projects'][current]['time'].append(tempObj)

		#= Once open project has been closed, do the switch
		#==================================================
		
		record['current'] = selection

		content = helpers.glue_updated_record(record)

		helpers.write_file(helpers.recordPath, content)

		msg.switching_project(selection)

		#= NEW: After switch, start tracking selected Item
		#=================================================

		markedTime = helpers.time_stamp()
		newItem = helpers.new_time_obj(markedTime)
		record['projects'][selection]['time'].append(newItem)
		content = helpers.glue_updated_record(record)
		helpers.write_file(helpers.recordPath, content)

	else:
		msg.done()