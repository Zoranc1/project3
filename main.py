from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_pymongo import PyMongo
from forms import reg_form, logIn_form, Updateform, diary_form
from flask_login import login_required
from bson.objectid import ObjectId
from base64 import b64encode
from flask_bcrypt import Bcrypt

import os
import base64
import datetime


app = Flask(__name__)

app.config['SECRET_KEY']= '87194741tu9i97rt0l6598poun562'
app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")

dbase = PyMongo(app)
bcrypt = Bcrypt(app)

def get_category_names():
    categories = []
    for category in dbase.db.collection_names():
        if not category.startswith("system."):
            categories.append(category)
    return categories    


@app.route("/")
def home():
    
    return render_template("home.html")

@app.route("/about")
def about():
    categories = get_category_names()
    return render_template("about.html", categories=categories, category='Task List')




@app.route("/register", methods=['GET', 'POST'])
def register():
    form = reg_form()
    if request.method == 'POST':
        users = dbase.db.users
        exist_users = users.find_one({'username':request.form['username']})
        
        if exist_users is None:
            hashpass = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')
            user = {'username':request.form['username'],
                        'email':request.form['email'], 'password' : hashpass,'time':datetime.datetime.now()}
            users.insert(user)
            
            
            # Login the new user
            session['username'] = user['username']
            if form.validate_on_submit():
                flash("Account has been successfully created with username: {}".format(user['username']), "success")
            return redirect(url_for("add_diary"))
        return 'That username already exist'
    
    return render_template("register.html", title='Register', form = form)


@app.route("/login", methods=['POST','GET'])
def login():
    form = logIn_form()
    if request.method=="POST":
        users = dbase.db.users
        user = users.find_one({'username':request.form['username']})
        
        if user:
            if bcrypt.check_password_hash(user['password'], request.form['password']):
                if form.validate_on_submit():
                    user['_id']=str(user['_id'])
                    session["username"] = user['username']
                    flash("You have been logged in!! ", "success")
                return redirect(url_for("my_diary"))
            else:
                flash('Login Unsuccessful. Please chack email and password','danger')
                return redirect(url_for("login"))
        else:
            flash('Login Unsuccessful. Please chack email and password','danger')
            return redirect(url_for("login"))
                
    else:
        return render_template("login.html", title='Login', form = form)
    
    
@app.route("/logout")
def logout():
    del session["username"]
    return redirect(url_for("login"))

@app.route("/diary",methods=['GET','POST'])
def diary():
    posts = dbase.db.diary.find({'username':session['username']})
    
    return render_template("my_diary.html", posts=posts)
    
    
@app.route("/add_diary",methods=['GET','POST'])
def add_diary(): 
    form = diary_form()
    if request.method == 'POST':
        diary = dbase.db.diary
        if form.validate_on_submit():
            d_post = {'username':session['username'],
                        'title':request.form['title'],'content':request.form['content'],'time':datetime.datetime.now()}
            diary.insert(d_post)
            flash('You just save a new content to your diary!!!','success')
            return redirect(url_for("diary"))
            
        else:
            return "All fields are requered"
    return render_template("add_diary.html",form= form)
    
    
@app.route("/account",methods=['POST','GET'])
def account():
    form = Updateform()
    if 'username' not in session:
        return redirect(url_for("login"))
        
    else:
        image=url_for('static',filename='image/default.png')
        if form.validate_on_submit():
            old_username=session['user']['username']
            session['user']['username']=form.username.data
            session['user']['email']=form.email.data
            user=dbase.db['users'].find_one({'username':old_username})
            
        return render_template("account.html", title='Account',image=image, form=form)



if __name__ == "__main__":
    app.secret_key ='mysecret'
    app.run(host=os.getenv('IP', '0.0.0.0'), port=int(os.getenv('PORT', 8080)), debug=True)