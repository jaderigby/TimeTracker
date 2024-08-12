import messages as msg
import helpers

# settings = helpers.get_settings()

def execute(ARGS):
	argDict = helpers.arguments(ARGS)
	record = helpers.load_record()
	newProject = helpers.kv_set(argDict, 'name')
	selectingProject = helpers.kv_set(argDict, 'use')

	current = record['current']

	#= Is there a current project? This check covers the case where it's the first time a project has been created.
	if current == '':
		msg.no_current_project()

	elif selectingProject:
		markedTime = helpers.time_stamp()
		markedDate = helpers.date_stamp()
		tempObj = {}
		openTracking = False

		#= find if current project has an unclosed time, ie, it's still tracking
		for item in record['projects'][current]['time']:
			if item['end'] == '':
				print("yep")
				openTracking = True
				tempObj = item

		if openTracking:
			# #= close out open project
			tempObj['end'] = markedTime
			tempObj['spent'] = helpers.time_spent(tempObj['start'], tempObj['end'])
			tempObj['spent_date'] = markedDate

			#= reassign current project to selected item; start tracking
			selectedProject = helpers.get_project_by_number(record, selectingProject)
			record['current'] = selectedProject
			selectedCurrent = selectedProject

			newItem = helpers.new_time_obj(markedTime)
			record['projects'][selectedCurrent]['time'].append(newItem)
			
			content = helpers.glue_updated_record(record)
			helpers.write_file(helpers.recordPath, content)

			msg.tracking_message(newItem, selectedCurrent)

		elif not openTracking:
			selectedProject = helpers.get_project_by_number(record, selectingProject)
			record['current'] = selectedProject
			selectedCurrent = selectedProject

			newItem = helpers.new_time_obj(markedTime)
			record['projects'][selectedCurrent]['time'].append(newItem)
			
			content = helpers.glue_updated_record(record)
			helpers.write_file(helpers.recordPath, content)

			msg.tracking_message(newItem, selectedCurrent)

	#= Otherwise, let's check if we are creating a project, tracking a current project, or if tracking is already running
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

		if openTracking and not newProject:
			msg.already_tracking(current)

		elif not openTracking and not newProject:
			newItem = helpers.new_time_obj(markedTime)
			record['projects'][current]['time'].append(newItem)

			content = helpers.glue_updated_record(record)
			helpers.write_file(helpers.recordPath, content)

			msg.tracking_message(newItem, current)
		
		elif openTracking and newProject:
			tempObj['end'] = markedTime
			tempObj['spent'] = helpers.time_spent(tempObj['start'], tempObj['end'])
			tempObj['spent_date'] = markedDate

			newItem = helpers.new_time_obj(markedTime)
			# record['projects'][current]['time'].append(tempObj)

			content = helpers.glue_updated_record(record)
			helpers.write_file(helpers.recordPath, content)

			helpers.add_project(newProject)

			msg.new_project_tracking(newProject, markedTime)

		elif newProject:
			helpers.add_project(newProject)

			msg.new_project_tracking(newProject, markedTime)

		#= if has open tracking, and not new project
		else:
			msg.already_tracking(current)