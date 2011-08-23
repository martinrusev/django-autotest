import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler 
from django.core.management.base import BaseCommand
from os import chdir
from django.conf import settings
from subprocess import Popen, PIPE, call
from os.path import split, dirname, join, abspath 
import os.path
import logging

def get_autotest_path():

	CURRENT_PATH =  abspath(dirname(__file__))
	AUTOTEST_PATH = abspath(join(CURRENT_PATH, '..'))

	return AUTOTEST_PATH

def absolute_path(path):

	return os.path.abspath(os.path.normpath(path))


class LoggingEventHandler(FileSystemEventHandler):


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

		print title
		print content
		os.system('./autotest/notify.sh "{0}" "{1}" '.format(title, content))
		

	def on_modified(self, event):
		super(LoggingEventHandler, self).on_modified(event)
		path_to_file, filename = split(event.src_path)

		self.run_test_suite()

	
class AutotestEventHandler(LoggingEventHandler):

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
			'{0}notifications.py'.format(get_autotest_path()),
			'--title={0}'.format(title),
			'--content={0}'.format(content)]
			)


		def on_modified(self, event):
			super(AutotestEventHandler, self).on_modified(event)
			print 'test'
			path_to_file, filename = split(event.src_path)
			self.run_test_suite()


class Command(BaseCommand):
	option_list = BaseCommand.option_list + ()
	help = 'Runs the test suite when a tests file is saved'
	args = '[appname ...]'

	requires_model_validation = False

	def handle(self, *args, **options):
		logging.basicConfig(level=logging.INFO,
				format='%(asctime)s - %(message)s',
				datefmt='%Y-%m-%d %H:%M:%S')
		#handler = AutotestEventHandler()
		handler = LoggingEventHandler()

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

