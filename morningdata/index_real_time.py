#!/usr/bin/env python3.4
# encoding: utf-8
"""
Created on 17-12-11

@author: Xu
"""
import tushare as ts
import datetime
import logging.config

from forex_python.converter import CurrencyRates
from sqlalchemy import create_engine
from common.pgutils import get_conn, execute_sql, get_engine

logging.config.fileConfig("logging.conf")
logger = logging.getLogger("root")

code_engine = get_engine()


def get_code():
    """
    使用sqlalchemy存储大盘指数行情数据获取 可获得上证指数、深证指数
    :return:
    """
    engine = create_engine(code_engine)
    df_index = ts.get_index()
    logger.info(df_index)
    # 存入数据库
    df_index.to_sql('middle_news_market', engine, schema='public', if_exists='replace')


def get_code1(conn):
    """
    使用常规存储方式存储大盘指数行情数据获取 可获得上证指数、深证指数
    :return:
    """
    df_index = ts.get_index()
    sql_market = """
    INSERT INTO middle_news_market(
        code, name, change_market, open_market, preclose, close_market, high, low, volume, amount
        ) 
    VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    for i in range(0, 25):
        code = df_index['code'][i]
        name = df_index['name'][i]
        change_market = str('%.2f' % df_index['change'][i])
        open_market = str('%.4f' % df_index['open'][i])
        preclose = str('%.4f' % df_index['preclose'][i])
        close = str('%.4f' % df_index['close'][i])
        high = str('%.4f' % df_index['high'][i])
        low = str('%.4f' % df_index['low'][i])
        volume = str(df_index['volume'][i])
        amount = str('%.4f' % df_index['amount'][i])
        sql_params = [code, name, change_market, open_market, preclose, close, high, low, volume, amount]
        logger.debug(sql_market)
        logger.debug(sql_params)
        # 存入数据库
        execute_sql(conn, sql_market, sql_params)


def get_rate(conn):
    """
    美元汇率查看
    :param conn:
    :return:
    """
    now = datetime.datetime.now()
    current_time = now.strftime("%Y-%m-%d %H:%M:%S")
    stamp_current_time = datetime.datetime.strptime(current_time, '%Y-%m-%d %H:%M:%S')
    c = CurrencyRates()
    c.get_rates('USD')  # 查看美元最新汇率
    stock_price = c.get_rate('USD', 'CNY')  # 人民币汇率
    stock_time = str(current_time)
    stock_name = '人民币汇率'
    stock_applies = None
    spider_data = stamp_current_time
    # 更新美元汇率
    sql_update = """
    UPDATE public.stock_code SET stock_time = %s, spider_data = %s, stock_name= %s, stock_price= %s, stock_applies= %s
    WHERE stock_name = '人民币汇率'
    """
    sql_params = [stock_time, spider_data, stock_name, stock_price, stock_applies]
    logger.debug(sql_update)
    logger.debug(sql_params)
    execute_sql(conn, sql_update, sql_params)


def main():
    conn = None
    try:
        get_code()
        conn = get_conn()
        with conn:
            get_rate(conn)
    finally:
        if conn:
            conn.close()


if __name__ == '__main__':
    main()
