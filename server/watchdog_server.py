import time
import subprocess
import os
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

logging.basicConfig(level=logging.INFO)

class ChangeHandler(FileSystemEventHandler):
    def __init__(self, command):
        self.command = command
        self.process = self.start_process()

    def start_process(self):
        logging.info("Starting process...")
        return subprocess.Popen(self.command, shell=True)

    def on_any_event(self, event):
        if event.event_type in ['modified', 'created', 'deleted']:
            self.restart()

    def restart(self):
        logging.info("Restarting process...")
        try:
            self.process.terminate()
            self.process.wait()
        except Exception as e:
            logging.error(f"Error terminating process: {e}")
        self.process = self.start_process()

if __name__ == "__main__":
    path = "."  # Monitor the current directory
    command = "python server.py"

    event_handler = ChangeHandler(command)
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        event_handler.process.terminate()
    observer.join()