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
    id2 = request.form.get("id2")
    roomname = "private chat"
    query10 = "SELECT username FROM user where id="+id1
    db.cursor.execute(query10)
    name1 = db.cursor.fetchall()
    query11 = "SELECT username FROM user where id="+id2
    db.cursor.execute(query11)
    if(db.cursor.rowcount==0):
        return jsonify(status="ERROR", message="User do not exist")
    name2 = db.cursor.fetchall()
    name11 = str(name1)
    name22 = str(name2)
    name111 = name11[16:-4]
    name222 = name22[16:-4]
    name3 = name111+" & "+name222
    query = "INSERT INTO chatrooms(name) values ('"+name3+"') "
    db.cursor.execute(query)
    db.db.commit()
    query1 = "SELECT chatroomlist FROM user where id="+id1
    db.cursor.execute(query1)
    chatroomlist1 = db.cursor.fetchall()
    query4 = "SELECT chatroomlist FROM user where id="+id2
    db.cursor.execute(query4)
    chatroomlist2 = db.cursor.fetchall()
    #chatlist1 = chatroomlist1[0].chatroomlist.spilt(',')
    query3 = "select id from chatrooms order by id DESC limit 1"
    db.cursor.execute(query3)
    roomid = db.cursor.fetchall()

    chatroomlist111 = str(chatroomlist1)
    chatroomlist222 = str(chatroomlist2)
    roomid1 = str(roomid)
    chatroomlist11 = chatroomlist111[20:-4]
    chatroomlist22 = chatroomlist222[20:-4]
    chatlist1 = chatroomlist11.split(',')
    chatlist2 = chatroomlist22.split(',')
    chatlist3 = set(chatlist1).intersection(set(chatlist2))
    repeat = len(chatlist3)
    if(repeat>1):
        return jsonify(status = "ERROR",message = "Already friends")
    roomid11 = roomid1[7:-4]
    newchat = chatroomlist11+','+roomid11
    query5 = "update user set chatroomlist ='"+newchat+"' where id ="+id1
    db.cursor.execute(query5)
    db.db.commit()
    newchat2 = chatroomlist22+','+roomid11
    query6 = "update user set chatroomlist ='"+newchat2+"' where id ="+id2
    db.cursor.execute(query6)
    db.db.commit()
    return jsonify(status = "OK",message = "success",data={'name':name3,'chat':newchat})


@app.route('/api/assgn3/register',methods=['POST'])
def register():
    my_db = condb.MyDataBase()
    name = request.form.get("username")
    password = request.form.get("password")
    query3 = "SELECT id, chatroomlist FROM user where username ='"+name+"'"
    my_db.cursor.execute(query3)
    rowa = my_db.cursor.fetchall()
    if(my_db.cursor.rowcount==1):
        return jsonify(status="ERROR", message="Repeat Username")

    if name == None or password == None:
        return jsonify(status="ERROR", message="missing parameters")

    query = "INSERT INTO user(username,password) values(%s,%s)"
    parameters = (name,password)
    my_db.cursor.execute(query,parameters)
    my_db.db.commit()

    query9 = "SELECT id, chatroomlist FROM user where username ='"+name+"'"
    my_db.cursor.execute(query9)
    rowa = my_db.cursor.fetchall()
    return jsonify(status="OK",message = "success", data = rowa[0])

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

@app.route('/api/assgn3/users',methods=['GET'])

def get_users():
    db = condb.MyDataBase()
    query = "SELECT * FROM user"

    db.cursor.execute(query)
    #get the result(rows)
    rows = db.cursor.fetchall()
    data = []
    data = rows
    return jsonify(status = "OK",data=data)

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
