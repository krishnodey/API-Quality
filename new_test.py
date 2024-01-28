import json
out_dir = './Outputs-REST-APIs/Adobe Audience Manager-CRUDyURI.txt'
in_dir = './REST-APIs/Adobe Audience Manager/Adobe Audience Manager.txt'

in_data = {}

with open(in_dir) as f:
    lines = f.read().strip().split("\n")
    for line in lines:
        method, uri, des = line.strip().split(">>")
        in_data[uri.strip()] = [method.strip(), des.strip()]

data = []

with open(out_dir) as f:
    lines = f.read().strip().split("\n")
    for line in lines:
        if line.strip().startswith('/'):
            nd = line.strip().split("\t")
            print(nd)
            if len(nd) == 3:
                uri = nd[0].strip()
                pname = nd[1].strip()
                comment = nd[2].strip()
            else:
                uri = nd[0].strip()
                pname = nd[1].strip()
                comment = ''
            #uri = uri.strip()
            if uri in in_data:
                #if method == in_data[uri][0]:
                d = {}
                d['uri'] = uri
                d['method'] = in_data[uri][0]
                d['description'] = in_data[uri][1]
                d['pattern_name'] = pname.strip()
                d['comment'] = comment
                data.append(d)
            else:
                print(f'URI not found: {uri}')


with open('test_out.jsonl', 'w') as f:
    for row in data:
        f.write(json.dumps(row) + "\n")

        

