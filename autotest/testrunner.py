from django.conf import settings
from django.test.simple import DjangoTestSuiteRunner
from django.test.utils import setup_test_environment, teardown_test_environment


class AutotestSuiteRunner(DjangoTestSuiteRunner):


	def setup_test_environment(self, **kwargs):
		setup_test_environment()
		settings.DEBUG = False

	def teardown_test_environment(self, **kwargs):
		teardown_test_environment()
