# import section
import win32com.client as win32
import os
import timeit
import codecs
from robot.api import logger
from CommonUtilities import timer


# Author Section
# Program Name: EmailOutlook.py                                     
# Created by Keshav at 20/05/22 9:38 p.m.                       


# Write your code here

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

    ## Note: If you need to insert images, please ensure that the html has img tags with the image
    mail.HTMLBody = """{}""".format(str_body)

    # To attache a file to the email (optional):
    logger.info(list_attachments)

    if len(list_attachments) > 1:
        for i, attachment in enumerate(list_attachments, start=1):
            if attachment != 'File Not Found':
                try:
                    os.path.exists(attachment)
                    attached = mail.Attachments.Add(attachment)
                    attached.PropertyAccessor.SetProperty("http://schemas.microsoft.com/mapi/proptag/0x3712001F",
                                                          "MyId{0}".format(i))
                    logger.info("Added Attachment {}:{}".format(i, attachment))
                except Exception as e:
                    logger.error("File Not Found: {}".format(attachment))
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


def test_email():
    str_to = 'keshavvprabhu@gmail.com'
    str_cc = "keshavvprabhu@gmail.com"
    str_subject = "Test Email"
    str_body = "Hello, This is a test email"
    list_attachments = ''
    send_email(str_to, str_cc, str_subject, str_body, list_attachments)


def send_email_image():
    signatureimage = r'/path/to/image.png'
    outlook = win32.Dispatch('outlook.application')
    mail = outlook.CreateItem(0)
    mail.To = "keshavvprabhu@gmail.com"
    mail.Subject = "Test Sample"
    attachment = mail.Attachments.Add(signatureimage)
    attachment.PropertyAccessor.SetProperty("http://schemas.microsoft.com/mapi/proptag/0x3712001F", "MyId1")
    mail.HTMLBody = "<html><body><img src=""cid:MyId1""></body></html>"
    mail.Send()


if __name__ == '__main__':
    test_email()
    pass
