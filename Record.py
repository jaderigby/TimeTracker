import messages as msg
import helpers

# settings = helpers.get_settings()

def execute():
	helpers.run_command('code {}/records/record.js'.format(helpers.path('util')))
	msg.done()
