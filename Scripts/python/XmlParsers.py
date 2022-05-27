# import section
from lxml import etree
import codecs
import os
import timeit
import pprint
import re
from robot.api import logger
import csv
encoding = 'utf-8'

# Author Section
# Program Name: XmlParsers.py.py                                     
# Created by Keshav at 27/05/22 2:14 a.m.                       

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
def parse_morningstar_datawarehouse_xml_file(input_file_path, delimiter):
    """
    Parse Morningstar Datawarehouse XML File - Ideal for fund FO and DMCLE XMLs
    Also found to be reusable for Stocks and ETFs
    Args:
        input_file_path:
        delimiter:

    Returns:

    """
    input_file_path = os.path.abspath(input_file_path)
    output_file_name = "{}.psv".format(os.path.splitext(os.path.basename(input_file_path))[0])
    output_file_path = os.path.join(os.path.dirname(input_file_path), os.path.basename(output_file_name))

    xml_iter = etree.iterparse(input_file_path, events=('start', 'end'))
    list_tag = list()
    key = None
    with codecs.open(output_file_path, 'w', encoding='utf-8') as fout:
        list_header = ['xml_record_id', 'investment_vehicle_id', 'xpath', 'value']
        str_header = delimiter.join(list_header)


if __name__ == '__main__':
    pass
