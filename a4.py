from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit, join_room, leave_room, send
app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'iems5722'
socketio = SocketIO(app)
@app.route("/api/a4/broadcast_room", methods=["POST"])
def broadcast_room():
    chatroom_id = request.form['chatroom_id']
    message = request.form['message']
    name = request.form['name']
    user_id = request.form['user_id']
    time = request.form['time']
    data={'chatroom_id' : chatroom_id, 'message' : message, 'name' :name,'user_id':user_id,'time':time}
    print('Sent')
    socketio.emit('messages',data,broadcast = True)
    if chatroom_id != None and message != None:
        return jsonify(status="OK")
    else:
        return jsonify(status="ERROR", messages="Input is Null")
@socketio.on('my event')
def my_event_handler(data):
    emit('messages',data,broadcast = True)
    print('send2')

@socketio.on('join')
def on_join(data):
    username = data['username']
    chatroom=data['chatroom_id']
    join_room(chatroom_id)
    print('Client join')
    socketio.emit('join',username+' entered the room.',chatroom_id = chatroom_id)
@socketio.on('leave')
def on_leave(data):
    username = data['username']
    chatroom=data['chatroom_id']
    leave_room(chatroom_id)
    send(username+' left the room.',chatroom_id = chatroom_id)

@socketio.on('connect')
def connect_handler():
    print('Client connected')

@socketio.on('disconnect')
def disconnect_handler():
    print('Client disconnected')

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=8001)