import messages as msg
import helpers

settings = helpers.get_settings()

def execute():
	recordRoot = '{}/records'.format(helpers.path('util'))
	recordFilepath = '{}/{}'.format(recordRoot, settings['record'])

	content = helpers.read_file(recordFilepath)
	jsContent = 'const data = ' + content

	helpers.write_file('{}/html/js/record.js'.format(recordRoot), jsContent)

	helpers.run_command('open {}/records/html/dates.html'.format(helpers.path('util')))

	msg.done()
