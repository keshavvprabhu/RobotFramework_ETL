# import section
import zlib
import getpass
from base64 import urlsafe_b64encode as b64e


# Author Section
# Program Name: EncodeCredentials.py                                     
# Created by Keshav at 11/05/22 1:26 a.m.                       


# Write your code here
def encode_credentials(data):
    data = bytearray(data, encoding='utf-8')
    return b64e(zlib.compress(data, 9)).decode('utf-8')


if __name__ == '__main__':
    user_id = input("Enter User ID: ")
    password = getpass.getpass(prompt="Enter Password: ")
    encoded_user_id = encode_credentials(user_id)
    encoded_password = encode_credentials(password)
    print("Encoded User ID: {}".format(encoded_user_id))
    print("Encoded Password: {}".format(encoded_password))

