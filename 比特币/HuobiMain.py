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

        can_sell_count = _can_sell(str(get_balance()))
        can_sell_count = str(1.00)
        if ( 0 < can_sell_count):
            print("###### %s 卖出： 交易[%s] 数量[%s] 价格[%s]" % 
                (_time(), symble, str(can_sell_count), m_sell_price))

            count = can_sell_count
            ret_info = commit_order(count, 'api', symble, 'sell-limit', m_sell_price)
            ret = ret_info['status']
            print ret_info

            if ( "ok" == ret):
                print("###### %s 卖出 [%s:%s] 成功 %s" % 
                    (_time(), count,str(m_sell_price),ret_info))
                return 0
            else:
                print("###### %s 卖出 [%s:%s] 失败 %s" % 
                    (_time(), count,str(m_sell_price),ret_info))
                return -1

    except Exception as e:
        print(" ###### 异常：%s" % str(e))
        return -1

# 买入/卖出价
m_buy_price = 0.00000922
m_sell_price = 0.00008353

# 计价货币/基础货币
m_base_currency = 'tnb' #'lsk'
m_quote_urrency = 'eth'

# 买入/卖出量
m_buy_count = 1
m_sell_count = 10

if __name__ == '__main__':
    _sell_combine()
    #print(get_currencys())
    #_is_transaction_valid(str(get_symbols()))
    #_buy_combine();
    parse_balance(str(get_balance()))
    # if len(sys.argv) < 6:
    #     print("参数不全")
    #     exit(0)

    # if len(sys.argv) >= 6:

    #     m_base_currency = str(sys.argv[1])
    #     m_title = str(sys.argv[2])
    #     m_buy_price = float(sys.argv[3])
    #     m_sell_price = float(sys.argv[4])
    #     m_buy_count = int(sys.argv[5])

    # if len(sys.argv) > 6:
    #     m_query = str(sys.argv[6])

    # print("-- 交易参数： 币种[%s] 币名[%s] 买入价[%s] 卖出价[%s] 买入量[%s] 账户余额显示[%s]\n" % (m_base_currency, m_title, m_buy_price, m_sell_price, m_buy_count,m_query))
    
    # if ( "1" == m_query):
    #     # print("###### 获取账户")
    #     # print(get_accounts())
    #     parse_balance(str(get_balance()))
    #     exit(0)
    # else:
    #     while 1:
    #         ret = _buy_combine();
    #         if( 0 == ret):
    #             while 1:
    #                 if( 0 != _sell_combine()):
    #                     time.sleep(1)
    #         elif( -2 == ret):
    #             continue
    #         else:
    #             exit(0)

    # #_can_sell(str(get_balance()))
    # exit(0)






    # --------------------------------------------------------------------
    # print("###### %s 获取1分钟线")
    # print(get_kline('btccny', '1min'))
    # print("###### %s 获取合并深度为1的盘口")
    # print(get_depth('btccny', 'step1'))
    # print("###### %s 获取Trade Detail")
    # print(get_trade('btccny'))
    # print("###### %s 获取 Market Detail 24小时成交量数据")
    # print(get_detail('btccny'))
    # print("###### %s 获取支持交易对")
    # print(get_symbols())
    
    # print("###### %s 获取账户")
    # print(get_accounts())

    #print("###### %s 获取当前账户资产")
    #print(get_balance())

    #print('############ 下单')
    #print(orders(0.01, 'api', 'btccny', 'buy-limit', 1000))
    #order = orders(1, 'api', m_symble, 'sell-limit', 0.0001)
    #order_id = order['data']
    #print(order)
    
    #print('############ 执行订单')
    #print(place_order(order_id))

    # print('############ 撤销订单')
    # print(cancel_order(order_id))
    # print('############ 查询某个订单')
    # print(order_info(order_id))
    # print('############ 查询某个订单的成交明细')
    # print(order_matchresults(order_id))
    # print('############ 查询当前委托、历史委托')
    # print(orders_list(m_symble, 'submitted'))
    # print('############ 查询当前成交、历史成交')
    # print(orders_matchresults('btccny'))
    # print('############ 查询虚拟币提币地址')
    # print(get_withdraw_address('btc'))
    # print('############ 新提币接口')
    # print(withdraw_new_create('', 0.01, 'btc', 0.0015))
    # print(get_content())



