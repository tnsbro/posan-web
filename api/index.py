from flask import Flask
from flask import request #브라우저의 요청을 처리하기 위한 클래스
from datetime import datetime, timezone
from flask import session
from datetime import timedelta
from functools import wraps
from flask import jsonify
from flask_cors import CORS
import pyrebase
import json
import firebase_admin
from firebase_admin import credentials, firestore, storage
import bcrypt
import os
from flask import session
from flask_session import Session
import uuid
import requests
from bs4 import BeautifulSoup
from google.api_core.datetime_helpers import DatetimeWithNanoseconds
from bson import ObjectId


cred = credentials.Certificate({
  "type": "service_account",
  "project_id": "rooky-de20b",
  "private_key_id": "3e0a9571b00b025a391573c460f020fb50c29749",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCjojJMqEyOnUDs\n82nyhwl7SSryeso8rmqA4E5ROCQY55dpTnl8rx5T4bcx5QnSmZCwEwY/A3T8Dn1l\nTvjzi4TZRiRG7DgHxWEhbup1rJvg1H9dKfjGltIdlKUY4EluiosgB6Y5e88zwRgR\n+3ZrxrBFxWZLVQFEVYgtagYVmiod4vcwQXHGb/aLLhjwG/zJpOqq97YQaQ6nZ2eD\nWr1ITfn/zwc/P1r+NXr7o0QkcBwgJPr5oV/SzSGl5ctF+WeOu8rxyl3zTvgQcI6k\nYm+S2w1hkwq4CQq5WCF0xKdkae/fIYYVelfO8E8wordc4iA01nt9YPtNmo4utKQ+\ngAK2mU5zAgMBAAECggEAFHlO4diM+6shXIR4VSggP5TAEubaNw17tfRa2D62BYe0\nojB3cupWWRh823lU6UzdlapLtcaw9Hi7p9lhvNdQH/9uupED0bUYmh5Op7qZJmBw\nLy/5OJ/WWm0m2x31EiezkKZkXfznyAn5AQb9oi6SD6jLS9Gu/uXUzBnf+QP5ERQJ\nscAcJqHmxKwrnLYTZf7OUNX/r6nphI/QYjLBUaE2wZcrYtMAQq/RhfqnXfhFL3uh\ny93iqmmsJstVK9sZtg/tIcm+h0SJ2VZnyG1DscP0dPfaTmvlbqmI6sz+8WAfb4Vx\nNoGEK7YyNXnOjl9q2b81SSMtwlMEVI1f+dB7i9CnQQKBgQDN5uq6rzoVucfFTDSw\n+rFEhPLk9aapKiSYijG1Q+9mfTvew2LeDG/DFpVWfsyGl2S6ZP3gRk5Ca9oY1Non\nh1cL2cledtbSqYN3iq/QUtZE1krVYdRzRXT4TjUg7i9PNbROI/tbR36HhjtXPKSm\nHVyhp96EH15Ivw+OEarqOeDdjQKBgQDLcn3+D4dhPLP98kYzNIieatEZ20V7RAZ2\nfy5qiKk9wZQAdergq1ax+Ce8bPSoBhpf0Nb+amSxQc3iK65vsizzfTCxB/y7UnAt\nXXlMnHB71xLIfzi3l2KMqv8cnbg6xb8dmH9nAv/0wcFpXH6gBK4UhBMb2QtcbVgF\nN46/MKnb/wKBgQCvmx/atBOf7+CXPpU507VYMONPrsrDP/QSPNqENDp7eJeVN6Kc\nqpKvGhWnvWEF8Ryxc+yqWIvqTj2mK/Ma/2yX6Ni7PjOdW4GKdLfZvqyL7Q/JyTP+\nU+Cc3WamfT3QGod6lWmMwf8B6tO1ZT0vh583KAq5OF+bP4gurJbOSSqlCQKBgAzv\nh7FKvXniSTOBXxNMaM9hzU/OkFlpFtwb9BCUBebGUynAVaHZYxbHx4cEin3QfYbQ\nGYttql9W5sdVra6ubotAz4LCFkC22ikYQ2kqnUBSiYA0DqAlwP9es//Wy2r5PdCc\n7KTZHPssAqc3WVnFUmg9iZWAtGc5EJqsUKg5aONzAoGAAtsDH+c2zdjGpt0eAKOb\n6AR0u73qaalv+/va2S9zVmavgnRE9pZ6owFtFh1yOBZpDNoz7IFNcP80lESYwcdP\nXi2hPHeXI0UUrNs7h5uWa9kVA10J6Z3V86aM6/+ndUiLMOXBNJSxQ2GTu0QtP/VR\n6Z8Crl7i7x1AUPUhR4QpS1I=\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-3nxmk@rooky-de20b.iam.gserviceaccount.com",
  "client_id": "112153943115042174057",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-3nxmk%40rooky-de20b.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
})

firebase_admin.initialize_app(cred, {
    'storageBucket' : 'rooky-de20b.appspot.com'
})
db = firestore.client()



app = Flask(__name__)    #플라스크 객체(서버) 생성
CORS(app)
app.config["SECRET_KEY"] = "posanprototype" # flash() 함수를 사용하기 위해서 설정해야 함. 플라스크에서
app.config['SESSION_TYPE'] = 'firestore'  


@app.route('/list', methods=['GET'])
def list_data():
    try:
        docs = db.collection('my_collection').stream()
        result = [{doc.id: doc.to_dict()} for doc in docs]
        return jsonify(result), 200
    except Exception as e:
        return f"An Error Occurred: {e}", 500

# 암호화 로직에 사용되므로 유출되면 안됨!

app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes=30) # 초기화 시간을 30분으로 설정


@app.template_filter("formatdatetime") # 필터 이름
def format_datetime(value): # html에서 필터가 적용된 변수값이 value로 넘어옴
    if value is None: # 예외 처리
        return ""
    else:
        pubdate = datetime.fromtimestamp((int(value)+9*60*60*1000)/1000)
        return pubdate.strftime("%Y-%m-%d %H:%M:%S")
    

class_loaction = {
    '2-6' : '본관 1층',
    'IB영어연극실' : '본관 1층',
    '고교학점제실1A' : '본관 1층',
    '고교학점제실1B' : '본관 1층',
    '컴퓨터실' : '본관 1층',
    '1-5' : '본관 2층',
    '1-6' : '본관 2층',
    '1-7(IB)' : '본관 2층',
    '1-8(IB)' : '본관 2층',
    '2-1' : '본관 2층',
    '2-2' : '본관 2층',
    '2-3' : '본관 2층',
    '2-4' : '본관 2층',
    '2-5' : '본관 2층',
    '1-1' : '본관 3층',
    '1-2' : '본관 3층',
    '1-3' : '본관 3층',
    '1-4' : '본관 3층',
    '2-7(IB)' : '본관 3층',
    'IB생명과학실' : '본관 3층',
    'IB화학실' : '본관 3층',
    '미술실' : '본관 3층',
    '원격수업지원실' : '본관 3층',
    '과학(준비실)' : '자율관 1층',
    '과학실1(물지)' : '자율관 1층',
    '과학실2(화생)' : '자율관 1층',
    '상상제작소1(첨단기구실)' : '자율관 1층',
    '상상제작소2(첨단제작실)' : '자율관 1층',
    '고교학점제2A' : '자율관 2층',
    '고교학점제2B' : '자율관 2층',
    '고교학점제2C' : '자율관 2층',
    '자기주도학습실1' : '자율관 2층',
    '자기주도학습실2' : '자율관 2층',
    '진로교실' : '자율관 2층',
    '고교학점제실4A' : '자율관 4층',
    '고교학점제실4B' : '자율관 4층',
    '고교학점제실4C' : '자율관 4층',
 
}



     
@app.route("/register", methods=["POST"]) #*
def register():
    if request.method == "POST":
        postData = request.json
        Class = postData['class']
        time = postData["time"]
        info = postData["info"]
        friends = postData["friends"]
        purpose = postData["purpose"]
        plus = postData["plus"]
        location = class_loaction[Class]
        targets = list(friends)
        targets.insert(0, info)
        doc_ref = db.collection('class').document(location).collection(Class).document(time)
        doc = doc_ref.get()
        not_list = []
        possible_list = list(friends)
        if doc.exists: 
            data = doc.to_dict()
            if data['possible'] == True:
                for target in targets:
                    set_ref = db.collection('students').document(target).collection('자습').document('자습')
                    set_datas = set_ref.get()
                    if set_datas.exists:
                        set_data = set_datas.to_dict()
                        if set_data[time] != '':
                            not_list.append(target)
                            try:
                                possible_list.remove(target)
                            except:
                                break

                    load_ref = db.collection('students').document(target).collection('loading').document('자습')
                    load = load_ref.get()
                    if load.exists:
                        load_data = load.to_dict()
                        try:
                            if load_data[time] != Class and load_data[time] != '':
                                not_list.append(target)
                                try:
                                    possible_list.remove(target)
                                except:
                                    break
                            else:
                                load_data[time] = Class
                                load_ref.set(load_data)
                        except:
                            load_data[time] = Class
                            load_ref.set(load_data)

                if len(not_list) != len(targets) and info not in not_list:
                    data['loading'] = True
                    doc_ref.set(data)
                    db.collection('class').document('loading').collection(Class).document(time).set({'location':location,'student' : info, 'purpose':purpose, 'friends' : possible_list, 'plus':plus})
                    return jsonify(['성공', not_list])
                else:
                    print(not_list, targets)
                    return jsonify(['잘못된 접근1'])

            else:
                return jsonify(['잘못된 접근2'])

        else:
            return jsonify(['잘못된 접근3'])
        



@app.route("/classappend", methods=['GET'])   
def classappend():
    time = ['점심시간', '8,9교시', '1자', '2자', '저녁시간']
    for c in class_loaction:
        for i in time:
            doc_ref = db.collection('class').document(class_loaction[c]).collection(class_loaction[c]).document(i) 
            doc_ref.set({'loading': False, 'possible': True})
    return '성공'

@app.route("/classes", methods=['POST'])   
def classes():
    data = request.json
    doc_name = data['building']
    time = data['time']
    docs_ref = db.collection('class').document(doc_name)
    docs = docs_ref.collections()
    doc_data = {}
    for c in docs:
        c_name = c.id
        doc = docs_ref.collection(c_name).document(time).get().to_dict()
        if doc['possible'] == True:
            if doc['loading'] == False:
                doc_data[c_name] = 'lightyellow'
            elif doc['loading'] == True:
                doc_data[c_name] = 'lightgreen'

    return jsonify(doc_data)



@app.route("/teacher", methods=['GET'])   
def teacher():
    docs_ref = db.collection('class').document('loading')
    docs = docs_ref.collections()
    data = {}
    for doc in docs:
        d_name = doc.id
        times = docs_ref.collection(d_name).stream()
        data[d_name] = [{time.id: time.to_dict()} for time in times]
    return jsonify(data)
    
    
@app.route("/allowed", methods=['POST'])   
def allowed():
    if request.method == 'POST':
        data = request.json
        Class = data['Class']
        time = data['time']
        person = data['person']
        location = class_loaction[Class]
        doc_ref = db.collection('class').document(location).collection(Class).document(time)
        doc = doc_ref.get().to_dict()
        doc['loading'] = False
        doc['possible'] = False
        doc_ref.set(doc)
        load_ref = db.collection('class').document('loading').collection(Class).document(time)
        load_ref.delete()
        for p in person:
            p_ref = db.collection('students').document(p)
            load_self_ref = p_ref.collection('loading').document('자습')
            load_self = load_self_ref.get().to_dict()
            load_self[time] = ''
            load_self_ref.set(load_self)
            self_ref = p_ref.collection('자습').document('자습')
            self_data = self_ref.get().to_dict()
            self_data[time] = Class
            self_ref.set(self_data)
        return jsonify('성공')
    else:
        return '잘못된 접근'
    
@app.route('/delclass', methods=["POST"])
def delclass():
    if request.method == 'POST':
        data = request.json
        info = data['info']
        Class = data['Class'].strip()
        time = data['time']
        doc_ref = db.collection('students').document(info).collection('loading').document('자습')
        doc = doc_ref.get().to_dict()  
        try:
            if doc[time] == Class:
                doc[time] = ''
                doc_ref.set(doc)
                load_class_ref = db.collection('class').document('loading').collection(Class).document(time)
                load_class_data = load_class_ref.get()
                if load_class_data.exists:
                    class_data_dic = load_class_data.to_dict()
                    if class_data_dic['student'] == info:
                        class_ref = db.collection('class').document(class_loaction[Class]).collection(Class).document(time)
                        class_data = class_ref.get().to_dict()
                        class_data['loading'] = False
                        class_ref.set(class_data)
                        friends = class_data_dic['friends']
                        for friend in friends:
                            friend_ref = db.collection('students').document(friend).collection('loading').document('자습')
                            friend_data = friend_ref.get().to_dict()
                            friend_data[time] = ''
                            friend_ref.set(friend_data)
                        load_class_ref.delete()
                        return jsonify('성공')
                    
                    else:
                        friends = class_data_dic['friends']
                        if info in friends:
                            friends.remove(info)
                            load_class_ref.update({'friends' : friends})
                            return jsonify('성공')
                        else :
                            return jsonify('잘못된 접근1')
                else :
                    return jsonify('잘못된 접근2')
            else :
                return jsonify('잘못된 접근3')
        except:
            return jsonify('잘못된 접근4')

    
"""@app.route("/reset", methods=['GET','POST'])   
def reset():
    if request.method == 'POST':
        classes = mongo.db.classes
        classes = classes.find({})
        for c in classes:
            id = str(c.get('_id'))
            classes.update_one({'_id' : ObjectId(id)}, {
                '%$set' : {
                    'info' : [],
                    'possible' : 'o',
                    'loading' : 'x',
                }
            })
        
        
    else:
        return '잘못된 접근'"""


    
@app.route("/")   
def index():
    return '대기'

      
@app.route('/signup', methods=['POST']) #*
def add_data():
    try:
        data = request.json
        doc_name = data['info']
        password = data['password'].encode('utf-8')
        name = data['name']
        docs = db.collection('students').where('info', '==', doc_name).stream()
        result = [{doc.id: doc.to_dict()} for doc in docs]
        
        if result:
            return jsonify('이미')
        else:
            db.collection('students').document(doc_name).set({'name' : name, 'info' : doc_name, 'password' : bcrypt.hashpw(password, bcrypt.gensalt())})
            db.collection('students').document(doc_name).collection('자습').document('자습').set({'점심시간':'', '8,9교시':'', '1자':'', '2자':'', '저녁시간':''})
            db.collection('students').document(doc_name).collection('loading').document('자습').set({})
            return jsonify('성공')
    except Exception as e:
        return f"An Error Occurred: {e}", 500
    
@app.route('/tsignup', methods=['POST']) #*
def tsignup():
    try:
        data = request.json
        doc_name = data['info']
        password = data['password'].encode('utf-8')
        name = data['name']
        docs = db.collection('teachers').where('info', '==', doc_name).stream()
        result = [{doc.id: doc.to_dict()} for doc in docs]
        
        if result:
            return jsonify('이미')
        else:
            db.collection('teachers').document(doc_name).set({'name' : name, 'info' : doc_name, 'password' : bcrypt.hashpw(password, bcrypt.gensalt())})
            db.collection('teachers').document(doc_name).collection('자습').document('자습').set({'점심시간':'', '8,9교시':'', '1자':'', '2자':'', '저녁시간':''})
            db.collection('teachers').document(doc_name).collection('loading').document('자습').set({})
            return jsonify('성공')
    except Exception as e:
        return f"An Error Occurred: {e}", 500

@app.route("/login", methods=['POST'])  #*
def login():
    if request.method == 'POST': 
        postData = request.json
        info = postData["info"]
        password = postData["password"].encode('utf-8')
        doc_ref = db.collection('students').document(info)
        doc = doc_ref.get()
        if doc.exists: 
            data = doc.to_dict()
            if bcrypt.checkpw(password, data["password"]):
                session_id = str(uuid.uuid4())
                session_ref = db.collection('sessions').document(info)
                if info in session:
                    session_ref.delete()
                    session.pop(info, None)

                session[info] = {
                    'session_id' : session_id,
                }
                session_ref.set({
                    'session_id' : session_id,
                })
                return jsonify('성공', session_id)
            else:
                return jsonify('비밀번호')
        else:
            doc_ref = db.collection('teachers').document(info)
            doc = doc_ref.get()
            if doc.exists: 
                data = doc.to_dict()
                if bcrypt.checkpw(password, data["password"]):
                    session_id = str(uuid.uuid4())
                    session_ref = db.collection('sessions').document(info)
                    if info in session:
                        session_ref.delete()
                        session.pop(info, None)

                    session[info] = {
                        'session_id' : session_id,
                    }
                    session_ref.set({
                        'session_id' : session_id,
                    })
                    return jsonify('선생님', session_id)
                else:
                    return jsonify('비밀번호')
            else:
                return jsonify('정보')
            
        

        
@app.route('/teachercheck/<id>', methods=['GET'])
def teachercheck(id) :
    teacher = db.collection('teachers').document(id).get()
    if teacher.exists:
        return jsonify('성공')
    else :
        return jsonify('잘못된 접근')



        
        
@app.route("/logcheck", methods=['POST'])
def logcheck():
    postData = request.json
    info = postData["info"]
    session_id = postData["session_id"]
    doc_ref = db.collection('sessions').document(info)
    doc = doc_ref.get()
    if doc.exists:
        session_data = doc.to_dict()
        if session_data["session_id"] == session_id:
            return jsonify('성공')
        else:
            session.pop(info, None)
            doc_ref.delete()
            return jsonify('로그인')
    else:
        return jsonify('로그인')

        
        
@app.route("/mypage", methods=['POST']) #*
def mypage():
    if request.method == 'POST': 
        info = request.json["info"]
        doc_ref = db.collection('students').document(info)
        doc = doc_ref.get()
        if doc.exists: 
            selves1 = doc_ref.collection('자습').document('자습').get().to_dict()
            selves2 = doc_ref.collection('loading').document('자습').get().to_dict()
            for self in selves2:
                if selves2[self] != '':
                    selves1[self] = str(selves2[self]) + ' (대기 중)'
            data = doc.to_dict()
            del data['password']
            data['자습'] = selves1

            return jsonify(data)
        else:
            return jsonify('잘못된 접근')
        
@app.route('/meals', methods=['POST'])
def meals():
    if request.method == 'POST':
        dayrange = request.json['range']
        print(dayrange)
        now = datetime.now()
        days = 1
        date = ''
        monthlist = [31,28,31,30,31,30,31,31,30,31,30,31]
        if dayrange == 'day':
            date = now.strftime('%Y%m%d')
            days = 1
            end_date = date
        elif dayrange == 'month':
            date = now.strftime('%Y%m')+'01'
            days = monthlist[now.month-1]
            end_date = now.strftime('%Y%m')+str(days)
            

        itemlist = {}

        for d in range(days):
            d_date = str(int(date)+d)
            itemlist[d_date] = {}

        webpage = requests.get(f'https://open.neis.go.kr/hub/mealServiceDietInfo?KEY=e551d44107644bb582cdd21f692e6dd4&Type=xml&plndex=1&pSize=100&ATPT_OFCDC_SC_CODE=D10&SD_SCHUL_CODE=7240189&MLSV_FROM_YMD={date}&MLSV_TO_YMD={end_date}')
        soup = BeautifulSoup(webpage.content, 'html.parser')
        rows = soup.select("row")
        for r in rows:
            items = r.select_one("ddish_nm").text.split("<br/>")
            i_date = r.select_one('MLSV_YMD').text
            mealType = r.select_one('MMEAL_SC_NM').text
            itemlist[i_date][mealType] = items

        return jsonify(itemlist)
        

# @app.route('/meal', methods=['GET'])
# def meals1():
#         dayrange = 'day'
#         now = datetime.now()
#         monthlist = [31,28,31,30,31,30,31,31,30,31,30,31]
#         if dayrange == 'day':
#             date = now.strftime('%Y%m%d')
#             days = 1
#             end_date = date
#         elif dayrange == 'month':
#             date = now.strftime('%Y%m')+'01'
#             days = monthlist[now.month-1]
#             end_date = now.strftime('%Y%m')+str(days)
            

#         itemlist = {

#         for d in range(days):
#             d_date = str(int(date)+d)
#             itemlist[d_date] = {}

#         webpage = requests.get(f'https://open.neis.go.kr/hub/mealServiceDietInfo?KEY=e551d44107644bb582cdd21f692e6dd4&Type=xml&plndex=1&pSize=100&ATPT_OFCDC_SC_CODE=D10&SD_SCHUL_CODE=7240189&MLSV_FROM_YMD={date}&MLSV_TO_YMD={end_date}')
#         soup = BeautifulSoup(webpage.content, 'html.parser')
#         rows = soup.select("row")
#         for r in rows:
#             items = r.select_one("ddish_nm").text.split("<br/>")
#             i_date = r.select_one('MLSV_YMD').text
#             mealType = r.select_one('MMEAL_SC_NM').text
#             itemlist[i_date][mealType] = items
#         print(itemlist)
#         return jsonify(itemlist)


@app.route('/communitylist', methods=['GET'])
def communitylist():
    docs = db.collection('community').stream()
    result = [{doc.id: doc.to_dict()} for doc in docs]
    return jsonify(result)

@app.route('/view/<id>', methods=['GET'])
def communityview(id):
    doc_ref = db.collection('community').document(id)
    doc = doc_ref.get()
    if doc.exists:
        doc_data = doc.to_dict()
        doc_ref.update({'view' : doc_data['view'] + 1})
        comments = doc_ref.collection('comments').stream()
        comments_data = [{comment.id : comment.to_dict()} for comment in comments]
        return jsonify(doc_data, comments_data)
    else:
        return jsonify('잘못된 접근')

@app.route('/commentsadd', methods=['POST'])
def commentsadd():
    data = request.json
    target = data['target']
    contents = data["contents"]
    writer = data["writer"]
    name = data['name']
    writerData = db.collection('students').document(writer).get()
    if contents.replace(' ', '') != '' and writerData.exists:
        if name == 'false':
            viewname = '익명'
        else :
            student = db.collection('students').document(writer).get().to_dict()
            viewname = student['name']
            
        id = str(ObjectId())
        db.collection('community').document(target).collection('comments').document(id).set({'contents' : contents, 'writer' : writer, 'good' : 0, 'name' : viewname, 'id' : id})
        return jsonify('성공')

    else:
        return jsonify('잘못된 접근')
    
@app.route('/commentdel', methods=['POST'])
def commentdel() :
    data = request.json
    target = data['target']
    writer = data['writer']
    id = data['id']
    doc_ref = db.collection('community').document(target).collection('comments').document(id)
    doc = doc_ref.get()
    if doc.exists:
        doc_data = doc.to_dict()
        if doc_data['writer'] == writer:
            doc_ref.delete()
            return jsonify('성공')
        else:
            return jsonify('잘못된 접근')
    else:
        return jsonify('잘못된 접근')
    
@app.route('/commentedit', methods=['POST'])
def commentedit():
    data = request.json
    target = data["target"]
    contents = data["contents"]
    writer = data["writer"]
    name = data['name']
    id = data['id']
    comment_ref = db.collection('community').document(target).collection('comments').document(id)
    commentData = comment_ref.get()
    if contents.replace(' ', '') != '' and commentData.exists:
        if commentData.to_dict()['name'] == writer:
            if name == 'false':
                viewname = '익명'
            else :
                student = db.collection('students').document(writer).get().to_dict()
                viewname = student['name']
                
            comment_ref.update({'contents' : contents, 'name' : viewname})
            return jsonify('성공')
        else:
            return jsonify('잘못된 접근')

    else:
        return jsonify('잘못된 접근')
    


@app.route('/communitydel', methods=['POST'])
def communitydel() :
    data = request.json
    target = data['target']
    writer = data['writer']
    doc_ref = db.collection('community').document(target)
    doc = doc_ref.get()
    if doc.exists:
        doc_data = doc.to_dict()
        if doc_data['writer'] == writer:
            doc_ref.delete()
            return jsonify('성공')
        else:
            return jsonify('잘못된 접근')
    else:
        return jsonify('잘못된 접근')
    
@app.route('/communityedit', methods=['POST'])
def communityedit():
    data = request.json
    title = data["title"]
    contents = data["contents"]
    writer = data["writer"]
    name = data['name']
    id = data['id']
    community_ref = db.collection('community').document(id)
    communityData = community_ref.get()
    if title.replace(' ', '') != '' and contents.replace(' ', '') != '' and communityData.exists:
        if communityData.to_dict()['name'] == writer:
            if name == 'false':
                viewname = '익명'
            else :
                student = db.collection('students').document(writer).get().to_dict()
                viewname = student['name']
                
            community_ref.update({'title' : title, 'contents' : contents, 'name' : viewname})
            return jsonify({'state' : '성공', 'id' : id})
        else:
            return jsonify({'state' : '잘못된 접근'})

    else:
        return jsonify({'state' : '잘못된 접근'})


 

@app.route('/communitywrite', methods=['POST'])
def communitywrite():
    data = request.json
    title = data["title"]
    contents = data["contents"]
    writer = data["writer"]
    name = data['name']
    writerData = db.collection('students').document(writer).get()
    if title.replace(' ', '') != '' and contents.replace(' ', '') != '' and writerData.exists:
        if name == 'false':
            viewname = '익명'
        else :
            student = db.collection('students').document(writer).get().to_dict()
            viewname = student['name']
            
        id = str(ObjectId())
        db.collection('community').document(id).set({'title' : title, 'contents' : contents, 'writer' : writer, 'view' : 0, 'good' : 0, 'id' : id, 'name' : viewname})
        return jsonify({'state' : '성공', 'id' : id})

    else:
        return jsonify({'state' : '잘못된 접근'})

bucket = storage.bucket()

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and file.filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
        blob = bucket.blob(file.filename)
        blob.upload_from_file(file)
        blob.make_public()  # 공개적으로 접근 가능하도록 설정
        file_url = blob.public_url
        return jsonify({'url': file_url}), 200

    return jsonify({'error': 'Invalid file type'}), 400
    
    


if __name__ == "__main__":   
    app.run(debug=True) 
