import pytest
import requests
import json
import pprint
from urllib.parse import urljoin
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter

pytest_plugins = ["docker_compose"]


def get_prometheus_response(path):
    prometheus_api_url = 'http://localhost:9090/api/v1/'
    url = prometheus_api_url + path
    r = requests.get(url)
    json_data = r.json()
    pprint.pprint(json_data)
    return json_data

def get_prometheus_runtime():
    return get_prometheus_response(path = 'status/runtimeinfo')

@pytest.fixture(scope="module")
def wait_for_api(module_scoped_container_getter):
    request_session = requests.Session()
    retries = Retry(total=5,
                    backoff_factor=0.1,
                    status_forcelist=[500, 502, 503, 504])
    request_session.mount('http://', HTTPAdapter(max_retries=retries))

    target_container_name = 'prometheus'
    service = module_scoped_container_getter.get(target_container_name).network_info[0]
    api_url = "http://%s:%s/" % (service.hostname, service.host_port)
    assert request_session.get(api_url)
    return request_session, api_url

def test_prometheus_runtimeinfo(wait_for_api):
    request_session, prom_url = wait_for_api
    prom_api_url = urljoin(prom_url, 'api/v1/')
    item = request_session.get(urljoin(prom_api_url, 'status/runtimeinfo')).json()
    pprint.pprint('status/runtimeinfo')
    pprint.pprint(item)
    assert item['status'] == 'success'

def test_prometheus_targets(wait_for_api):
    request_session, prom_url = wait_for_api
    prom_api_url = urljoin(prom_url, 'api/v1/')
    item = request_session.get(urljoin(prom_api_url, 'targets')).json()
    pprint.pprint('targets')
    pprint.pprint(item)
    assert item['status'] == 'success'
