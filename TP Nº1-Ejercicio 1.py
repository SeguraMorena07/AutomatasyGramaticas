import re


def validate_string(string):
    match = re.findall(r'\w', string)
    search = re.search(r'[a-zA-Z]', string)
    if search:
        print('TRUE')
    else:
        print('FALSE')

    for i in string:
        if i in match:
            print('TRUE')
        else:
            print('FALSE')

    if len(string) >= 8:
        print('TRUE')
    else:
        print('FALSE')


validate_string(str(input('Ingrese una cadena: ')))
