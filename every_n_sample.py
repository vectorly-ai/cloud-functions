# /// script
# dependencies = [
#   "redis",
#   "requests",
#   "boto3",
# ]
# ///
import json
import logging
import sys
import os
import time
from Coinfer import requests, CheckResponseSubject

logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format="{levelname:.1s}{asctime} {process}{filename}:{lineno} {message}",
    style='{',
)

from common.redis_sample_data import RedisSampleReader

logger = logging.getLogger(__name__)
params = json.loads(sys.argv[1])
experiment_id = params['experiment_id']
batch_id = params['batch_id']
run_id = params['run_id']
chain_name = params['chain_name']
n_iteration = params['n_iteration']

reader = RedisSampleReader()
result = {}
for varname, data in reader.get_data(experiment_id).items():
  result[varname] = ("avg", sum(data[:n_iteration]) / n_iteration)

tm = time.time()
logger.info("%s %s", tm, result)
token = os.environ['COINFER_AUTH_TOKEN']
url_root = os.environ['COINFER_SERVER_ENDPOINT']

rsp = requests.post(
    url_root + f'/api/object/{experiment_id}?tm={tm}',
    json={
        "payload": {
            "object_type": "experiment.nsample_stat",
            "batch_id": batch_id,
            "run_id": run_id,
            "chain_name": chain_name,
            "n_sample": n_iteration,
            "stat": result
        }
    }, 
    check_subjects=CheckResponseSubject.ALL,
    headers={"Authorization": f"Bearer {token}"},
)
if requests.errmsg:
    sys.exit(1)
