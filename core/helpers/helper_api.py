import logging
import time
import uuid

import requests
import simplejson as json

logger = logging.getLogger()

TIMEOUT = 5


# borrowing from the other ^^
def api(api_base, headers=None):
    S = requests.Session()

    def req(method, endpoint, data=None, json_encoded=True, force_data=False):
        url = api_base() + endpoint
        method = method.upper()
        log_id = uuid.uuid4().hex
        t1 = time.time()
        logger.info('%s-start|%s|%s|%s|%d' % (method, log_id, url, json.dumps(data), t1))
        try:
            if method == 'GET':
                resp = S.get(url, headers=headers, params=data, timeout=TIMEOUT)
            elif method == 'POST':
                if json_encoded and not force_data:
                    resp = S.post(url, headers=headers, json=data, timeout=TIMEOUT)
                else:
                    resp = S.post(url, headers=headers, data=data, timeout=TIMEOUT)
            elif method == 'PUT':
                resp = S.put(url, headers=headers, data=data, timeout=TIMEOUT)
            else:
                return None, {}, {'error': 'wrong-method'}

            logger.info('%s-end|%s|%s|%s|spent: %d' % (method, log_id, url, resp.status_code, time.time() - t1))
            if resp.status_code == 200:
                return resp.json(), {'error': '', 'status_code': resp.status_code}
            else:
                logging.warning(
                    '%s-fail|%s|%s|status_code: %s|response: %s' % (method, log_id, url, resp.status_code, resp.content)
                )
                return None, {'error': resp.content.decode('utf-8'), 'status_code': resp.status_code}
        except requests.RequestException as e:
            logger.warning('%s-error|%s|%s|exception: %s|spent: %d' % (method, log_id, url, e, time.time() - t1))
            return None, {'error': str(e), 'status_code': 500}

    return req
