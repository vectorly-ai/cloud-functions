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
n_iteration = params['n_iteration']

reader = RedisSampleReader()
result = {}
for varname, data in reader.get_data(experiment_id).items():
  result[varname] = ("avg", sum(data[:n_iteration]) / n_iteration)

logger.info("%s", result)
token = os.environ['COINFER_AUTH_TOKEN']
url_root = os.environ['COINFER_SERVER_ENDPOINT']
rsp = requests.post(
    url_root + f'/mcmc/experiment/{experiment_id}/runinfo/{batch_id}/{run_id}/nsample', 
    json={"n_sample": n_iteration, "stat": result}, 
    check_subjects=CheckResponseSubject.TIMEOUT | CheckResponseSubject.STATUS_CODE | CheckResponseSubject.JSON | CheckResponseSubject.STATUS,
    headers={"Authorization": f"Bearer {token}"},
)
if requests.errmsg:
    sys.exit(1)
