from flask import request,Flask,render_template,redirect,url_for,make_response,jsonify
from flask_pymongo import PyMongo
import jwt
import uuid
from werkzeug.security import generate_password_hash,check_password_hash
from datetime import datetime,timedelta
from config import Config
from functools import wraps
from helpers import objidconv


app = Flask(__name__)
app.config.from_object(Config)
mongo = PyMongo(app)
user_db = mongo.db.user.user_data

def get_id(token):
    data = jwt.decode(token,app.config['SECRET_KEY'],algorithms=['HS256'])
    return data['id']

def get_token(id):
    token = jwt.encode({
    'id':id,
    'exp':datetime.utcnow()+timedelta(minutes=5)
    }, app.config['SECRET_KEY'],algorithm="HS256")
    return token

def renew_token():
    token = request.headers['x-access-token']
    data = jwt.decode(token, app.config['SECRET_KEY'],algorithms=["HS256"])
    return get_token(data['id'])


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({'message':'Token is missing'}),401

        data = jwt.decode(token, app.config['SECRET_KEY'],algorithms=["HS256"])
        usr = user_db.find_one({'id':data['id']})
        if usr is None:
            return jsonify({'message':'Token is invalid'}),401
        
        return f(*args, **kwargs)
    return decorated

@app.route('/')
def red(): return redirect('login')



@app.route('/update',methods=['GET'])
@token_required
def update():
    data = request.args.to_dict()
    token =  request.headers['x-access-token']
    data = user_db.find_one_and_update({'id':get_id(token)},{'$set':{"email":data['email'],"username":data['username'],"address":data['address']}})
    data = jsonify({"respone":"user updated"})
    return data



@app.route('/delete',methods=['GET'])
@token_required
def delete():
    token = renew_token()
    user_db.delete_one({"id":get_id(token)})
    return redirect(url_for('signup'))


@app.route('/user',methods=['GET'])
@token_required
def get_user():
    token = renew_token()
    data = user_db.find_one({'id':get_id(token)})
    if data is None:
        return jsonify({'message':'User does not exist'})
    else:
        print(data)
        data = jsonify(objidconv(data))
        data.set_cookie('x-access-token',token)
        return data

@app.route('/getuser',methods=['GET'])
def getuser():
    return render_template('index.html')


@app.route('/login',methods=['GET'])
@app.route('/login',methods=['POST'])
def login():
    if request.method == 'GET':
        
        msg = request.args.to_dict()
        if 'val' not in msg:
            val=""
        else: val = msg['val']
        return render_template('login.html',val=val)

    if request.method == 'POST':
        auth = request.form.to_dict()
        if not auth or not auth['email'] or not auth['password']:
            return render_template('login.html',val="Values missing!")
    
        user = user_db.find_one({'email':auth['email']})

        if not user:
            return render_template('login.html',val="user does not exist!")
        
        if check_password_hash(user['password'],auth['password']):
            ret = redirect('getuser')
            ret.set_cookie('x-access-token',get_token(user['id']))
            return ret
        
        return render_template("login.html",val="Wrong email id or password!")

@app.route('/signup',methods=['GET'])
@app.route('/signup', methods =['POST'])
def signup():
    if request.method =='GET':
        return render_template('signup.html')
    if request.method == 'POST':
        # creates a dictionary of the form data
        data = request.form
    
        # gets name, email and password
        username, email,address = data.get('username'), data.get('email'),data.get('address')
        password = data.get('password')
    
        # checking for existing user
        user = user_db.find_one({"$or":[{"username":username},{"email":email}]})
        if not user:
            # database ORM object
            id= str(uuid.uuid4())
            user_db.insert_one({"id":id,"email":email, "username":username, "password":generate_password_hash(password),"address":address,"userdata":[]})
            resp = redirect('getuser')
            resp.set_cookie('x-access-token',get_token(id))
            return resp
        else:
            # returns 202 if user already exists
            resp = 'User already exists. Please Log in.'
            return redirect(url_for('login',val=resp),)

if __name__ == '__main__':

    app.run(debug=True)