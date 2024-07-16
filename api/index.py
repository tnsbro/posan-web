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
app.config["SECRET_KEY"] = "abcd" # flash() 함수를 사용하기 위해서 설정해야 함. 플라스크에서


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
        time = postData["time"]
        info = postData["info"]
        friends = postData["friends"]
        doc_ref = db.collection('class').document(Class).collection(time).document(time)
        doc = doc_ref.get()
        if doc.exists: 
            data = doc.to_dict()
            if data['loading'] == False and data['possible'] == True:
                data['loading'] = True
                data['possible'] = False
                doc_ref.set(data)
                d = Class+'-'+time
                load_ref = db.collection('students').document(info).collection('loading').document('자습')
                load = load_ref.get()
                if load.exists:
                    load = load.to_dict()
                    load[d] = '1'
                else:
                    load = {d:'1'}
                db.collection('class').document('loading').collection(Class).document(time).set({'student' : info, 'friends' : friends})
                load_ref.set(load)
                return '성공'

            else:
                return '잘못된 접근1'

        else:
            return '잘못된 접근2'
        
@app.route("/timecheck", methods=["POST"])
def timecheck():
    if request.method == "POST":
        postData = request.json
        Class = postData['class']
        timelist = ['점심시간', '저녁시간', '8,9교시','1자','2자']
        result = {'점심시간':'', '저녁시간':'', '8,9교시':'','1자':'','2자':''}
        for t in timelist:
            doc_ref = db.collection('class').document(Class).collection(t).document(t)
            doc = doc_ref.get()
            if doc.exists: 
                data = doc.to_dict()
                if data['loading'] == False:
                    if data['possible'] == True:
                        result[t] == '1'
                    else:
                        result[t] == '0'
                else:
                    result[t] == '2'

            else:
                return '잘못된 접근'
        
        return jsonify(result)



@app.route("/classappend", methods=['POST'])   
def classappend():
    time = ['점심시간', '8,9교시', '1자', '2자', '저녁시간']
    data = request.json
    doc_name = data['class']
    for i in time:
        doc_ref = db.collection('class').document(doc_name).collection(i).document(i) 
        doc_ref.set({'loading': False, 'possible': True})
    return '성공'



@app.route("/teacher", methods=['GET'])   
def teacher():
    docs = db.collection('class').stream()
    result = docs.to_dict()
    return jsonify(result)
    


@app.route('/search', methods=['GET'])
def search_documents():
    field = request.args.get('field')
    value = request.args.get('value')
    
    if not field or not value:
        return jsonify({"error": "Field and value query parameters are required"}), 400

    try:
        # Firestore에서 해당 필드와 값에 해당하는 문서 검색
        collection_ref = db.collection('class')
        query = collection_ref.where(field, '==', value)
        results = query.stream()
        
        documents = []
        for doc in results:
            documents.append(doc.to_dict())
        
        return jsonify(documents), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    
# @app.route("/allowed", methods=['POST'])   
# def allowed():
#     if request.method == 'POST':
#         data = request.json
#         id = data['id']
#         classes = mongo.db.classes
#         classes.update_one({'_id' : ObjectId(id)}, {
#             '$set' : {
#                 'loading' : 'x',
#                 'possible' : 'x',
#             }
#         })
#         return jsonify(data)
#     else:
#         return '잘못된 접근'
    
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
            return '이미'
        else:
            db.collection('students').document(doc_name).set({'name' : name, 'info' : doc_name, 'password' : bcrypt.hashpw(password, bcrypt.gensalt())})
            db.collection('students').document(doc_name).collection('자습').document('자습').set({'점심시간':'', '8,9교시':'', '1자':'', '2자':'', '저녁시간':''})
            db.collection('students').document(doc_name).collection('loading').document('자습').set({})
            return '성공'
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
                return '성공'
            else:
                return '비밀번호'
        else:
            return '정보'
        
        
        
@app.route("/mypage", methods=['POST']) #*
def mypage():
    if request.method == 'POST': 
        info = request.json["info"]
        doc_ref = db.collection('students').document(info)
        doc = doc_ref.get()
        if doc.exists: 
            selves = doc_ref.collection('자습').document('자습').get().to_dict()
            data = doc.to_dict()
            del data['password']
            return jsonify(data, selves)
        else:
            return '잘못된 접근'

    


if __name__ == "__main__":   
    app.run(debug=True) 
