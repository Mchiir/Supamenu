import time
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class ChangeHandler(FileSystemEventHandler):
    def __init__(self, command):
        self.command = command
        self.process = subprocess.Popen(self.command, shell=True)

    def on_any_event(self, event):
        if event.event_type in ['modified', 'created', 'deleted']:
            self.restart()

    def restart(self):
        self.process.terminate()
        self.process.wait()
        self.process = subprocess.Popen(self.command, shell=True)

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
    observer.join()