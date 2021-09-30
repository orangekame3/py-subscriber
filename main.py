import paho.mqtt.client
import ssl
import subprocess
import json
import plot

Endpoint = "xxxxxxxxxxxxxxxxxxxxx.iot.ap-northeast-1.amazonaws.com"
Port = 8883
SubTopic = "topic/to/subscribe"
RootCAFile = "AmazonRootCA1.pem"
CertFile = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx-certificate.pem.crt"
KeyFile = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx-private.pem.key"


def on_connect(client, userdata, flags, respons_code):
    print("connected")
    client.subscribe(SubTopic)


def on_message(client, userdata, msg):
    print("received:" + msg.payload.decode("utf-8"))
    data = json.loads(msg.payload.decode("utf-8"))
    message = plot.worker()
    cmd = ["./alexa_remote_control.sh", "-e", "speak:" + message]
    res = subprocess.call(cmd)


if __name__ == '__main__':
    client = paho.mqtt.client.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.tls_set(
        RootCAFile,
        certfile=CertFile,
        keyfile=KeyFile,
        cert_reqs=ssl.CERT_REQUIRED,
        tls_version=ssl.PROTOCOL_TLSv1_2,
        ciphers=None)
    client.connect(Endpoint, port=Port, keepalive=60)
    client.loop_forever()