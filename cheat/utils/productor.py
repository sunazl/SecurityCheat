import paho.mqtt.client as mqtt

client = mqtt.Client("productor")
client.connect('sunazl.cn', 1883, 600)  # 600为keepalive的时间间隔
client.publish('test_topic', payload='你好老白', qos=1)
client.publish('test', payload='你好老白2', qos=1)
