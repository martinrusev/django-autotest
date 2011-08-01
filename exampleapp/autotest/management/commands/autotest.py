import time
from watchdog.observers import Observer
from watchdog.events import  PatternMatchingEventHandler
from django.core.management.base import BaseCommand
from os import path
from django.conf import settings


class AutotestEventHandler(PatternMatchingEventHandler):
	def on_any_event(self, event):
		print event.src_path

		path_to_file, filename = path.split(event.src_path)

		print path.split(event.src_path)

class Command(BaseCommand):
	option_list = BaseCommand.option_list + (
			)
	help = ''
	args = '[appname ...]'

	requires_model_validation = False

	def handle(self, *args, **options):
		self.event_handler = AutotestEventHandler(patterns=['*.py'], ignore_directories=True)
		self.run(*args, **options)

	def run(self, *args, **options):
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

	def inner_run(self, *args, **options):
		from django.test.utils import get_runner

		self.stdout.write("Validating models...\n\n")

		verbosity = int(options.get('verbosity', 1))
		interactive = options.get('interactive', True)
		failfast = options.get('failfast', False)
		TestRunner = get_runner(settings)

		if hasattr(TestRunner, 'func_name'):
			import warnings
			warnings.warn(
					'Function-based test runners are deprecated. Test runners should be classes with a run_tests() method.',
					DeprecationWarning
					)
			failures = TestRunner(args, verbosity=verbosity, interactive=interactive)
		else:
			test_runner = TestRunner(verbosity=verbosity, interactive=interactive, failfast=failfast)
			failures = test_runner.run_tests(args)

		print failures
