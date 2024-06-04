from flask import Flask
from flask import request #브라우저의 요청을 처리하기 위한 클래스
from flask import render_template #페이지 렌더링을 위한 함수
from flask_pymongo import PyMongo
from bson.objectid import ObjectId # 몽고DB의 _id 필드값 처리를 위해 추가
from flask import abort # 웹 사이트에서 발생하는 오류 처리를 위한 클래스
from flask import redirect # 인자로 전달된 주소 호출
from flask import url_for # 인자로 전달된 함수가 가리키는 URL 주소 생성
from flask import flash
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


cred = credentials.Certificate('../serviceAccountKey.json')
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
        docs = db.collection('students').where('name', '==', name).stream()
        result = [{doc.id: doc.to_dict()} for doc in docs]
        
        if not result:
            return '이미'
        else:
            db.collection('students').document(doc_name).set({'name' : name, 'password' : bcrypt.hashpw(password, bcrypt.gensalt())})
            db.collection('students').document(doc_name).collection('자습').document('자습').set({'점심시간':'', '8,9교시':'', '1자':'', '2자':'', '저녁시간':''})
            return '성공'
    except Exception as e:
        return f"An Error Occurred: {e}", 500

@app.route("/login", methods=['POST'])  #*
def login():
    if request.method == 'GET': 
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
