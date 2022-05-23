# import section
import datetime
import json
import os
import pprint
import pymssql
import sys
import timeit
from robot.api import logger
import matplotlib.pyplot as plt
import pandas as pd
import requests
import urllib3
import numpy as np
import csv
import io
import codecs
import logging
import timeit
from pandas.io.excel import ExcelWriter
from matplotlib.ticker import MaxNLocator

# Author Section
# Program Name: GeneralUtilities.py.py                                     
# Created by Keshav at 20/05/22 9:55 p.m.                       

encoding ='utf-8'
urllib3.disable_warnings()
plt.style.use('ggplot')

# Write your code here

# # Replaced by robot.api.logger
# def create_logger():
#     """
#     Creates a logger for this program
#     Returns:
#
#     """
#     log_name = "{}.log".format(os.path.basename(__file__).rsplit('.')[0])
#     global logger
#     logger = logging.getLogger(__name__)
#     current_working_directory = os.getcwd()
#     logger.setLevel(logging.INFO)
#     logger_folder_path = os.path.join(current_working_directory, 'Scripts/log')
#     logger_folder_path = os.path.abspath(logger_folder_path)
#     print(logger_folder_path)
#     if not os.path.exists(logger_folder_path):
#         os.makedirs(logger_folder_path)
#
#     log_file_path = os.path.join(logger_folder_path, log_name)
#     handler = logging.FileHandler(log_file_path)
#     handler.setLevel(logging.INFO)
#     formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
#     handler.setFormatter(formatter)
#     logger.addHandler(handler)

def timer(fn):
    """
    This is the timer decorator that can provide the elapsed time of each function passed as argument
    Args:
        fn:

    Returns:

    """

    def inner(*args, **kwargs):
        start_time = timeit.default_timer()
        logger.info("Started: {}".format(fn.__name__))
        to_execute = fn(*args, **kwargs)
        end_time = timeit.default_timer()
        execution_time = end_time - start_time
        logger.info("Completed: {}".format(fn.__name__))
        logger.info("{0} took {1}s to execute".format(fn.__name__, execution_time))
        return to_execute

    return inner

# No more changes needed
def get_current_timestamp():
    """
    Returns current timestamp
    Returns:

    """
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    return str(timestamp)

def get_current_date_yyyymdd():
    currdate = datetime.datetimte.now().strftime('%Y%m%d')
    return str(currdate)


def generate_oauth_token(environment, auth_code, scope_value):
    """
    This function will return the oauth token required to access APIs
    Args:
        environment:
        auth_code:
        scope_value:

    Returns: Bearer Token

    """
    client_id_value = r'1234-5678-9101112-13141516'
    client_secret_value = r'RsomerandomvalueStringwithrandomlettersandrandomnumbers'
    if environment in ('DEV', 'SIT'):
        oauth_url = "https://url.company.com/as/token.oauth2"
        dict_data =  {
            r'client_id' : r'{}'.format(client_id_value),
            r'client_secret': r'{}'.format(client_secret_value),
            r'grant_type': r'client_credentials',
            r'scope': r'{}'.format(scope_value),
        }
        r = requests.post(oauth_url, data = dict_data)

    dict_token = r.json()
    access_token = dict_token.get('access_token',"{}".format(r.json()))
    return access_token

# No more changes needed
@timer
def query_sql_server(db_host, db_port, db_name, db_user_id, db_password, sql_stmt, output_file_path, delimiter="|",
                     header_flag=True):
    """
    Executes the SQL Select Query on the Microsoft SQL Server Database and writes the result set into a delimited file
    Args:
        db_host:
        db_port:
        db_name:
        db_user_id:
        db_password:
        sql_stmt:
        output_file_path:
        delimiter:
        header_flag: True means header will be written; False means only the data will be written.

    Returns:

    """

    output_file_path = os.path.abspath(output_file_path)
    with pymssql.connect(host=db_host, port=db_port, user=db_user_id, password=db_password, database=db_name) as conn:
        cursor = conn.cursor()
        cursor.execute(sql_stmt)

        if os.path.exists(output_file_path):
            os.remove(output_file_path)

        with codecs.open(output_file_path, 'wb', encoding='utf-8') as fout:
            csvwriter = csv.writer(fout, delimiter=delimiter, quoting=csv.QUOTE_MINIMAL)
            if header_flag:
                column_names = [item[0] for item in cursor.description]
                csvwriter.writerow(column_names)

            for row in cursor:
                try:
                    columns = [str(column or '') for column in row]
                    # csvwriter.writerow(columns)
                    out_rec = delimiter.join(columns)
                    fout.write(u"{}\n".format(out_rec))
                except UnicodeEncodeError:
                    logger.error("Unicode Encode Error: Skipping this record: {}".format(row))

    return output_file_path


def query_single_value_from_table(db_host, db_port, db_name, db_user_id, db_password, sql_stmt):
    """
    Query Single value like count etc from a table
    Args:
        db_host:
        db_port:
        db_name:
        db_user_id:
        db_password:
        sql_stmt:

    Returns:

    """
    with pymssql.connect(host=db_host, port=db_port, user=db_user_id, password=db_password, database=db_name) as conn:
        cursor = conn.cursor()
        cursor.execute(sql_stmt)
        for row in cursor:
            column_value = row[0].strip()

    return column_value

@timer
def merge_files_into_excel_sheets(output_excel_file_path, delimiter, *args):
    """
    Merges multiple delimited files provided as *args into one excel workbook
    Args:
        output_excel_file_path:
        delimiter:
        *args:

    Returns:

    """
    with ExcelWriter(output_excel_file_path) as excel_writer:
        for i, input_csv in enumerate(args, start=1):
            input_csv = os.path.abspath(input_csv)
            df = pd.read_csv(input_csv, sep=delimiter, na_filter=False, low_memory=False)
            excel_sheet_name = os.path.basename(input_csv).rsplit('.')[0]
            excel_sheet_name = '{}_{}'.format(i, excel_sheet_name)[:31]
            df.to_excel(excel_writer, sheet_name=excel_sheet_name, index=False)
            logger.info("Added {}  to {}".format(input_csv, output_excel_file_path))


if __name__ == '__main__':
    pass
