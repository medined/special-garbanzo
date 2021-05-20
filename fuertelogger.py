from datetime import datetime
from timeit import default_timer as timer
import atexit
import inspect
import logging
import os
import pathlib

if 'SPY_PYTHONPATH' in os.environ:
    script_name = 'RUN_IN_SPYDER'
else:
    script_name = inspect.stack()[-1][1]
    script_name = os.path.basename(script_name)

now = datetime.now().strftime('%Y%m%d_%H%M%S')
log_filename = f'log-{script_name}-{now}.log'

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

