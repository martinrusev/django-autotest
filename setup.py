from setuptools import setup, find_packages
import os

SRC_DIR = 'src'


def read(filename):
    return open(os.path.join(os.path.dirname(__file__), filename)).read()
 
version = '0.1.0'
 
setup(
    name='django_autotest',
    version=version,
    description="Django autotest is a command that automaticaly runs the test suite",
    long_description=read('README.rst'),
    classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Framework :: Django",
        "Environment :: Web Environment",
    ],
    keywords='django, tests, autotest,',
    author='Martin Rusev',
    author_email='martinrusev@live.com',
    url='https://github.com/martinrusev/django-autotest',
    license='BSD',
	package_dir={'': SRC_DIR},
	packages=find_packages(SRC_DIR),
	package_data = {'': ['*.sh']},
	include_package_data=True,
    zip_safe=False,
    install_requires=['setuptools','watchdog',],
) 
