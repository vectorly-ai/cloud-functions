# /// script
# dependencies = [
#   "redis",
#   "requests",
#   "boto3",
# ]
# ///
import logging
import asyncio
import sys

logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format="{levelname:.1s}{asctime} {filename}:{lineno} {message}",
    style='{',
)

from common.keyparts import KeyParts
from common.redis_sample_data import redis
from common.redis_sample_flusher import RedisSampleFlusher


logger = logging.getLogger(__name__)

runs = set()
for key in redis.keys('exp:*'):
    if len(key.split(b":")) <= 2:
        continue
    key_parts = KeyParts.build(key.decode('utf-8'))
    runs.add((key_parts.experiment_id, key_parts.batch_id, key_parts.run_id))
for experiment_id, batch_id, run_id in runs:
    asyncio.run(RedisSampleFlusher.dump_to_s3(experiment_id, batch_id, run_id))
