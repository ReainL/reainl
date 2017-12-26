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
    大盘指数行情数据获取 可获得上证指数、深证指数
    :return:
    """
    engine = create_engine(code_engine)
    df_index = ts.get_index()
    logger.info(df_index)
    # 存入数据库
    df_index.to_sql('middle_news_market', engine, schema='public', if_exists='replace')


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
