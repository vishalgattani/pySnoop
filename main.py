import time

import schedule

from logger import logger
from sys_utils import run_health_checks


def main():
    logger.info("Running system health checks...")
    schedule.every(1).seconds.do(run_health_checks)
    while True:
        schedule.run_pending()
    logger.info("Health checks completed.")


if __name__ == "__main__":
    logger.info("Snooping on the system...")
    main()
