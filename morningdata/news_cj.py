#!/usr/bin/env python3.4
# encoding: utf-8
"""
Created on 17-12-11

@author: Xu
"""
import time
import datetime
import config
import re
import logging.config

from bs4 import BeautifulSoup
from selenium import webdriver
from common.pgutils import get_conn, execute_sql, execute_select
from lxml import etree
from config import logger_path
from xvfbwrapper import Xvfb


logging.config.fileConfig(logger_path)
logger = logging.getLogger("root")

sql_cj = "INSERT INTO news_cj(news_date, spider_data, news_source, news_type, news) VALUES(%s, %s, %s, %s, %s)"

chromedriver_path = config.get_config("chromedriver", "chromedriver_path")
html_path = config.get_config("htmlpath", "html_path")


def get_news(conn, max_date, current_time):
    """
    华尔街见闻抓取
    :param conn:
    :param max_date: 数据库中最新新闻的日期
    :param current_time: 当前时间
    :return:
    """
    func_name = "采集华尔街见闻"
    logger.info('start %s ' % func_name)
    spider_data = datetime.datetime.strptime(current_time, '%Y-%m-%d %H:%M:%S')
    driver = None
    try:
        xvfb = Xvfb(width=1280, height=720)
        xvfb.start()
        driver = webdriver.Firefox(executable_path=chromedriver_path)
        driver.get('https://wallstreetcn.com/live/global')
        # 让页面滚动到下面,window.scrollBy(0, scrollStep),ScrollStep ：间歇滚动间距
        js = 'window.scrollBy(0,3000)'
        driver.execute_script(js)
        time.sleep(5)
        js = 'window.scrollBy(0,60000)'
        driver.execute_script(js)
        time.sleep(5)
        pages = driver.page_source
        soup = BeautifulSoup(pages, 'html.parser')
        soup1 = soup.find('div', class_='livenews')
        content = soup1.find_all('div', class_='live-item')
        news_source = '华尔街见闻'
        news_type = '宏观'
        last_news_time = '23:59'
        d_date = datetime.datetime.strptime(current_time, '%Y-%m-%d %H:%M:%S')
        for cont in content:
            news_time = cont.find('span', attrs={'class': 'live-item__time__text'}).get_text()
            news = cont.find('span', attrs={'class': 'content-html'})
            if news is None:
                return
            news = news.get_text().strip().replace('//', '')
            if last_news_time < news_time:
                d_date = d_date - datetime.timedelta(days=1)
            s_date = d_date.strftime("%Y-%m-%d")
            over_time = s_date + ' ' + news_time
            if max_date > over_time:
                break
            sql_params = [over_time, spider_data, news_source, news_type, news]
            logger.debug(sql_cj)
            logger.debug(sql_params)
            execute_sql(conn, sql_cj, sql_params)
            last_news_time = news_time
        logger.info('end %s ' % func_name)
    finally:
        if driver:
            # driver.close()
            driver.quit()
            xvfb.stop()


def get_sina_news(conn, max_date, current_time):
    """
    爬取新浪财经突发live板块新闻
    :param conn:
    :param max_date: 数据库中最新新闻的日期
    :param current_time: 当前时间
    :return:
    """
    func_name = "采集新浪财经新闻"
    logger.info('start %s ' % func_name)
    spider_data = datetime.datetime.strptime(current_time, '%Y-%m-%d %H:%M:%S')
    driver = None
    try:
        xvfb = Xvfb(width=1280, height=720)
        xvfb.start()
        driver = webdriver.Firefox(executable_path=chromedriver_path)
        for num in range(1, 2):
            # url = 'http://live.sina.com.cn/zt/app_zt/f/v/finance/globalnews1/?page=' + str(num)
            url = 'http://finance.sina.com.cn/7x24/'
            driver.get(url)
            # 让页面滚动到下面,window.scrollBy(0, scrollStep),ScrollStep ：间歇滚动间距
            js = 'window.scrollBy(0,3000)'
            driver.execute_script(js)
            time.sleep(5)
            js = 'window.scrollBy(0,5000)'
            driver.execute_script(js)
            time.sleep(5)
            pages = driver.page_source
            xml = etree.HTML(pages)
            time_list = xml.xpath('//*[@class="bd_c0"]/div[@class="bd_list"]/div["bd_i"]/@data-time')
            soup = BeautifulSoup(pages, 'html.parser')
            save_file(soup.encode('utf-8'))
            soup1 = soup.find('div', id='liveList01')
            content = soup1.select('.bd_i')
            news_source = '新浪财经'
            for i in range(len(time_list)):
                time_stamp = time_list[i]
                data = content[i]
                over_time_1 = data.find('p', attrs={'class': 'bd_i_time_c'}).get_text()
                over_time = time_stamp + over_time_1
                over_time_d = datetime.datetime.strptime(over_time, "%Y%m%d%H:%M:%S")
                over_time = datetime.datetime.strftime(over_time_d, "%Y-%m-%d %H:%M:%S")
                if max_date <= over_time:
                    # data_type = data.find('p', attrs={'class': 'bd_i_tags'}).get_text().strip().replace("\n", "")
                    # news_type = data_type.replace(' ', '')
                    news_type = ''
                    try:
                        message = data.find('p', attrs={'class': 'bd_i_txt_c'}).get_text()
                        mes = re.sub(r"http(.*)", '', message)
                        news = re.sub('\s$', '', mes)
                    except Exception as e:
                        logger.error(e)
                    sql_params = [over_time, spider_data, news_source, news_type, news]
                    logger.debug(sql_cj)
                    logger.debug(sql_params)
                    execute_sql(conn, sql_cj, sql_params)
                else:
                    return
        logger.info('end %s ' % func_name)
    finally:
        if driver:
            # driver.close()
            driver.quit()
            xvfb.stop()


def save_file(data):
    n = datetime.datetime.now()
    s_date = n.strftime("%Y%m%d")
    save_path = html_path + s_date + '_sina.txt'
    f_obj = open(save_path, 'wb')  # wb 表示打开方式,也可用w
    f_obj.write(data)
    f_obj.close()


def main():
    now = datetime.datetime.now()
    current_time = now.strftime("%Y-%m-%d %H:%M:%S")
    one_day = now - datetime.timedelta(days=1)
    one_day_ago = one_day.strftime('%Y-%m-%d %H:%M:%S')[:16]
    history_day = (now - datetime.timedelta(days=10)).strftime('%Y-%m-%d %H:%M:%S')[:16]
    conn = None
    try:
        conn = get_conn()
        with conn:
            sql_max_date = """
                SELECT max(CASE WHEN news_source='新浪财经' THEN news_date END),
                    max(CASE WHEN news_source='华尔街见闻' THEN news_date END)
                FROM news_cj
            """
            res = execute_select(conn, sql_max_date)
            max_date_sina = res[0][0] if res[0][0] else one_day_ago
            max_date_news = res[0][1] if res[0][1] else one_day_ago
            sql_delete = """
                DELETE FROM news_cj
                WHERE news_date <= %s  
                    OR (news_source='华尔街见闻' AND news_date=%s) OR (news_source='新浪财经' AND news_date=%s)
            """
            execute_sql(conn, sql_delete, (history_day, max_date_news, max_date_sina))
            get_news(conn, max_date_news, current_time)
            get_sina_news(conn, max_date_sina, current_time)
    except Exception as e:
        logger.error(str(e))
    finally:
        if conn:
            conn.close()


if __name__ == '__main__':
    main()
