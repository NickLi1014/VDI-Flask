from flask import Flask,request,render_template,redirect,flash,Flask,session,g,jsonify, render_template, request
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from views.checkaccount import *
from datetime import timedelta
from flask_session import Session
import os
import json
import smtplib
import time
from email.mime.text import MIMEText
from email.header import Header
import logging
from logging import FileHandler,Formatter
from logging.handlers import TimedRotatingFileHandler 
import logging.handlers


app = Flask(__name__)

#----loging----
#logging.basicConfig(filename='/var/log/flask/flask.log', level=logging.DEBUG, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

#----session----
app.config['SECRET_KEY'] = os.urandom(24)
app.config['SESSION_TYPE'] = 'filesystem'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=5)
Session(app)

#----url----
@app.route('/')
def index():
    flash('flash-1')
    
    
    return redirect("/login")

@app.route('/login',methods=['GET', 'POST'])  
def login():  
    login_msg = ""
    if 'uname' in session and session.get('token') == "@Dmin123":
        return redirect("/loginweb")
    else:
        if request.method == 'POST':

            # 利用request取得表單欄位值            
            userid = request.values['acname']
            pw = request.values['passwd']
            login_msg = linux_account_check(userid,pw)
            if login_msg == "Success":
                
                #設置session
                session["uname"] = userid
                session["token"] = "@Dmin123"
                
                session.permanent = True

                return redirect("/loginweb")
            else:
                error_message = f"Sorry , wrong user or password , please login again"
                #return error_message
    return render_template('login.html',**locals())

@app.route('/admin',methods=['GET', 'POST'])  
def admin():  
    error_message = ""
    if 'uname' in session and session.get('admin') == "admin":
        return redirect("/loginweb")
    else:
        if request.method == 'POST':
            #  利用request取得表單欄位值
            userid = request.values['acname']
            pw = request.values['passwd']
            login_msg = "Success"
            if login_msg == "Success":
                
                #設置session
                session["uname"] = userid
                session["token"] = "@Dmin123"
                session["admin"] = "admin"
                session.permanent = True
                return redirect("/loginweb")
            else:
                error_message = f"Sorry , wrong user or password , please login again"
                #return error_message
    return render_template('loginadmin.html',**locals())

@app.route('/loginweb',methods=['GET', 'POST'])  
def loginweb():  
    import os
    msg = ""
    if "uname" in session and session.get('token') == "@Dmin123":
        usname=session.get('uname')
        filepath = f"/home/{usname}/email"
        if os.path.isfile(filepath):
            fmsg="yes"
            fd = os.open(filepath, os.O_RDONLY)
            ret = os.read(fd,100)
            print(ret.decode())
            ret = ret.decode()
            

        else:
            fmsg="no"
        session.permanent = True
        if request.method == 'POST':
            userid = request.values['uname']
            email = request.values['umail']                                    
            #----linux----
            
            msg = ""
            dir=f"/home/{userid}/googleOTP"
            home = f"/home/{userid}"
            
            a=os.popen(f'echo {email} > {home}/email')
            a=os.popen(f'su - {userid} -c ""')
            time.sleep(1) 
            
            a=os.popen(f'su - {userid} -c "/usr/bin/google-authenticator -f -t -w 3 -r 3 -R 30 -d -e 1 -Q utf8 -l vpn -i vpn" > {dir}')
            time.sleep(2)
            f = open(f'{dir}','r')
            line = f.readlines()
            #Qrcode = Qrcode.replace('www.google.com','chart.googleapis.com')

            #-----SMTP----
            smtp=smtplib.SMTP("smtp.gmail.com", 587)  
            smtp.ehlo()
            smtp.starttls()
            smtp.login("syspost1176@gmail.com", "qzlpizjfxuhqqpzg") 
            from_addr="syspost1176@gmail.com"
            to_addr=[email]
            message = MIMEText( line[0]+line[1]+line[2]+line[3]+line[4]+line[5] , 'plain', 'utf-8')
            message['From'] = Header("SYS", 'utf-8')   # 发送者
            message['To'] =  Header("vpnuser", 'utf-8')        # 接收者
            subject = 'Vpn驗證碼'
            message['Subject'] = Header(subject, 'utf-8')
            f.close()
            status=smtp.sendmail(from_addr, to_addr, message.as_string())
            if status=={}:
                msg = "Success"
            else:
                msg = "failed"
            smtp.quit()
            
        return render_template('loginweb.html',**locals())
    return redirect("/login") 

@app.route('/useradd',methods=['GET', 'POST'])
def useradd():
    if 'uname' in session and session.get('admin') == "admin":
        return redirect("/useraddweb")
    else:
        if request.method == 'POST':
            #  利用request取得表單欄位值
            userid = request.values['acname']
            pw = request.values['passwd']
            login_msg = linux_admin(userid,pw)
            if login_msg == "Success":
                
                #設置session
                session["uname"] = userid
                session["token"] = "@Dmin123"
                session["admin"] = "admin"
                session.permanent = True
                return redirect("/useraddweb")
            else:
                error_message = f"Sorry , wrong user or password , please login again"
                #return error_message
    return render_template('useradd.html',**locals())

@app.route('/useraddweb',methods=['GET', 'POST'])  
def useraddweb():  
    msg = ""
    if 'uname' in session and session.get('admin') == "admin":
        session.permanent = True
        if request.method == 'POST':
            userid = request.values['uname']
            passwd = request.values['upasswd']
            #----linux----
            import os
            usercheck=os.system(f"id {userid}")
            if usercheck == 0 :
                msg = "failed"
            else:
                msg = ""
                os.system(f"ssh root@10.60.110.11 useradd {userid}")
                os.system(f"ssh root@10.60.110.11 echo '{passwd}' | passwd --stdin {userid}")
                os.system(f"ssh root@10.60.110.12 useradd {userid}")
                os.system(f"ssh root@10.60.110.12 echo '{passwd}' | passwd --stdin {userid}")
                usercheck1=os.system(f"ssh root@10.60.110.11 id {userid}")
                usercheck2=os.system(f"ssh root@10.60.110.12 id {userid}")
                if usercheck1 == 0 and usercheck2 == 0:
                    msg = "Success"
                else:
                    msg = "failed"
            
        return render_template('useraddweb.html',**locals())
    return redirect("/useradd") 

@app.route('/userlistweb',methods=[ "GET",'POST'])
def userlistweb():
    msg = ""
    if 'uname' in session and session.get('admin') == "admin":
        session.permanent = True
        # if 'name' in request.args and request.args['name'] != "" :
        #     key = request.args['name']
            #f = open(f'/etc/shadow','r')
            #array = f.readlines()[25:]
            #a = 0
            #listn = {}
            #for item in array:
                #item=item.split(":")
                #if key in item[0]:
                    #if item[0] == "admin" or item[0] == "checkpass":
                        #continue
                    #a=a+1 #編號
                    # n = []
                    # n.append(item[0])
                    # listn[a] = n
                    # user=item[0] 
                    # filepath = f"/home/{user}/email"  
                    # if os.path.isfile(filepath):                             
                    #     fd = os.open(filepath, os.O_RDONLY)
                    #     ret = os.read(fd,100)
                    #     print(ret.decode())
                    #     n.append(ret.decode())
                    #     listn[a] = n
                    #     msg =""   
            # if len(listn) == 0 :
              #  msg = "沒有資料"
                    
        return render_template('userlistweb.html',**locals())   
        #else:
            # f = open(f'/etc/shadow','r')
            # array = f.readlines()[25:]
            # a = 0
            # listn = {}
            # for item in array:
            #     item=item.split(":")
            #     if item[0] == "admin" or item[0] == "checkpass":
            #         continue
            #     a=a+1 #編號
            #     n = []
            #     n.append(item[0])
            #     listn[a] = n


            #     user=item[0] 
            #     filepath = f"/home/{user}/email"  
            #     if os.path.isfile(filepath):                             
            #         fd = os.open(filepath, os.O_RDONLY)
            #         ret = os.read(fd,100)
            #         print(ret.decode())
            #         n.append(ret.decode())
            #         listn[a] = n
               

        return render_template('userlistweb.html',**locals())
    return redirect("/login") 



@app.route('/route_function',methods=[ "GET",'POST'])
def route_function():
    if request.method == 'POST':
        userlist_name = request.form.get('theName')
        import os
        os.system(f"ssh root@10.60.110.11 userdel --remove {userlist_name}")
        os.system(f"ssh root@10.60.110.12 userdel --remove {userlist_name}")
        usercheck1=os.system(f"ssh root@10.60.110.11 id {userlist_name}")
        usercheck2=os.system(f"ssh root@10.60.110.12 id {userlist_name}")
        print(usercheck1)
        print(usercheck2)
        if usercheck1 == 256 and usercheck2 == 256:
            msg = "刪除成功"
        else:
            msg = "刪除失敗或未同步,請聯絡管理員!!"

        return jsonify({'validate':msg,'PayAmount':1500,'Name':userlist_name})
    return render_template('404.html')


@app.route('/logout')  
def logout():  
    session.clear()
    return redirect("/login")





if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0',port='8000')

