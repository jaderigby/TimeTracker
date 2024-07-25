import sys, sizzle
import messages as msg
import Track
import Untrack
import List
import Summary
import Run
import Record
import AllTimeByDate
import AllTime
import Status
import Category
import Archive
# new imports start here

# settings = helpers.get_settings()

try:
	action = str(sys.argv[1])
except:
	action = None

args = sys.argv[2:]

if action == None:
	msg.statusMessage()

elif action == '-action':
	sizzle.do_action(args)

elif action == '-profile':
	sizzle.profile()

elif action == '-helpers':
	sizzle.helpers()

elif action == '-alias':
	sizzle.alias()

elif action == "t":
	Track.execute(args)

elif action == "u":
	Untrack.execute()

elif action == "test":
	Test.execute()

elif action == "l":
	List.execute()

elif action == "show":
	Summary.execute()

elif action == "-":
	Run.execute(args)

elif action == "record":
	Record.execute()

elif action == "T":
	AllTimeByDate.execute()

elif action == "all":
	AllTime.execute()

elif action == "status":
	Status.execute()

elif action == "c":
	Category.execute()

elif action == "archive":
	Archive.execute()
# new actions start here
