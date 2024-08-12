import messages as msg
from datetime import datetime, timedelta
import helpers, calendar, os, json

settings = helpers.get_settings()

def execute():
	recordPath = '{}/records/record.js'.format(helpers.path('util'))
	currDateStr = datetime.now()
	newDocSnippet = '''const data = {
    "current": "Dev Standup",
    "projects": {
        "Dev Standup": {
            "category": "Admin",
            "description": "",
            "orderId": 1,
            "time": []
		}
    }
}'''

	if 'blueprint' in settings:
		projects = json.dumps(settings['blueprint'], sort_keys=True, indent=4)
		indentedProjects = "\n".join("    " + line for line in projects.splitlines())
		newDocSnippet = '''const data = {{
    "current": "Dev Standup",
    "projects": {}
}}'''.format(indentedProjects)

	if currDateStr.day <= 5:
		firstDay = currDateStr.replace(day=1)
		lastDayByDate = firstDay - timedelta(days=1)
		lastDayByDateFormatted = lastDayByDate.strftime("%Y-%m-%d")
		# monthStr = lastDayByDate.strftime("%B")

		archiveRecordPath = '{}/records/record-{}.js'.format(helpers.path('util'), lastDayByDateFormatted)
	else:
		lastDay = calendar.monthrange(currDateStr.year, currDateStr.month)[1]
		lastDayByDate = currDateStr.replace(day=lastDay)
		lastDayByDateFormatted = lastDayByDate.strftime("%Y-%m-%d")
		# monthStr = lastDayByDate.strftime("%B")

		archiveRecordPath = '{}/records/record-{}.js'.format(helpers.path('util'), lastDayByDateFormatted)
		
	if not os.path.isfile(archiveRecordPath):
		helpers.run_command('mv {} {}'.format(recordPath, archiveRecordPath), False)
		helpers.write_file(recordPath, newDocSnippet)
		msg.archiving(archiveRecordPath, recordPath)
	else:
		print('\n{}'.format(helpers.decorate('yellow', 'Record already exists!')))

	msg.done()