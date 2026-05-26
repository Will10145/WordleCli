import threading, sys, time
class loading_spinner:
    def __init__(self, message="Loading"):
        self.message = message
        self.stop_event = threading.Event()
        self.spinner_thread = None

    def _spin(self):
        # The animation frames you asked for
        frames = ['|', '/', '-', '\\']
        idx = 0
        while not self.stop_event.is_set():
            # \r moves the cursor to the start of the line
            # end='' prevents printing a newline
            sys.stdout.write(f"\r{self.message}... {frames[idx]}")
            sys.stdout.flush()
            idx = (idx + 1) % len(frames)
            time.sleep(0.1)
        
        # Clean up the line and show a success checkmark when done
        sys.stdout.write(f"\r{self.message}... Done!\n")
        sys.stdout.flush()

    def __enter__(self):
        self.stop_event.clear()
        self.spinner_thread = threading.Thread(target=self._spin)
        self.spinner_thread.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop_event.set()
        if self.spinner_thread:
            self.spinner_thread.join()

if __name__ == "__main__":
    print('Do NOT run this script directly!')