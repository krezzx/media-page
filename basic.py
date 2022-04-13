from email.policy import default
from flask import Flask, render_template, flash, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate  
from werkzeug.utils import secure_filename
import os
#import magic
import urllib.request
basedir = os.path.abspath(os.path.dirname(__file__))

app=Flask(__name__)
app.config['SECRET_KEY']='my secret key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False 
UPLOAD_FOLDER = 'static/uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
 return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


db=SQLAlchemy(app)

Migrate(app,db)

class Posts(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    roll_no=db.Column(db.String(20))
    caption=db.Column(db.String(200))
    pic=db.Column(db.String(150))
    appr=db.Column(db.Integer,default=0)

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/feed')
def feed():
    P=Posts.query.with_entities(Posts.pic).all()
    P.reverse()
    p=dict()
    for i in P:
        post=Posts.query.filter_by(pic=i[0]).first()
        if(post.appr==1):
            a=[]
            a.append(post.roll_no)
            a.append(post.caption)
            picname='uploads/'+i[0]
            p[picname]=a
    return render_template('feedv1.html',p=p)

@app.route('/newfeed')
def newfeed():
    P=Posts.query.with_entities(Posts.pic).all()
    P.reverse()
    p=dict()
    for i in P:
        post=Posts.query.filter_by(pic=i[0]).first()
        a=[]
        a.append(post.roll_no)
        a.append(post.caption)
        picname='uploads/'+i[0]
        dec=False
        if(post.appr==1):
            dec=True   
        a.append(dec) 
        p[picname]=a
    return render_template('feed1.html',p=p,)

        

@app.route('/uplaod')
def upload():
    return render_template('upload.html')

@app.route('/uploader',methods=['GET','POST'])
def uploader():
    file = request.files['inputFile']
    #name tag of form
    roll_no = request.form['roll']
    caption=request.form['caption']
    filename=str(roll_no)+'_'+file.filename
    filename = secure_filename(filename)
  
    if file and allowed_file(file.filename):
       file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
  
       newFile = Posts(pic=filename, roll_no=roll_no,caption=caption)
       db.session.add(newFile)
       db.session.commit()
       flash('File successfully uploaded ' + file.filename + ' to the database!')
       return redirect(url_for('feed'))
    else:
       flash('Invalid Uplaod only txt, pdf, png, jpg, jpeg, gif') 
    return redirect(url_for('feed'))



@app.route('/review/<picid>',methods=['GET','POST']) 
def approve(picid):
    p=Posts.query.filter_by(pic=picid).first()
    p.appr=1
    db.session.commit()
    return redirect(url_for('newfeed'))

@app.route('/remove/<picid>',methods=['GET','POST']) 
def remove(picid):
    p=Posts.query.filter_by(pic=picid).first()
    p.appr=0
    db.session.commit()
    return redirect(url_for('newfeed'))



if __name__=='__main__':
    app.run(debug=True)
