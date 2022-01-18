from turtle import position
from fastapi import FastAPI
from paho import mqtt
from fastapi_mqtt import FastMQTT, MQTTConfig
import re
import haversine as hs
from haversine import Unit

import sqlite3
con = sqlite3.connect('/home/battisti/versionado/iot2022/dashboard/position')
cur = con.cursor()

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
    text_file = open(FILE_NAME, "a+")
    n = text_file.write(payload.decode()+"\n")
    text_file.close()
    latlng = payload.decode().split(",")
    sql_str = "INSERT INTO position VALUES ('{}','{}')".format(latlng[0], latlng[1])
    cur.execute(sql_str)
    con.commit()
    loc1=(-22.9045472,-43.1310969)
    loc2=(float(latlng[0]), float(latlng[1]))
    distance = hs.haversine(loc1,loc2,unit=Unit.METERS)
    print(distance)

    return 0

@app.get("/getdatasqlite")
async def get_data():
    sql_str = "SELECT * FROM position"
    rows = []
    for row in cur.execute(sql_str):
        rows.append({
            "lat": float(row[0]),
            "lng": float(row[1]),
        })    
    return rows
    # mf = open(FILE_NAME, "r+")
    # file_content = mf.readlines()
    # angle = re.findall( r'\d+\.*\d*', str(file_content))    
    # return {float(angle[0])}


@app.get("/getdist")
async def get_data():
    sql_str = "SELECT * FROM position"
    rows = []

    loc1=(-22.9045472,-43.1310969)
    
    cont = 0

    for row in cur.execute(sql_str):
        cont += 1

        if cont % 10 == 0:

            loc2=(float(row[0]), float(row[1]))
            distance = hs.haversine(loc1,loc2,unit=Unit.METERS)        

            rows.append({
                "cont": cont,
                "dist": distance
            })    

    return rows
    # mf = open(FILE_NAME, "r+")
    # file_content = mf.readlines()
    # angle = re.findall( r'\d+\.*\d*', str(file_content))    
    # return {float(angle[0])}


@app.get("/getdata")
async def get_data():
    mf = open(FILE_NAME, "r+")
    file_content = mf.readlines()
    # return file_content

    ret_pos = []

    for line in file_content:
        aux = line.replace("\n","")
        aux = aux.split(",")
        ret_pos.append({
            "lat": float(aux[0]),
            "lng": float(aux[1]),
        })

    return ret_pos
    # angle = re.findall( r'\d+\.*\d*', str(file_content))    
    # return {float(angle[0])}

# @app.get("/post")
# async def post_data():
#     fast_mqtt.publish(mqtt_topic, "Hello from Fastapi") #publishing mqtt topic 
#     return {"result": True,"message":"Published" }


@app.get("/teste")
async def teste():
    return {"data": 25, "idade":90}