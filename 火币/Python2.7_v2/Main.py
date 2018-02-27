#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-12-15 15:40:03
# @Author  : KlausQiu
# @QQ      : 375235513
# @github  : https://github.com/KlausQIU

from Utils import *
from HuobiService import*
from Logger import *
from Global import *

import time
import sys

def _time():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

# 购买
########################################################################################
# 检查币种上线
def parse_content(content):

    ret = content.split(": [")
    items = ret[1].split("}, {")

    for item in items:
        s = item.split(", u")
        c_base = c_quote = ""

        for kv in s:
            if "base-currency" in kv:               #基础货币
                c_base = kv.split(": u")[1].strip("'")
            elif "quote-currency" in kv:            #计价货币
                c_quote = kv.split(": u")[1].strip("'")
            
        ide = "'" + c_base + c_quote + "'"
        m_ide = "'" + m_base_currency + m_quote_urrency + "'"

        #log.debug "########%s %s" %(ide, m_ide)
        if ide == m_ide:# and tit == title:
            return 0
    
    return -1

# 取实时价格
# {u'status': u'ok', u'ch': u'market.abteth.kline.1min', u'data': [{u'count': 2, u'vol': 10.8771839683, u'high': 0.00143083, u'amount': 7602.01, u'low': 0.00143083, u'close': 0.00143083, u'open': 0.00143083, u'id': 1519722600}], u'ts': 1519722610172}
def get_price(content):

    price = 0

    ret = content.split(": [")
    items = ret[1].split(", u")

    for item in items:
        print item

        s = item.split(", u")
        c_base = c_quote = ""

        for kv in s:
            if "close" in kv:               #基础货币
                price = kv.split(": ")[1].strip("'")

    return price

# 买 成功返回买入价
def _buy():
    try:
        while 1:
            symble = m_base_currency + m_quote_urrency

            if ( 0 == parse_content(str(get_symbols()))):
                # 检查交易对存在，可以进行交易
                while 1:
                    m_buy_price = get_price(str(get_kline(symble,'1min',1)))
                    if ( 0 >= m_buy_price):
                        m_buy_price = _gol.buy_price()

                    log.info("买入： 交易[%s] 数量[%s] 价格[%s]" % 
                        (symble, m_buy_count, m_buy_price))

                    ret_info = send_order(m_buy_count, 'api', symble, 'buy-limit', m_buy_price)
                    ret = ret_info['status']

                    if ( "ok" == ret):
                        log.info("买入 [%s:%s] 成功 %s" % 
                            (m_buy_count,m_buy_price,ret_info))
                        return 0
                    else:
                        log.debug("重试 %s 执行订单 " % (ret_info))
                        time.sleep(0.1)
            else:
                log.debug("币种未上线 %s" % m_base_currency)

    except Exception as e:
            log.error("异常：%s" % str(e))
            return -1

# 出售
#######################################################################################
# 检查账户可售数量
def _can_sell(content):
    try:
        ret = content.split(": [")
        items = ret[1].split("}, {")

        for item in items:
            if m_base_currency in item and "frozen" not in item:
                s = item.split("', u'")
                
                for k in s:                
                    if "balance" in k:
                        rmb = k.split("': u'")[1][0:20]
                        rmb = int(float(rmb))

                        if rmb > 0:
                            return int(rmb)
                        else:
                            return 0

    except Exception as e:
        log.error("异常：%s" % str(e))
        return -1


# 卖
def _sell_combine():
    try:
        symble = m_base_currency + m_quote_urrency

        _sell_count = 0
        
        if(m_sell_count > 0):
            _sell_count = m_sell_count
        else:
            _sell_count = _can_sell(str(get_balance()))

        if ( 0 < _sell_count):
            # 卖价等于买入价乘以倍数
            log.info("卖出： 交易[%s] 数量[%s] 价格[%s]" % 
                (symble, str(_sell_count), m_buy_price*_gol.rate()))

            ret_info = send_order(_sell_count, 'api', symble, 'sell-limit', m_buy_price*_gol.rate())
            ret = ret_info['status']
            
            if ( "ok" == ret):
                log.debug("卖出 [%s:%s] 成功 %s" % 
                    (_sell_count,m_buy_price*_gol.rate(),ret_info))
                return 0
            else:
                log.error("卖出 [%s:%s] 失败 %s" % 
                    (_sell_count,m_buy_price*_gol.rate(),ret_info))
                return -1
        else:
            log.error("卖出失败（数量不足）： 交易[%s] 数量[%s] 价格[%s]" % 
                (symble, str(_sell_count), m_buy_price*_gol.rate()))
            return -1

    except Exception as e:
        log.error("异常：%s" % str(e))
        return -1


# 解析账户资产
#######################################################################################
def parse_balance(content):
    #log.debug("-- 获取当前账户资产 %s\n" % (content))
    ret = content.split(": [")

    items = ret[1].split("}, {")
    
    for item in items:
        s = item.split("', u'")
        
        for k in s:
            if "balance" in k:
                rmb = k.split("': u'")[1][0:10]
                if float(rmb) > 0:
                    log.debug(item)

    return 0


# 买入量 'api' 'iostbtc' 'buy-limit'  买入价格
# 卖出量 'api' 'iostbtc' 'sell-limit' 卖出价格
# send_order(amount, source, symbol, _type, price=0):

if __name__ == '__main__':
    _gol = gol()
    
    m_quote_urrency = _gol.quote_urrency()
    m_base_currency = _gol.base_currency()
    
    m_buy_count = _gol.buy_count()
    m_sell_count = _gol.sell_count()

    _logf = "/Users/hubao/Desktop/日志/" + _gol.get_user() + ".log"
    log = Logger(_logf,logging.ERROR,logging.DEBUG)

    parse_balance(str(get_balance()))
    #log.debug(get_detail('tnbeth'))
    #log.debug order_info(1980353438)
    #_buy()
    #_sell_combine()
    #exit(0)
    #parse_content(str(get_symbols()))
    #log.debug(get_detail('htbtc'))
    #log.debug(get_currencys())
    #log.debug(get_symbols())

    if(0 == _buy()):
        while 1:
            _sell_combine();    
    