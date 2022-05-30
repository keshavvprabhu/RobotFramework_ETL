# import section
import codecs
import csv
import filecmp
import glob
import os
import re
import shutil
import timeit
import zipfile

import pandas as pd
from robot.api import logger


# Author Section
# Program Name: FileConverters.py                                     
# Created by Keshav at 20/05/22 11:04 p.m.                       


# Write your code here
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


@timer
def get_folder_path(input_file_path):
    """
    Returns the directory path of the input_file_path proided
    Args:
        input_file_path:

    Returns:

    """
    input_file_path = os.path.abspath(input_file_path)
    return os.path.dirname(input_file_path)


@timer
def get_file_name(input_file_path):
    """
    Returns the filename of the input_file_path provided
    Args:
        input_file_path:

    Returns:

    """
    input_file_path = os.path.abspath(input_file_path)
    return os.path.basename(input_file_path)


@timer
def get_file_name_without_ext(input_file_path):
    """
    Returns the file name without the extension
    Args:
        input_file_path:

    Returns:

    """
    input_file_path = os.path.abspath(input_file_path)
    return os.path.splitext(os.path.basename(input_file_path))[0]


@timer
def get_file_ext(input_file_path):
    """
    Returns the file extension of the input file
    Args:
        input_file_path:

    Returns:

    """
    input_file_path = os.path.abspath(input_file_path)
    return os.path.splitext(os.path.basename(input_file_path))[-1]


@timer
def convert_file_delimiters(input_file_path, from_delimiter, to_delimiter):
    """
    Changes the delimiters of the input file path
    Args:
        input_file_path:
        from_delimiter:
        to_delimiter:

    Returns:

    """
    from_delimiter = str(from_delimiter)
    to_delimiter = str(to_delimiter)
    input_file_path = os.path.abspath(input_file_path)
    df = pd.read_csv(input_file_path, delimiter=from_delimiter, header=None, encoding='utf-8',
                     quoting=csv.QUOTE_MINIMAL)
    output_file_name = "temp_{}".format(os.path.basename(input_file_path))
    output_folder_path = os.path.dirname(input_file_path)
    output_file_path = os.path.join(output_folder_path, output_file_name)
    output_file_path = os.path.abspath(output_file_path)
    df.to_csv(output_file_path, sep=to_delimiter, index=False, header=False, encoding='utf-8',
              quoting=csv.QUOTE_MINIMAL)
    os.remove(input_file_path)
    os.rename(output_file_path, input_file_path)
    logger.info("Delimiter converted from {} to {} for input file : {}".format(from_delimiter, to_delimiter,
                                                                               input_file_path))


@timer
def detect_encoding(input_file_path):
    """
    Reads a file and detects the encoding used within the file
    Args:
        input_file_path:

    Returns: detected_encoding

    """

    import chardet
    input_file_path = os.path.abspath(input_file_path)
    list_encoding = list()
    with codecs.open(input_file_path, 'rb', encoding='utf-8') as fin:
        for record in fin:
            list_encoding = chardet.detect(record)
    return list_encoding


@timer
def parse_autosys_jil_extract(environment_name, input_file_path, delimiter="|"):
    """
    Parses Autosys JIL file and generates and output file (delimited)
    Args:
        environment_name:
        input_file_path:
        delimiter:

    Returns:

    """
    input_file_path = os.path.abspath(input_file_path)
    input_file_name = os.path.basename(input_file_path)
    input_folder_path = os.path.dirname(input_file_path)
    output_file_name = "parsed_{}".format(input_file_name)
    output_file_path = os.path.join(input_folder_path, output_file_name)
    with codecs.open(input_file_path, 'rb', encoding='utf-8') as fin, codecs.open(output_file_path, 'wb',
                                                                                  encoding='utf-8') as fout:
        csvreader = csv.reader(fin, delimiter=":")
        csvwriter = csv.writer(fout, delimiter=delimiter, quoting=csv.QUOTE_MINIMAL)
        csvwriter.writerow(['JobName', 'AttributeName', 'AttributeValue'])

        for record in csvreader:
            list_output_record = list()

            if record not in ([], '', None) and len(record) != 1:
                if record[0].strip() == 'insert_job':
                    global job_name
                    job_name = record[1].strip().split(' ')[0]

                if len(record) == 3 and record[0] != 'insert_job':
                    attribute_name = record[0].strip()
                    attribute_name = re.sub(r'{}_'.format(environment_name), r'ENV_', attribute_name)
                    attribute_value = "{}:{}".format(record[1].strip(), record[2].strip())
                    attribute_value = re.sub(r"{}_".format(environment_name), r'ENV_', attribute_value)
                    list_output_record.append(job_name)
                    list_output_record.append(attribute_name)
                    list_output_record.append(attribute_value)

                if list_output_record is not list():
                    csvwriter.writerow(list_output_record)
    return output_file_path


@timer
def diff_two_files(source_file_path, target_file_path, output_report_path):
    """
    Diffs two files and writes the output into output report path
    Args:
        source_file_path:
        target_file_path:
        output_report_path:

    Returns:

    """
    source_file_path = os.path.abspath(source_file_path)
    target_file_path = os.path.abspath(target_file_path)
    output_report_path = os.path.abspath(output_report_path)

    source_file_name = os.path.basename(source_file_path)
    target_file_name = os.path.basename(target_file_path)

    comparison_result = filecmp.cmp(source_file_path, target_file_path)
    logger.info("Source File: {}".format(source_file_name))
    logger.info("Target File: {}".format(target_file_name))

    logger.info("Comparison Result: {}".format(comparison_result))

    if os.path.exists(output_report_path):
        with codecs.open(output_report_path, 'ab', encoding='utf-8') as fout:
            fout.write(f"{source_file_name}|{target_file_name}|{comparison_result}\n")
    else:
        with codecs.open(output_report_path, 'wb', encoding='utf-8') as fout:
            fout.write("Source_File_Name|Target_File_Name|Comparison_Result\n")

    if comparison_result is True:
        os.remove(source_file_path)
        os.remove(target_file_path)


@timer
def combine_files(input_folder_path, input_file_pattern, output_file_path, delimiter='|'):
    """
    Combines multiple files having the same structure into one file
    Note: The output_file_path must be in a different folder than the input_folder_path.
    Otherwise we will get permission denied error.

    Args:
        input_folder_path:
        input_file_pattern:
        output_file_path:
        delimiter:

    Returns:

    """

    input_folder_path = os.path.abspath(input_folder_path)
    input_file_path_pattern = os.path.join(input_folder_path, input_file_pattern)
    logger.info("Combining files having pattern: {}".format(input_file_path_pattern))
    output_file_path = os.path.abspath(output_file_path)

    with codecs.open(output_file_path, 'wb', encoding='utf-8') as fout:
        for counter, input_file_path in enumerate(glob.glob(input_file_path_pattern), start=1):
            with codecs.open(input_file_path, 'rb', encoding='utf-8') as fin:
                for record in fin:
                    fout.write(record)
            logger.debug("Merged: {}".format(input_file_path))
            os.remove(input_file_path)


@timer
def zip_file(input_file_path, keep_orig_file=True):
    """
    Zips an individual file in the same directory as the original file
    Args:
        input_file_path:
        keep_orig_file: when True keeps the original file, when False deletes the original file

    Returns:

    """
    input_file_path = os.path.abspath(input_file_path)
    input_folder_path = os.path.dirname(input_file_path)
    input_file_name = os.path.basename(input_file_path)
    curr_directory = os.getcwd()
    zip_file_path = "{}.zip".format(input_file_path)

    if os.path.exists(input_file_path):
        logger.info("Compressing {} into {}".format(input_file_path, zip_file_path))
        with zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED) as zout:
            os.chdir(input_folder_path)
            zout.write(input_file_name)

        logger.info("Zip File Created Successfully: {}".format(zip_file_path))

        os.chdir(curr_directory)

        if not keep_orig_file:
            os.remove(input_file_path)
            logger.info("Original File: {} has been deleted")
    else:
        logger.error("File Not Found: {}".format(input_file_path))
        raise RuntimeError


@timer
def zip_multiple_files(list_input_file_paths, output_zip_file_path):
    """
    Copies multiple files provided as a list to a folder and zips the folder
    Args:
        list_input_file_paths:
        output_zip_file_path:

    Returns:

    """
    output_zip_file_path = os.path.abspath(output_zip_file_path)
    logger.info(output_zip_file_path)
    output_zip_folder_path = os.path.dirname(output_zip_file_path)
    logger.info(output_zip_folder_path)
    output_zip_folder_name = os.path.splitext(output_zip_file_path)[0]
    logger.info(output_zip_folder_name)

    if not os.path.exists(output_zip_folder_name):
        os.makedirs(output_zip_folder_name)
        for input_file_path in list_input_file_paths:
            if os.path.isfile(input_file_path):
                shutil.copy(input_file_path, output_zip_folder_name)

        shutil.make_archive(output_zip_file_path, 'zip', output_zip_folder_name)

    logger.info("Created: {}".format(output_zip_file_path))


if __name__ == '__main__':
    pass
