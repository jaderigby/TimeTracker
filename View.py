import messages as msg
import helpers

# settings = helpers.get_settings()

def execute():
	helpers.run_command('open {}/records/html/projects.html'.format(helpers.path('util')))
	msg.done()
