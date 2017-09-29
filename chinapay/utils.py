# -*- coding: utf-8 -*-
"""
    chinapay.utils
    ~~~~~~~~~~~~~~~

    This module provides some useful utilities.

    :copyright: (c) 2014 by messense.
    :license: MIT, see LICENSE for more details.
"""
import string
import copy
import hashlib
import socket
import random
import six
import six.moves.urllib.parse as urlparse


class ObjectDict(dict):
    """Makes a dictionary behave like an object, with attribute-style access.
    """

    def __getattr__(self, key):
        if key in self:
            return self[key]
        return None

    def __setattr__(self, key, value):
        self[key] = value


class ChinapaySigner(object):
    """Chinapay data signer"""

    def __init__(self, delimiter=b''):
        self._data = []
        self._delimiter = to_binary(delimiter)

    def add_data(self, *args):
        """Add data to signer"""
        for data in args:
            self._data.append(to_binary(data))

    @property
    def signature(self):
        """Get data signature"""
        self._data.sort()
        str_to_sign = self._delimiter.join(self._data)
        return hashlib.sha1(str_to_sign).hexdigest()


def check_signature(token, signature, timestamp, nonce):
    # TODO check signature
    pass


def timezone(zone):
    """Try to get timezone using pytz or python-dateutil

    :param zone: timezone str
    :return: timezone tzinfo or None
    """
    try:
        import pytz
        return pytz.timezone(zone)
    except ImportError:
        pass
    try:
        from dateutil.tz import gettz
        return gettz(zone)
    except ImportError:
        return None


def random_string(length=16):
    rule = string.ascii_letters + string.digits
    rand_list = random.sample(rule, length)
    return ''.join(rand_list)


def get_querystring(uri):
    """Get Querystring information from uri.

    :param uri: uri
    :return: querystring info or {}
    """
    parts = urlparse.urlsplit(uri)
    return urlparse.parse_qs(parts.query)


def byte2int(c):
    if six.PY2:
        return ord(c)
    return c


def get_external_ip():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        chinapay_ip = socket.gethostbyname('cb.chinapay.com')
        sock.connect((chinapay_ip, 80))
        addr, port = sock.getsockname()
        sock.close()
        return addr
    except socket.error:
        return '127.0.0.1'
