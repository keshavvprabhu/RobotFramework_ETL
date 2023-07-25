# import section
import codecs
import os
import pprint
from base64 import urlsafe_b64encode as b64e
import numpy as np
import pandas as pd
import requests
from jira.client import JIRA


# Author Section
# Program Name: jira_extractor.py
# Created by Keshav at 30/05/22 1:10 a.m.                       


# Write your code here

def get_jira_status(jira_filter, username, password, output_file_path, delimiter):
    """
    
    Args:
        jira_filter:
        username: 
        password: 
        output_file_path: 
        delimiter: 

    Returns:

    """
    output_file_path = os.path.abspath(output_file_path)

    jira_options = {'server': 'https://jiraserver.domain.com', 'verify': False}
    jira = JIRA(options=jira_options, basic_auth=(username, password))
    issues_in_project = jira.search_issues(jira_filter, maxResults=500)
    with codecs.open(output_file_path, 'wb', encoding='utf-8') as fout:
        list_output_header = ['Key', 'IssueType', 'Summary', 'Reporter', 'Assignee', 'Status', 'Labels', 'Sprint']
        str_output_header = delimiter.join(list_output_header)
        fout.write(u"{}\n".format(str_output_header))
        list_output_values = list()

        for issue in issues_in_project:
            list_output_values.append(str(issue.key))
            list_output_values.append(str(issue.fields.issuetype))
            list_output_values.append(str(issue.fields.summary))
            list_output_values.append(str(issue.fields.reporter))
            list_output_values.append(str(issue.fields.assignee))
            list_output_values.append(str(issue.fields.status))
            list_output_values.append(str(issue.fields.labels))
            list_output_values.append('FixVersion_Value')
            str_output_values = delimiter.join(list_output_values)
            list_output_values = []
            fout.write(u"{}\n".format(str_output_values))


def create_status_count_report(data_frame, output_file_path, delimiter):
    """
    Creates the Status Count JIRA Summary Report
    Args:
        data_frame:
        output_file_path:
        delimiter:

    Returns:

    """

    table2 = pd.pivot_table(data_frame, index=['IssueType'], columns=['Status'], values='Key', aggfunc=np.count_nonzero)
    table2['Total'] = table2.sum(axis=1)
    table2 = table2.fillna(0)
    table2 = table2.apply(pd.to_numeric, errors='ignore')
    table2 = table2.astype(int)
    table2.to_csv(output_file_path, sep=delimiter)
    append_summary_total('IssueType', output_file_path, delimiter)


def append_summary_total(df_index, file_path, delimiter):
    """
    Appends Summary Total
    Args:
        df_index: 
        file_path: 
        delimiter: 

    Returns:
    
    """
    df = pd.read_csv(file_path, sep=delimiter)
    # sums = df.select_dtypes(pd.np.number).sum().rename('Grand Total')
    df.loc['Grand Total'] = df.select_dtypes(pd.np.number).sum()
    df = df.fillna("GrandTotal")
    df = df.set_index(df_index)
    df = df.apply(pd.to_numeric, errors='ignore')
    df = df.astype(int)
    df.to_csv(file_path, sep=delimiter)


def connect_to_jira():
    username = 'keshavvprabhu@gmail.com'
    api_key = "ATATT3xFfGF0gBaQ1tlHZKoSSWaEmNTlmsIzF626WlL9BIsAAxJR7o35Cn-PWSa2dqRVmmwiShUCJQg1TvlMxuvrx1lbDBqvUYHWFxh8JR7Q3cDxPxrJFnIfIRO7ggko864aCE5rDyHfGTwbPQotnqQNT6gUpdw5jdtW96skqs_hmXiVdwVUQSo=16C6A424"
    url = "https://phyurious.atlassian.net/rest/api/3/issue/ITEM-5"

    string_to_encode = f"{username}:{api_key}"
    encoded_value = b64e(bytearray(string_to_encode, encoding='utf-8'))
    print(f"Token: {encoded_value}")
    api_header = {'Authorization': 'Basic {}'.format(encoded_value)}
    r  = requests.get(url, headers=api_header, verify=False)
    pprint.pprint(r.json(), indent=4)

if __name__ == '__main__':
    connect_to_jira()
    pass
