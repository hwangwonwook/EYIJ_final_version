from flask import Flask, render_template, flash,redirect,url_for
from flask import request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Session
import os
basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.secret_key ="asd"
app.config['SQLALCHEMY_DATABASE_URI'] = \
    'sqlite:///' + os.path.join(basedir, 'ey_db.db')
db=SQLAlchemy(app)


#회원가입db
class Eydb(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uid= db.Column(db.String(80), unique=True, nullable=False)
    upw = db.Column(db.String(100), unique=False, nullable=False)
    nn = db.Column(db.String(80), unique=True, nullable=False)
    uimg = db.Column(db.String(500), unique=False, nullable=False)
    mt= db.Column(db.String(4), unique=False, nullable=False)
    ut= db.Column(db.String(300), unique=False, nullable=False)



#글쓰기 db
class Podb(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pt = db.Column(db.String(20), unique=False, nullable=False)
    ct = db.Column(db.String(500), unique=False, nullable=False)
    comments = db.relationship('Com_t', backref='podb', lazy=True)

    
    # 댓글 db 테이블
class Com_t(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    u_coment = db.Column(db.String(200), unique=False, nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('podb.id'), nullable=False)
with app.app_context():
    db.create_all()

# 댓글 생성 클래스


@app.route('/coment_create/<int:post_id>')
def coment_create(post_id):
    u_coment_recive = request.args.get("comment")
    p_id = request.args.get("p_id")
    com_t = Com_t(u_coment=u_coment_recive, post_id=p_id)
    db.session.add(com_t)
    db.session.commit()
    return redirect(url_for('ey_post_con', p_id=p_id))
# 상세 게시글


@app.route('/ey_post_con')
def ey_post_con():
    postid = request.args.get("p_id")
    session = Session(bind=db.engine)
    dpost = session.get(Podb, postid)
    cposts = Com_t.query.filter_by(post_id=postid).all()
    post_con_list = Com_t.query.all()
    # return render_template('ey_post_con.html', data=post_con_list)
    return render_template('ey_post_con.html', post=dpost, com_t=cposts)
# 게시물 상세 페이지


@app.route('/ey_d_post/<int:post_id>', methods=['POST'])
def ey_d_post(post_id):
    session = Session(bind=db.engine)
    dpost = session.get(Podb, post_id)
    cposts = Com_t.query.filter_by(post_id=post_id).all()
    return render_template('ey_post_con.html', post=dpost, com_t=cposts)


# 댓글 삭제 클래스


@app.route('/coment_edit/<int:com_t_id>', methods=['POST'])
def coment_edit(com_t_id):
    act = request.form.get('com_b')
    # print(act, com_t_id)
    com_del = Com_t.query.get(com_t_id)
    postid = request.form.get("p_id")
    if com_del:
        db.session.delete(com_del)
        db.session.commit()
    return redirect(url_for('ey_post_con', p_id=postid))

# 댓글 업데이트


@app.route('/coment_update')
def coment_update():
    commenId = request.args.get('commentId')
    content = request.args.get('content')
    postid = request.args.get('postId')
    print(commenId, content, postid, "포스트아이디")
    comment = Com_t.query.get(commenId)
    if commenId:
        comment.u_coment = content
        db.session.commit()
    return redirect(url_for('ey_post_con', p_id=postid))


#회원가입 함수
@app.route('/join')
def ey_join():
    uid_recive=request.args.get("u_id")
    upw_recive=request.args.get("u_pw")
    nn_recive=request.args.get("nn")
    mt_recive=request.args.get("mt")
    ut_recive=request.args.get("ut")
    uimg_recive="asdf"

    eydb=Eydb(uid=uid_recive, upw=upw_recive, nn=nn_recive, mt=mt_recive, ut=ut_recive, uimg=uimg_recive)
    db.session.add(eydb)
    db.session.commit()
    return render_template('ey_in.html')


# 로그인 함수
@app.route('/ey_uid')
def ey_uid():
    u_id=request.args.get("l_id")
    u_pw=request.args.get("l_pw")
    print(u_id,u_pw)
    user =Eydb.query.filter_by(uid=u_id).first() #비교하는코드
    if user:
        if u_pw==user.upw:
            flash('로그인에 성공했습니다!')
            
            return redirect(url_for('home'))
        
    flash("로그인실패")
    return redirect(url_for('ey_login'))
@app.route('/')
def home():
    return render_template('eyij.html')


#글쓰기
@app.route('/write-post')
def submit_post():
    pt = request.form.get('title')
    ct = request.form.get('content')
    # like=request.form.get('like')
    return render_template('write-post.html')


#글쓰기 저장
@app.route('/cr_post', methods=['POST'])
def cr_post():
    u_pt = request.form.get('title')
    u_ct = request.form.get('content')

    podb = Podb(pt=u_pt, ct=u_ct)
    db.session.add(podb)
    db.session.commit()
    return redirect(url_for('popular_posts'))


#게시글 페이지
@app.route('/ey_post')
def popular_posts():
    print('asd')
    post_list = Podb.query.all()
    print(post_list)
    return render_template('ey_post.html', data=post_list)


#팀소개 페이지
@app.route('/ey_team')
def ey_team():
    return render_template('ey_team.html')


#로그인 페이지
@app.route('/ey_login')
def ey_login():
    return render_template('ey_login.html')


#회원가입 페이지
@app.route('/ey_in')
def ey_in():
    return render_template('ey_in.html')


#게시물 수정
@app.route('/update-post/<int:post_id>', methods=['POST'])
def update_post(post_id):
    post = Podb.query.get_or_404(post_id)
    post.pt = request.form['postTitle']
    post.ct = request.form['postContent']
    db.session.commit()
    return redirect(url_for('popular_posts'))



# 게시물 삭제
@app.route('/delete_post/<int:post_id>', methods=['POST'])
def delete_post(post_id):
    post = Podb.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('popular_posts'))


if __name__ == '__main__':
    app.run(debug=True)


