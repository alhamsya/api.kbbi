import requests
import re
import time
import sys
import random

from bs4 import BeautifulSoup
from flask import Blueprint, request

from core.hooks import resp_err, resp_success
from core.decorators import is_connection
from core.utils import get_now

main_bp = Blueprint("main", __name__)

def auth_email():
    auth_login = [
        # 'data.alham@gmail.com',
        # 'alhamsya@gmail.com',
        # 'finance.alham@gmail.com',
        # 'game.alham@gmail.com',
        # 'bot.alham1@gmail.com',
        # 'bot.alham2@gmail.com',
        # 'bot.alham3@gmail.com',
        # 'bot.alham1@hotmail.com',
        # 'bot.alham2@hotmail.com',
        # 'bot.alham3@hotmail.com',
        # 'bot.alham4@hotmail.com',
        # 'bot.alham5@hotmail.com',
        # 'bot.alham6@hotmail.com',
        'bot.alham7@hotmail.com',
        'bot.alham8@hotmail.com',
        'bot.alham9@hotmail.com',
        'bot.alham10@hotmail.com',
        'bot.alham11@hotmail.com',
        'bot.alham12@hotmail.com',
        'bot.alham13@hotmail.com',
        'bot.alham14@hotmail.com',
        'bot.alham15@hotmail.com',
        'aysmahla@gmail.com',
        'indiastutiksri@gmail.com'
    ]

    return auth_login


@main_bp.route("/", methods=['GET'])
@is_connection
def main_info():
    ip = requests.get('https://api.ipify.org').text
    result = {
        "local_time": get_now('ID'),
        "local_date": get_now('ID', True),
        "host": ip
    }
    return resp_success(result, "Request method POST and param json:<word>")


@main_bp.route("/", methods=['POST'])
@is_connection
def app_info():
    # Initial var
    sleep = 0
    auth = dict()
    # Validation request
    post_data = request.get_json()
    if not post_data:
        return resp_err("Input not valid", 1)

    # Validation empty
    word_req = post_data.get("word")
    if not word_req:
        return resp_err("Input not valid", 2)

    # word_req.strip()
    word_req = re.sub('[^A-Za-z0-9-]+', '', word_req)

    # Start auto login
    s = requests.session()
    resp_login = s.get('https://kbbi.kemdikbud.go.id/Account/Login')
    sou = BeautifulSoup(resp_login.content, "html.parser")
    csrf = sou.find('input', {"name": "__RequestVerificationToken"})
    token = csrf.attrs['value']
    password = "123456789"

    num_auth = 0
    iteration = 0
    while True:
        iteration += 1
        rant_int = random.randrange(len(auth_email()))
        email = auth_email()[rant_int]

        if len(auth_email()) * 2 == num_auth:
            print('=' * 50)
            print('All account limit')
            print('=' * 50)
            sys.stdout.flush()
            return resp_err("All account limit", 3)

        auth.update({"Posel": email})
        auth.update({"KataSandi": password})
        auth.update({"__RequestVerificationToken": token})

        try:
            s.post('https://kbbi.kemdikbud.go.id/Account/Login', data=auth)
            # End auto login

            url_req = "https://kbbi.kemdikbud.go.id/entri/%s" % (word_req)

            resp = s.get(url_req, timeout=5)
            # time.sleep(sleep)
            soup = BeautifulSoup(resp.content, "html.parser")
        except Exception as e:
            print("err: %s | %s | %s" % (e, iteration, word_req))
            sys.stdout.flush()
            return resp_err("Website KBBI not response", 4, 500)

        limit_request = soup.find(text=" Batas Sehari")
        if limit_request:
            print('Limit account - %s' % email)
            sys.stdout.flush()
            num_auth += 1
            continue

        error_request = soup.find(text="Terjadi Kesalahan")
        if error_request:
            print('Error request word : %s | %s' % (word_req, iteration))
            sys.stdout.flush()
            num_auth += 1
            continue

        data_text = soup.find(text=" Entri tidak ditemukan.")
        render_finish = soup.findAll("span", {"class": "glyphicon-info-sign"})
        if data_text and render_finish:
            result = {
                "sts_word": False,
                "word": word_req
            }
            return resp_success(result, "Word is not found")

        if not data_text and render_finish:
            break

        # sleep += 0.25

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
