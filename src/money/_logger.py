import logging
import os

log_directory = os.path.join(os.getcwd(), "logs")
log_file = os.path.join(log_directory, "money.log")
logging.basicConfig(
    format="%(asctime)s %(levelname)-8s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    filename=log_file,
    level=logging.INFO,
)
logger = logging.getLogger(name="money")
