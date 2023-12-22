import threading
import json
import time

class AutoSaveDict(dict):
    def __init__(self, path, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.path = path
        self.__last_hash = None
        self.lock = threading.Lock()
        self._stop_event = threading.Event()
        self._save_thread = threading.Thread(target=self._auto_save)
        self._save_thread.start()
        

    def __hash__(self) -> int:
        with self.lock:
            return hash(json.dumps(self))

    def _auto_save(self):
        while not self._stop_event.is_set():
            now_hash = self.__hash__()
            if self.__last_hash is not None and self.__last_hash == now_hash:
                time.sleep(10)
                continue

            self.lock.acquire()
            try:
                with open(self.path, 'w') as file:
                    json.dump(self, file)
            finally:
                self.lock.release()
            time.sleep(10)  # wait for 10 seconds

    def stop_auto_save(self):
        self._stop_event.set()
        self._save_thread.join()

    def __setitem__(self, key, value):
        with self.lock:
            super().__setitem__(key, value)

    def __delitem__(self, key):
        with self.lock:
            super().__delitem__(key)

    def clear(self):
        with self.lock:
            super().clear()

    def pop(self, key, default=None):
        with self.lock:
            return super().pop(key, default)
        
    def popitem(self):
        with self.lock:
            return super().popitem()
        
    def update(self, *args, **kwargs):
        with self.lock:
            super().update(*args, **kwargs)

    def __getitem__(self, key):
        with self.lock:
            return super().__getitem__(key)
        
    