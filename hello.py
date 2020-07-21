import os

import redis
from flask import Flask, render_template, request, jsonify
import json
import time

from werkzeug.utils import secure_filename

app = Flask(__name__)
app.debug = True


# @app.route('/')
# def index():
#     return render_template('home.html')
# 根据键值读字符串
def get_values(r, key):
    return eval(r.get(key))

# dic 字典
def set_values(r, key, dic):
    r.set(key, str(dic))


def remove_key(r, key):
    r.delete(key)


# callback_obj字典对象
def write_queue(r,queue_name, callback_obj):
    callback_obj = json.dumps(callback_obj)
    callback_mapping = {
        callback_obj: time.time()
    }
    r.zadd(queue_name, callback_mapping)


def read_queue(r,queue_name):
    range_list = r.zra0nge(queue_name, 0, 1)
    if range_list:
        set_del_task = range_list[0]
        set_del_task = json.loads(set_del_task)
        return set_del_task

def read_all_queue(r,queue_name,num):
    range_list = r.zrange(queue_name, 0, num)
    list = []
    if range_list:
        for data in range_list:
        # set_del_task = range_list[0]
            set_del_task = json.loads(data)
            list.append(set_del_task)
        return list

def remove_queue(r,queue_name, callback_obj):
    callback_obj = json.dumps(callback_obj)
    r.zrem(queue_name,callback_obj)

def read_queue_num(r, queue_name):
    list = r.zrange(queue_name,0,-1)
    return len(list)
def init_redis():
    pwd = "anlly12345"
    host = '192.168.31.184'
    host = 'localhost'
    pwd = ''
    redis_obj = redis.Redis(host=host, port=6379, password=pwd, db=8, decode_responses=True)
    return redis_obj


def read_jsonfile(filename):
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf8')as fp:
            json_data = json.load(fp)

            return json_data
    else:
        # 文件名不存在，写入日志
        print("文件不存在")
        return False



@app.route('/')
def home():
    return render_template('test1.html')




@app.route('/info', methods=['GET', 'POST'])
def info():
    # r = init_redis()
    # r = redis.Redis(host='localhost', port=6379,db=8, decode_responses=True)
    # 获取到完成队列的列表
    # datas = r1.zrange("finish_queue",0,10)

    datas = read_all_queue(r,"finish_queue",2)
    list = []
    for data in datas:
        temp = get_values(r, data)
        list.append(temp)
    datas = list

    print("---: ", request.form) # 获取到post携带的参数
    return jsonify(datas)    # 返回10个成功的列表

@app.route('/wait_list', methods=['GET', 'POST'])
def wait_list():
    datas = read_all_queue(r,"wait_queue",2)
    if datas:
        list = []
        for data in datas:
            temp = get_values(r, data)
            list.append(temp)
        datas = list

    print("---: ", request.form) # 获取到post携带的参数
    return jsonify(datas)    # 返回10个成功的列表


@app.route('/fail_list', methods=['GET', 'POST'])
def fail_list():
    # r = init_redis()
    # r = redis.Redis(host='localhost', port=6379,db=8, decode_responses=True)
    # 获取到完成队列的列表
    # datas = r1.zrange("finish_queue",0,10)

    datas = read_all_queue(r,"fail_queue",2)
    if datas:
        list = []
        for data in datas:
            temp = get_values(r, data)
            list.append(temp)
        datas = list

        print("---: ", request.form) # 获取到post携带的参数
    return jsonify(datas)    # 返回10个成功的列表

@app.route('/queue_num', methods=['GET', 'POST'])
def queue_num():
    # 获取三个队列的数量

    dic = {
        "finish_quque":"",
        "wait_queue":"",
        "fail_queue":""
    }
    dic = {}
    dic['finish_queue'] = read_queue_num(r,"finish_queue")
    dic["wait_queue"] = read_queue_num(r,"wait_queue")
    dic['fail_queue'] = read_queue_num(r,"fail_queue")

    return jsonify(dic)


@app.route('/config_file', methods=['GET', 'POST'])
def config_file():
    # 读取配置文件，并可以修改配置
    # 读取配置文件，返回数据，分两种情况，
    # 一种是get，即读取文件进行显示，
    # 一种是post，需要修改参数的
    if request.method == "GET":
        # 读取json数据，并返回
        filename = os.path.join('D:', '\\Code', 'FlaskCode', 'config.json')
        dic = read_jsonfile(filename)

    elif request.method == "POST":
        # 读取表格提交的数据，并写入
        dic = request.get_json()
        dic = dic
        print(dic)
        # 写入data文件
        with open('data.json', 'w') as f:
            json.dump(dic, f)
        # 写入文件

    #print(os.getcwd()) # 打印当前路径 D:\MyProgram\PyCharm 2020.1.3\jbr\bin

    # print(filename)
    # try:
    #     with open(filename) as f:
    #         jsonStr = json.load(f)
    #         return json.dumps(jsonStr)
    # except Exception as e:
    #     return jsonify({"code": "异常", "message": "{}".format(e)})

    return jsonify(dic)


@app.route('/status',methods=['GET','POST'])
def status():
    # r = redis.StrictRedis(host='localhost', port=6379, db=8, decode_responses=True)

    # r = redis.Redis(host='localhost', port=6379, db=8, decode_responses=True)
    range_list = r.zrange("status_queue", 0, -1)
    # set_del_task = json.loads(range_list)
    # data = read_queue(r,"status_queue")
    range_list.append('hello world')

    datas = read_all_queue(r, "status_queue", 2)
    list = []
    for data in datas:
        temp = get_values(r, data)
        list.append(temp)

    return jsonify(list)

if __name__ == '__main__':
    r = redis.StrictRedis(host='localhost', port=6379, db=8, decode_responses=True)

    # r = redis.Redis(host='localhost', port=6379, db=8, decode_responses=True)

    app.run()

