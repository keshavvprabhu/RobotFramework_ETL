# import section
import win32com.client as win32
import os
import timeit
import codecs
from robot.api import logger


# Author Section
# Program Name: EmailOutlook.py                                     
# Created by Keshav at 20/05/22 9:38 p.m.                       


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
def send_email(str_to, str_cc, str_subject, str_body, list_attachments):
    """
    Sends email using Microsoft Outlook using Win32 APIs
    Args:
        str_to:
        str_cc:
        str_subject:
        str_body:
        list_attachments:

    Returns:

    """
    outlook = win32.Dispatch('outlook.application')
    mail = outlook.CreateItem(0)
    mail.To = str_to
    mail.Cc = str_cc
    mail.Subject = str_subject
    mail.HTMLBody = """{}""".format(str_body)

    # To attache a file to the email (optional):
    logger.info(list_attachments)

    if len(list_attachments) > 1:
        for i, attachment in enumerate(list_attachments, start=1):
            if attachment != 'File Not Found':
                try:
                    os.path.exists(attachment)
                    mail.Attachments.Add(attachment)
                    logger.info("Added Attachment {}:{}".format(i, attachment))
                except Exception as e:
                    logger.error("File Not Foung: {}".format(attachment))
                    logger.error(e)

    mail.Send()
    logger.info("Email has been sent. Please check your sent items folder in Outlook")


@timer
def read_html_file_content(html_file_path):
    """
    Reads HTML file and returns the whole file content
    Args:
        html_file_path:

    Returns:

    """
    html_file_path = os.path.abspath(html_file_path)
    with codecs.open(html_file_path, 'rb', encoding='utf-8') as fin:
        return fin.read()


if __name__ == '__main__':
    pass
