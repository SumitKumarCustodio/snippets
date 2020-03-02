import json
import os

def flatten_json(y):
    # Flatten json/dict
    out = {}

    def flatten(x, name='', title=''):
        if type(x) is dict:
            for a in x:
                flatten(x[a], name + a + '_', a)
        elif type(x) is list:
            i = 0
            for a in x:
                flatten(a, name + str(i) + '_', str(i))
                i += 1
        else:
            out[title] = x

    flatten(y)
    return out

def convert_time(line):
    # Convert _time to @timestamp, as _time gets in problem when parsed by splunk
    data = json.loads(line)
    data = flatten_json(data)
    if '_time' in data.keys():
        data['@timestamp'] = data['_time']
        data.pop('_time')
    final = json.dumps(OrderedDict(sorted(data.items()))).encode('utf-8')
    return final

def parse_json(inp):
    if not inp.endswith('.json'):
        # Not a json file
        return False

    if inp.endswith('_py.json'):
        # Already parsed
        return False

    output = os.path.splitext(inp)[0] + '_py.json'

    f = open(inp, 'rb')
    g = open(output, 'wb')

    for line in f.readlines():
        data = convert_time(line)
        g.write(data)
        #data = json.loads(line)
        #g.write(json.dumps(flatten_json(data)).encode('utf-8'))
        g.write(b'\n')

    f.close()
    g.close()
    return True

def tree(path=''):
    contents = os.listdir(path)
    for content in contents:
        fullpath = os.path.join(path, content)
        if os.path.isdir(fullpath):
            # recursive
            tree(fullpath)
        elif os.path.isfile(fullpath):
            result = parse_json(fullpath)
            if result == True:
                # Delete original file
                os.remove(fullpath)

if __name__=="__main__":
    tree('.')