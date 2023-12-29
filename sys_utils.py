import psutil

from logger import logger


def check_cpu_usage(threshold=50):
    cpu_usage = psutil.cpu_percent(interval=1)
    if cpu_usage > threshold:
        logger.warning(f"High CPU usage detected: {cpu_usage}%")
    else:
        logger.info(f"CPU usage detected: {cpu_usage}%")
    return cpu_usage


def check_memory_usage(threshold=80):
    memory_usage = psutil.virtual_memory().percent
    memory_free = psutil.virtual_memory().free
    memory_used = psutil.virtual_memory().used
    if memory_usage > threshold:
        logger.warning(f"High memory usage detected: {memory_usage}%")
    else:
        logger.info(f"Memory usage detected: {memory_usage}%")
    return memory_usage


def check_disk_space(path="/", threshold=75):
    disk_usage = psutil.disk_usage(path).percent
    if disk_usage > threshold:
        logger.warning(f"Low disk space detected: {disk_usage}%")
    else:
        logger.info(f"Disk space detected: {disk_usage}%")
    return disk_usage


def check_network_traffic(threshold=100 * 1024 * 1024):
    network_traffic = (
        psutil.net_io_counters().bytes_recv + psutil.net_io_counters().bytes_sent
    )
    if network_traffic > threshold:
        logger.warning(f"High network traffic detected: {network_traffic:.2f} MB")
    else:
        logger.info(f"Network traffic detected: {network_traffic:.2f} MB")
    return network_traffic


def run_health_checks():
    health_data = {
        "cpu_usage": check_cpu_usage(),
        "memory_usage": check_memory_usage(),
        "disk_space": check_disk_space(),
        "network_traffic": check_network_traffic(),
    }
    return health_data
