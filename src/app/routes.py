from flask import render_template, send_from_directory, request, redirect, Flask, session, make_response, flash, url_for
from app import app
from pymongo import MongoClient
# from werkzeug.utils import secure_filename
import os

client = MongoClient('mongodb', 27017)
db = client.authen_DB

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
UPLOAD_FOLDER = 'app\\images\\upload'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = 'something random'


@app.route('/', methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html', message="Please enter your username and password")
    if request.method == 'POST':
        input_uname = str(request.form.get("uname"))
        input_pwd = str(request.form.get("pwd"))
        check_existed_user = db.authen.find_one({"username": input_uname})
        if (check_existed_user != None):
            if (check_existed_user["password"] == input_pwd):
                resp = make_response(redirect('cabinet'))
                resp.set_cookie('userID', value=str(input_uname))
                print(resp)
                return resp
        return render_template('login.html', message="Not correct username or password!")

   

@app.route('/cabinet')
def cabinet():
    state = request.cookies.get("userID")
    if (state != ''):
        uname = str(request.cookies.get('userID'))
        return render_template('cabinet.html', username = uname)
    return render_template('login.html', message="You have to log in first")


@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html', message='')
    if request.method == 'POST':
        input_uname = str(request.form.get("uname"))
        input_pwd = str(request.form.get("pwd"))
        check_existed_user = db.authen.find_one({"username": input_uname})
        if (check_existed_user == None):
            db.authen.insert({
                "username": input_uname,
                "password": input_pwd
            })
            return render_template('login.html', message='Register successful!')
        else:
            return render_template('register.html', message='User already exists!')
        

@app.route('/viewgalery')
def viewgalery():
    state = request.cookies.get("userID")
    if (state != ''):
        return render_template('index.html')
    return render_template('login.html', message="You have to log in first")

@app.route('/images/<path:filename>')
def custom_static(filename):
    return send_from_directory('images', filename)

@app.route('/logout')
def logout():
    resp = make_response(redirect('/'))
    resp.set_cookie('userID', value='')
    return resp

@app.route('/changepwd', methods=['GET', 'POST'])
def changepwd():
    uname = str(request.cookies.get('userID'))
    if request.method == 'GET':
        return render_template('changepwd.html', username = uname)
    if request.method == 'POST':
        input_pwd1 = str(request.form.get("pwd1"))
        input_pwd2 = str(request.form.get("pwd2"))
        if (input_pwd1 != input_pwd2):
            return render_template('changepwd.html', username = uname, message='Password did not match!')
        else:
            db.authen.update_one({"username": uname},{"$set": {"password": input_pwd1}})
            return render_template('login.html', message="You have to log in with the new password")



def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET','POST'])
def upload():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        
        if not allowed_file(file.filename):
            flash('Invalid file extension')
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            # filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))

            flash('Successfully saved', 'success')
            return redirect(url_for('uploaded_file', filename=file.filename))

    return render_template('upload.html')
            
@app.route('/upload/<path:filename>')
def uploaded_file(filename):
    return send_from_directory('images/upload', filename)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)