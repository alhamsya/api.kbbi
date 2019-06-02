from flask import jsonify, request
import urllib3


def resp_err(message, error_num=None, err_code=400):
    content = {
        "status": False,
        "message": message,
        "meta": {
            "response_code": err_code,
            "error_code": error_num
        }
    }
    return jsonify(content), err_code


def resp_success(data, message=None, code=200):
    content = {
        "status": True,
        "message": message,
        "data": data
    }
    return jsonify(content), code


def check_connection():
    try:
        http = urllib3.PoolManager()
        http.request('GET', 'http://216.58.192.142', timeout=5.5)
        return True
    except (urllib3.exceptions.NewConnectionError, urllib3.exceptions.MaxRetryError):
        return False