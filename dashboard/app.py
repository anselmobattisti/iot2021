from flask import Flask, render_template
from flask_mqtt import Mqtt

app = Flask(__name__)
app.config['MQTT_BROKER_URL'] = 'broker.hivemq.com'
app.config['MQTT_BROKER_PORT'] = 1883

mqtt = Mqtt(app)
FILE_NAME = "data.txt"

@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    mqtt.subscribe('iot2021/estudante1')

@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    text_file = open(FILE_NAME, "w+")
    n = text_file.write(message.payload.decode())
    text_file.close()

@app.route('/')
def index():
    mf = open(FILE_NAME, "r+")
    file_content = mf.readlines()
    print(file_content)
    return str(file_content)