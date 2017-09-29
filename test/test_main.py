# -*- coding: utf-8 -*-
from __future__ import (print_function, division, absolute_import, unicode_literals,)

import unittest

from nose.tools import eq_

from json_rpc import register, rpc_dispatcher
from json_rpc.server.http import RPCHandler as HTTPHandler  # TODO:
from json_rpc.server.ws import RPCHandler as WebSocketHandler  # TODO:


suite = unittest.TestSuite()
loader = unittest.TestLoader()
# use `nosetests --with-doctest`
# suite.addTests(doctest.DocTestSuite(letexpr))


# you can appoint method name for rpc call
@register('plus')
def plus(x, y):
    return x + y


def test_plain():
    result = plus(1, 2)
    assert result == 3, result


def test_positional_rpc_call():
    rpc_result = rpc_dispatcher({
        'jsonrpc': '2.0',
        'method': 'plus',
        'params': [1, 2],
        'id': 111,
    })
    assert rpc_result.get('result') == 3, rpc_result


def test_named_rpc_call():
    rpc_result = rpc_dispatcher({
        'jsonrpc': '2.0',
        'method': 'plus',
        'params': {'x': 1, 'y': 2},
        'id': 111,
    })
    assert rpc_result.get('result') == 3, rpc_result


def test_multiple():
    req1 = {
        'jsonrpc': '2.0',
        'method': 'plus',
        'params': [1, 2],
        'id': 111,
    }
    req2 = {
        'jsonrpc': '2.0',
        'method': 'plus',
        'params': [10, 20],
        'id': 111,
    }
    rpc_result = rpc_dispatcher([req1, req2])
    assert rpc_result[0].get('result') == 3, rpc_result
    assert rpc_result[1].get('result') == 30, rpc_result


def test_notify():
    rpc_result = rpc_dispatcher({
        'jsonrpc': '2.0',
        'method': 'plus',
        'params': {'x': 1, 'y': 2},
    })
    assert rpc_result is None, rpc_result


def test_notify_multiple():
    req1 = {
        'jsonrpc': '2.0',
        'method': 'plus',
        'params': [1, 2],
        'id': 111,
    }
    req2 = {
        'jsonrpc': '2.0',
        'method': 'plus',
        'params': [10, 20],
    }
    rpc_result = rpc_dispatcher([req1, req2])

    assert len(rpc_result) == 1, rpc_result
    assert rpc_result[0].get('result') == 3, rpc_result
