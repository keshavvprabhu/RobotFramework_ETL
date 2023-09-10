# import section
import codecs
import os
import pprint
from base64 import urlsafe_b64encode as b64e
import numpy as np
import pandas as pd
import requests
from jira.client import JIRA
import matplotlib.pyplot as plt
from CommonUtilities import timer
from robot.api import logger


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
    r = requests.get(url, headers=api_header, verify=False)
    pprint.pprint(r.json(), indent=4)


@timer
def create_jira_pivot_reports(input_file_path, delimiter=","):
    """
    Creates some useful JIRA Pivot Reports
    Args:
        input_file:
        delimiter:

    Returns:

    """
    input_file_path = os.path.abspath(input_file_path)
    input_folder_path = os.path.dirname(input_file_path)
    input_file_name = os.path.basename(input_file_path)
    input_file_name_wo_ext = input_file_name.rsplit(".", 1)[0].strip()

    pivot_file_name = f"Pivot_IssueType_{input_file_name}"
    pivot_file_path = os.path.join(input_folder_path, pivot_file_name)
    status_chart_file_path = os.path.join(input_folder_path, f"{input_file_name_wo_ext}_status_count_chart.png")
    issuetype_chart_file_path = os.path.join(input_folder_path, f"{input_file_name_wo_ext}_issuetype_chart.png")

    pd.options.display.width = None
    pd.options.display.max_columns = None
    pd.set_option('display.max_rows', 3000)
    pd.set_option('display.max_columns', 3000)

    if os.path.exists(input_file_path):
        logger.info("File exists")
    else:
        logger.error("File does not exist")

    df = pd.read_csv(input_file_path)
    df_status_counts = df['Status'].value_counts()
    logger.warn(df_status_counts)

    ## Plot donut chart (Status)
    fig, ax = plt.subplots()
    df_status_counts.plot(kind='pie', title="Status", autopct="%1.1f%%", pctdistance=0.75)
    total = df_status_counts.sum()
    centre_circle = plt.Circle((0, 0), 0.50, fc="white")
    fig = plt.gcf()
    fig.gca().add_artist(centre_circle)
    ax.text(0, 0, "{}\nIssues".format(total), ha='center', va='center', fontsize='20')
    plt.tick_params(labelsize=8)
    plt.axis('off')
    plt.savefig(status_chart_file_path, dpi=500)
    plt.close()

    # IssueType Summary
    df_pivot1 = pd.pivot_table(df, index=['IssueType'], columns=["Status"], values="Key", aggfunc=np.count_nonzero)
    df_pivot1['Total'] = df_pivot1.sum(axis=1)
    df_pivot1 = df_pivot1.fillna(0)
    df_pivot1 = df_pivot1.apply(pd.to_numeric, errors='ignore')
    df_pivot1 = df_pivot1.astype(int)

    #plot donut chart (issuetype)
    fig, ax = plt.subplots()
    df_pivot1['Total'].plot(kind='pie', legend=False, title="Issue Type", autopct="%1.1f%%", pctdistance=0.75)
    centre_circle = plt.Circle((0, 0), 0.50, fc="white")
    fig = plt.gcf()
    fig.gca().add_artist(centre_circle)
    ax.text(0, 0, "{}\nIssues".format(total), ha='center', va='center', fontsize='20')
    plt.tick_params(labelsize=8)
    plt.axis('off')
    plt.savefig(issuetype_chart_file_path, dpi=500)
    plt.close()

    df_pivot1.reset_index(inplace=True)
    df_pivot1.to_csv(pivot_file_path, sep=delimiter, index=False, na_rep='')

    if not df_pivot1.empty:
        append_summary_total('IssueType', pivot_file_path, delimiter)
        create_jira_report_html("IssueType vs Status", "", pivot_file_path, delimiter, enable_hyperlink=False)



if __name__ == '__main__':
    connect_to_jira()
    pass
