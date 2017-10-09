# -*- coding: utf-8 -*-
from chinapay.pay.base import BaseChinapayAPI


class Refund(BaseWeChinapayAPI):

    def apply(self,refund_order_id, order_id, origin_date, origin_time, 
            total_fee, refund_fee, fee_type='CNY', notify_url, custom_field=None):
        """
        申请退款

        :param total_fee: 订单总金额，单位为分
        :return: 返回的结果数据
        """
        now = datetime.fromtimestamp(time.time())

        # TODO productType

        data = {
            'Version': '20170419',
            'MerId': self._client.mer_id,
            'MerOrderNo': refund_order_id,
            'TranDate': now.strftime('%Y%m%d'),
            'TranTime': now.strftime('%H%M%S'),
            'OriOrderNo': order_id,
            'OriTranDate': origin_date,
            'OriTranTime': origin_time,
            'RefundAmt': refund_fee,
            'OrderAmt': total_fee,
            'TranType': '0401',
            'ProductType': '',
            'BusiType': '0001',
            'CurryNo': fee_type,
            'MerBgUrl': notify_url,
            'MerResv': custom_field,
        }
        return self._post('overseasRefund/SingleRefund.do', data=data)

