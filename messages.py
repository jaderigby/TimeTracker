import helpers, json

actionList = json.loads(helpers.read_file('{}/{}'.format(helpers.path('util'), 'action-list.json')))

def statusMessage():
	if len(actionList['actions']) > 0:
		print("")
		for item in actionList['actions']:
			print('''[ {} {} ]\t\t{}'''.format(actionList['alias'], item['name'], item['description']))
		print("")
	else:
		print('''
TimeTracker is working successfully!
''')

def done():
	print('''
[ Process Completed ]
''')

def example():
	print('''
process working!
''')

def no_current_project():
	print('''
You currently have no project set.
''')

def tracking_message(OBJ, CURRENT):
	print('''
===========================================
Project: {}

Beginning tracking: {}

{}
===========================================
'''.format(CURRENT, OBJ['start'], helpers.decorate('green', '[ TIME RECORDING ... ]')))

def new_project_tracking(PROJECT, TIME):
	print('''
===========================================
New Project Created: {}

Beginning tracking: {}

{}
===========================================
'''.format(PROJECT, TIME, helpers.decorate('green', '[ TIME RECORDING ... ]')))

def already_tracking(ITEM):
	print('''
{}
'''.format(helpers.decorate('yellow', helpers.decorate('yellow', 'Project \"{}\" already being tracked.'.format(ITEM)))))

def untracking_message(PROJECT, OBJ):
	spent = helpers.decorate('cyan', OBJ['spent'])
	print('''
===========================================
{status}

Project: {project}

Ending tracking: {end}

Time spent: {spent}
===========================================
'''.format(project= PROJECT, end= OBJ['end'], status= helpers.decorate('yellow', '[ ... TIME RECORDED ]'), spent=spent))

def nothing_being_tracked():
	print('''
{}
'''.format(helpers.decorate('yellow', 'Nothing is currently tracking.')))

def currentProject(ITEM, DESCRIPTION, TOTAL, TIME, TRACKING):
	trackingString = ""
	if TRACKING == True:
		trackingString = helpers.decorate('green', "\n* Currently being tracked *")
	print('''
Current Project:
===========================================

TITLE: {title} ({total_time})

DESCRIPTION: {description}

TODAY: {time_today}
{tracked}
===========================================
'''.format(title=helpers.decorate('bold', ITEM), description=DESCRIPTION, total_time=helpers.decorate('lilac', TOTAL), time_today=helpers.decorate('cyan', TIME), tracked=trackingString))

def switch_to_a_project(ITEMS, CURRENT):
	i = 1
	print()
	print("Projects:")
	print("---------")
	print()
	for item in ITEMS:
		if item['name'] == CURRENT:
			isCurrent = '*'
			isCurrentFront = helpers.decorate('green', "** ")
			isCurrentBack = helpers.decorate('green', " **")
			itemName = helpers.decorate('green', item['name'])
		else:
			isCurrentFront = ""
			isCurrentBack = ""
			itemName = helpers.decorate('bold', item['name'])
		print('[{number}] {isCurrentFront}{item}{isCurrentBack} ({total})\n    Today: {today}\n'.format(number=i, isCurrentFront=isCurrentFront, isCurrentBack=isCurrentBack, item=itemName, total=helpers.decorate('lilac', item['total']), today=helpers.decorate('cyan', item['total_today'])))
		i += 1
	print("[x] Exit")
	print()
	selection = helpers.user_input(helpers.decorate('yellow', "Select a project to switch to: "))
	print()
	return selection

def switching_to_project(PROJECT):
	print("Switching to Project: {}".format(PROJECT))

def switching_project(PROJECT):
	print("Switching to: {}\n".format(PROJECT))

def select_project_for_times(SETTINGS):
	i = 0
	print()
	print('Projects:')
	print('---------')
	print()
	for item in SETTINGS['projects']:
		i += 1
		print('[{number}] {name}'.format(number=i, name=item))
	print()
	print('[x] Exit')
	print()

	projectSelection = helpers.user_input('Please select a project: ')

	return projectSelection

def show_projects_for_date(LIST, DATE):
	print(LIST)

def archiving(OLD_RECORD, NEW_RECORD):
	print('''
===========================================

Archiving Record:
{}

New record generated:
{}

===========================================
'''.format(helpers.decorate('yellow', OLD_RECORD), helpers.decorate('green', NEW_RECORD)))

def chrono_breakdown(DATE, DATA):
	dateFormatted = helpers.format_date(DATE)
	label = '''
Chronological breakdown for {}:
( {} )
'''.format(helpers.decorate('yellow', dateFormatted), DATE)

	print('{}'.format(label))

	for entry in DATA:
		print('''
{PROJECT}
-----------------------------
from:  {FROM}
to:    {TO}
'''.format(
	PROJECT = helpers.decorate('bold', entry['project']),
	FROM = helpers.decorate('cyan', entry['start'].strftime('%H:%M')),
	TO = helpers.decorate('cyan', entry['end'].strftime('%H:%M'))
))
