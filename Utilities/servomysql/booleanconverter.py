def boolean_converter(value):
    if value == '0' or value == 0 or value == 'False':
        return False
    elif value == '1' or value == 1 or value == 'True':
        return True
    elif value is True:
        return 1
    elif value is False:
        return 0
    elif isinstance(value, str):
        return value
