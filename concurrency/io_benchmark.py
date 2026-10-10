import os
import time
import asyncio
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

def fetch_data_sync(request_id = 1):
    time.sleep(.1)
    return f"Result: {request_id}"

async def fetch_data_async(request_id = 1):
    await asyncio.sleep(.1)
    return f"Result: {request_id}"

CPU_CORES = os.cpu_count() or 6
NUM_TASKS = 150

def run_sequential():
    start = time.perf_counter()
    _ = [fetch_data_sync(i) for i in range(NUM_TASKS)]
    return time.perf_counter() - start

def run_threading():
    start = time.perf_counter()
    with ThreadPoolExecutor(max_workers=CPU_CORES) as exec:
        _ = list(exec.map(fetch_data_sync, range(NUM_TASKS)))
    return time.perf_counter() - start

def run_multiprocessing():
    start = time.perf_counter()
    with ProcessPoolExecutor(max_workers=CPU_CORES) as exec:
        _ = list(exec.map(fetch_data_sync, range(NUM_TASKS)))
    return time.perf_counter() - start

async def run_asyncio_main():
    start = time.perf_counter()
    tasks = [fetch_data_async(i) for i in range(NUM_TASKS)]
    _ = await asyncio.gather(*tasks)
    return time.perf_counter() - start

def run_asyncio():
    return asyncio.run(run_asyncio_main())

if __name__ == "__main__":

    print(f"Found {CPU_CORES} logical cores. Fetching {NUM_TASKS} requests with max {CPU_CORES} workers...")

    seq_time = run_sequential()
    print(f"Sequential:\t\t{seq_time:.4f}s")
    
    thread_time = run_threading()
    print(f"Multithreading:\t\t{thread_time:.4f}s")
    
    proc_time = run_multiprocessing()
    print(f"Multiprocessing:\t{proc_time:.4f}s")
    
    async_time = run_asyncio()
    print(f"Asyncio:\t\t{async_time:.4f}s")