import messages as msg
import json, re
from settings import settings

from datetime import datetime
from time import gmtime, strftime, localtime
from datetime import timedelta

profilePath = settings['profile_url'] + settings['profile']

def load_profile():
	import os
	return json.loads(read_file(profilePath)) if os.path.exists(profilePath) else json.loads("{}")

def get_settings():
	profile = load_profile()
	return profile['settings'] if 'settings' in profile else False

def path(TYPE):
	import os
	if TYPE == 'user':
		return os.path.expanduser('~/')
	elif TYPE == 'util' or TYPE == 'utility':
		return os.path.dirname(os.path.realpath(__file__))
	else:
		return False

def read_file(FILEPATH):
	FILE = open(FILEPATH, 'r')
	data = FILE.read()
	FILE.close()
	return data

def write_file(FILEPATH, DATA):
	with open(FILEPATH, 'w') as f: f.write(DATA)

def run_command(CMD, option = True):
	import subprocess
	shellStatus = True
	str = ''
	showCmd = CMD
	if isinstance(CMD, list):
		shellStatus = False
		for item in CMD:
			str += (' ' + item)
		showCmd = str
	if option:
		print('\n============== Running Command: {}\n'.format(showCmd))
	subprocess.call(CMD, shell=shellStatus)

def run_command_output(CMD, option = True):
	import subprocess
	if option:
		print('\n============== Outputting Command: {}\n'.format(CMD))
	result = False
	if CMD != None:
		process = subprocess.Popen(CMD, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
		out, err = process.communicate()

		if err:
			print(err)
		else:
			result = out.decode('utf-8')

	return result

def decorate(COLOR, STRING):
	bcolors = {
		 'lilac' : '\033[95m'
		,'blue' : '\033[94m'
		,'cyan' : '\033[96m'
		,'green' : '\033[92m'
		,'yellow' : '\033[93m'
		,'red' : '\033[91m'
		,'bold' : '\033[1m'
		,'underline' : '\033[4m'
		,'endc' : '\033[0m'
	}

	return bcolors[COLOR] + STRING + bcolors['endc']

def user_input(STRING):
	try:
		return raw_input(STRING)
	except:
		return input(STRING)

def list_expander(LIST):
    baseList = LIST.replace(' ', '').split(',')
    expandedList = []
    for item in baseList:
        if '-' in item:
            rangeList = item.split('-')
            tempList = [elem for elem in range(int(rangeList[0]), int(rangeList[1]) + 1)]
            expandedList += tempList
        else:
            expandedList.append(int(item))
    return expandedList

# generates a user selection session, where the passed in list is presented as numbered selections; selecting "x" or just hitting enter results in the string "exit" being returned. Any invaild selection is captured and presented with the message "Please select a valid entry"
def user_selection(DESCRIPTION, LIST, LIST_SELECT = False):
	import re
	str = ''
	for i, item in enumerate(LIST, start=1):
		str += '\n[{index}] {item}'.format(index=i, item=item)
	str += '\n\n[x] Exit\n'

	finalAnswer = False

	while True:
		print(str)
		selection = user_input('{}'.format(DESCRIPTION))
		pat = re.compile("[0-9,\- ]+") if LIST_SELECT else re.compile("[0-9]+")
		if pat.match(selection):
			selection = list_expander(selection) if LIST_SELECT else int(selection)
		if isinstance(selection, int) or isinstance(selection, list):
			finalAnswer = selection
			break
		elif selection == 'x':
			finalAnswer = 'exit'
			break
		elif selection == '':
			finalAnswer = 'exit'
			break
		else:
			print("\nPlease select a valid entry...")
	return finalAnswer

def arguments(ARGS, DIVIDER=':'):
	return dict(item.split('{}'.format(DIVIDER)) for item in ARGS)

def kv_set(DICT, KEY, DEFAULT = False):
	if KEY in DICT:
		DICT[KEY] = 't' if DICT[KEY] == 'true' else 'f' if DICT[KEY] == 'false' else DICT[KEY]
		return DICT[KEY]
	else:
		return DEFAULT


# custom helpers start here
# =========================

settings = get_settings()
recordPath = '{}/records/{}'.format(path('util'), settings['record'])

def load_record():
	data = read_file(recordPath)
	data = data.replace('const data = ', '')
	return json.loads(data)

def time_stamp():
	return strftime("%Y-%m-%d %H:%M", localtime())

def date_stamp():
	return strftime("%Y-%m-%d", localtime())

def glue_updated_record(RECORD):
	recordString = 'const data = ' + json.dumps(RECORD, sort_keys=True, indent=4)
	return recordString

def create_new_project(TIME):
	record = load_record()
	tempObj	 = {}
	timeObj = {}
	tempObj['description'] = ""
	tempObj['category'] = ""
	tempObj['orderId'] = len(record['projects']) + 1
	tempObj['time'] = []
	timeObj['start'] = TIME
	timeObj['end'] = ""
	timeObj['spent'] = ""
	timeObj['spent_date'] = ""
	tempObj	['time'].append(timeObj)
	return tempObj

def add_a_description():
	return user_input("Please enter a description: ")

def handle_category():
	return user_input("Category: ")

def add_project(PROJECT):
	record = load_record()
	current = record['current']
	recordedTime = time_stamp()

	def verify_exists(VAL, RECORD):
		for item in record['projects']:
			if item == VAL:
				return True
		return False
	
	if verify_exists(PROJECT, record):
		record['current'] = PROJECT

		content = glue_updated_record(record)
		write_file(recordPath, content)
	else:
		record['current'] = PROJECT
		record['projects'][PROJECT] = create_new_project(recordedTime)
		record['projects'][PROJECT]['description'] = add_a_description()
		record['projects'][PROJECT]['category'] = handle_category()

		content = glue_updated_record(record)
		write_file(recordPath, content)

def new_time_obj(START_TIME):
	newObj = {}

	newObj["start"] = START_TIME
	newObj["end"] = ""
	newObj["spent"] = ""
	newObj["spent_date"] = ""

	return newObj

def time_spent(START, END):
	startFormat = datetime.strptime(START, '%Y-%m-%d %H:%M')
	endFormat = datetime.strptime(END, '%Y-%m-%d %H:%M')
	spent = endFormat - startFormat
	timeFormatted = str(spent)[:-3]
	return timeFormatted

def format_timedelta(td):
	#= http://stackoverflow.com/questions/28503838/how-can-i-display-timedelta-in-hoursminsec
	minutes, seconds = divmod(td.seconds + td.days * 86400, 60)
	hours, minutes = divmod(minutes, 60)
	return '{:d}:{:02d}:{:02d}'.format(hours, minutes, seconds)

def calculate_time(A, B):
	if not A or not B:
		totalTime = '00:00'
	else:
		hrPat = ":[0-9]{2}"
		minPat = "[0-9]+:"
		re.sub(hrPat, '', A)

		aHours 		= int( re.sub(hrPat, '', A) )
		aMinutes 	= int( re.sub(minPat, '', A) )
		bHours 		= int( re.sub(hrPat, '', B) )
		bMinutes 	= int( re.sub(minPat, '', B) )

		totalHrs = aHours + bHours
		totalMinutes = aMinutes + bMinutes

		totalTimeString = str(timedelta(minutes=totalMinutes))[:-3]

		# totalTime = "{}:{}".format(totalHrs, totalMinutes)

		totalTime = str(format_timedelta(timedelta(minutes=totalMinutes + (totalHrs * 60))))[:-3]

	return totalTime

def calculate_total_time(TIME):
	timeList = []
	for item in TIME:
		if item['spent'] == '' and item['spent_date'] == '' and item['end'] == '':
			item['spent'] = time_spent(item['start'], time_stamp())
		timeList.append(item['spent'])
	timeItem = '00:00'
	for i in timeList:
		timeItem = calculate_time(timeItem, i)
	return timeItem

def calculate_total_time_today(TIME, TODAY):
	timeList = []
	for item in TIME:
		if item['spent_date'] == TODAY:
			timeList.append(item['spent'])
	timeItem = '00:00'
	for i in timeList:
		timeItem = calculate_time(timeItem, i)
	return timeItem

def select_project(OBJ, QUICK_SELECT=False):
	current = OBJ['current']
	today = date_stamp()
	projectList = []
	projectListTimes = []

	#= Get list of project names
	for item in OBJ['projects']:
		projectList.append(item)

	# sortedProjects = sort_projects_by_date(OBJ)
	sortedProjects = sort_projects_by_sortId(OBJ)

	#= Construct project info for message
	for proj in sortedProjects:
		item = OBJ['projects'][proj['project']]
		newObj = {}
		newObj['name'] = proj['project']
		newObj['description'] = item['description']
		t = calculate_total_time(item['time'])
		tt = calculate_total_time_today(item['time'], today)
		newObj['total'] = t
		newObj['total_today'] = tt
		projectListTimes.append(newObj)

	if not QUICK_SELECT:
		selection = msg.switch_to_a_project(projectListTimes, current)
	else:
		selection = QUICK_SELECT
	
	if selection != 'x':
		selectionName = sortedProjects[int(selection) - 1]['project']
	else:
		selectionName = 'x'
	return selectionName

def sort_projects_by_date(OBJ):
	keyList = dict.keys(OBJ['projects'])
	objectsToBeOrdered = []

	for item in keyList:
		tempObj = {}
		tempObj['project'] = item
		tempObj['date'] = OBJ['projects'][item]['time'][0]['end']

		objectsToBeOrdered.append(tempObj)
	
	orderedProjects = sorted(objectsToBeOrdered, key = lambda i: i['date'])
	
	return orderedProjects

def sort_projects_by_sortId(OBJ):
	orderedItems = sorted(OBJ['projects'].items(), key=lambda x: x[1]["orderId"])
	orderedItemsNameOnly = sorted(item[0] for item in orderedItems)
	objectsToBeOrdered = []

	for item in orderedItemsNameOnly:
		tempObj = {}
		tempObj['project'] = item
		if len(OBJ['projects'][item]['time']) != 0:
			tempObj['date'] = OBJ['projects'][item]['time'][0]['end']
		
		objectsToBeOrdered.append(tempObj)

	return objectsToBeOrdered

def get_project_by_number(OBJ, NUMBER):
	orderedItems = sorted(OBJ['projects'].items(), key=lambda x: x[1]["orderId"])
	orderedItemsNameOnly = sorted(item[0] for item in orderedItems)
	objectsToBeOrdered = []

	for item in orderedItemsNameOnly:
		tempObj = {}
		tempObj['project'] = item
		tempObj['date'] = OBJ['projects'][item]['time'][0]['end']

		objectsToBeOrdered.append(tempObj)
	
	orderedProjects = sorted(objectsToBeOrdered, key = lambda i: i['date'])

	selectedProject = objectsToBeOrdered[int(NUMBER) - 1]['project']

	return selectedProject

#========================================

def retrieve_project_name(ID, PROJECTS):
	projectName = PROJECTS[int(ID) - 1]
	return projectName

def project_list(SETTINGS):
	i = 0
	newList = []
	for item in SETTINGS['projects']:
		newList.append(item)
	return newList

def calculate_total_time_daily(TIME):
	tempList = dissolve_to_unique_dates(TIME, 'spent_date')
	newSet = []
	#= each item in list
	for item in tempList:
		totalTime = "00:00"
		newObj = {}
		newList = []
		#= compare all items to current
		for i in TIME:
			if item == i['spent_date']:
				newList.append(i['spent'])
		for s in newList:
			totalTime = calculate_time(s, totalTime)
		newObj['date'] = item
		newObj['spent'] = totalTime
		newSet.append(newObj)
	return newSet

def dissolve_to_unique_dates(OBJ, KEY):
	tempList = []
	newList = []
	for item in OBJ:
		tempList.append(item[KEY])
	for n in tempList:
		if n not in newList:
			newList.append(n)
	return newList

def collect_projects_by_date(DATE, RECORD):
	timeList = []
	for item in RECORD['projects']:
		for time in RECORD['projects'][item]['time']:
			if time['spent_date'] == DATE:
				tempObj = {}
				tempObj['name'] = item
				tempObj['time'] = time
				timeList.append(tempObj)
	# for item in timeList:

def convert_spent_time(spent):
    """Convert spent time from 'HH:MM' string to timedelta"""
    hours, minutes = map(int, spent.split(':'))
    return timedelta(hours=hours, minutes=minutes)

def get_projects_and_time(DATE, RECORD):
    projectsTime = {}
    
    for project, details in RECORD.items():
        totalTime = timedelta()
        for entry in details['time']:
            if entry['spent_date'] == DATE:
                totalTime += convert_spent_time(entry['spent'])
        if totalTime:
            projectsTime[project] = totalTime
    
    return projectsTime

def get_chronological_entries(DATE, RECORD):
    entries = []
    
    for project, details in RECORD.items():
        for entry in details['time']:
            if entry['spent_date'] == DATE:
                entries.append({
                    'project': project,
                    'start': datetime.strptime(entry['start'], '%Y-%m-%d %H:%M'),
                    'end': datetime.strptime(entry['end'], '%Y-%m-%d %H:%M'),
                    'spent': convert_spent_time(entry['spent'])
                })
    
    # Sort the entries by start time
    sortedEntries = sorted(entries, key=lambda x: x['start'])
    
    return sortedEntries

def format_date(date_str):
    # Parse the date string to a datetime object
    dateObj = datetime.strptime(date_str, '%Y-%m-%d')
    
    # Get the day with the appropriate suffix
    day = dateObj.day
    if 11 <= day <= 13:
        suffix = 'th'
    else:
        suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(day % 10, 'th')
    
    # Format the datetime object to the desired string format
    dateFormatted = dateObj.strftime(f"%A, %B {day}{suffix}")
    return dateFormatted

def format_date_and_year(date_str):
    # Parse the date string to a datetime object
    dateObj = datetime.strptime(date_str, '%Y-%m-%d')
    
    # Get the day with the appropriate suffix
    day = dateObj.day
    if 11 <= day <= 13:
        suffix = 'th'
    else:
        suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(day % 10, 'th')
    
    # Format the datetime object to the desired string format
    dateFormatted = dateObj.strftime(f"%A, %B {day}{suffix}")
    yearFormatted = date_str.split('-')[0]
    dateAndYearFormatted = dateFormatted + ', ' + yearFormatted
    return dateAndYearFormatted

def format_date_w_day(DATE):
    # Parse the date string to a datetime object
    dateObj = datetime.strptime(DATE, '%Y-%m-%d')
    
    # Format the datetime object to include the day of the week
    dateFormatted = dateObj.strftime("%A, %Y-%m-%d")
    return dateFormatted
