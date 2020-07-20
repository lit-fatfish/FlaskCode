import json
import redis
from flask import Flask, render_template, request, jsonify
import json
import time

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
    range_list = r.zrange(queue_name, 0, 1)
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



# @app.route('/')
# @app.route('/<name>')
# def manager(name=None):
#     r = redis.Redis(host='localhost', port=6379, decode_responses=True)
#     # 获取到完成队列的列表
#     data = r.zrange("finish_queue",0,10)
#     print(data)
#     id_str = read_queue(r,"finish_queue")
#     dic = {}
#     dic["data_id"] = id_str
#     dics = {
#         "hello":"hello",
#         "world":"world"
#     }
#     return render_template('manager.html', name=name, dic=dic, data=data,dics=dics)
# @app.route('/')
# def home():
#     return  render_template('manager.html')

@app.route('/')
def home():
    return render_template('test1.html')


@app.route('/info', methods=['GET', 'POST'])
def info():
    r1 = redis.StrictRedis(host='localhost', port=6379, db=8, decode_responses=True)
    # r = redis.Redis(host='localhost', port=6379,db=8, decode_responses=True)
    # 获取到完成队列的列表
    # datas = r1.zrange("finish_queue",0,10)

    datas = read_all_queue(r,"finish_queue",2)
    print(datas)
    list = []
    for data in datas:
        temp = get_values(r, data)
        list.append(temp)
    # print(type(list))
    # print(list)
    # datas = str(list)
    # datas = json.dumps(datas)
    # print(type(datas))
    # print(datas)
    # datas = read_queue(r,"finish_queue")
    # datas = get_values(r, datas)

    datas = list

    print("---: ", request.form) # 获取到post携带的参数
    return jsonify(datas)    # 返回10个成功的列表


@app.route('/status',methods=['GET','POST'])
def status():
    r = redis.StrictRedis(host='localhost', port=6379, db=8, decode_responses=True)

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

