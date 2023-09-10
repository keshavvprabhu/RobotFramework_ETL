import zlib
from base64 import urlsafe_b64decode as b64d


def decode_value(data):
    credential = zlib.decompress(b64d(data))
    credential = credential.decode('utf-8')
    return credential


if __name__ == '__main__':
    pass
