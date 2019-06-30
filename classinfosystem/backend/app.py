#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import json
import datetime
import xlwt
import zipfile
import shutil
from flask import Flask, g, jsonify, make_response, request, send_file
from flask_cors import CORS
from flask_httpauth import HTTPBasicAuth
from flask_sqlalchemy import SQLAlchemy
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import BadSignature, SignatureExpired
from passlib.apps import custom_app_context
from sqlalchemy import extract
from sqlalchemy import and_

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

# r'/*' 是通配符，让本服务器所有的 URL 都允许跨域请求
CORS(app, supports_credentials=True, resources={r"/api/*": {"origins": "*"}})
app.config['SECRET_KEY'] = 'hard to guess string'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_RECORD_QUERIES'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(basedir, 'data.sqlite')
app.config['UPLOAD_FOLDER'] = 'user_upload'
app.config['DOWNLOAD_FOLDER'] = 'user_download'
ALLOWED_EXTENSIONS = set(['pdf','PDF','doc','docx','wps','rar','zip','7z','txt'])

db = SQLAlchemy(app)    ##初始化数据库
auth = HTTPBasicAuth()
CSRF_ENABLED = True
app.debug = True



def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def allowed_memeber(number,classN):
    allClassmate = Classmate.query.filter_by(classN= classN).all()
    for item in allClassmate:
        classmate_number = int(item.number)
        if classmate_number == int(number):
            return item.name
    return ""


def make_excle(hcode):
    file_dir = os.path.join(basedir, app.config['DOWNLOAD_FOLDER'])
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
    allClassmate = Classmate.query.filter_by().all()
    record = []
    nosubmit = []
    for item in allClassmate:
        user_name = item.name
        user_number = int(item.number)
        record_id = item.id
        user_record = HomeworkRecord.query.filter_by(code=hcode, user=user_number).order_by(
            HomeworkRecord.id.desc()).first()
        if user_record is None:
            user_file_name = "无"
            user_date = "无"
            user_info = [user_name, user_number, user_file_name, user_date, record_id]
            nosubmit.append(user_info)
        else:
            user_file_name = user_record.token
            user_date = user_record.date
            user_info = [user_name, user_number, user_file_name, user_date, record_id]
            record.append(user_info)
    workbook = xlwt.Workbook(encoding='utf-8')
    worksheet1 = workbook.add_sheet('已交')
    worksheet2 = workbook.add_sheet('未交')
    worksheet1.write(0, 0, "姓名")
    worksheet1.write(0, 1, "学号")
    worksheet1.write(0, 2, "文件名")
    worksheet1.write(0, 3, "日期")
    worksheet2.write(0, 0, "姓名")
    worksheet2.write(0, 1, "学号")
    worksheet2.write(0, 2, "文件名")
    worksheet2.write(0, 3, "日期")
    i = 1
    for item in record:
        worksheet1.write(i, 0,str(item[0]))
        worksheet1.write(i, 1,str(item[1]))
        worksheet1.write(i, 2,str(item[2]))
        worksheet1.write(i, 3, str(item[3]))
        i=i+1
    i = 1
    for item in nosubmit:
        worksheet2.write(i, 0, str(item[0]))
        worksheet2.write(i, 1, str(item[1]))
        worksheet2.write(i, 2, str(item[2]))
        worksheet2.write(i, 3, str(item[3]))
        i = i + 1
    workbook.save(file_dir+'/'+str(hcode)+'SUMMARY.xls')
    return str(hcode)+'SUMMARY.xls'


def make_zip(hcode):
    startdir = os.path.join(basedir, app.config['UPLOAD_FOLDER'],str(hcode))
    file_news = str(hcode) + '.zip'
    path = os.path.join(basedir,app.config['DOWNLOAD_FOLDER'],file_news)
    if os.path.exists(path):
        os.remove(path)
    z = zipfile.ZipFile(file_news, 'w', zipfile.ZIP_DEFLATED)  # 参数一：文件夹名
    for dirpath, dirnames, filenames in os.walk(startdir):
        fpath = dirpath.replace(startdir, '')
        fpath = fpath and fpath + os.sep or ''
        for filename in filenames:
            z.write(os.path.join(dirpath, filename), fpath + filename)
    z.close()
    r_path = os.path.join(basedir, app.config['DOWNLOAD_FOLDER'])
    shutil.move(basedir +'/'+ file_news, r_path)


class User(db.Model):      #账户ORM
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), index=True)
    password = db.Column(db.String(128))
    userclass = db.Column(db.INTEGER)
    role = db.Column(db.String(32))
    last_time = db.Column(db.TEXT)
    last_ip = db.Column(db.TEXT)
    nickname = db.Column(db.TEXT)

    # 密码加密
    def hash_password(self, password):
        self.password = custom_app_context.encrypt(password)

    # 密码解析
    def verify_password(self, password):
        return custom_app_context.verify(password, self.password)

    # 获取管理员token，有效时间10min
    def generate_auth_token(self, expiration=1200):
        s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.id ,'role':g.user.role})

    # 解析token，确认登录的用户身份
    @staticmethod
    def verify_auth_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None  # 有效 token, 但是过期
        except BadSignature:
            return None   # 无效的 token
        user = User.query.get(data['id'])             # 返回用户信息
        return user

    def to_json(self):
        dict = self.__dict__
        if "_sa_instance_state" in dict:
            del dict["_sa_instance_state"]
        return dict


class Visitor(db.Model):
    __tablename__ = 'visitors'
    id = db.Column(db.Integer, primary_key=True)
    v_date = db.Column(db.DATETIME)
    ip = db.Column(db.String(32))
    system = db.Column(db.String(32))


class Meeting(db.Model):
    __tablename__ = 'meeting'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.TEXT)
    date_s = db.Column(db.TEXT)
    date_e = db.Column(db.TEXT)
    address=db.Column(db.String(128))

    def to_json(self):
        dict = self.__dict__
        if "_sa_instance_state" in dict:
            del dict["_sa_instance_state"]
        return dict


class Question(db.Model):
    __tablename__ = 'question'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.TEXT)
    title = db.Column(db.TEXT)
    status=db.Column(db.Integer)

    def to_json(self):
        dict = self.__dict__
        if "_sa_instance_state" in dict:
            del dict["_sa_instance_state"]
        return dict


class ClassCost(db.Model):
    __tablename__ = 'classcost'
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer)
    type=db.Column(db.TEXT)
    description = db.Column(db.TEXT)
    datetime = db.Column(db.TEXT)
    balance = db.Column(db.Integer)

    def to_json(self):
        dict = self.__dict__
        if "_sa_instance_state" in dict:
            del dict["_sa_instance_state"]
        return dict


class Notice(db.Model):
    __tablename__ = 'notice'
    id = db.Column(db.Integer, primary_key=True)
    content=db.Column(db.TEXT)
    title = db.Column(db.TEXT)
    source = db.Column(db.TEXT)

    def to_json(self):
        dict = self.__dict__
        if "_sa_instance_state" in dict:
            del dict["_sa_instance_state"]
        return dict


class Homework(db.Model):
    __tablename__ = 'homework'
    id = db.Column(db.Integer, primary_key=True)
    code=db.Column(db.INTEGER)
    request_n = db.Column(db.INTEGER)
    has_n = db.Column(db.INTEGER)
    class_n = db.Column(db.INTEGER)
    description = db.Column(db.TEXT)

    def to_json(self):
        dict = self.__dict__
        if "_sa_instance_state" in dict:
            del dict["_sa_instance_state"]
        return dict


class HomeworkRecord(db.Model):
    __tablename__ = 'homeworkRecord'
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.TEXT)
    home = db.Column(db.TEXT)
    code = db.Column(db.Integer)
    token = db.Column(db.TEXT)
    date = db.Column(db.TEXT)

    def to_json(self):
        dict = self.__dict__
        if "_sa_instance_state" in dict:
            del dict["_sa_instance_state"]
        return dict


class Classmate(db.Model):
    __tablename__ = 'class'
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer)
    name = db.Column(db.TEXT)
    classN = db.Column(db.Integer)

    def to_json(self):
        dict = self.__dict__
        if "_sa_instance_state" in dict:
            del dict["_sa_instance_state"]
        return dict


@auth.verify_password                # 认证用户  如果这里认证失败将放回401
def verify_password(name_or_token, password):
    if not name_or_token:
        return False
    result_name = re.compile(r"[[a-zA-z]\\w{0,9}]")
    result_password = re.compile(r"^[a-zA-Z]\w{3,18}")
    if result_name.match(name_or_token) is False or result_password.match(password) is False:
        return False
    name_or_token = re.sub(r'^"|"$', '', name_or_token)
    user = User.verify_auth_token(name_or_token)       # 分析用户身份
    if user is None:
        user = User.query.filter_by(name=name_or_token).first()
        if user is None or user.verify_password(password) is False:
            return False
    g.user = user
    return True


@app.route('/api/login', methods=['POST'])          # 登录
@auth.login_required
def get_admin_auth_token():
    token = g.user.generate_auth_token()
    sys = "Windows"
    if "Linux x86_64" in request.headers.get("User-Agent"):
        sys = "Linux"
    elif "Android" in request.headers.get("User-Agent"):
        sys = "Android"

    last_time = datetime.datetime.now()
    last_ip = request.remote_addr
    g.user.last_ip = last_ip
    g.user.last_time = last_time
    db.session.commit()
    visitor = Visitor(ip=request.remote_addr,system = sys,v_date=datetime.datetime.now())
    db.session.add(visitor)
    db.session.commit()
    return jsonify({'code': 200, 'msg': "登录成功", 'token': token.decode('ascii'), 'name': g.user.name,'role':g.user.role})


@app.route('/api/signup',methods=['POST'])           # 注册
def get_user_auth_token():
    data = json.loads(str(request.data, encoding="utf-8"))
    username = data['username']
    hasUser = User.query.filter_by(name=username).first()
    if hasUser is not None:
        return jsonify({'code': 900, 'msg': "该用户已存在，请直接登录"})
    newUser = User(name=data['username'],password= custom_app_context.encrypt(data['password']),userclass=data['userclass'],role='General')
    db.session.add(newUser)
    db.session.commit()
    return jsonify({'code': 200, 'msg': "恭喜你成功加入了我们"})


@app.route('/api/requestmeeting',methods=['POST'])           # 添加会议
@auth.login_required
def add_meeting():
    data = json.loads(str(request.data, encoding="utf-8"))
    newM = Meeting(date_s=data['date_s'],date_e= data['date_e'],address=data['address'],title=data['title'])
    print(data['date_s'])
    db.session.add(newM)
    db.session.commit()
    return jsonify({'code': 200, 'msg': "添加会议成功！"})


@app.route('/api/requestcost',methods=['POST'])      #增加班费收支记录
@auth.login_required
def add_classcost():
    data = json.loads(str(request.data, encoding="utf-8"))
    newC = ClassCost(number=data['cost_number'],type=data['cost_type'],description=data['cost_description'],datetime=data['costday'],balance=data['cost_balance'])
    db.session.add(newC)
    db.session.commit()
    return jsonify({'code': 200, 'msg': "添加班费收支成功！"})


@app.route('/api/requestNewNotice',methods=['POST'])      #增加通知
@auth.login_required
def add_notice():
    data = json.loads(str(request.data, encoding="utf-8"))
    newN = Notice(content=data['content'],title=data['title'],source=data['source'])
    db.session.add(newN)
    db.session.commit()
    return jsonify({'code': 200, 'msg': "添加通知成功！"})


@app.route('/api/requestNewQuestion',methods=['POST'])      #增加问题
@auth.login_required
def add_Question():
    data = json.loads(str(request.data, encoding="utf-8"))
    newN = Question(content=data['content'],title=data['title'],status=0)
    db.session.add(newN)
    db.session.commit()
    return jsonify({'code': 200, 'msg': "添加问题成功！"})


@app.route('/api/requestNewHomework',methods=['POST'])      #增加作业
@auth.login_required
def add_Homework():
    data = json.loads(str(request.data, encoding="utf-8"))
    has = Homework.query.filter_by(code=data['homecode']).first()
    if has:
        return jsonify({'code': 990, 'msg': "作业码已存在！请更换"})
    newN = Homework(code=data['homecode'],description=data['homeContent'],has_n=0,request_n=data['all']
                    ,class_n=data['homeClass'])
    db.session.add(newN)
    db.session.commit()
    return jsonify({'code': 200, 'msg': "添加作业成功！"})


@app.route('/api/setpwd', methods=['POST'])        # 修改密码
@auth.login_required
def set_auth_pwd():
    data = json.loads(str(request.data, encoding="utf-8"))
    user = User.query.filter_by(name=g.user.name).first()
    if user and user.verify_password(data['oldpass']):
        user.hash_password(data['newpass'])
        db.session.add(g.user)
        db.session.commit()
        return jsonify({'code': 200, 'msg': "密码修改成功"})
    else:
        return jsonify({'code': 500, 'msg': "请检查旧密码"})


@app.route('/api/getadmin',methods=['GET'])               #获取管理员主页信息
@auth.login_required
def get_admin_info():
    user_number = User.query.filter_by(role="General").count()
    all = Visitor.query.count()
    win_cnt = Visitor.query.filter_by(system="Windows").count()
    and_cnt = Visitor.query.filter_by(system="Android").count()
    lin_cnt = Visitor.query.filter_by(system="Linux").count()
    dayNumber=[]
    for i in range(-6,1):
        thisday =datetime.datetime.now() + datetime.timedelta(i)
        dayNumber.append(Visitor.query.filter(and_(extract('year', Visitor.v_date) == thisday.year,
                                                   extract('month', Visitor.v_date) == thisday.month,
                                                   extract('day', Visitor.v_date) == thisday.day)).count())
    questionQuery = Question.query.filter_by(status = 0).all()
    questionNotHandle = []
    for item in questionQuery:
        questionNotHandle.append(item.to_json())
    return jsonify({'code':200,'all':all,'win_cnt': win_cnt,'lin_cnt':lin_cnt,'and_cnt':and_cnt,'day_number':dayNumber,
                    'user_number':user_number,'question':questionNotHandle})


@app.route('/api/getmeeting',methods=['GET'])               #获取会议信息
@auth.login_required
def get_meeting():
    meetingQuery = Meeting.query.filter_by().all()
    meeting = []
    for item in meetingQuery:
        meeting.append(item.to_json())
    return jsonify({'code':200,'meeting':meeting})


@app.route('/api/getcost',methods=['GET'])               #获取班费信息
@auth.login_required
def get_cost():
    costQuery = ClassCost.query.filter_by().all()
    cost = []
    for item in costQuery:
        cost.append(item.to_json())
    return jsonify({'code':200,'cost':cost})


@app.route('/api/homework/get',methods=['GET'])               #获取作业信息
@auth.login_required
def get_homework():
    hcode = request.args.get("homecode", type=int)
    homeQuery = Homework.query.filter_by(code=hcode).all()
    homework = []
    for item in homeQuery:
        homework.append(item.to_json())
    return jsonify({'code':200,'homework':homework})


@app.route('/api/homework/getall',methods=['GET'])               #获取全部作业信息
@auth.login_required
def get_homework_all():
    homeQuery = Homework.query.filter_by().all()
    homework = []
    for item in homeQuery:
        homework.append(item.to_json())
    return jsonify({'code':200,'history':homework})


@app.route('/api/homeworkRecord/get',methods=['GET'])               #获取作业提交记录
@auth.login_required
def get_homeworkRecord():
    hcode = request.args.get("homecode", type=int)
    hasHomework = Homework.query.filter_by(code=hcode).first()
    if hasHomework is None:
        return jsonify({'code':991,'record':"作业码错误！！不存在该作业！"})
    else :
        homework_content = hasHomework.description
    allClassmate = Classmate.query.filter_by().all()
    record = []
    nosubmit = []
    for item in allClassmate:
        user_name = item.name
        user_number = int(item.number)
        record_id = item.id
        user_record = HomeworkRecord.query.filter_by(code=hcode,user=user_number).order_by(HomeworkRecord.id.desc()).first()
        if user_record is None:
            user_file_name = "无"
            user_date = "无"
            user_info = [user_name,user_number,user_file_name,user_date,record_id]
            nosubmit.append(user_info)
        else:
            user_file_name = user_record.token
            user_date = user_record.date
            user_info = [user_name, user_number, user_file_name, user_date, record_id]
            record.append(user_info)
    hasHomework.has_n = len(record)
    db.session.add(hasHomework)
    db.session.commit()
    if len(record) == 0:
        return jsonify({'code':990,'record':"提交记录为空!"})

    return jsonify({'code':200,'record':record,'nosubmit':nosubmit,'homework_content':homework_content})


@app.route('/api/notice/get',methods=['GET'])               #获取通知信息
@auth.login_required
def get_notice():
    noticeQuery = Notice.query.filter_by().all()
    notice = []
    for item in noticeQuery:
        notice.append(item.to_json())
    return jsonify({'code':200,'notice':notice})


@app.route('/api/getuser',methods=['GET'])               #获取所有用户信息
@auth.login_required
def get_user():
    userQuery = User.query.filter_by().all()
    user = []
    for item in userQuery:
        user.append(item.to_json())
    return jsonify({'code':200,'user':user})


@app.route('/api/getUserInfo',methods=['GET'])               #获取用户信息
@auth.login_required
def get_UserInfo():
    ip = request.remote_addr
    user_name = request.args.get('user',type=int)
    nickname = User.query.filter_by(name = user_name).first().nickname
    homeworkQuery = HomeworkRecord.query.filter_by(user = user_name).all()
    homework = []
    for item in homeworkQuery:
        homework.append(item.to_json())
    return jsonify({'code':200,'homework':homework,'ip':ip,'nickname':nickname})


@app.route('/api/homework/excel',methods=['POST'])               #获取Excel表格
@auth.login_required
def get_excel():
    data = json.loads(str(request.data, encoding="utf-8"))
    hcode = data["code"]
    hasHomework = Homework.query.filter_by(code=hcode).first()
    if hasHomework is None:
        return jsonify({'code': 991, 'msg': "作业码错误！！不存在该作业！",'token':""})
    token=make_excle(hcode)
    return jsonify({'code':200,'msg':"Success",'token':token})


@app.route('/api/homework/zip',methods=['POST'])               #获取Excel表格
@auth.login_required
def get_zip():
    data = json.loads(str(request.data, encoding="utf-8"))
    hcode = data["code"]
    hasHomework = Homework.query.filter_by(code=hcode).first()
    if hasHomework is None:
        return jsonify({'code': 991, 'msg': "作业码错误！！不存在该作业！",'token':""})
    make_zip(hcode)
    return jsonify({'code':200,'msg':"Success",'token':str(hcode)+'.zip'})


@app.route('/api/user/remove',methods=['GET'])               #删除选定用户信息
@auth.login_required
def remove_user():
    remove_id = request.args.get('id', type=int)
    user = User.query.filter_by(id=remove_id).first()
    db.session.delete(user)
    db.session.commit()
    return jsonify({'code':200,'msg':"您已成功删除该用户"})


@app.route('/api/notice/remove',methods=['GET'])               #删除选定通知信息
@auth.login_required
def remove_notice():
    remove_id = request.args.get('id', type=int)
    notice = Notice.query.filter_by(id=remove_id).first()
    db.session.delete(notice)
    db.session.commit()
    return jsonify({'code':200,'msg':"您已成功删除该通知"})


@app.route('/api/fileUpload',methods=['POST'])
@auth.login_required
def add_file():
    file_dir = os.path.join(basedir, app.config['UPLOAD_FOLDER'])
    f = request.files['file']
    data = request.form.to_dict()
    userName = data.get("userName")
    homecode = data.get("homecode")
    homeName = data.get("homeName")
    number = eval(data.get("userNumber"))
    hasHomework = Homework.query.filter_by(code=homecode).first()
    if hasHomework is None:
        return jsonify({'code': 990, 'msg': "不存在该作业,请确认您的作业码,可点击上方按钮查询确认！"})
    class_n = hasHomework.class_n
    hasName = allowed_memeber(number,class_n)
    if hasName=="":
        return jsonify({'code': 900, 'msg': "您不是该班级成员！如有误请联系管理员！"})
    if(userName=="") :
        userName = hasName
    file_dir = file_dir + '/' + homecode
    last = HomeworkRecord.query.filter_by(code=homecode,user = number).order_by(HomeworkRecord.id.desc()).first()
    last_token=""
    if  last:
        last_token = last.token
    if last_token and os.path.exists(file_dir+'/'+last_token):
        os.remove(file_dir+'/'+last_token)
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
    if f and allowed_file(f.filename):
        file_name = number+'_'+str(class_n)+'班'+'_'+userName+'_'+homeName+'.'+f.filename.rsplit('.', 1)[1]
        f.save(os.path.join(file_dir, file_name))
        token = file_name
        record = HomeworkRecord(user=number, code=homecode, home=homeName,token=token,
                                date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        db.session.add(record)
        db.session.commit()
        return jsonify({'code': 200, 'msg': "您已成功上传文件"})

    return jsonify({'code': 990, 'msg': "上传文件为空或格式不允许！"})


@app.route("/api/download/<filename>", methods=['GET'])
def download(filename):
    file_path = os.path.join(basedir, app.config['DOWNLOAD_FOLDER'], filename)
    response = make_response(send_file(file_path))
    return response


@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)


if __name__ == '__main__':
    db.create_all()      #建表
    app.run(host='0.0.0.0')