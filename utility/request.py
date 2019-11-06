#!/usr/bin/env python
# encoding: utf-8

"""
@author: Bocheng.Zhang
@license: MIT
@contact: bocheng0000@gmail.com
@file: request.py
@time: 2019-07-03 06:37
"""

import requests
from retrying import retry

import config as cf
from utility import util


def post_request(ip: str, method, params={}, user="", password=""):
    try:
        resp = requests.post("https://" + ip, json={"method": method, "params": params},
                             headers={"content-type": "application/json"},
                             auth=requests.auth.HTTPBasicAuth(user, password))
        if resp.status_code == 200:
            return resp.json()
        else:
            print(util.red("Request Error:{}".format(resp.status_code)))
            return None
    except requests.exceptions.RequestException as e:
        print(util.red(e.__str__()))
        return None


@retry(stop_max_attempt_number=5)
def get_block_height(url: str, user="", password=""):
    resp = post_request(url, "getcurrentheight", params={}, user=user, password=password)
    if resp is not None:
        return resp["result"]
    else:
        return resp


@retry(stop_max_attempt_number=5)
def get_block_by_height(url: str, height=0, user="", password=""):
    resp = post_request(url, "getblockbyheight", params={"height": height}, user=user, password=password)
    if resp is not None:
        return resp["result"]
    else:
        return resp


@retry(stop_max_attempt_number=5)
def get_balance(address: str, url: str, user="", password=""):
    if len(address) != 34:
        return None
    resp = post_request(url, "getreceivedbyaddress", params={"address": address}, user=user, password=password)
    if resp is not None:
        return resp["result"]
    else:
        return resp


@retry(stop_max_attempt_number=5)
def get_utxos(address: str, url: str, user="", password=""):
    if len(address) != 34:
        return None
    resp = post_request(url, "listunspent", params={"addresses": [address]}, user=user,
                        password=password)
    if resp is not None:
        return resp["result"]
    else:
        return resp


@retry(stop_max_attempt_number=5)
def get_utxos_by_amount(address: str, amount: str, url: str, user="", password=""):
    if len(address) != 34:
        return None
    resp = post_request(url, "getutxosbyamount", params={"address": address, "amount": amount}, user=user,
                        password=password)
    if resp is not None:
        return resp["result"]
    else:
        return resp


@retry(stop_max_attempt_number=5)
def send_tx(raw_tx: str, url: str, user="", password=""):
    resp = post_request(url, "sendrawtransaction", params={"data": raw_tx}, user=user, password=password)
    if resp is not None:
        return resp["result"]
    else:
        return resp


@retry(stop_max_attempt_number=5)
def get_tx(tx_id: str, url: str, user="", password=""):
    resp = post_request(url, "getrawtransaction", params={"txid": tx_id, "verbose": True}, user=user,
                        password=password)
    if resp is not None:
        return resp["result"]
    else:
        return resp


def get_request(url: str):
    try:
        resp = requests.get(url=url)
        if resp.status_code == 200:
            return resp.json()
        else:
            print(util.red(resp.status_code))
            return None
    except requests.exceptions.RequestException as e:
        print(util.red(e.__str__()))
        return None
