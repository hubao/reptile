#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-12-15 15:40:03
# @Author  : KlausQiu
# @QQ      : 375235513
# @github  : https://github.com/KlausQIU

from Utils import *
from Custorm import *

from HuobiService import*
import time

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

        #print "########%s %s" %(ide, m_ide)
        if ide == m_ide:# and tit == title:
            return 0

    return -1

# 买
def _buy():
    try:
        while 1:
            symble = m_base_currency + m_quote_urrency

            if ( 0 == parse_content(str(get_symbols()))):
                # 检查交易对存在，可以进行交易
                while 1:
                    
                    print("###### %s 买入： 交易[%s] 数量[%s] 价格[%s]" % 
                        (_time(), symble, m_buy_count, m_buy_price))

                    ret_info = send_order(m_buy_count, 'api', symble, 'buy-limit', m_buy_price)
                    ret = ret_info['status']

                    if ( "ok" == ret):
                        print("###### %s 买入 [%s:%s] 成功 %s" % 
                            (_time(),m_buy_count,m_buy_price,ret_info))
                        return 0
                    else:
                        print("###### %s 重试 %s 执行订单 ############" % (_time(),ret_info))
                        time.sleep(0.1)
            else:
                print("###### %s 币种未上线 %s" % 
                    (_time(), m_base_currency))
                time.sleep(0.5)

    except Exception as e:
            print(" ###### 异常：%s" % str(e))
            return -1

# 出售
#######################################################################################
# 检查账户可售数量
def _can_sell(content):
    ret = content.split(": [")
    items = ret[1].split("}, {")


    for item in items:
        if m_base_currency in item and "frozen" not in item:
            s = item.split("', u'")
            
            for k in s:                
                if "balance" in k:
                    rmb = k.split("': u'")[1][0:20]
                    
                    print("###### %s 检查账户参数： 数量[%s]" % 
                        (_time(), rmb))
                    if float(rmb) > 0:
                        return int(float(rmb)) 
                    else:
                        return 0

    return -1

# 卖
def _sell_combine():
    try:
        _sell_count = 0
        
        if(m_sell_count > 0):
            _sell_count = m_sell_count
        else:
            _sell_count = _can_sell(str(get_balance()))

        if ( 0 < _sell_count):
            symble = m_base_currency + m_quote_urrency
            
            print("###### %s 卖出： 交易[%s] 数量[%s] 价格[%s]" % 
                (_time(), symble, str(_sell_count), m_sell_price))

            ret_info = send_order(_sell_count, 'api', symble, 'sell-limit', m_sell_price)
            ret = ret_info['status']
            
            if ( "ok" == ret):
                print("###### %s 卖出 [%s:%s] 成功 %s" % 
                    (_time(), _sell_count,m_sell_price,ret_info))
                return 0
            else:
                print("###### %s 卖出 [%s:%s] 失败 %s" % 
                    (_time(), _sell_count,m_sell_price,ret_info))
                return -1

    except Exception as e:
        print(" ###### 异常：%s" % str(e))
        return -1


# 解析账户资产
#######################################################################################
def parse_balance(content):
    #print("-- 获取当前账户资产 %s\n" % (content))
    ret = content.split(": [")

    items = ret[1].split("}, {")
    
    for item in items:
        s = item.split("', u'")
        
        for k in s:
            if "balance" in k:
                rmb = k.split("': u'")[1][0:10]
                if float(rmb) > 0:
                    print(item)

    return 0


# 买入量 'api' 'iostbtc' 'buy-limit'  买入价格
# 卖出量 'api' 'iostbtc' 'sell-limit' 卖出价格
# send_order(amount, source, symbol, _type, price=0):

# 买入/卖出价
m_buy_price = 0.00008344
m_sell_price = 0.00008353

# 计价货币/基础货币
m_quote_urrency = 'eth'
m_base_currency = 'tnb'

# 买入/卖出量
m_buy_count = 1
m_sell_count = 10

if __name__ == '__main__':
    parse_balance(str(get_balance()))
    #print(get_detail('tnbeth'))
    #print order_info(1980353438)
    #_buy()
    #_sell_combine()
    #exit(0)
    #parse_content(str(get_symbols()))
    #print(get_detail('htbtc'))
    #print(get_currencys())
    #print(get_symbols())

    # if(0 == _buy()):
    #     while 1:
    #         _sell_combine();
        