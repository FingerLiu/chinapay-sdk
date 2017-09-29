# -*- coding: utf-8 -*-
import inspect
import logging
import requests
import xmltodict
from xml.parsers.expat import ExpatError
from optionaldict import optionaldict

from chinapay.exceptions import ChinapayException, InvalidSignatureException
from chinapay.utils import (
    random_string, calculate_signature, _check_signature, dict_to_xml
)
from chinapay.base import BaseChinapayAPI
from chinapay import api


__version__ = '0.0.1'
__author__ = 'liupeng'


logger = logging.getLogger(__name__)


def _is_api_endpoint(obj):
    return isinstance(obj, BaseChinapayAPI)


class Chinapay(object):
    """
    chinapay 接口

    :param cert_file:
    :param password:
    :param debug: 

    build_data
    sign
    verify
    verify_file
    encrypt
    decrypt

    create_order
    refund
    get_order


    """
    _http = requests.Session()

    order = api.Order()
    """订单接口"""
    refund = api.Refund()
    """退款接口"""

    API_BASE_URL = 'https://api.mch.weixin.qq.com/'
    API_BASE_TEST_URL = 'https://api.mch.weixin.qq.com/'

    def __new__(cls, *args, **kwargs):
        self = super(Chinapay, cls).__new__(cls)
        api_endpoints = inspect.getmembers(self, _is_api_endpoint)
        for name, _api in api_endpoints:
            api_cls = type(_api)
            _api = api_cls(self)
            setattr(self, name, _api)
        return self

    def __init__(self, cert_file, password, test=False):
        """
        :param cert_file:
        :param password:
        :param debug: 
    
        """
        self.cert_file = cert_file
        self.password = password
        self.test = test
        if self.test:
            self.API_BASE_URL = self.API_BASE_TEST_URL

    def _request(self, method, url_or_endpoint, **kwargs):
        if not url_or_endpoint.startswith(('http://', 'https://')):
            api_base_url = kwargs.pop('api_base_url', self.API_BASE_URL)
            url = '{base}{endpoint}'.format(
                base=api_base_url,
                endpoint=url_or_endpoint
            )
        else:
            url = url_or_endpoint

        if isinstance(kwargs.get('data', ''), dict):
            data = optionaldict(kwargs['data'])
            kwargs['data'] = body

        # TODO build request data
        pass
        res = None
        return self._handle_result(res)

    def _handle_result(self, res):
        # TODO handle response and exception

        return data

    def get(self, url, **kwargs):
        return self._request(
            method='get',
            url_or_endpoint=url,
            **kwargs
        )

    def post(self, url, **kwargs):
        return self._request(
            method='post',
            url_or_endpoint=url,
            **kwargs
        )

    def check_signature(self, params):
        return _check_signature(params, self.cert_file, self.password)

    def parse_payment_result(self, data):
        """解析支付结果通知"""
        sign = data.pop('sign', None)
        # TODO parse and check signature
        real_sign = calculate_signature(data, self.api_key)
        return data
