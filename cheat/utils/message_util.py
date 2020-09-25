import paho.mqtt.client as mqtt

from utils.log import log


def on_connect(self, client, userdata, flags, rc):
    print("Connected with result code: " + str(rc))
    log.info("客服端:" + str(client))


def on_message(self, client, userdata, msg):
    print(msg.topic + " " + str(msg.payload,encoding="utf-8"))
    log.debug("发送了一条消息")


def on_subscribe(self, client, userdata, mid, granted_qos):
    print("On Subscribed: qos = %d" % granted_qos)
