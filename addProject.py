import messages as msg
import helpers

from time import gmtime, strftime

def execute(PROJECT):
	record = helpers.load_record()

	current = record['current']
	recordedTime = helpers.time_stamp()

	def verify_exists(VAL, RECORD):
		for item in record['projects']:
			if item == VAL:
				return True
		return False

	if verify_exists(PROJECT, record):
		print "Switching to Project: {}".format(PROJECT)
		record['current'] = PROJECT

		content = helpers.glue_updated_record(record)
		helpers.write_file(helpers.recordPath, content)
	else:
		record['current'] = PROJECT
		record['projects'][PROJECT] = helpers.create_new_project(recordedTime)
		record['projects'][PROJECT]['description'] = helpers.add_a_description()

		content = helpers.glue_updated_record(record)
		helpers.write_file(helpers.recordPath, content)
