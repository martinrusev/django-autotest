import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, PatternMatchingEventHandler
from os import getcwd, sep, path
import re


class AutotestEventHandler(PatternMatchingEventHandler):
    def on_any_event(self, event):
		print event.src_path
		
		path_to_file, filename = path.split(event.src_path)

		
		#print path.split(event.src_path)
		#print event.event_type



event_handler = AutotestEventHandler(patterns=['*.py'], ignore_directories=True)

if __name__ == "__main__":
    observer = Observer()
    observer.schedule(event_handler, getcwd(), recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
