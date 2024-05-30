from flask import Flask
from flask import request, render_template, json, jsonify

from sqllite_client import get_all_device_records,insert_recording

app = Flask(__name__)

cur_temp = None
cur_humidity = None


@app.route("/")
def hello():
    print(request.args.get("var"))
    return "We received value: " + str(request.args.get("var"))


@app.route("/post", methods=['POST'])
def set_stat():
    if request.method == 'POST':
        data_json = request.json
        audio, motion, id = data_json.get('audio'), data_json.get('motion'),data_json.get('id')
        print("Audio data is:" + data_json.get('audio'))
        print("Motion data is:" + data_json.get('motion'))
        print("id is:" + data_json.get('id'))
        print(data_json)
        insert_recording(id,audio,motion)
        


@app.route("/get")
def get_stat():
    id = int(request.args.get("id"))
    record_list = get_all_device_records(id)
    return jsonify(record_list)
