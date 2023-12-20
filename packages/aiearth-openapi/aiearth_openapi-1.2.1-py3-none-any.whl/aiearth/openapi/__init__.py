from aiearth.core import g_var
from aiearth.core.client.endpoints import Endpoints
from alibabacloud_tea_openapi.models import Config

__ENDPOINT__ = Endpoints.OPENAPI_ENDPOINT
__REGION_ID__ = Endpoints.OPENAPI_REGION_ID

__version__ = "1.2.1"

from aiearth.openapi.client import ExtClient

import logging

log_lvl = 'INFO'
if g_var.has_var(g_var.GVarKey.Log.LOG_LEVEL):
    log_lvl = g_var.get_var(g_var.GVarKey.Log.LOG_LEVEL).upper()

# create logger
logger = logging.getLogger('openapi')
logger.setLevel(log_lvl)

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(log_lvl)

# create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# add formatter to ch
ch.setFormatter(formatter)

# add ch to logger
logger.addHandler(ch)

def build_client(access_key_id, access_key_secret, endpoint=__ENDPOINT__):
    config = Config(
        access_key_id=access_key_id,
        access_key_secret=access_key_secret,
        region_id=__REGION_ID__,
        endpoint=endpoint
    )

    from aiearth import core
    core.Authenticate(access_key_id=access_key_id, access_key_secret=access_key_secret)

    return ExtClient(config)
