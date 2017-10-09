# -*- coding: utf-8 -*-
import time
import random
from datetime import datetime, timedelta

from chinapay.base import BaseChinapayAPI
from chinapay.utils import (
    timezone, get_external_ip, random_string, to_text, json, calculate_signature
)


class Order(BaseChinapayAPI):

    def create(self, order_id, total_fee, fee_type, redirect_url, notify_url, custom_field):
        """
        统一下单接口


        :return: 返回的结果数据
        """
        # now = datetime.fromtimestamp(time.time(), tz=timezone('Asia/Shanghai'))
        now = datetime.fromtimestamp(time.time())

        # TODO productType

        data = {
            'Version': '20170419',
            'MerId': self._client.mer_id,
            'MerOrderNo': order_id,
            'TranDate': now.strftime('%Y%m%d'),
            'TranTime': now.strftime('%H%M%S'),
            'OrderAmt': total_fee,
            'TranType': '0001',
            'ProductType': '',
            'BusiType': '0001',
            'CurryNo': fee_type,
            'MerPageUrl': redirect_url,
            'MerBgUrl': notify_url,
            'MerResv': custom_field,
        }
        return self._post('overseasPay/TransGetPage', data=data)

