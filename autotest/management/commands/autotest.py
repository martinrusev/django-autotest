import time
from watchdog.observers import Observer
from watchdog.events import  PatternMatchingEventHandler
from django.core.management.base import BaseCommand
from os import path, chdir
from django.conf import settings
from subprocess import Popen, PIPE, call
from autotest import AUTOTEST_PATH


class AutotestEventHandler(PatternMatchingEventHandler):
	
	
	def run_test_suite(self):


		chdir(settings.PROJECT_ROOT)
		result = Popen(['./manage.py', 'autotestrunner'], stdout=PIPE, stderr=PIPE, close_fds=True).communicate() 
		
		title = ''
		content = ''
		for line in result:
			split_lines = line.split('\n')
			for l in split_lines:
				if l.startswith('Ran'):
					title = l
				if l.startswith('OK') or l.startswith('FAIL'):
					content = l

		call(['/usr/bin/python',
			'{0}notifications.py'.format(AUTOTEST_PATH),
			'--title={0}'.format(title),
			'--content={0}'.format(content)]
		)


	def on_modified(self, event):
		path_to_file, filename = path.split(event.src_path)
		print filename
		self.run_test_suite()


class Command(BaseCommand):
	option_list = BaseCommand.option_list + (
			)
	help = 'Runs the test suite when a tests file is saved'
	args = '[appname ...]'

	requires_model_validation = False

	def handle(self, *args, **options):
		self.event_handler = AutotestEventHandler(patterns=['*.py'],ignore_directories=True)
		self.run()

	def run(self):
		app_path = settings.PROJECT_ROOT

		observer = Observer()
		observer.schedule(self.event_handler, app_path, recursive=True)
		observer.start()
		try:
			while True:
				time.sleep(1)
		except KeyboardInterrupt:
			observer.stop()
		observer.join()

