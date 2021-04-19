from flask import Flask, jsonify, g, request
import condb
import math
import time
app = Flask(__name__)
@app.route('/api/a3/get_chatrooms', methods=["GET"])
def get_chatrooms():
    mydb= condb.MyDataBase()
    query = "SELECT * FROM `iems5722`.`chatrooms`"
    mydb.cursor.execute(query)
    chatrooms = mydb.cursor.fetchall()
    return jsonify(status="OK", data=chatrooms)

@app.route('/api/assgn3/add_friends',methods=['POST'])
def add_friends():
    db = condb.MyDataBase()
    id1 = request.form.get("id1")
    query2 = "SELECT username FROM where id="+id1
    parameters = ("private chat")
    query = "INSERT INTO chatrooms (name) values (%s)"
    db.cursor.execute(query,parameters)
    db.db.commit()
    query1 = "SELECT user FROM where id="+id1
    db.cursor.execute(query1)
    chatroomlist1 = db.cursor.fetchall()
    query3 = "select id from chatrooms order by id DESC limit 1;"
    db.cursor.execute(query3)
    query5 = "update user set chatroomlist (%s) where id ="+id1
    p = newchat
    db.cursor.execute(query5,p)
    db.db.commit()
    roomid = db.cursor.fetchall()
    chatroomlist1 = chatroomlist1 + roomid
    return jsonify(status = "OK",data=chatroomlist1)

@app.route('/api/a3/get_messages', methods=["GET"])
def get_messages():
    mydb= condb.MyDataBase()
    chatroom_id = request.args.get('chatroom_id',default=1,type = int)
    page = request.args.get('page',default = 1, type = int)
    query = "SELECT * FROM `iems5722`.`messages` WHERE chatroom_id = %s ORDER BY id DESC LIMIT 5 Offset %s"
    params = (chatroom_id,5*(page-1),)
    mydb.cursor.execute(query,params)
    messages2 = mydb.cursor.fetchall()
    query2 = "SELECT MAX(id) FROM `iems5722`.`messages`"
    mydb.cursor.execute(query2)
    total = mydb.cursor.fetchall()
    total = total[0]
    total = total["MAX(id)"]
    datajson = {
            'current_page' :page,
            'messages' :messages2,
            'total_page' :total}
    if messages2 is None:
        return jsonify(stsaus="ERROR", messages="NOT FOUND")
    else:
        return jsonify(status="OK", data=datajson)

@app.route('/api/a3/send_message', methods=["POST"])
def send_message():
    print('received')
    mydb= MyDatabase()
    chatroom_id = request.form['chatroom_id']
    user_id = request.form['user_id']
    name = request.form['name']
    message = request.form['message']
    query = "INSERT INTO `iems5722`.`messages`(`chatroom_id`,`user_id`,`name`,`message`,`message_time`) VALUES (%s,%s,%s,%s,now());"
    params=(chatroom_id,user_id,name,message,)
    mydb.cursor.execute(query,params)
    mydb.conn.commit()
    current_time = time.strftime('%A %B, %d %Y %H:%M:%S')
    url ="http://localhost:8001/api/a4/broadcast_room"
    data = {'chatroom_id': chatroom_id,'message':message,'name':name,'user_id':user_id,'time':current_time}
    r = requests.post(url,data=data)
    print(str(r.status_code))
    if r.status_code!= 200:
        return jsonify(status="ERROR")
    else:
        return jsonify(status="OK")

if __name__ == '__main__':
    app.run(host='0.0.0.0')
