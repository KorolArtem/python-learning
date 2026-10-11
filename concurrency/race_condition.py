import threading
import time

class ThreadsCounter:
    def __init__(self):
        self.value = 0
        self.lock = threading.Lock()
        self.INCREMENT_TIMES = 250_000

    def increment_without_lock(self):
        for _ in range(self.INCREMENT_TIMES):
            current_value = self.value
            time.sleep(0)
            self.value = current_value + 1

    def increment_with_lock(self):
        for _ in range(self.INCREMENT_TIMES):
            with self.lock:
                current_value = self.value
                time.sleep(0)
                self.value = current_value + 1

def run_test(target_func, num_threads):
    threads = []

    for _ in range(num_threads):
        t = threading.Thread(target=target_func)
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

if __name__ == "__main__":
    THREADS_NUM = 2

    print("Incrementing without lock...")
    unsafe_counter = ThreadsCounter()
    run_test(unsafe_counter.increment_without_lock, THREADS_NUM)
    print(f"Final counter after incrementing for {THREADS_NUM * unsafe_counter.INCREMENT_TIMES} times without lock: {unsafe_counter.value}")

    print("Starting with lock...")
    safe_counter = ThreadsCounter()
    run_test(safe_counter.increment_with_lock, THREADS_NUM)
    print(f"Final counter after incrementing for {THREADS_NUM * safe_counter.INCREMENT_TIMES} times with lock: {safe_counter.value}")