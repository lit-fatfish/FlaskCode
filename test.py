import json
import os

def read_jsonfile(filename):
    if os.path.isfile(filename):
        with open(filename, 'r', encoding='utf8')as fp:
            json_data = json.load(fp)

        return json_data
    else:
        # 文件名不存在，写入日志
        print("文件不存在")
        return False



print(os.path.exists('static/config.json'))

with open('static/config.json', 'r', encoding='utf8') as fp:
    json_data = json.load(fp)

    print(json_data)

print(read_jsonfile('static/config.json'))

