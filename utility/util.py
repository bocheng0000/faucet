#!/usr/bin/env python
# encoding: utf-8

"""
@author: Bocheng.Zhang
@license: MIT
@contact: bocheng0000@gmail.com
@file: util.py
@time: 2019-07-02 21:39
"""

from copy import deepcopy
import linecache
import os
import time

from utility import request
from wallet import transaction as t

# 设置输出格式
BOLD, BLUE, RED, GREY, YELLOW, GREEN = ("", ""), ("", ""), ("", ""), ("", ""), ("", ""), ("", "")
if os.name == 'posix':
    # primitive formatting on supported
    # terminal via ANSI escape sequences:
    BOLD = ('\033[0m', '\033[1m')
    BLUE = ('\033[0m', '\033[0;34m')
    RED = ('\033[0m', '\033[0;31m')
    GREY = ('\033[0m', '\033[1;30m')
    YELLOW = ('\033[0m', '\033[1;33m')
    GREEN = ('\033[0m', '\033[1;32m')


def formate_string(mode, string: str):
    if mode == "BOLD" or mode == 0:
        return ("{}%s" % string + "{}").format(BOLD[1], BOLD[0])
    elif mode == "GREEN" or mode == 1:
        return ("{}%s" % string + "{}").format(GREEN[1], GREEN[0])
    elif mode == "RED" or mode == 2:
        return ("{}%s" % string + "{}").format(RED[1], RED[0])
    elif mode == "YELLOW" or mode == 3:
        return ("{}%s" % string + "{}").format(YELLOW[1], YELLOW[0])
    elif mode == "BLUE" or mode == 4:
        return ("{}%s" % string + "{}").format(BLUE[1], BLUE[0])
    elif mode == "GREY" or mode == 5:
        return ("{}%s" % string + "{}").format(GREY[1], GREY[0])
    else:
        return "[" + string + "]"


def bold(string: str):
    return formate_string("BOLD", string)


def green(string: str):
    return formate_string("GREEN", string)


def red(string: str):
    return formate_string("RED", string)


def yellow(string: str):
    return formate_string("YELLOW", string)


def blue(string: str):
    return formate_string("BLUE", string)


def grey(string: str):
    return formate_string("GREY", string)


# OS
def check_dir(dir: str):
    """
    Check if the dir exists. If the dir does not exist, create a file.
    :param filename: the path of the dir
    :return:None
    """
    if not os.path.exists(dir):
        os.makedirs(dir)


def check_file(filename: str):
    """
    Check if the file exists. If the file does not exist, create a file.
    :param filename: the name of the file
    :return:None
    """
    if not os.path.exists(filename):
        os.system("touch {}".format(filename))


# log
DEBUG = 0
INFO = 1
WARNING = 2
ERROR = 3
CRITICAL = 4


def getCoinbaseByHeight(hei: int) -> dict:
    """
    get the coinbase transaction at the specified height
    :param hei: the specified height
    :return: A dict representing the block data.
    """

    # get the block at the specified height
    _block = request.get_block_by_height(height=hei)
    # get all transactions in the block
    _txs = _block["tx"]

    # The coinbase transaction must be the first transaction and type 0
    _coinbase = _txs[0]
    assert _coinbase["type"] == 0
    return _coinbase


def getCoinbaseOutput(hei: int) -> list:
    """
    return the coinbase's outputs at the specified height
    :param hei: the specified height
    :return: coinbase's outputs
    """
    _coinbase = getCoinbaseByHeight(hei)
    return _coinbase["vout"]


def SelaToEla(value: int) -> str:
    """
    convert sela to ela
    :param value: sela, 1 ela = 10^8 sela
    :return: a string representing the amount in ela
    """
    value = int(value)
    front = int(value / 100000000)
    after = value % 100000000
    return str(front) + "." + "0" * (8 - len(str(after))) + str(after)


def strElaToIntSela(value: str) -> int:
    dotLocation = value.find(".")
    if dotLocation == -1:
        value_sela = int(value) * 100000000
        return value_sela
    else:
        front = value[:dotLocation]
        end = value[dotLocation + 1:]
        assert len(end) <= 8
        end = end + "0" * (8 - len(end))
        value_sela = int(front) * 100000000 + int(end)
        return value_sela


# utility for time
def get_block_date(height: int) -> str:
    blockInfo = request.get_block_by_height(height=height)
    return timestamp_to_data(blockInfo["time"])


def timestamp_to_data(timestamp: int) -> str:
    time_gm = time.gmtime(timestamp)
    return time.strftime("%Y-%m-%d", time_gm)


# utility for transaction
def gen_intput_by_utxo(utxos: dict):
    amount = 0
    inputs = []
    for _utxo in utxos:
        amount += strElaToIntSela(_utxo["amount"])
        _input = t.TxInput(txid=_utxo["txid"], index=_utxo["vout"])
        inputs.append(_input)
    return inputs, amount


def gen_output_by_receiver(receivers: dict):
    if len(receivers.keys()) == 0:
        return None
    else:
        outputs = []
        for _add in receivers.keys():
            _value = int(receivers[_add])
            _output = t.TxOutput(address=_add, value=_value)
            outputs.append(_output)
        return outputs


def replace_angle_brackets(s):
    return s.replace('<', '{').replace('>', '}').replace('}\n\t{', '},\n\t{').replace('}{', '},\n\t{').replace('\n',
                                                                                                               '').replace(
        '\t', "")


if __name__ == '__main__':
    pass
