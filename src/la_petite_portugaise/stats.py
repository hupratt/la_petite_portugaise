
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import locale
import re
import time
import os
import pandas as pd
import psycopg2
import logging
from base64 import b64decode
import json


def setLogger():
    os.chdir("/var/log/apache2/")
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    # create a file handler
    handler = logging.FileHandler('ip_local_error.log')
    handler.setLevel(logging.INFO)
    # create a logging format
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    # add the handlers to the logger
    logger.addHandler(handler)
    return logger


def create_connection_postgres_lpp():
    try:
        connection = psycopg2.connect(user=os.environ.get('dbuser'),
                                      password=os.environ.get('dbpassword'),
                                      host=os.environ.get('hostipdev'),
                                      port=os.environ.get('pnumber'),
                                      database=os.environ.get('dbname'))
        cursor = connection.cursor()
    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
    return cursor, connection


def create_connection_postgres_pbots():
    try:
        connection = psycopg2.connect(user=os.environ.get('dbuser_pbots'),
                                      password=os.environ.get(
            'dbpassword_pbots'),
            host=os.environ.get('hostipdev'),
            port=os.environ.get('pnumber'),
            database=os.environ.get('dbname_pbots'))
        cursor = connection.cursor()
    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
    return cursor, connection


def grab_sessions(c, conn):
    try:
        dic = {}
        c.execute(
            'SELECT session_data FROM django_session')
        for i, item in enumerate(c.fetchall()):
            decoded = b64decode(item[0]).decode("utf-8")
            hey = decoded[decoded.find(':')+1:]
            # print(decoded, type(decoded))
            # print(json)
            # json_ = json.dumps(hey)
            json_ = json.loads(hey)
            dic[i] = json_
        for key, value in dic.items():
            for k, v in value.items():
                if k == 'client_address':
                    print(v)
    except (Exception, psycopg2.Error) as error:
        print(error)
        logger.error('Database Error on write')
        logger.error(error)
    # closing database connection.
    if(conn):
        c.close()
        conn.close()
        print("PostgreSQL connection is closed")


c, conn = create_connection_postgres_lpp()
grab_sessions(c, conn)
