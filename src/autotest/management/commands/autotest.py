import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler 
from django.core.management.base import BaseCommand
from os import chdir
from django.conf import settings
from subprocess import Popen, PIPE 
from os.path import split, dirname, join, abspath 
import os.path
import re
from optparse import make_option


CURRENT_PATH =  abspath(dirname(__file__))
AUTOTEST_PATH = abspath(join(CURRENT_PATH, '..'))

def absolute_path(path):

	return os.path.abspath(os.path.normpath(path))


class LoggingEventHandler(FileSystemEventHandler):


	def __init__(self, *args, **options):
		self.quick = options.get('quick', False)
		self.current_app = ''
		self.project_path = settings.PROJECT_ROOT.split(os.sep)

	def run_test_suite(self):

		chdir(settings.PROJECT_ROOT)
		test_command = ['python','manage.py', 'autotestrunner']
		if self.quick is True:
			test_command.append(self.current_app)
		result = Popen(test_command, stdout=PIPE, stderr=PIPE, close_fds=True).communicate() 

		title = ''
		content = ''
		for line in result:
			split_lines = line.split('\n')
			for l in split_lines:
				if l.startswith('Ran'):
					title = l
				if l.startswith('OK') or l.startswith('FAIL'):
					content = l

		print line # Display the test suite results in the terminal
		chdir(AUTOTEST_PATH)
		os.system('chmod u+rwx notify.sh')
		os.system('./notify.sh "{0}" "{1}" '.format(title, content))
		

	def on_modified(self, event):
		super(LoggingEventHandler, self).on_modified(event)
		path_to_file, filename = split(event.src_path)
		valid_test = re.compile('(?:^|[\\b_\\.-])[Tt]ests?.py$') # extended from nose


		if valid_test.search(filename):
			
			path_to_file_list = path_to_file.split(os.sep)
			current_app_path = list(set(path_to_file_list) - set(self.project_path))
			self.current_app = ".".join(current_app_path)
			
			self.run_test_suite()
	

class Command(BaseCommand):
	option_list = BaseCommand.option_list + (
		make_option('--quick', default=False ,dest="quick", action="store_true",
					help='Runs the tests only for the application you are currently working on'),
		)	
	help = 'Runs the test suite when a tests file is saved'

	requires_model_validation = False

	def handle(self, *args, **options):
		quick = options.get('quick', False)
		handler = LoggingEventHandler(quick=quick)

		app_path = absolute_path(settings.PROJECT_ROOT)

		observer = Observer()
		observer.schedule(handler, path=app_path, recursive=True)
		observer.start()
		try:
			while True:
				time.sleep(1)
		except KeyboardInterrupt:
			observer.stop()
		observer.join()

