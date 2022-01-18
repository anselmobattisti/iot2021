from fastapi import FastAPI
from paho import mqtt
from fastapi_mqtt import FastMQTT, MQTTConfig
import re

mqtt_broker = 'broker.mqttdashboard.com'
mqtt_port = 1883
mqtt_topic = "iot2022/estudante1"
FILE_NAME = "data.txt"

app = FastAPI()

fast_mqtt = FastMQTT(config=MQTTConfig(host = mqtt_broker, port= mqtt_port, keepalive = 60))

fast_mqtt.init_app(app)

# Mensagem de conecção
@fast_mqtt.on_connect()
def connect(client, flags, rc, properties):
    # fast_mqtt.client.subscribe("/mqtt") #subscribing mqtt topic 
    print("Connected: ", client, flags, rc, properties)

# Quando uma mensagem é postada no tópíco
@fast_mqtt.on_message()
async def message(client, topic, payload, qos, properties):
    print("Received message: ",topic, payload.decode(), qos, properties)
    return 0

# Mensagem de desconexão
@fast_mqtt.on_disconnect()
def disconnect(client, packet, exc=None):
    print("Disconnected")

# Mensagem de subscrição
@fast_mqtt.on_subscribe()
def subscribe(client, mid, qos, properties):
    print("subscribed", client, mid, qos, properties)

# Subscrição em um determinado tópíco
@fast_mqtt.subscribe(mqtt_topic)
async def get_topic_data(client, topic, payload, qos, properties):
    print("data: ", topic, payload.decode(), qos, properties)
    text_file = open(FILE_NAME, "w+")
    n = text_file.write(payload.decode())
    text_file.close()    
    return 0

@app.get("/getdata")
async def get_data():
    mf = open(FILE_NAME, "r+")
    file_content = mf.readlines()
    angle = re.findall( r'\d+\.*\d*', str(file_content))    
    return {float(angle[0])}

# @app.get("/post")
# async def post_data():
#     fast_mqtt.publish(mqtt_topic, "Hello from Fastapi") #publishing mqtt topic 
#     return {"result": True,"message":"Published" }
