from django.core.management.base import BaseCommand
from django.conf import settings


def get_runner(settings):
	runner = 'autotest.testrunner.AutotestSuiteRunner'
	test_path = runner.split('.')
	# Allow for Python 2.5 relative paths
	if len(test_path) > 1:
		test_module_name = '.'.join(test_path[:-1])
	else:
		test_module_name = '.'
	test_module = __import__(test_module_name, {}, {}, test_path[-1])
	test_runner = getattr(test_module, test_path[-1])

	return test_runner


class Command(BaseCommand):
    option_list = BaseCommand.option_list + ()
    help = 'Internal command for the autotest app'
    args = '[appname ...]'

    requires_model_validation = False

    def handle(self, *test_labels, **options):
      
		TestRunner = get_runner(settings)
		
		if hasattr(TestRunner, 'func_name'):
			import warnings
			warnings.warn(
					'Function-based test runners are deprecated. Test runners should be classes with a run_tests() method.',
					DeprecationWarning
					)
			failures = TestRunner(verbosity=1, interactive=True)
		else:
			test_runner = TestRunner(verbosity=1, interactive=True, failfast=True)
			failures = test_runner.run_tests(test_labels)

