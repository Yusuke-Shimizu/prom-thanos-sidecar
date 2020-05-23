import pytest
import requests
import json
import pprint
from urllib.parse import urljoin
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
from retrying import retry

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
def wait_for_prometheus(module_scoped_container_getter):
    request_session = requests.Session()
    retries = Retry(total=5,
                    backoff_factor=0.1,
                    status_forcelist=[500, 502, 503, 504])
    request_session.mount('http://', HTTPAdapter(max_retries=retries))

    target_container_name = 'prometheus'
    service = module_scoped_container_getter.get(target_container_name).network_info[0]
    api_url = "http://%s:%s/" % (service.hostname, service.host_port)
    assert request_session.get(api_url)

    prom_api_url = urljoin(api_url, 'api/v1/')
    return request_session, prom_api_url

def test_prometheus_runtimeinfo(wait_for_prometheus):
    request_session, prom_url = wait_for_prometheus
    item = request_session.get(urljoin(prom_url, 'status/runtimeinfo')).json()
    pprint.pprint('status/runtimeinfo')
    pprint.pprint(item)
    assert item['status'] == 'success'

@retry(stop_max_delay=30 * 1000, wait_incrementing_start=1000, wait_incrementing_increment=1000)
def check_prometheus_targets(wait_for_prometheus, target_name):
    request_session, prom_url = wait_for_prometheus
    item = request_session.get(urljoin(prom_url, 'targets')).json()
    pprint.pprint('targets')
    pprint.pprint(item)

    active_targets = item['data'] ['activeTargets']
    assert len(active_targets) > 0

    scrape_list = [d.get('scrapePool') for d in active_targets]
    target_index = scrape_list.index(target_name)
    assert active_targets[target_index]['health']== 'up'

@pytest.mark.parametrize('target_name', [
    'prometheus',
    # 'thanos_sidecar',
])
def test_prometheus_targets(wait_for_prometheus, target_name):
    check_prometheus_targets(wait_for_prometheus, target_name)
