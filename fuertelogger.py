from datetime import datetime
from timeit import default_timer as timer
import atexit
import inspect
import logging
import os
import uuid

if 'SPY_PYTHONPATH' in os.environ:
    script_name = 'RUN_IN_SPYDER'
else:
    script_name = inspect.stack()[-1][1]
    script_name = os.path.basename(script_name)

now = datetime.now().strftime('%Y%m%d_%H%M%S')
randomizer = str(uuid.uuid4())[:4].upper()
log_filename = f'log-{script_name}-{now}-{randomizer}.log'

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)-8s - %(name)s - %(message)s',
    datefmt='%m-%d %H:%M',
    filename=log_filename,
    filemode='w',
)

console = logging.StreamHandler()
console.setLevel(logging.INFO)
console.setFormatter(logging.Formatter('%(asctime)s - %(levelname)-8s - %(name)s - %(message)s'))
logging.getLogger('').addHandler(console)

logging.getLogger('boto3').setLevel(logging.WARN)
logging.getLogger('botocore').setLevel(logging.WARN)
logging.getLogger('urllib3').setLevel(logging.WARN)

FUERTELOGGER_START = timer()

def end_program():
    elapsed_in_seconds = timer() - FUERTELOGGER_START
    elapsed_in_minutes = elapsed_in_seconds / 60
    logger = logging.getLogger(__name__)
    logger.info('-------------------------------------')
    logger.info(f'Execution time (sec): {elapsed_in_seconds:.2f}')
    logger.info(f'Execution time (min): {elapsed_in_minutes:.2f}')
    logger.info('-------------------------------------')
    logger.info(f'Log File: {log_filename}')

atexit.register(end_program)
