from flask import Flask
from flask import request, render_template, json

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
        print("Audio data is:" + data_json.get('audio'))
        print("Motion data is:" + data_json.get('motion'))
        print(data_json)

    print(request.args.get("temp"))
    print(request.args.get("humidity"))
    global cur_temp, cur_humidity
    cur_temp = str(request.args.get('temp'))
    cur_humidity = str(request.args.get('humidity'))


@app.route("/get")
def get_stat():
    return f"Current temp: {cur_temp}\n Current humidity: {cur_humidity}"
