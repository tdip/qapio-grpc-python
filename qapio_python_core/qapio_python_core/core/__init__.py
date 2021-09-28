from rx.scheduler import ThreadPoolScheduler

optimal_thread_count = 4  # multiprocessing.cpu_count()

scheduler = ThreadPoolScheduler(optimal_thread_count)
