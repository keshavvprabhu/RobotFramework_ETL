import codecs
import csv
import os
import pprint
import re

import pandas as pd
from robot.api import logger
from robot.api.deco import not_keyword

from CommonUtilities import timer


@timer
def parse_autosys_jil(input_file_path, delimiter="^"):
    """
    Parse autosys jil file and creates a delimited file with 3 columns: JobName, AttributeName, AttributeValue.
    Args:
        input_file_path:
        delimiter:

    Returns: output_file_path

    """
    input_file_path = os.path.abspath(input_file_path)
    input_file_name = os.path.basename(input_file_path)
    input_folder_path = os.path.dirname(input_file_path)
    output_file_name = f"parsed_{input_file_name}"
    output_file_path = os.path.join(input_folder_path, output_file_name)
    output_file_path = os.path.abspath(output_file_path)

    with codecs.open(input_file_path, "rb", "utf-8") as fin, codecs.open(output_file_path, "wb", "utf-8") as fout:
        csvreader = csv.reader(fout, delimiter, quoting=csv.QUOTE_MINIMAL)
        csvwriter = csv.writer(fout, delimiter, quoting=csv.QUOTE_MINIMAL)
        csvwriter.writerow(['JobName', 'AttributeName', 'AttributeValue'])

        for i, record in enumerate(csvreader, start=1):
            list_output_record = list()
            # print(record)
            if record not in ([], '', None) and len(record) != 1:
                if record[0].strip() in ('insert_job', 'update_job'):
                    global job_name, job_type
                    job_name = record[1].strip().split(' ')[0]
                    job_type = record[-1].strip()
                    operation = record[0].strip()
                    list_output_record.append(job_name)
                    list_output_record.append(operation)
                    csvwriter.writerow(list_output_record)
                    list_output_record = list()
                    list_output_record.append(job_name)
                    list_output_record.append('job_type')
                    list_output_record.append(job_type)

                if len(record) == 3 and record[0].strip() not in ('insert_job', 'update_job'):
                    attribute_name = record[0].strip()
                    attribute_value = "{}:{}".format(record[1].strip(), record[2].strip())
                    list_output_record.append(job_name)
                    list_output_record.append(attribute_name)
                    list_output_record.append(attribute_value)

                if len(record) == 2:
                    list_output_record.append(job_name)
                    attribute_name = record[0].strip()
                    attribute_value = record[1].strip()
                    if attribute_name == 'condition':
                        # logger.info(attribute_name)
                        # logger.info("Befor Sorting Conditions: {attribute_value}")
                        sorted_attribute_value = " & ".join(sorted([i.strip() for i in attribute_value.split("&")]))
                        # logger.info("After Sorting Conditions: {sorted_attribute_value}")
                        list_output_record.append(attribute_name)
                        list_output_record.append(sorted_attribute_value)
                    else:
                        list_output_record.append(attribute_name)
                        list_output_record.append(attribute_value)

                if list_output_record != []:
                    csvwriter.writerow(list_output_record)

    return output_file_path


@timer
def create_autosys_jil_report(input_file_path, delimiter="^"):
    """
    Create a report of the autosys jil file from the parsed file.
    Args:
        input_file_path:
        delimiter:

    Returns:

    """
    input_file_path = os.path.abspath(input_file_path)
    input_file_name = os.path.basename(input_file_path)
    input_folder_path = os.path.dirname(input_file_path)
    output_file_name = f"Report_{input_file_name}"
    output_file_path = os.path.join(input_folder_path, output_file_name)
    output_file_path = os.path.abspath(output_file_path)
    excel_output_file_path = os.path.join(input_file_name.rsplit(".", 1)[0] + ".xlsx")
    logger.info(output_file_path)

    df = pd.read_csv(input_file_path, delimiter=delimiter, quoting=csv.QUOTE_MINIMAL)
    duplicates = df.duplicated()
    df_dups = df[duplicates]

    if not df_dups.empty:
        duplicates_file_path = os.path.join(input_folder_path, f"duplicates_{input_file_name}_err")
        logger.error("Writing duplicates file: {duplicates_file_path}")
        logger.error(df_dups)
        df_dups.to_csv(duplicates_file_path, index=False, encoding="utf-8", na_rep='')

    df_out = df.pivot(index='JobName', columns='AttributeName', values='AttributeValue')
    df_out.reset_index(inplace=True)
    df_out.to_csv(output_file_path, index=False, encoding="utf-8", na_rep='')
    #     df_out.to_excel(excel_output_file_path, index=False)
    return output_file_path


@timer
def create_autosys_status_report(input_file_path):
    """
    Parses the autosys status report and splits the columns.
    Args:
        input_file_path:

    Returns:

    """
    input_file_path = os.path.abspath(input_file_path)
    input_file_name = os.path.basename(input_file_path)
    input_folder_path = os.path.dirname(input_file_path)
    output_file_name = f"Report_{input_file_name}"
    output_file_path = os.path.join(input_folder_path, output_file_name)
    output_file_path = os.path.abspath(output_file_path)

    logger.info(output_file_path)
    with codecs.open(input_file_path, "rb", "utf-8") as fin, codecs.open(output_file_path, "wb", "utf-8") as fout:
        csvreader = csv.reader(fout, delimiter="^", quoting=csv.QUOTE_MINIMAL)
        csvwriter = csv.writer(fout, delimiter="^", quoting=csv.QUOTE_MINIMAL)

        csvwriter.writerow(['JobName', 'LastStart', 'LastEnd', 'JobStatus', 'RunEntry', 'StatusCode'])

        len_output_record = set()
        for i, record in enumerate(csvreader, start=1):
            output_record = list()
            formatted_output_record = list()
            if i >= 4:
                output_record = [column.strip() for column in record if column != '']
                len_output_record.add(len(output_record))

                job_name = output_record[0] if output_record[0] else ''
                last_start_datetime = ''
                last_end_datetime = ''
                job_status = ''
                run_entry = ''
                status_code = ''

                if output_record[1] == '-----' and output_record[2] == '-----':
                    last_start_datetime = output_record[1]
                    last_end_datetime = output_record[2]
                    job_status = output_record[3] if output_record[3] else ''
                    run_entry = output_record[4] if output_record[4] else ''
                    try:
                        status_code = output_record[5]
                    except IndexError:
                        status_code = ''

                elif output_record[1] == '-----' and output_record[3] != '-----':
                    last_start_datetime = output_record[1]
                    last_end_datetime = f"{output_record[2]} {output_record[3]}"
                    job_status = output_record[4] if output_record[4] else ''
                    run_entry = output_record[5] if output_record[5] else ''
                    try:
                        status_code = output_record[6]
                    except IndexError:
                        status_code = ''

                elif output_record[1] != '-----' and output_record[3] == '':
                    last_start_datetime = f"{output_record[1]} {output_record[2]}"
                    last_end_datetime = output_record[3]
                    job_status = output_record[4] if output_record[4] else ''
                    run_entry = output_record[5] if output_record[5] else ''
                    try:
                        status_code = output_record[6]
                    except IndexError:
                        status_code = ''

                elif output_record[1] != '-----' and output_record[2] != '-----' and output_record[3] != '-----' and \
                        output_record[4] != '-----':
                    last_start_datetime = f"{output_record[1]} {output_record[2]}"
                    last_end_datetime = f"{output_record[3]} {output_record[4]}"
                    job_status = output_record[5] if output_record[5] else ''
                    run_entry = output_record[6] if output_record[6] else ''
                    try:
                        status_code = output_record[7]
                    except IndexError:
                        status_code = ''

                formatted_output_record.append(job_name)
                formatted_output_record.append(last_start_datetime)
                formatted_output_record.append(last_end_datetime)
                formatted_output_record.append(job_status)
                formatted_output_record.append(run_entry)
                formatted_output_record.append(status_code)

                csvwriter.writerow(formatted_output_record)
    format_autosys_status_report(output_file_path, "^")
    return output_file_path


@timer
def format_autosys_status_report(input_file_path, delimiter="^"):
    input_file_path = os.path.abspath(input_file_path)
    df = pd.read_csv(input_file_path, delimiter=delimiter, quoting=csv.QUOTE_MINIMAL)
    logger.info("=" * 50)
    logger.info("Before Datatype Conversion")
    logger.info(df.info(memory_usage="deep"))
    logger.info("=" * 50)

    df['LastStart'] = pd.to_datetime(df['LastStart'], errors='coerce')
    df['LastEnd'] = pd.to_datetime(df['LastEnd'], errors='coerce')
    df['JobStatus'] = df['JobStatus'].astype('category')

    logger.info("=" * 50)
    logger.info("After Datatype Conversion")
    logger.info(df.info(memory_usage="deep"))
    logger.info("=" * 50)

    df['ElapsedTime'] = df['LastEnd'] - df['LastStart']

    df_job_status = df.groupby('').agg('count')
    logger.info("\n {}".format(df_job_status))

    df.to_csv(input_file_path, index=False, encoding="utf-8", delimiter="^", quoting=csv.QUOTE_MINIMAL)


@timer
def convert_csv_to_jil(input_file_path, delimiter, output_file_path):
    """
    Converts CSV fule to JIL
    Args:
        input_file_path:
        delimiter:
        output_file_path:

    Returns:

    """
    input_file_path = os.path.abspath(input_file_path)
    input_file_name = os.path.basename(input_file_path)
    output_file_path = os.path.abspath(output_file_path)

    with codecs.open(input_file_path, 'rb', encoding='utf-8') as fin, codecs.open(output_file_path, 'wb',
                                                                                  encoding='utf-8') as fout:
        csvreader = csv.DictReader(fin, quoting=csv.QUOTE_MINIMAL, delimiter=delimiter)

        list_keys = ['box_name',
                     'command',
                     'machine',
                     'owner',
                     'permission',
                     'date_conditions',
                     'box_success',
                     'run_calendar',
                     'condition',
                     'days_of_week',
                     'start_mins',
                     'exclude_calendar',
                     'start_times',
                     'description',
                     'n_retrys',
                     'std_out_file',
                     'std_err_file',
                     'max_run_alarm',
                     'alarm_if_fail',
                     'job_load',
                     'priority',
                     'max_exit_success',
                     'profile',
                     'alarm_if_terminated',
                     'envvars',
                     'timezone',
                     'watch_file',
                     'watch_file_recursive',
                     'watch_file_type',
                     'watch_no_change',
                     'continuous',
                     'watch_fule_change_type',
                     'watch_interval',
                     'status',
                     ]
        for i, record in enumerate(csvreader, start=1):
            job_name = record['JobName']
            job_type = record['job_type']
            operation = record['operation']

            fout.write(f"/* -------------- {job_name} --------------*/\n")

            #other attributes
            for key in list_keys:
                if record.get(key, '') != '':
                    fout.write(f"{key}: {record.get(key,'')}\n")

            fout.write("\n\n")



if __name__ == "__main__":
    pass
