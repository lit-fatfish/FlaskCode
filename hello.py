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


def remove_queue(r,queue_name, callback_obj):
    callback_obj = json.dumps(callback_obj)
    r.zrem(queue_name,callback_obj)



@app.route('/')
@app.route('/<name>')
def manager(name=None):
    r = redis.Redis(host='localhost', port=6379, decode_responses=True)
    # 获取到完成队列的列表
    data = r.zrange("finish_queue",0,10)
    print(data)
    id_str = read_queue(r,"finish_queue")
    dic = {}
    dic["data_id"] = id_str
    dics = {
        "hello":"hello",
        "world":"world"
    }
    return render_template('manager.html', name=name, dic=dic, data=data,dics=dics)

@app.route('/test', methods=['POST'])
def test():
    print("---: ", request.form)
    return jsonify({"a":1})


if __name__ == '__main__':
    r = redis.Redis(host='localhost', port=6379, decode_responses=True)
    app.run()

