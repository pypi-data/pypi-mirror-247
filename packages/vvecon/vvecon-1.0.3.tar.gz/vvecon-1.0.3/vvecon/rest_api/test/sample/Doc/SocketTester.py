import socketio
from dotenv import load_dotenv
from os import environ

load_dotenv("../.env")

# Initialize a Socket.IO client instance
sio = socketio.Client()


# Define a function to be executed when the 'connect' event is received
@sio.on('connect', namespace="/user")
def on_connect():
    user_data = {
        'host': environ.get("USER"),
        'api_key': environ.get("USER_API_KEY"),
    }
    sio.emit('login', user_data, namespace="/user")
    print('Connected to server')


@sio.on('message', namespace='/user')
def on_message(data):
    print("message", data)


@sio.on('abort', namespace='/user')
def on_abort(data):
    print("abort", data)


# Connect to the Socket.IO server
sio.connect('http://ip_addr/user')

# Keep the script running to maintain the connection
sio.wait()
