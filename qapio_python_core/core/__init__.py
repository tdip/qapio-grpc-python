from rx.scheduler import ThreadPoolScheduler

optimal_thread_count = 6  # multiprocessing.cpu_count()

scheduler = ThreadPoolScheduler(optimal_thread_count)
