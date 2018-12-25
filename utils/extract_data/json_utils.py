import json


def write_json_to_file(data, path):
    if not isinstance(path, basestring):
        raise ValueError('second arg to write_json_to_file must be path')

    with open(path, 'w+') as out_file:
        json.dump(data, out_file, indent=4)
