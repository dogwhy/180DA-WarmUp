import paho.mqtt.client as mqtt

result_received = False  # Flag to indicate when the result is received

def on_connect(client, userdata, flags, rc):
    client.subscribe("rps/player1/result", qos=1)

def on_disconnect(client, userdata, rc):
    if rc != 0:
        print('Unexpected Disconnect')
    else:
        print('Expected Disconnect')

def on_message(client, userdata, message):
    global result_received
    result = str(message.payload, 'utf-8')
    if result == 'win':
        print("You won!")
    elif result == 'lose':
        print("You lose!")
    elif result == 'draw':
        print("It's a draw!")
    result_received = True  # Set the flag to indicate that the result is received

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
    if move == "q":
        break
    client.publish(topic, move, qos=1)
    
    # Wait for the other player to make a move
    result_received = False  # Reset the flag
    while not result_received:
        pass  # Wait until the result is received

print("Round completed. Make another move or 'q' to quit.")
