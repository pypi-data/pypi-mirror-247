"""Common utilities for the api portion of the sdk."""
import requests
from functools import partial
from requests.auth import HTTPBasicAuth
from .. import settings

url = settings.dodata_url
auth = HTTPBasicAuth(settings.dodata_user, settings.dodata_password)
delete = partial(requests.delete, auth=auth)
get = partial(requests.get, auth=auth)
post = partial(requests.post, auth=auth)
