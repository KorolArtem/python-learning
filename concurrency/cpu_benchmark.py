import os
import time
import asyncio
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

def mandelbrot(c, max_iter = 10000):
    a = 0
    for n in range(max_iter):
        if abs(a) > 2:
            return n
        a = a*a + c
    return 0

def process_chunk(chunk):
    return [mandelbrot(c) for c in chunk]

TASK_DATA = [
    complex(-2. + (i % 200) * .0125, -1.2 + (i // 200) * .024)
    for i in range(20000)
]

CPU_CORES = os.cpu_count() or 6
NUM_CHUNKS = int(CPU_CORES * 1.5)
CHUNK_SIZE = max(1, len(TASK_DATA) // NUM_CHUNKS)
CHUNKS = [TASK_DATA[i:i + CHUNK_SIZE] for i in range(0, len(TASK_DATA), CHUNK_SIZE)]

def run_threading():
    start = time.perf_counter()
    with ThreadPoolExecutor(max_workers=NUM_CHUNKS) as executor:
        results = list(executor.map(process_chunk, CHUNKS))
    _ = [item for sublist in results for item in sublist]
    return time.perf_counter() - start

def run_multiprocessing():
    start = time.perf_counter()
    with ProcessPoolExecutor(max_workers=NUM_CHUNKS) as executor:
        results = list(executor.map(process_chunk, CHUNKS))
    _ = [item for sublist in results for item in sublist]
    return time.perf_counter() - start

async def async_worker(chunk):
    loop = asyncio.get_running_loop()
    # using run_in_executor is making it like a multithread execution, 
    # but idk how to honestly compare pure async and multithread in cpu-bound task,
    # of course i could write an async process chunk func, but there is no point i think
    return await loop.run_in_executor(None, process_chunk, chunk) 

async def run_asyncio_main():
    start = time.perf_counter()
    tasks = [async_worker(chunk) for chunk in CHUNKS]
    results = await asyncio.gather(*tasks)
    _ = [item for sublist in results for item in sublist]
    return time.perf_counter() - start

def run_asyncio():
    return asyncio.run(run_asyncio_main())

def run_sequential():
    start = time.perf_counter()
    results = [process_chunk(chunk) for chunk in CHUNKS]
    _ = [item for sublist in results for item in sublist]
    return time.perf_counter() - start

if __name__ == '__main__':

    print(f"Found {CPU_CORES} logical cores. Starting the calculations with {NUM_CHUNKS} chunks...")

    seq_time = run_sequential()
    print(f"Sequential:\t\t{seq_time:.4f}s")
    
    thread_time = run_threading()
    print(f"Multithreading:\t\t{thread_time:.4f}s")
    
    proc_time = run_multiprocessing()
    print(f"Multiprocessing:\t{proc_time:.4f}s")
    
    async_time = run_asyncio()
    print(f"Asyncio:\t\t{async_time:.4f}s")