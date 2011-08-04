import sys
import pynotify
import getopt

if __name__ == '__main__':

	args = sys.argv[1:]
	optlist,args = getopt.getopt(args, "tc:d",  ['title=', 'content='])

	title = optlist[0][1]
	content = optlist[1][1]
	n = pynotify.Notification(title, content)
	n.show()
