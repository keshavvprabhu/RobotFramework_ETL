# import section
import csv
import os
import timeit
from robot.api import logger
import pandas as pd
import numpy as np
import codecs
import csv
from collections import Counter


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


if __name__ == '__main__':
    pass
