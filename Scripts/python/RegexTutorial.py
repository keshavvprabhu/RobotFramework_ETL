import re


# re.compile()
str1 = """
abcdefghijklmnopqrstuvwxyz abcwelrtu-0werim\
ABCDEFGHIJKLMNOPQRSTUVWXYZ

0123456789

!@#%^@$%*$^&(
437-991-8011
(647) 821 5964

"""
pattern = re.compile(r'\d', re.I)

matches = pattern.finditer(str1)

for match in matches:
    print(match[0])