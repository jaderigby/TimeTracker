import messages as msg
import helpers, json

from time import gmtime, strftime

# settings = helpers.get_settings()

def execute():
	record = helpers.load_record()

	selection = helpers.select_project(record)

	if selection != 'x':
		record['current'] = selection

		content = helpers.glue_updated_record(record)

		helpers.write_file(helpers.recordPath, content)

		msg.switching_project(selection)

	else:
		msg.done()