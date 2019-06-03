import requests
import re

from bs4 import BeautifulSoup
from flask import Blueprint, request

from core.hooks import resp_err, resp_success
from core.utils import get_now

main_bp = Blueprint("main", __name__)


@main_bp.route("/", methods=['GET'])
def main_info():
    result = {
        "local_time": get_now('ID'),
        "local_date": get_now('ID', True)
    }
    return resp_success(result, "Request method POST and param json:<word>")


@main_bp.route("/", methods=['POST'])
def app_info():
    # Validation request
    post_data = request.get_json()
    if not post_data:
        return resp_err("Input not valid", 1)

    # Validation empty
    word_req = post_data.get("word")
    if not word_req:
        return resp_err("Input not valid", 2)

    word_req.strip()
    word_req= re.sub('[^A-Za-z0-9]+', '', word_req)

    url_req = "https://kbbi.kemdikbud.go.id/entri/%s" % (word_req)
    resp = requests.get(url_req)
    soup = BeautifulSoup(resp.content, "html.parser")

    data_text = soup.find(text=" Entri tidak ditemukan.")
    if data_text:
        result = {
            "sts_word": False,
            "word": word_req
        }
        return resp_success(result, "Word is not found")

    all_resp = soup.find_all('ul', class_="adjusted-par")
    all_meaning_word = []
    for item in all_resp:
        meaning = item.find("li").getText()
        all_meaning_word.append(meaning)

    result = {
        "sts_word": True,
        "word": word_req,
        "meaning": all_meaning_word
    }

    return resp_success(result, "Word found in the KBBI")
