import messages as msg
import helpers

from time import gmtime, strftime, localtime

settings = helpers.get_settings()

def execute():
	record = helpers.load_record()
	result = helpers.get_project_by_number(record)

	print(result)
	