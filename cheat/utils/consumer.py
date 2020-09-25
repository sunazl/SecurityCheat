import paho.mqtt.client as mqtt

from utils.log import log


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        log.info("连接远程服务器成功,code:%s", str(rc))
        print(client)
    else:
        log.error("连接远程服务器失败,代码:%s", str(rc))


def on_message(client, userdata, msg):
    log.debug("接收到来自:%s的消息")
    print(msg.topic + " " + str(msg.payload, encoding="utf-8"))


client = mqtt.Client("consumer")
client.on_connect = on_connect
client.on_message = on_message

client.connect('sunazl.cn', 1883, 600)  # 600为keepalive的时间间隔
client.subscribe('test_topic', qos=1)
client.subscribe('test', qos=1)
client.loop_forever()  # 保持连接
