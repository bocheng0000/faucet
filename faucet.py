#!/usr/bin/env python
# encoding: utf-8

"""
@author: Bocheng.Zhang
@license: Apache Licence 
@contact: bocheng0000@gmail.com
@file: faucet.py
@time: 2019/11/6 10:24
"""

import argparse
import time

import config as cf
from wallet import transaction as t
from utility import util, request, encoding

# local_port = 23336

faucet_addr = cf.faucet["address"]
faucet_pk = cf.faucet["publickey"]
faucet_pri = cf.faucet["privatekey"]


def sendTestCoin(chain, outputAddr, value):
    if chain == "ela":
        node_url = cf.ela_url
    else:
        node_url = cf.did_url

    valueSela = util.strElaToIntSela(value)

    # check faucet status
    _balance = request.get_balance(address=faucet_addr, url=node_url)
    if not _balance:
        print(util.red("Get balance error:{}".format(faucet_addr)))
        exit(2)
    elif util.strElaToIntSela(_balance) < valueSela + cf.tx_fee:
        print(util.red("ADD[{}]'s balance is not enough {}".format(faucet_addr, _balance)))
        exit(2)

    print(util.green("Faucet's balance is {}".format(_balance)))

    # Get utxo
    _utxos = request.get_utxos(address=faucet_addr, url=node_url)
    assert _utxos

    # Create input
    inputs, utxoAmount = util.gen_intput_by_utxo(utxos=_utxos)

    # Create output
    _changeValue = utxoAmount - valueSela - cf.tx_fee
    outputs = util.gen_output_by_receiver({outputAddr: valueSela})
    _changeOutput = t.TxOutput(address=faucet_addr, value=_changeValue)
    outputs.append(_changeOutput)

    tx = t.Transaction(inputs=inputs, outputs=outputs)
    txid_infile = encoding.bytes_to_hexstring(data=tx.hash(), reverse=True)

    # Sign the transactriron
    _code = encoding.get_code_from_pb(faucet_pk)
    _parameter = t.ecdsa_sign(faucet_pri, data=tx.serialize_unsigned()).hex()
    tx.programs = [t.Program(code=_code, parameter=_parameter)]

    # Serialize the transaction to get the raw data of the transaction
    raw_tx = tx.serialize().hex()

    # 4. Send transaction to the node
    txid_returned = request.send_tx(raw_tx=raw_tx, url=node_url)

    if txid_returned != txid_infile:
        print(util.red("Send TX ERROR!txid:[{}], return:[{}]".format(txid_infile, txid_returned)))
        exit(2)
    else:
        time_str = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(time.time()))
        _heightSent = request.get_block_height(url=node_url)
        print(util.green("[{}]Tx[{}] is send to node, height[{}].".format(time_str, txid_returned, _heightSent)))

    # 5. Waiting for a node to package the transaction
    print(util.green("Wait for transaction to be confirmed."))

    while True:
        time.sleep(10)
        _height = request.get_block_height(url=node_url)
        if _height > _heightSent:
            tx_details = request.get_tx(tx_id=txid_returned, url=node_url)
            if tx_details["confirmations"] > 0:

                time_str = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(time.time()))
                _balance = request.get_balance(address=outputAddr, url=node_url)
                print(util.green("Tx[{}] is confirmed at height[{}].".format(txid_returned, _height)))

                print(util.green("[{}] {}'s balance is {}, bye".format(time_str, outputAddr, _balance)))
                break
            else:
                continue


if __name__ == '__main__':
    # default value
    nodeType = "did"
    toaddress = ""
    valueToSend = "0.0001"

    parser = argparse.ArgumentParser(description="input parameter")
    parser.add_argument("-n", "--node", type=str, dest="node", choices=["ela", "did", "token", "neo"], help="node type")
    parser.add_argument("-t", "--to", type=str, dest="toaddress", help="address used to received test coin")
    parser.add_argument("-v", "--value", dest="value", help="value of test coins sent")

    args = parser.parse_args()
    if args.node:
        nodeType = args.node
    if args.toaddress:
        toaddress = args.toaddress
    if args.value:
        valueToSend = args.value

    print(util.green("Try to send {} testcoin to {}'s address[{}]".format(valueToSend, nodeType, toaddress)))
    sendTestCoin(nodeType, toaddress, valueToSend)
