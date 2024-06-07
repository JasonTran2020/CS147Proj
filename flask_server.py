import datetime

from flask import Flask
from flask import request, render_template, json, jsonify

from sqllite_client import get_all_device_records, insert_recording, get_all_devices, get_all_within_day

app = Flask(__name__)

cur_temp = None
cur_humidity = None


@app.route("/")
def hello():
    print(request.args.get("var"))
    return render_template("home.html")


@app.route("/post", methods=['POST'])
def set_stat():
    if request.method == 'POST':
        data_json = request.json
        audio, motion, id = int(data_json.get('audio')), int(data_json.get('motion')),int(data_json.get('id'))
        print("Audio data is:" + str(data_json.get('audio')))
        print("Motion data is:" + str(data_json.get('motion')))
        print("id is:" + str(data_json.get('id')))
        print(data_json)
        insert_recording(id,audio,motion)
        return "Posted"


@app.route("/get")
def get_stat():
    id = request.args.get("id")
    if (request.args.get("id") is None):
        id = 1
    id = int(id)
    date = None
    if (request.args.get("rdate") is None):
        date = datetime.datetime.now(tz=datetime.timezone.utc)
    else:
        offset = request.args.get("tzoffset")
        if offset is None:
            date = datetime.datetime.strptime(request.args.get("rdate") +" 23:59:59+00:00","%Y-%m-%d %H:%M:%S%z")
        else:
            offset = int(offset)//60
            if offset < 10:
                offset = "0"+str(offset)
            print(offset)
            if (offset> 0):
                date = datetime.datetime.strptime(request.args.get("rdate") + " 23:59:59-"+offset+":00", "%Y-%m-%d %H:%M:%S%z")
            else:
                date = datetime.datetime.strptime(request.args.get("rdate") + " 23:59:59+" + offset + ":00",
                                                  "%Y-%m-%d %H:%M:%S%z")
    record_list = get_all_within_day(id,date)
    return jsonify(record_list)

@app.route("/get_devices")
def get_devices():
    device_list = get_all_devices()
    return jsonify(device_list)
