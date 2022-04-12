import messages as msg
import helpers

# settings = helpers.get_settings()

def execute(ARGS):
	argDict = helpers.arguments(ARGS)
	itemToUse = helpers.kv_set(argDict, 'use')
	newProject = helpers.kv_set(argDict, 'name')

	record = helpers.load_record()

	if newProject:
		helpers.new_project(newProject)

	selection = helpers.get_project_by_number(record, itemToUse)

	if selection:

		if selection != 'x':
			record['current'] = selection

			content = helpers.glue_updated_record(record)
			helpers.write_file(helpers.recordPath, content)

			print("")
			msg.switching_project(selection)

	else:
		msg.done()
