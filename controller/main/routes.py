import requests
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
    return resp_success(result)


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

    url_req = "https://kbbi.kemdikbud.go.id/entri/%s" % (word_req)
    resp = requests.get(url_req)
    soup = BeautifulSoup(resp.content, "html.parser")

    data_text = soup.find(text=" Entri tidak ditemukan.")
    if data_text:
        return resp_err("Word not found", 3)

    all_resp = soup.find_all('ul', class_="adjusted-par")
    all_meaning_word = []
    for item in all_resp:
        meaning = item.find("li").getText()
        all_meaning_word.append(meaning)

    result = {
        "word": word_req,
        "meaning": all_meaning_word
    }

    return resp_success(result)
