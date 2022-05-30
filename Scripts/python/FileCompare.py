# import section
import codecs
import csv
import gc
import glob
# import logging
import os
import sqlite3
import sys
import timeit
from datetime import datetime
from sqlite3 import Error
import numpy as np
import pandas as pd
from robot.api import logger
# import cx_Oracle


# Author Section
# Program Name: FileCompare.py
# Created by Keshav Prabhu at 08/05/2018 8:53 p.m.


def timer(fn):
    """
    This is the timer decorator that can provide the elapsed time of each function
    Args:
        fn:

    Returns:

    """

    def inner(*args, **kwargs):
        start_time = timeit.default_timer()
        print(f"Started: {fn.__name__}")
        to_execute = fn(*args, **kwargs)
        end_time = timeit.default_timer()
        execution_time = end_time - start_time
        print(f"Completed: {fn.__name__}() in {execution_time} s. ")
        return to_execute

    return inner


# def create_logger():
#     """
#     Create a Native Logger for this program
#     Returns:
#
#     """
#     log_file_name = f"{os.path.basename(__file__).rsplit(',')[0]}.log"
#     global logger
#     logger = logging.getLogger(__name__)
#     current_working_directory = os.getcwd()
#     logger.setLevel(logging.INFO)
#     logger_folder_path = os.path.join(current_working_directory, 'Scripts/log')
#     logger_folder_path = os.path.abspath(logger_folder_path)
#
#     if not os.path.exists(logger_folder_path):
#         os.makedirs(logger_folder_path)
#
#     log_file_path = os.path.join(logger_folder_path, log_file_name)
#
#     handler = logging.FileHandler(log_file_path)
#     handler.setLevel(logging.INFO)
#     formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
#     handler.setFormatter(formatter)
#     logger.addHandler(handler)

@timer
def prepare_files(dict_configuration, switch):
    """
    Prepares the files provided for FileComparison Utility. The source and target files provided are transformed in
    this function.
    Args:
        dict_configuration: This isa configuration dictionary that is created by reading the configuration files
        switch: This parameter has two possible values 'source' and 'target'

    Returns: temp_file_path

    """
    switch = switch.lower()
    file_path = os.path.abspath(dict_configuration['()_file_path'.format(switch)])
    folder_path = os.path.dirname(file_path)
    file_name = os.path.basename(file_path)
    temp_file_name = "{}_{}".format(switch, file_name)
    temp_file_path = os.path.join(folder_path, temp_file_name)
    file_delimiter = dict_configuration['{}_file_delimiter'.format(switch)]
    key_columns = dict_configuration['key_columns']
    result_delimiter = dict_configuration['result_delimiter']
    list_key_indices = []
    ignore_columns = dict_configuration['ignore_columns']
    list_comparable_indices = []
    list_header = []

    with codecs.open(file_path, 'rb', encoding='utf-8') as fin, \
            codecs.open(temp_file_path, 'wb', encoding='utf-8') as fout:
        csvreader = csv.reader(fin, delimter=file_delimiter)
        r = 1

        for idx, record in enumerate(csvreader, start=1):
            if idx == 1:
                list_header = record
                list_header_cols = list(range(len(list_header)))
                list_key_indices = [list_header.index(i) for i in key_columns]
                if ignore_columns not in (list(), ['']):
                    list_ignore_indices = [list_header.index(i) for i in ignore_columns]
                else:
                    list_ignore_indices = []

                list_non_key_indices = [item for item in list_header_cols if item not in list_key_indices]
                list_comparable_indices = [item for item in list_non_key_indices if item not in list_ignore_indices]
            else:
                list_record = record
                list_file_keys = [list_record[i] for i in list_key_indices]
                str_file_keys = result_delimiter.join(list_file_keys)

                for i in list_comparable_indices:
                    if r == 1:
                        temp_header = "{1}{0}{2}{0}{3}".format(result_delimiter,
                                                               result_delimiter.join([k for k in key_columns]),
                                                               'column_name',
                                                               "{}_value".format(switch))
                        fout.write(temp_header + '\n')
                        r += 1
                        column_name = list_header[i].strip()
                        try:
                            column_value = list_record[i]
                        except Exception as e:
                            temp_record = "{1}{0}{2}{0}{3}".format(result_delimiter, str_file_keys,
                                                                   column_name, column_value)
                            logger.error(e)
                            raise RuntimeError(temp_record)

                    try:
                        if sys.version_info.major == 2:
                            temp_record = u"{1}{0}{2}{0}{3}".format(result_delimiter, str_file_keys, column_name,
                                                                    column_value)
                        else:
                            temp_record = "{1}{0}{2}{0}{3}".format(result_delimiter, str_file_keys, column_name,
                                                                   column_value)

                        fout.write("{}{}".format(temp_record, "\n"))
                    except Exception as e:
                        logger.error(e)
                        raise RuntimeError("Unknown Python Version: {}".format(str(sys.version_info)))

    return temp_file_path


@timer
def verify_file_existence(switch, file_path):
    """
    Verifies the existence of a file. This is used to do some initial verifications of the details specified in the
    configuration provided as an input to the compare_files() function.
    Args:
        switch: can contain value 'source' or 'target'
        file_path: is the actual file path

    Raises: FileNotFoundError if the file is not found or does not exist
    Returns:

    """
    file_path = os.path.abspath(file_path)
    if not os.path.exists(file_path):
        # logger.ERROR("ERROR: '{}' : '{}' does not exist".format(switch, file_path))
        raise FileNotFoundError("ERROR: '{}' : '{}' does not exist".format(switch, file_path))


@timer
def retrieve_file_header_as_set(file_path, file_delimiter):
    """
    Retrieves the file header and the retrieved file header is stored as a set.
    Doing so eliminates duplicate attributes, if any.
    Args:
        file_path:
        file_delimiter:

    Returns:

    """
    set_file_header = set()
    file_path = os.path.abspath(file_path)
    with codecs.open(file_path, 'rb', encoding='utf-8') as fin:
        for i, record in enumerate(fin, start=1):
            record = record.strip()
            if i == 1:
                set_file_header = set(record.split(file_delimiter))
    return set_file_header


@timer
def verify_file_columns(file_path, file_delimiter, file_columns):
    """
    Verifies whetherthe columns provided in the config file are actually contained in the file. If the columns are not
    presetn then the function will log the difference observed and raise a RuntimeError
    Args:
        file_path:
        file_delimiter:
        file_columns:
    Raises: RuntimeError if the column provided in the config file cannot be found in the file
    Returns:

    """
    set_file_header = retrieve_file_header_as_set(file_path, file_delimiter)
    set_file_columns = set(file_columns)
    if set_file_columns.symmetric_difference(set_file_header) != set():
        logger.error("ERROR: '{}' : file_header and file_columns do not match".format(file_path))
        logger.error("file_header = {}".format(sorted(set_file_header)))
        logger.error('file_column = {}'.format(sorted(set_file_columns)))
        diff_col = set_file_header - set_file_columns
        logger.error("Differences: {}".format(list(diff_col)))
        raise RuntimeError


@timer
def verify_imp_columns(file_path, file_delimiter, imp_columns):
    """
    Verifies whether the important columns such as Key Columns and Ignore Columns are actually present in the file. If
    the important columns are not present in the file header then the function will log the difference observed and
    raise a RuntimeError

    Args:
        file_path:
        file_delimiter:
        imp_columns:
    Raises: RuntimeError if the key columns and ignore columns are not found in the file.
    Returns:

    """
    set_file_header = retrieve_file_header_as_set(file_path, file_delimiter)
    set_imp_columns = set(imp_columns)
    if set_imp_columns.issubset(set_file_header):
        pass
    else:
        logger.error("ERROR: '{}': key_columns could not be found in the file_header")
        logger.error("file_header = {}".format(sorted(set_file_header)))
        logger.error("file_column = {}".format(sorted(set_imp_columns)))
        diff_col = set_imp_columns - set_file_header
        logger.error("Difference observed: {}".format(list(diff_col)))
        raise RuntimeError("ERROR: '{}': key_columns could not be found in the file_header")


@timer
def verify_configuration(dict_configuration, switch):
    """
    Verifies the correctness of the configuration values used by the FileCompare Utility.
    Args:
        dict_configuration:
        switch:

    Returns:

    """
    file_path = dict_configuration['{}_file_path'.format(switch)]
    file_columns = dict_configuration['{}_file_columns'.format(switch)]
    file_delimiter = dict_configuration['{}_file_delimiter'.format(switch)]
    key_columns = dict_configuration['key_columns']
    ignore_columns = dict_configuration['ignore_columns']
    verify_file_existence('{}_file_path'.format(switch), file_path)
    verify_file_columns(file_path, file_delimiter, file_columns)
    verify_imp_columns(file_path, file_delimiter, key_columns)
    if ignore_columns not in (list(), ['']):
        verify_imp_columns(file_path, file_delimiter, ignore_columns)


@timer
def compare_file_headers(dict_configuration):
    """
    Compares the file headers between source and target files. This feature is enabled only if the flag is set to true
    in the configuration file. If the 'compare_file_headers' value is set to False then the File compare utility will
    ignore the order of the columns in the file but still compare the values.
    Args:
        dict_configuration:
    Raises: RuntimeError if the file headers do not match
    Returns:

    """
    source_file_path = dict_configuration['source_file_path']
    target_file_path = dict_configuration['target_file_path']
    source_file_delimiter = dict_configuration['source_file_delimiter']
    target_file_delimiter = dict_configuration['target_file_delimiter']
    source_header = get_file_header(source_file_path, source_file_delimiter)
    target_header = get_file_header(target_file_path, target_file_delimiter)
    if dict_configuration.get('compare_file_headers', 'False') in ('True', True, 'True'.lower(), 'True'.upper()):
        if source_header != target_header:
            logger.error("Source File Header and Target File Header do not match")
            logger.error("Source File Header: {}".format(source_header))
            logger.error("Target File Header: {}".format(target_header))
            raise RuntimeError("Source File Header and Target File Header do not match")


@timer
def file_record_count(input_file_path):
    """
    Get the record count in the input file provided
    Args:
        input_file_path:

    Returns: Record Count (integer)

    """

    input_file_path = os.path.abspath(input_file_path)
    with codecs.open(input_file_path, 'rb', encoding='utf-8') as f:
        for i, l in enumerate(f):
            pass
    return i


@timer
def create_stats_report(dict_configuration, config_file_path):
    """
    Creates the File Compare Statistics Report. This is the report that contains the details that gets written
    into the File Comparison Summary HTML Report and is also the place were we can insert the comparison summary
    into a database of our choice and have tableau reporting established over it.
    Args:
        dict_configuration:
        config_file_path:

    Returns: record

    """

    source_file_path = os.path.abspath(dict_configuration['source_file_path'])
    target_file_path = os.path.abspath(dict_configuration['target_file_path'])
    result_file_path = os.path.abspath(dict_configuration['result_file_path'])
    result_folder_path = os.path.dirname(result_file_path)
    result_stats_file_path = os.path.abspath(dict_configuration['result_stats_file_path'])
    result_delimiter = dict_configuration['result_delimiter']

    list_header = ('TestEnvironment', 'TestName', 'SourceFileName', 'TargetFileName',
                   'DetailedResultFileName', 'SourceRecordCount', 'TargetRecordCount',
                   'MismatchedRecordCount', 'MissingInSourceRecordCount', 'MissingInTargetRecordCount',
                   'PassPercent', 'TestResult', 'InsertedTimeStamp', 'RunDate', 'MachineName',
                   'UserName')
    header = result_delimiter.join(list_header).upper()

    if os.path.exists(result_stats_file_path):
        pass
    else:
        with codecs.open(result_stats_file_path, 'wb', encoding='utf-8') as fout:
            fout.write("{}\n".format(header))

    if os.path.exists(result_file_path):
        with codecs.open(result_file_path, 'rb', encoding='utf-8') as fin:
            list_result_key_columns = []
            value_mismatch_counter = 0
            source_missing_counter = 0
            target_missing_counter = 0
            for i, rec in enumerate(fin):
                rec = rec.strip()
                if i > 1:
                    result_columns = rec.split(result_delimiter)
                    result_key_columns = result_columns[:-4]
                    str_result_category = result_columns[-1]
                    result_key_columns.append(str_result_category)
                    str_result_key_columns = result_delimiter.join(result_key_columns)
                    list_result_key_columns.append(str_result_key_columns)
            set_result_key_columns = set(list_result_key_columns)
            list_set_result_columns = list(set_result_key_columns)

            for item in list_set_result_columns:
                list_mismatch = item.split(result_delimiter)
                if list_mismatch[-1] == 'Value_Mismatch':
                    value_mismatch_counter += 1
                if list_mismatch[-1] == 'Missing_in_Source':
                    source_missing_counter += 1
                if list_mismatch[-1] == 'Missing_in_Target':
                    target_missing_counter += 1

            source_record_count = file_record_count(source_file_path)
            target_record_count = file_record_count(target_file_path)

            if int(source_record_count) >= int(target_record_count):
                divisor = source_record_count
            else:
                divisor = target_record_count

            # Calculate Pass Percent
            # Formula = 100 - (x*100 / total records in source)
            pass_percentage = 0.0

            disjoint = False

            total_mismatches = int(value_mismatch_counter) + int(source_missing_counter) + int(target_missing_counter)

            if value_mismatch_counter == 0 and int(source_missing_counter) == 0 and int(target_missing_counter) == 0:
                pass_percentage = 100.00
            elif source_record_count == target_missing_counter and target_record_count == source_missing_counter:
                pass_percentage = 0.0
                disjoint = True
            else:
                pass_percentage = float(100) - float(total_mismatches) * 100 / float(divisor)
                pass_percentage = abs(float(pass_percentage))
                if pass_percentage > 100.00:
                    pass_percentage = 'Error'
                else:
                    pass_percentage = "{:3.2f}".format(pass_percentage)

            record = list()

            if value_mismatch_counter == 0 and source_missing_counter == 0 and target_missing_counter == 0:
                test_result = 'PASS'
            elif disjoint:
                test_result = 'FAIL(DISJOINT)'
            else:
                test_result = 'FAIL'

            obj_date_time = datetime.now()
            str_timestamp = obj_date_time.strftime("%Y-%m-%d %h:%M:%S.%f")
            record.append(dict_configuration.get('test_environment', ''))
            record.append(dict_configuration.get('test_name', ''))
            record.append(os.path.basename(source_file_path))
            record.append(os.path.basename(target_file_path))
            record.append(os.path.basename(result_file_path))
            record.append(str(source_record_count))
            record.append(str(target_record_count))
            record.append(str(value_mismatch_counter))
            record.append(str(source_missing_counter))
            record.append(str(target_missing_counter))
            record.append("{}%".format(str(pass_percentage)))
            record.append(str(test_result))
            record.append(str_timestamp)
            run_date = obj_date_time.strftime("%Y-%m-%d")
            record.append(run_date)
            computer_name = str(os.environ.get('COMPUTERNAME', 'UNKNOWN').upper())
            record.append(computer_name)
            user_name = str(os.environ.get('USERNAME', 'UNKNOWN').upper())
            record.append(user_name)

            dict_record = dict(zip(list_header, record))

            df_comparison_summary = pd.DataDrame(dict_record.items())

            # Commenting out the comparison summary html file path to reduce file clutters in th result folderPath
            # This feature will need to be added later and auto-uploaded to JIRA
            # comparison_summary_html_file_name = "{}_Test_Summary.html".format(
            #     dict_configuration.get('test_name', 'TestNameNotProvided'))
            # comparison_summary_html_file_path = os.path.join(result_folder_path, comparison_summary_html_file_name)
            # print("Comparison Summary HTML FIle: {}".format(comparison_summary_html_file_path)
            # df_comparison_summary.to_html(comparison_summary_html_file_path, header=False, index=False, justify='right')
            with codecs.open(result_stats_file_path, 'a', encoding='utf-8') as fout:
                str_record = result_delimiter.join(record)
                fout.write("{}\n".format(str_record))
    else:
        logger.error("ERROR: {} does not exist".format(result_file_path))
        raise RuntimeError

    # Delate the comparison report if there are no mismatches to avoid
    # the clutter of having to look through all the comparison result files
    if test_result == 'PASS':
        logger.info("Removing the result file: {}".format(os.path.basename(result_file_path)))
        os.remove(result_file_path)

        logger.info("Removing the index and tables in sqlite database to conserve Disk Space")
        table_name = os.path.basename(config_file_path).rsplit('.', 1)[0]
        source_table_name = "source_{}".format(table_name)
        target_table_name = "target_{}".format(table_name)
        drop_index_and_table(dict_configuration, source_table_name)
        drop_index_and_table(dict_configuration, target_table_name)

    create_detailed_mismatch_report_html("Data Comparison Summary Report", result_stats_file_path,
                                         result_delimiter)

    logger.info("\n\n")
    logger.info("COMPARISON RESULT".center(100, '-'))
    logger.info(df_comparison_summary.to_string(index=False, header=False))
    logger.info("-" * 100)
    logger.info("\n\n")

    if test_result == "PASS":
        logger.info("There are no mismatches")

    if os.path.exists(result_file_path):
        create_detailed_mismatch_report_html(os.path.basename(result_file_path), result_file_path,
                                             result_delimiter)
        get_attribute_mismatch_stats(result_file_path, result_delimiter)

    return record


@timer
def prepare_dict_config(config_file_path):
    """
    Reads the configuration file and creates a dictionary of configuration values that  can be subsequently used
    by other functions within the FileCompare Utility
    Args:
        config_file_path:

    Returns: dict_config - This is a dictionay representation of the configuration values

    """

    # my_name = "prepare_dict_config()"
    # st = timeit.default_timer()
    # logger.info("Entered: {}".format(my_name))

    if not os.path.exists(config_file_path):
        logger.error("ERROR: {} does not exist".format(config_file_path))
        raise FileNotFoundError("ERROR: {} does not exist".format(config_file_path))

    list_config = []
    with codecs.open(config_file_path, 'rb', encoding='utf-8') as fin:
        csvreader = csv.reader(fin, delimiter='=')
        for rec in csvreader:
            list_config.append(rec)

    dict_config = dict(list_config)
    result_delimiter = dict_config.get('result_delimiter', '|')
    source_file_delimiter = dict_config['source_file_delimiter']
    target_file_delimiter = dict_config['target_file_delimiter']
    dict_config['ignore_columns'] = dict_config['ignore_columns'].split(result_delimiter)
    dict_config['key_columns'] = dict_config['key_columns'].split(result_delimiter)
    dict_config['source_file_columns'] = dict_config['source_file_columns'].split(source_file_delimiter)
    dict_config['target_file_columns'] = dict_config['target_file_columns'].split(target_file_delimiter)
    return dict_config


@timer
def create_sqlite_database(database_file_path):
    """
    Creates a SQLite Database that will be used by FileCompare Utility. Before we invoke compare_files(config_file_path)
    one must call this function to create a local SQLite Database and the path needs to be included in the Test Setup
    Args:
        database_file_path:

    Returns:

    """
    # debug_flag = True
    # create_logger()

    database_file_path = os.path.abspath(database_file_path)
    if not os.path.exists(database_file_path):
        try:
            with sqlite3.connect(database_file_path):
                logger.info("Database {} created".format(database_file_path))
        except Error as e:
            logger.error("Error while creating SQLite Database: {}".format(database_file_path))
            raise RuntimeError("ERROR: {}".format(e))


@timer
def compare_files(config_file_path):
    """
    This is the starting point of the entire FileCompare utility. This is the function that is invoked from
    Robot Framework or another Python Program. This function takes the configuration file as a parameter.
    The configuration file for File Compare Utility resembles a properties file and you can name it whatever you like.
    Args:
        config_file_path: Supply the path of the config file

    Returns: PASS or FAIL or FAIL (DISJOINT)

    """

    config_file_path = os.path.abspath(config_file_path)
    dict_configurations = prepare_dict_config(config_file_path)
    for i in ['source', 'target']:
        verify_configuration(dict_configurations, i)
    compare_file_headers(dict_configurations)
    source_temp_file = prepare_files(dict_configurations, 'source')
    target_temp_file = prepare_files(dict_configurations, 'target')
    database_file_path = dict_configurations['database_file_path']
    table_name = os.path.basename(config_file_path).rsplit('.', 1)[0]
    source_table_name = 'source_{}'.format(table_name)
    target_table_name = 'target_{}'.format(table_name)
    # source_file_delimiter = dict_configurations['source_file_delimiter']
    # target_file_delimiter = dict_configurations['target_file_delimiter']
    result_delimiter = dict_configurations['result_delimiter']
    load_delimited_file_into_sqlite(dict_configurations, source_table_name, source_temp_file, result_delimiter)
    load_delimited_file_into_sqlite(dict_configurations, target_table_name, target_temp_file, result_delimiter)
    select_stmt = create_comparison_query(source_temp_file, target_temp_file,
                                          result_delimiter, result_delimiter,
                                          source_table_name, target_table_name)
    result_file_path = dict_configurations['result_file_path']
    if os.path.exists(result_file_path):
        os.remove(result_file_path)
    # result_delimiter = dict_configurations['result_delimiter']
    header_flag = True
    query_sqlite_database(database_file_path, select_stmt, result_file_path, result_delimiter, header_flag)

    returned_test_result = create_stats_report(dict_configurations, config_file_path)
    os.remove(source_temp_file)
    os.remove(target_temp_file)
    gc.collect()
    return returned_test_result

@timer
def create_comparison_query(source_file_path, target_file_path, source_delimiter, target_delimiter, source_table,
                            target_table):
    """
    Constructs the comparison query based on teh source and target transformed file headers
    Args:
        source_file_path:
        target_file_path:
        source_delimiter:
        target_delimiter:
        source_table:
        target_table:

    Returns: comparison_query

    """
    source_file_path = os.path.abspath(source_file_path)
    target_file_path = os.path.abspath(target_file_path)
    source_header = get_file_header(source_file_path, source_delimiter)
    target_header = get_file_header(target_file_path, target_delimiter)

    # Safety Checks
    if len(source_header) != len(target_header):
        logger.error("ERROR: Source and target have different number of columns")
        logger.error("Source Header: {}".format(source_delimiter.join(source_header)))
        logger.error("Target Header: {}".format(target_delimiter.join(target_header)))
        raise RuntimeError

    updated_source_header = ["s.{}".format(s) for s in source_header]
    updated_target_header = ["t.{}".format(t) for t in target_header]
    if sys.version_info.major == 2:
        zip_header = zip(updated_source_header, updated_target_header)
    else:
        zip_header = list(zip(updated_source_header, updated_target_header))
    query_join_cond = "\n and ".join(["{} = {}".format(g[0], g[1]) for g in zip_header[:-1]])
    query_part1_attr = ", ".join(["s.{0} as {0}".format(s) for s in source_header[:-1]])
    query_part2_attr = ", ".join(["t.{0} as {0}".format(t) for t in target_header[:-1]])
    comparison_query = """select {0}, s.source_value as source_value, coalesce(t.target_value, '~~Missing~~') as target_value,
case 
    when s.source_value = t.target_value then 'Match'
    when s.source_value != t.target_value then 'Mismatch'
    when s.column_name is null then  'Missing_in_Source'
    when t.column_name is null then 'Missing_in_Target'
    else 'Undefined_Error'
end as mismatch_category
from {1} s left join {2} t on (
\t{3}
) where coalesce(s.source_value,'') != coalesce(t.target_value,'')
union 
select {4}, coalesce(s.source_value, '~~Missing~~') as source_value, t.target_value as target_value,
case 
    when s.source_value = t.target_value then 'Match'
    when s.source_value != t.target_value then 'Value_Mismatch'
    when s.column_name is null then 'Missing_in_Source'
    when t.column_name is null then 'Missing_in_Target'
    else 'Undefined_Error'
end as mismatch_category
from {2} t left join {1} s on (
\t{3}
) where coalesce(s.source_value,'') != coalesce(t.target_value, '');""".format(query_part1_attr,
                                                                               source_table,
                                                                               target_table,
                                                                               query_join_cond,
                                                                               query_part2_attr)
    return comparison_query


@timer
def get_file_header(input_file_path, delimiter):
    """
    read the file and return the header as list of columns
    Args:
        input_file_path:
        delimiter:

    Returns: list_header_columns

    """
    input_file_path = os.path.join(input_file_path)
    with codecs.open(input_file_path, 'rb', encoding='utf-8') as fin:
        csvreader = csv.reader(fin, delimiter=delimiter)
        for i, record in enumerate(csvreader, start=1):
            if i == 1:
                list_header_columns = record
                break
    return list_header_columns


@timer
def execute_sql_stmt_on_sqlite_database(database_file_path, sql_stmt):
    """
    Executes SQL Statement on the FileCompare SQLite Database. If ther is anything wring with the SQL Statement, then
    the error will be written and the FileCompare Utility will end with a RuntimeError
    Args:
        database_file_path:
        sql_stmt:
    Raises: RuntimeError if there is something wrong while trying to execute the sql_stmt

    Returns:

    """
    # my_name = 'execute_sql_stmt_on_sqllite_database()'
    # st = timeit.default_timer()
    # logger.info("Entered: {}".format(my_name))
    database_file_path = os.path.abspath(database_file_path)
    logger.info("Executing: \"{}\" on {}".format(sql_stmt, database_file_path))
    try:
        with sqlite3.connect(database_file_path) as conn:
            cursor = conn.cursor()
            cursor.execute(sql_stmt)
            logger.info("Execution Completed: {}".format(sql_stmt))
    except Error as e:
        # logger.error("ERROR: {}".format(e))
        logger.error("Failed while executing SQL Statement: \n {}".format(sql_stmt))
        raise RuntimeError("ERROR: {}".format(e))


@timer
def query_sqlite_database(database_file_path, select_stmt, output_file_path, delimiter, header_flag):
    """
    Queries the FileCompare SQLite Database and outputs the query result into a file
    Args:
        database_file_path:
        select_stmt:
        output_file_path:
        delimiter:
        header_flag:

    Returns:

    """
    database_file_path = os.path.abspath(database_file_path)
    with sqlite3.connect(database_file_path) as conn:
        conn.text_factory = str
        cursor = conn.cursor()
        if sys.version_info.major == 2:
            sql = select_stmt.encode('utf-8')
        else:
            sql = str(select_stmt)
            logger.info(sql)
        cursor.execute(sql)
        with codecs.open(output_file_path, 'wb', encoding='utf-8') as fout:

            if header_flag:
                if sys.version_info.major == 2:
                    column_names = [item[0].encode('utf-8') for item in cursor.description]
                else:
                    column_names = [str(item[0]) for item in cursor.description]
                header = delimiter.join(column_names)

                fout.write("{}{}".format(header, '\n'))
            for row in cursor:
                try:
                    columns = [column for column in row]
                    fout.write("{}{}".format(delimiter.join(columns), '\n'))
                except UnicodeEncodeError:
                    logger.error("Unicode Encod Error - Skipping this record {}".format(row))


@timer
def bulk_load_file_into_table(database_file_path, table_name, input_file_path, delimiter):
    """
    Bulk load the file into the SQLite Database
    Args:
        database_file_path:
        table_name:
        input_file_path:
        delimiter:

    Returns:

    """
    database_file_path = os.path.abspath(database_file_path)
    input_file_path = os.path.abspath(input_file_path)
    dfs = pd.read_csv(input_file_path, sep=delimiter, na_filter=False, chunksize=1000000, dtype=object,
                      quoting=csv.QUOTE_MINIMAL)
    try:
        with sqlite3.connect(database_file_path) as conn:
            conn.text_factory = str
            for i, df in enumerate(dfs, start=1):
                logger.info("Loading Dataframe Chunk {} of shape {} into {}".format(i, df.shape, table_name))
                df.to_sql(table_name, conn, if_exists='append', index=False)
    except Error as e:
        logger.error("ERROR: {}".format(e))
        raise RuntimeError("ERROR: {}".format(e))


@timer
def generate_create_index_command(table_name, index_name, list_key_columns):
    """
    Generates the create index statement for the table. INdexes are created base dn the key_columns supplied in the
    FileCompare Configuration File. If the key column(s) supplied cannot uniquely identify a record for file compare
    then the utility will raise a RuntimeError

    Args:
        table_name:
        index_name:
        list_key_columns:

    Returns: create index statement

    """
    key_columns = ", ".join(list_key_columns)
    key_columns = "{}, column_name".format(key_columns)
    craete_index_stmt = "create unique index if not exists {0} on {1} ({2});".format(index_name, table_name,
                                                                                     key_columns)
    return craete_index_stmt


@timer
def generate_create_table_command(table_name, list_header_columns):
    """
    Generate the Create Table Command based on the header columns of the File
    Args:
        table_name:
        list_header_columns:

    Returns:

    """
    list_attributes_def = ["{} text".format(col.replace(' ', '_').strip()) for col in list_header_columns]
    table_attributes = "\n, ".join(list_attributes_def)
    create_table_stmt = """create table if not exists {} (\n{}\n);""".format(table_name, table_attributes)
    logger.info(create_table_stmt)
    return create_table_stmt


@timer
def load_delimited_file_into_sqlite(dict_configuration, table_name, input_file_path, delimiter):
    """
    Loads the delimited file into SQLite
    Args:
        dict_configuration:
        table_name:
        input_file_path:
        delimiter:

    Returns:

    """
    table_name = table_name.strip()
    if ' ' in table_name:
        table_name = table_name.replace(' ', '_').strip()

    index_name = "idx_{}".format(table_name)
    database_file_path = dict_configuration['database_file_path']
    database_file_path = os.path.abspath(database_file_path)
    input_file_path = os.path.abspath(input_file_path)
    list_header_columns = get_file_header(input_file_path, delimiter)
    drop_index_stmt = "drop index if exists {};".format(index_name)
    execute_sql_stmt_on_sqlite_database(database_file_path, drop_index_stmt)
    drop_table_stmt = "drop table if exists {};".format(table_name)
    execute_sql_stmt_on_sqlite_database(database_file_path, drop_table_stmt)
    create_table_stmt = generate_create_table_command(table_name, list_header_columns)
    execute_sql_stmt_on_sqlite_database(database_file_path, create_table_stmt)
    bulk_load_file_into_table(database_file_path, table_name, input_file_path, delimiter)
    list_key_columns = dict_configuration['key_columns']
    create_index_stmt = generate_create_index_command(table_name, index_name, list_key_columns)
    execute_sql_stmt_on_sqlite_database(database_file_path, create_index_stmt)


@timer
def drop_index_and_table(dict_configuration, table_name):
    """
    Drops the index and table ifthe comparison was successful and there are no mismatches to report.
    This is done to conserve disk space on the slave machine
    Returns:
    """
    table_name = table_name.strip()
    if ' ' in table_name:
        table_name = table_name.replace(' ', '_').strip()
    index_name = "idx_{}".format(table_name)
    database_file_path = dict_configuration['database_file_path']
    database_file_path = os.path.abspath(database_file_path)
    drop_index_stmt = "drop index if exists {};".format(index_name)
    execute_sql_stmt_on_sqlite_database(database_file_path, drop_index_stmt)
    drop_table_stmt = "drop table if exists {};".format(table_name)
    execute_sql_stmt_on_sqlite_database(database_file_path, drop_table_stmt)


@timer
def create_detailed_mismatch_report_html(page_title, file_path, delimiter):
    """
    Creates the detaile mismatch report html format form teh detailed mismatch report
    Args:
        page_title:
        file_path:
        delimiter:

    Returns:

    """
    # create logger
    folder_path = os.path.dirname(os.path.abspath(file_path))
    file_name = os.path.basename(file_path)
    output = file_name.rsplit(".", 1)
    output_file_path = os.path.join(folder_path, "{}.html".format(output[0]))
    if os.path.exists(output_file_path):
        os.remove(output_file_path)
    partial_flag = False
    message = ''
    _html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset= "UTF-8">
    <title>""" + str(page_title) + """</title> 
    <link rel="stylesheet" href="https://cdn.datatables.net/1.10.12/css/jquery.dataTables.min.css">
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
    <script type="text/javascript" src="https://code.jquery.com/jquery-1.12.3.min.js"></script>
    <script type="text/javascript" src="https://cdn.datatables.net/1.10.12/js/jquery.dataTables.min.js"></script>
    <script type="text/javascript" src="https://code.jquery.com/jquery-3.5.1.js"></script>
    <script type="text/javascript" src="https://cdn.datatables.net/1.10.21/js/jquery.dataTables.min.js"></script>
    <script type="text/javascript" src="https://cdn.datatables.net/1.6.2/js/dataTables.buttons.min.js"></script>
    <script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/jszip/3.1.3/jszip.min.js"></script>
    <script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/pdfmake/0.1.53/pdfmake.min.js"></script>
    <script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/pdfmake/0.1.53/vfs_fonts.js"></script>
    <script type="text/javascript" src="https://cdn.datatables.net/buttons/1.6.2/js/buttons.html5.min.js"></script>
    <script>
        ${document}.ready(function() {
            //Setup - add a text input to each footer cell 
            $('#example thead tr').clone(true).appendTo('#example thead');
            $('#example thead tr:eq(1) th').each( function (i) {
            var title = $(this).text();
            $(this).html('<input type="text" placeholder="'+title+'" />');
            $( 'input', this ).on('keyup change' function() {
                if ( table.colum(i).search() !== this.value ) {
                    table 
                        .column(i)
                        .search(this.value)
                        .draw();
                }
            });
        });
        var table = $('#example').DataTable( {
        orderCellsTop: true,
        fixedHeader: true,
        scrollX:true,
        dom: 'B<"clear">lftrip', buttons:['excelHtml5, 'csvHtml5']
            });
        });
    </script>
</head>
<body>"""
    with codecs.open(file_path, 'rb', encoding='utf-8') as fin, codecs.open(output_file_path, 'wb',
                                                                            encoding='utf-8') as fout:
        fout.write(_html)
        fout.write('\n<br>\n<h2 align="center">{}</h2>\n<br>'.format(page_title))
        fout.write('\n\t<div class=\"container-fluid\">')
        fout.write(
            "\n\t<table ud=\"example\" class=\"display table table-striped table-bordered\" style\"width:100%\">")
        thead = 0
        tbody = 0
        tr = 0
        for line_count, row in enumerate(fin, start=1):
            if line_count >= 10000:
                partial_flag = True
                message = """Showing first 10,000 records in the html report. 
For full details, pelase refer {}""".format(file_path)
                logger.info(message)
                break
            for col_count, item in enumerate(row.split(delimiter), start=1):
                if line_count == 1:
                    if thead == 0:
                        fout.write("\n\t<thead>")
                        thead += 1
                    if tr == 0:
                        fout.write("\n\t\t<tr>")
                        tr += 1
                    fout.write(r"{}{}{}".format("\n\t\t\t<th class=\"bg-success\">", item.strip(), "</th>"))
                else:
                    if tbody == 0:
                        fout.write("\n\t<tbody")
                        tbody += 1
                    if tr == 0:
                        fout.write("\n\t\t<tr>")
                        tr += 1
                    fout.write(r"{}{}{}".format("\n\t\t\t<td>", item, "</td>"))
            if tr > 0:
                fout.write("\n\t\t</tr>")
                tr -= 1

            if line_count == 1 and thead == 1:
                fout.write("\n\t</thead>")
        fout.write("""\n\t</tbody>\n\t</table>\n</div>""")
        if partial_flag:
            fout.write("""\n<br><br><p>Note: {}</p>""".format(message))
        fout.write("""\n</body></html>""")
    return output_file_path


@timer
def get_attribute_mismatch_stats(input_file_path, delimiter):
    """
    This function contains the logic that helps us to report how many times an attribute has value mismatches 
    during the comparison process
    Args:
        input_file_path:
        delimiter:
        
    Returns:
        
    """
    input_file_path = os.path.abspath(input_file_path)
    input_folder_path = os.path.dirname(input_file_path)
    input_file_name_ext = os.path.basename(input_file_path)
    output_file_name_ext = "MismatchStats_{}".format(input_file_name_ext)
    output_file_path = os.path.join(input_folder_path, output_file_name_ext)
    delimiter = str(delimiter)
    dfs = pd.read_csv(input_file_path, sep=delimiter, na_filter=False, chunksize=1000000)
    temp_df = pd.DataFrame()

    for i, df in enumerate(dfs):
        try:
            df = df[df['mismatch_category'] == "Value_Mismatch"]
            out_df = df[['column_name, mismatch_category']]
            df2 = out_df.pivot_table(index='column_name', values='mismatch_category', aggfunc=np.count_nonzero)
            temp_df = temp_df.append(df2)
        except KeyError:
            logger.error("No Value Mismatches")

    try:
        final_df = temp_df.pivot_table(index='column_name', values='mismatch_category', aggfunc=np.sum)
        final_df = final_df.reset_index()
        final_df.columns = ['Mismatching_Column_Name', 'Mismatch_Count']
        logger.info("\n Msmatching Attribute Count".center(50, '-'))
        final_df.index = np.arange(1, len(final_df) + 1)
        logger.info(final_df.to_string(index=False, header=False))
        logger.info("\n {}".format("-" * 50))
        final_df.to_csv(output_file_path, sep=delimiter, index=False, header=True)
        create_detailed_mismatch_report_html('Mismatching Attribute Count', output_file_path, delimiter)
    except KeyError:
        logger.error("No value mismatches")


@timer
def query_sqlite_pragma_table_info(database_file_path, entity_table_name):
    """
    Gets the column names from the SQLite Table
    Args:
        database_file_path:
        entity_table_name:
    
    Returns:
        
    """
    database_file_path = os.path.abspath(database_file_path)
    list_column_names = list()
    # This method works only with Python3. Hence I commented it out 
    # if sys.version_info.major == 3:
    #     with sqlite3.connect(database_file_path) as conn:
    #         conn.text_factory = str 
    #         cursor = conn.cursor()
    #         sql = "select name from pragma_table_info('{}') order by cid".format(entity_table_name)
    #         cursor.execute(sql)
    #         list_column_names = list()
    #         for row in cursor:
    #             try:
    #                 for column in row:
    #                     list_column_names.append(column)
    #             except UnicodeEncodeError:
    #                 logger.error("UnicodeEncodeError : Skipping this record: {}".format(row))
    #         print(list_column_names)
    #         return list_collumn_names

    # This method works with all Python versions. Keeping this change.
    with sqlite3.connect(database_file_path) as conn:
        conn.text_factory = str
        cursor = conn.cursor()
        sql = "select * from {} limit 5;", format(entity_table_name)
        cursor.execute(sql)
        list_column_names = [description[0] for description in cursor.description]
        return list_column_names


@timer
def merge_mismatch_stats():
    """
    Merges alll the Mid-Level Mismatch Stats reports into a Single File for a consolidated view
    Returns:
        
    """
    delimiter = '|'
    folder_path = r'C:\workspace\RobotFramework_ETL\Results\FileCompare'
    file_name_pattern = "MismatchStats_ComparisonResult_*.psv"
    output_file_name = "Consolidated_MismatchStats_Report.psv"
    output_file_path = os.path.join(folder_path, output_file_name)
    list_files = glob.glob("{}/{}".format(folder_path, file_name_pattern))
    print(list_files)
    merged_df = pd.DataFrame()
    for file in list_files:
        df = pd.read_csv(file, sep=delimiter)
        file_name = os.path.basename(file)
        df['File_Name'] = file_name
        df = df[['File_Name', 'MismatchingColumn_Name', 'Mismatch_Count']]
        merged_df = merged_df.append(df)
    merged_df.to_csv(output_file_path, sep=delimiter, index=False)


# @timer
# def insert_comparison_summary_into_oracle(record):
#     """
#     This is an optional function that can be activated in the configuration file. If the flag value is set to truen then
#     Args:
#         record:
#
#     Returns:
#
#     """
#     # my_name = "insert_comparison_summary_into_oracle()"
#     # logger.info("Entered: {}".format(my_name))
#     # st = timeit.default_timer()
#     db_host = ''
#     db_port = ''
#     db_name = ''
#     db_user = ''
#     db_password = ''
#     db_role = cx_Oracle.SYSDBA
#     sql_stmt = """
#     insert into {}.{} values
#     {}
#     """.format(schema_name, table_name, str(tuple(record)))
#     logger.info(sql_stmt)
#     with cx_Oracle.connect(db_user, db_password, "{}:{}/{}".format(db_host, db_port, db_name), db_role,
#                            encoding='utf-8') as conn:
#         cursor = conn.cursor()
#         cursor.execute(sql_stmt)
#         conn.commit()
#
#     # et = timeit.default_timer() - st
#     # logger.info("Finished : {}; Elapsed Time: {}".format(my_name, et))


if __name__ == '__main__':
    pass
