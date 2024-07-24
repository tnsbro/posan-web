from flask import Flask
from flask import request #브라우저의 요청을 처리하기 위한 클래스
from datetime import datetime
from flask import session
from datetime import timedelta
from functools import wraps
from flask import jsonify
from flask_cors import CORS
import pyrebase
import json
import firebase_admin
from firebase_admin import credentials, firestore
import bcrypt
import os
from flask import session
from flask_session import Session
import uuid
import requests
from bs4 import BeautifulSoup


cred = credentials.Certificate({
  "type": "service_account",
  "project_id": "prototype-ba6c5",
  "private_key_id": "c79ac1ee9627bee6626a972242a3714f6e733a88",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQCyXBPpwTi5jh9Y\n0chAIsSRGKwhUHJXXPlQ6rXhemGLB/pgNXBYyajsduHKGM1/v62yNGWQH+lLcMXd\n/cqZkkD+GORl6m+7dIy+iGccGhWFt8mhjQERGcNKm2svsROIuFrty5WzMkdSRXOR\nxHvKELGSHeRspusad4thqCwNE+0h6M+Rp3dbAD/gVJM3O0Eb4SvC/kx8ysbQYP2E\nW6D9vDb/K5hhvUSy90SHTxhnr/6EPxxWn7PqaS2vWOz3yKLoRwxfSHKXwqALNuyj\nQflGgnjOVMGUtVYs+4I8vlt5Q3uobCMj62LcmyXkYzVoTr8C3V57k6q1QYnI2s5a\nls81qslbAgMBAAECggEAHFE8JB+2RteGqI5d8bjTZon5QizIipBLUQqCp/LLK8yv\ndrjlRmN1+10AihqX/dFL3YAuI8y9OGoGMDGMCgfLY8xF7txisutVMSbs3+xQQHOm\ngoylf7aMZ/r28JJ3nHxQi3KIKPQxmKFIMPt1/+XYm289hfaWWxRhv7Z4j/b67igJ\nPs7e3z5uKVFjME91IPrBBHMaQsvySGNsivB2pif4mF2n4/jtHmkbnK25b37dfYKR\nHTGYEZu3niaBb697wHagm/unDEEpZDHkJrxvf8KwNFiH89uwPckNt1Cpm6a+g1Rm\nphCX3jUq8W4QvljWKB9bpRnVa9HT0u66ND2f8UGUsQKBgQDoJNL02jgHqJjUkM93\ncnd1brJ6wKq1HTON/ghc9oy4HBF5BeQ7rOmYXNasyTyV6qDj2E/6VpTil6g12wvb\nYkH7bXpRPnPpTd3Jju/WLNER7McWbyhHPPttacZLpenNJr7P3CpGqdZN/3G+e3tA\nbcmCtTRaUIBYcWFdLxSlLuQaMwKBgQDEsFCX58PhIJewJDQALCi7+6vUWGbmnGCQ\nQ1queO/mzeM5xH3A+eTH5jyIU21bQXZMYQQJtM2lEi0SYwHUsA7U/soYMtjSgh7X\nulTJ28LfC0NPK0SS5jm3E1KUh4nAwrTUdkxeMKCl1gI3HjDzc0J2nk5TIhKp9Eis\nqYHp4088OQKBgQChzLi0LDyNKfeLgHr5t/CHCuafJBZXMckzGHHfyX/++qE7Bt4y\nsawGo/6EY6Y0n1oQND5aL2qKHEYDc27qM6vlgEKWyb6kR79jspp7XrVBlxSUEFm0\nfU6IzgaFx1gTwwOPgNZ+dfWGW5p9tzcKivq+fWnF4QHzouLHvf7Xur0FfQKBgCAp\nJERyZRj+l0753HbawZ5bPHFwMwMqNq/gE4fLxo5aw/jCJD3Vno8BGoy/93WgcpNy\nmZJsueNv4WbMQZRhZUt2jdz/E2z4Ucq8cPjAslB+Kvda/891TaKdyjb3IpMeQysq\nXLpaASqcn6gbi62C/y8eG3iEbcDUbL2uyctQm7ghAoGBAMgmil9dQL1pH4azM6Ks\nOFla9j7ADMZMhJ10pDAR/nOa/uAW3dS9Ug5cKnmIn3uHrAqBbJXWv29r1Pu3mFIV\n04i5NS9XcclAY9wqD1prUJS/s2wj7F6zn4L0ttK4vBRf1VeRYd64zEn/HKRq0e8G\n0sIYWqOsM+Kzdctq3TekZ7/D\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-ty81b@prototype-ba6c5.iam.gserviceaccount.com",
  "client_id": "107445036565747793492",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-ty81b%40prototype-ba6c5.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
})

firebase_admin.initialize_app(cred)
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



     
@app.route("/register", methods=["POST"]) #*
def register():
    if request.method == "POST":
        postData = request.json
        Class = postData['class']
        location = postData['location']
        time = postData["time"]
        info = postData["info"]
        friends = postData["friends"]
        purpose = postData["purpose"]
        plus = postData["plus"]
        targets = list(friends)
        targets.append(info)
        doc_ref = db.collection('class').document(location).collection(Class).document(time)
        doc = doc_ref.get()
        not_list = []
        possible_list = list(friends)
        if doc.exists: 
            data = doc.to_dict()
            if data['possible'] == True:
                for target in targets:
                    load_ref = db.collection('students').document(target).collection('loading').document('자습')
                    load = load_ref.get()
                    if load.exists:
                        load_data = load.to_dict()
                        try:
                            if load_data[time] != Class:
                                not_list.append(target)
                                try:
                                    possible_list.remove(target)
                                except:
                                    continue
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
                    return jsonify(['잘못된 접근1'])

            else:
                return jsonify(['잘못된 접근2'])

        else:
            return jsonify(['잘못된 접근3'])
        



# @app.route("/classappend", methods=['GET'])   
# def classappend():
#     time = ['점심시간', '8,9교시', '1자', '2자', '저녁시간']
#     names = ['과학실1(물지)']
#     for doc_name in names:
#         for i in time:
#             doc_ref = db.collection('class').document('자율관 1층').collection(doc_name).document(i) 
#             doc_ref.set({'loading': False, 'possible': True})
#     return '성공'

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
        location = data['location']
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

@app.route("/login", methods=['POST'])  #*
def login():
    if request.method == 'POST': 
        postData = request.json
        info = postData["info"]
        password = postData["password"].encode('utf-8')
        doc_ref = db.collection('students').document(info)
        doc = doc_ref.get()
        SESSION_EXPIRATION_MINUTES = 5
        if doc.exists: 
            data = doc.to_dict()
            if bcrypt.checkpw(password, data["password"]):
                session_id = str(uuid.uuid4())
                session_ref = db.collection('sessions').document(info)
                expiration_time = datetime.now() + timedelta(minutes=SESSION_EXPIRATION_MINUTES)
                if info in session:
                    session_ref.delete()
                    session.pop(info, None)

                session[info] = {
                    'session_id' : session_id,
                    'expiration_time': expiration_time
                }
                session_ref.set({
                    'session_id' : session_id,
                    'expiration_time': expiration_time
                })
                return jsonify('성공', session_id)
            else:
                return jsonify('비밀번호')
        else:
            return jsonify('정보')
        
@app.route("/logout", methods=['POST']) 
def logout():
    if request.method == 'POST': 
        postData = request.json
        info = postData["info"]
        session.pop(info, None)
        try:
            session_ref = db.collection('sessions').document(session.sid)
            session_ref.delete()
            return jsonify('성공')
        except Exception as e:
            return f"An Error Occurred: {e}", 500
        
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
            expiration_time = session_data['expiration_time']
            if expiration_time >= datetime.now():
                return jsonify('성공')
            else:
                session.pop(info, None)
                doc_ref.delete()
                return jsonify('로그인')
        else:
            return jsonify('잘못된 접근')
    else:
        return jsonify('로그인')


@app.route('/test', methods=['GET'])
def test():
    doc_ref = db.collection('sessions').document('2508')
    doc_ref.delete()
    session.pop(2508, None)
    return '0'
        
        
        
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
                    selves1[self] = str(selves2[self]) + '대기'
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
            

#         itemlist = {}

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
    


if __name__ == "__main__":   
    app.run(debug=True) 
