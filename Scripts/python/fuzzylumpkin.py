
from fuzzywuzzy import


def get_version():
    r = fuzz.ratio("this is a test", "is this a test")
    print(r)

if __name__ == '__main__':
    get_version()
    pass
