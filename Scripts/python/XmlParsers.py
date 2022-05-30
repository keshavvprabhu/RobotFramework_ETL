# import section
import codecs
import os
import re
import timeit

import pandas as pd
from lxml import etree
from robot.api import logger

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
def parse_ms_datawarehouse_xml_file(input_file_path, delimiter):
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
        fout.write(u"{}\n".format(list_header))
        xml_id = 0
        for event, elem in xml_iter:
            if event == 'start':
                if elem.tag == 'InvestmentVehicle' and elem.attrib:
                    xml_id += 1
                    iv_id = elem.attrib
                    key = iv_id.get('_Id', 'NULL')

                if elem.attrib:
                    dict_elem_attrib = dict(elem.attrib)
                    for k, v in dict_elem_attrib.items():
                        list_tag_now = "/".join(list_tag)
                        write_attr = delimiter.join(
                            (key, "{}/{}_{}".format(list_tag_now, elem.tag, k).replace('__', '_'), v))
                        fout.write("{}|{}".format(xml_id, write_attr))
                    list_tag.append("{}".format(elem.tag))
                else:
                    list_tag.append(elem.tag)

                if elem.text:
                    x_path = "/".join(list_tag)
                    elem_text = elem.text
                    elem_text = re.sub(r"(\r\n|\n|\r|\|)", r"", elem_text)
                    fout.write("{}|{}|{}|{}\n".format(xml_id, key, x_path, elem_text))

            if event == 'end':
                list_tag.pop()

            elem.clear()
            while elem.getprevious() is not None:
                del elem.getparent()[0]

    logger.info("Output File Path: {}".format(output_file_path))
    return output_file_path


@timer
def fast_iter_headers(context):
    set_headers = set()
    list_header = list()
    for event, elem in context:
        list_header = get_attributes_header_list(elem, set_headers)
        elem.clear()
        while elem.getprevious() is not None:
            del elem.getparent()[0]

    list_header = sorted(list_header)
    del context
    return list_header


@timer
def get_attributes_header_list(element, set_headers):
    set_headers.add('Message_Symbol')
    for item in element:
        set_headers.add(item.attrib['id'])
    list_headers = list(set_headers)
    return list_headers


@timer
def fast_iter_values(context, header, output_file_path, delimiter='|'):
    """
    Iter values fast through the xml
    Args:
        context:
        header:
        output_file_path:
        delimiter:

    Returns:

    """
    output_file_path = os.path.abspath(output_file_path)
    len_header = len(header)
    for event, elem in context:
        pos = header.index('Message Symbol')
        list_values = ['' for _ in range(len_header)]
        list_values[pos] = elem.attrib['symbol']

        for fld in elem:
            for h in header:
                if fld.attrib['id'] == h:
                    pos = header.index(h)
                    list_values[pos] = fld.text

        with codecs.open(output_file_path, 'ab', encoding='utf-8') as fout:
            fout.write("{}\n".format(delimiter.join(list_values)))

        elem.clear()
        while elem.getprevious is not None:
            del elem.getparent()[0]

    del context


def convert_ms_webservice_xml_to_csv(input_xml_file_path, output_file_path, delimiter='|'):
    """
    Convert MS WebService XML to CSV format
    Args:
        input_xml_file_path:
        output_file_path:
        delimiter:

    Returns:

    """
    input_xml_file_path = os.path.abspath(input_xml_file_path)
    output_folder_path = os.path.dirname(output_file_path)
    if not os.path.exists(output_folder_path):
        os.makedirs(output_folder_path)

    context = etree.iterparse(input_xml_file_path, events=('end',), tag='{http://ms.com}message')
    header = fast_iter_headers(context)

    with codecs.open(output_file_path, 'wb', encoding='utf-8') as fout:
        fout.write(delimiter.join(header) + '\n')

    context = etree.iterparse(input_xml_file_path, events=('end',), tag='{http://ms.com}message')
    fast_iter_values(context, header, output_file_path, delimiter)
    print("Completed. Output: {}".format(output_file_path))


@timer
def append_files_with_different_columns(output_file_path, *args):
    """
    This function appends files with different columns together and generates a csv file output
    Args:
        output_file_path:
        *args:

    Returns:

    """
    output_file_path = os.path.abspath(output_file_path)
    set_columns = set()
    for arg in args:
        for item in arg:
            df = pd.read_csv(item, delimiter='|', dtype=str)
            for column in df.columns:
                set_columns.add(column)

    list_columns = list(set_columns)
    list_columns = sorted(list_columns)
    out_df = pd.DataFrame(columns=list_columns)

    for arg in args:
        for item in sorted(arg):
            df = pd.read_csv(item, delimiter="|", dtype=str, na_values=['NA', 'NaN'], na_filter=False).astype('str')
            df = df.replace('nan', '')
            out_df = pd.concat([out_df, df], axis=0, sort=False)

    out_df.to_csv(output_file_path, sep='|', index=False)


@timer
def parse_fspx_xml(input_file_path, delimiter='|'):
    """
    Parser for FS Px XML file
    Args:
        input_file_path:
        delimiter:

    Returns:

    """
    input_file_path = os.path.abspath(input_file_path)
    input_folder_path = os.path.dirname(input_file_path)
    input_file_name_without_ext = os.path.basename(input_file_path).rsplit('.')[0]
    output_file_path = os.path.join(input_folder_path, f"{input_file_name_without_ext}.psv")

    xml_iter = etree.iterparse(input_file_path, events=('start', 'end'))
    list_tag = list()
    key = None

    with codecs.open(output_file_path, 'wb', encoding='utf-8') as fout:
        list_header = ['xml_record_id', 'xpath', 'value']
        str_header = delimiter.join(list_header)
        fout.write(u"{}\n".format(str_header))
        xml_id = 0
        xmlns = '{fsrv}'
        output_record = list()
        for event, elem in xml_iter:
            if event == 'start':
                print(elem.tag, elem.attrib, elem.text)
                list_tag.append(elem.tag)
                xpath = "/".join([i.replace(xmlns, '') for i in list_tag])

                if xpath == 'PriceSet/Price/PriceRec':
                    xml_id += 1

                if elem.text:
                    elem_text = elem.text
                    elem_text = re.sub(r'(\r\n|\r|\n|\|)', r'', elem_text)
                    fout.write(u"{}|{}|{}\n".format(xml_id, xpath, elem_text))

            if event == 'end':
                list_tag.pop()

            elem.clear()
            while elem.getprevious() is not None:
                del elem.getparent()[0]

    return output_file_path


if __name__ == '__main__':
    pass
