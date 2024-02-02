import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    print("Connection returned result: " + str(rc))

def on_disconnect(client, userdata, rc):
    if rc != 0:
        print('Unexpected Disconnect')
    else:
        print('Expected Disconnect')

def on_message(client, userdata, message):
    result = str(message.payload, 'utf-8')
    print(f"Result received: {result}")

client = mqtt.Client()
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message

client.connect_async('mqtt.eclipseprojects.io')
client.loop_start()

player_name = "player1"
topic = f"rps/{player_name}"

while True:
    move = input("Enter your move (r for rock, p for paper, s for scissors): ")
    if (move == "q"):break
    client.publish(topic, move, qos=1)
    print(f"Move '{move}' sent to referee.")
