#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-12-15 15:40:03
# @Author  : KlausQiu
# @QQ      : 375235513
# @github  : https://github.com/KlausQIU

from Utils import *
from HuobiServices import *

import subprocess
import operator
import sys
import time

def _time():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

# 检查交易对可用
def _is_transaction_valid(content):
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

        if ide == m_ide:# and tit == title:
            return 0

    return -1


# 解析账户资产
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


def _buy_combine():
    try:
        while 1:
            symble = m_base_currency + m_quote_urrency

            if ( 0 == _is_transaction_valid(str(get_symbols()))):
                print("###### %s 买入： 交易[%s] 数量[%s] 价格[%s]" % 
                    (_time(), symble, m_buy_count, m_buy_price))

                while 1:
                    ret_info = commit_order(m_buy_count, 'api', symble, 'buy-limit', m_buy_price)
                    ret = ret_info['status']

                    if ( "ok" == ret):
                        print("###### %s 买入 [%s:%s] 成功 %s" % 
                            (_time(), m_buy_count,str(m_buy_price),ret_info))
                        return 0
                    else:
                        print("###### %s 重试 %s 执行订单 ############" % 
                            (_time(), ret_info))
                        time.sleep(0.1)
            else:
                print("###### %s 币种未上线 %s" % (_time(), m_base_currency))
                time.sleep(0.01)

    except Exception as e:
        print(" ###### 异常：%s" % str(e))
        return -2
    

def _sell_combine():
    try:
        symble = m_base_currency + m_quote_urrency
        if ( 0 != _is_transaction_valid(str(get_symbols()))):
            return -1

        _sell_count = 0
        
        if(m_sell_count > 0):
            _sell_count = m_sell_count
        else:
            _sell_count = _can_sell(str(get_balance()))

        if ( 0 < _sell_count):
            print("###### %s 卖出： 交易[%s] 数量[%s] 价格[%s]" % 
                (_time(), symble, str(_sell_count), m_sell_price))

            ret_info = commit_order(_sell_count, 'api', symble, 'sell-limit', m_sell_price)
            ret = ret_info['status']
            print ret_info

            if ( "ok" == ret):
                print("###### %s 卖出 [%s:%s] 成功 %s" % 
                    (_time(), _sell_count,str(m_sell_price),ret_info))
                return 0
            else:
                print("###### %s 卖出 [%s:%s] 失败 %s" % 
                    (_time(), _sell_count,str(m_sell_price),ret_info))
                return -1

    except Exception as e:
        print(" ###### 异常：%s" % str(e))
        return -1

# 买入/卖出价
m_buy_price = 0.000115
m_sell_price = 0.0004

# 计价货币/基础货币
m_quote_urrency = 'eth'
m_base_currency = 'wpr'

# 买入/卖出量
m_buy_count = 8000
m_sell_count = 0

stdout_backup = sys.stdout
log_file = open("message.log", "w")
sys.stdout = log_file
log_file.close()

if __name__ == '__main__':
    _sell_combine()
    #print(get_currencys())
    #_is_transaction_valid(str(get_symbols()))
    #_buy_combine();
    parse_balance(str(get_balance()))
    # if len(sys.argv) < 6:
    #     print("参数不全")
    #     exit(0)

