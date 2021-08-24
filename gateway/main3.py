import socket
import time
import paho.mqtt.publish as publish

mqtt_broker = 'broker.mqttdashboard.com'
mqtt_port = 1883
mqtt_topic = "iot2021/estudante1"

HOST = ''
PORT = 5555

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind((HOST, PORT))
        print('Aguardando dados ...')
        while (1):
            message, address = s.recvfrom(8192)
            ts = int(time.time())
            print(message)
            if ts%5 == 0:
                sensor_data = str(message).split(",")
                timestamp = sensor_data[0].replace("b'", "")
                y_pos = sensor_data[3]
                msg = "t:{},y:{}".format(timestamp,y_pos)
                publish.single(mqtt_topic, msg, hostname=mqtt_broker, port=mqtt_port)
                print(msg)

if __name__ == "__main__":
    main()