import paho.mqtt.client as mqtt


# Callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connection returned result: " + str(rc))

# Callback of the client when it disconnects.
def on_disconnect(client, userdata, rc):
    if rc != 0:
        print('Unexpected Disconnect')
    else:
        print('Expected Disconnect')

# Default message callback (won’t be used if only publishing, but can still exist)
def on_message(client, userdata, message):
    print('Received message: "' + str(message.payload) + '" on topic "' +
          message.topic + '" with QoS ' + str(message.qos))

# Create a client instance.
client = mqtt.Client()

# Add callbacks to the client.
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message

# Connect to a broker using one of the connect*() functions.
client.connect_async('mqtt.eclipseprojects.io')

# Start the loop to maintain network traffic flow with the broker.
client.loop_start()

# Use input() to get user input for the message
while(1):
    user_input = input("Say something ('end' to stop): ")
    if (user_input == "end"): break
    print('Publishing...')
    client.publish("sharpiespeaks", user_input, qos=1)

client.loop_stop()
client.disconnect()