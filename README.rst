=================
django-autotest
=================

Django autotest is a custom command for your applications
that runs the test suite when you save a test file and displays
a desktop notification with the results.

===============
 Installation
===============


1. Install the package with ``pip install django_autotest`` or alternatively you can  
download the tarball and run ``python setup.py install``

2. Add ``autotest`` to your INSTALLED_APPS list in settings.py
   

::

	INSTALLED_APPS = ('autotest')


3. Install the desktop notification library according to your operating system:

    On Linux install **libnotify-bin**


=========
 Usage 
=========

::

    ./manage.py autotest
    
    ############
    #  Options
    ############

    # Runs the tests only for the app you are currently working on
    ./manage.py autotest --quick 



===============
 Requirements
===============


Django 1.2+

watchdog

For the notifications:

libnotify ( Linux )
Growl ( Windows and Mac )


