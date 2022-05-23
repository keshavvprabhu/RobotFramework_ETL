# import section
import jaydebeapi
import jpype
import os
import sys
import csv
import codecs
from robot.api import logger
import timeit


# Author Section
# Program Name: db2_utilities.py                                     
# Created by Keshav at 23/05/22 4:04 a.m.                       


# Write your code here
def query_zos_db2_database(hostname, port, database, user_name, password, sql_stmt, output_file_path, delimiter="|", header_flag=True):
    """
    Function to connect to DB2 Database on a zOS mainframe
    Args:
        hostname:
        port:
        database:
        user_name:
        password:
        sql_stmt:
        output_file_path:
        delimiter:
        header_flag:

    Returns:

    """
    curr_dir = os.getcwd()
    jar_file_path = "{}/../drivers/db2jcc/db2jcc.jar".format(curr_dir)
    jar_file_path = os.path.abspath(jar_file_path)
    if not os.path.exists(jar_file_path):
        logger.error("File Not Found : {}".format(jar_file_path))
        raise SystemExit("DB2 Driver not found")

    list_credentials = list()
    list_credentials.append(user_name)
    list_credentials.append(password)
    jdbc_conn_str = "jdbc:db2://{0}:{1}/{2}".format(hostname, port, database)

    with jaydebeapi.connect('com.ibm.db2.jcc.DB2Driver', jdbc_conn_str, list_credentials, jar_file_path) as conn:
        cursor = conn.cursor()
        cursor.execute(sql_stmt)
        if os.path.exists(output_file_path):
            os.remove(output_file_path)

        with codecs.open(output_file_path, 'wb', encoding='utf-8') as fout:
            csvwriter = csv.writer(fout, delimiter=delimiter, quoting=csv.QUOTE_MINIMAL)
            if header_flag is True or header_flag=='True':
                if sys.version_info.major ==2:
                    column_names = [item[0].endode('utf-8') for item in cursor.description]
                    logger.info(column_names)
                else:
                    column_names = [item[0] for item in cursor.description]

                csvwriter.writerow(column_names)

            for row in cursor.fetchall():
                try:
                    if sys.version_info.major == 2:
                        columns = [uncode(column or '') for column in row]
                    else:
                        columns = [str(column or '') for column in row]

                    out_rec = delimiter.join(columns)
                    fout.write(u"{}\n".format(out_rec))
                except UnicodeEncodeError:
                    logger.error("UnicodeEncodeError: Skipping the record : {}".format(row))


def query_as400_db2_database(hostname, port, database, user_name, password, sql_stmt, output_file_path, delimiter="|",
                           header_flag=True):
    """
    Function to connect to DB2 Database on a zOS mainframe
    Args:
        hostname:
        port:
        database:
        user_name:
        password:
        sql_stmt:
        output_file_path:
        delimiter:
        header_flag:

    Returns:

    """
    curr_dir = os.getcwd()
    jar_file_path = "{}/../drivers/jt400/jt400.jar".format(curr_dir)
    jar_file_path = os.path.abspath(jar_file_path)
    if not os.path.exists(jar_file_path):
        logger.error("File Not Found : {}".format(jar_file_path))
        raise SystemExit("DB2 Driver not found")

    list_credentials = list()
    list_credentials.append(user_name)
    list_credentials.append(password)
    jdbc_conn_str = "jdbc:as400://{0};prompt=false;translate binary=true;naming=system".format(hostname)

    with jaydebeapi.connect('com.ibm.as400.access.AS400JDBCDriver', jdbc_conn_str, list_credentials, jar_file_path) as conn:
        cursor = conn.cursor()
        cursor.execute(sql_stmt)
        if os.path.exists(output_file_path):
            os.remove(output_file_path)

        with codecs.open(output_file_path, 'wb', encoding='utf-8') as fout:
            csvwriter = csv.writer(fout, delimiter=delimiter, quoting=csv.QUOTE_MINIMAL)
            if header_flag is True or header_flag == 'True':
                if sys.version_info.major == 2:
                    column_names = [item[0].endode('utf-8') for item in cursor.description]
                    logger.info(column_names)
                else:
                    column_names = [item[0] for item in cursor.description]

                csvwriter.writerow(column_names)

            for row in cursor.fetchall():
                try:
                    if sys.version_info.major == 2:
                        columns = [uncode(column or '') for column in row]
                    else:
                        columns = [str(column or '') for column in row]

                    out_rec = delimiter.join(columns)
                    fout.write(u"{}\n".format(out_rec))
                except UnicodeEncodeError:
                    logger.error("UnicodeEncodeError: Skipping the record : {}".format(row))


if __name__ == '__main__':
    pass
