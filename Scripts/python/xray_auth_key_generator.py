from base64 import urlsafe_b64encode as b64e
# import section

# Author Section
# Program Name: xray_auth_key_generator.py                                     
# Created by Keshav at 23/05/22 3:26 a.m.                       


# Write your code here

def generate_xray_auth_key():
    """
    Generates the xray_auth_key required by the Xray Listener
    Returns:

    """
    user_id = input("Enter User ID: ")
    user_id = user_id.strip()
    api_key = input("Enter API Key: ")
    api_key = api_key.strip()
    string_to_encode = f"{user_id}:{api_key}"
    encoded_value = b64e(bytearray(string_to_encode, encoding='utf-8'))
    print(f"Xray Auth Key: {encoded_value}")


if __name__ == '__main__':
    generate_xray_auth_key()
    pass
