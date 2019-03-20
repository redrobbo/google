#-----------------------------------------------------------------------------------------------------------------------
# Script | routes.py
# Author | Jonathan Cox
# Date   | 18 / 3 / 18
#-----------------------------------------------------------------------------------------------------------------------
# Imports
#-----------------------------------------------------------------------------------------------------------------------

from flask import render_template, url_for, flash, redirect, request, abort, Response
from web import app, db, bcrypt, mail
from web.forms import Registration, Login, UpdateAccount, PostForm, RequestReset, ResetPassword, Search, SearchForm
from web.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message
from PIL import Image
import secrets
import os

import json

#-----------------------------------------------------------------------------------------------------------------------
# Main Pages
#-----------------------------------------------------------------------------------------------------------------------

@app.route("/")
def start():
    return redirect(url_for('home'))

#-----------------------------------------------------------------------------------------------------------------------

@app.route("/home", methods=['GET', 'POST'])
def home():
    search = Search()
    if search.validate_on_submit():
        page = request.args.get('page', 1, type=int)
        posts = Post.query.filter(Post.animal_name.like('%' + str(search.search_name.data) + '%'), Post.animal_type.like('%' + str(search.search_type.data) + '%'), Post.animal_gender.like('%' + str(search.search_gender.data) + '%'), Post.animal_breed.like('%' + str(search.search_breed.data) + '%'), Post.animal_color.like('%' + str(search.search_color.data) + '%')).order_by(Post.date.desc()).paginate(page=page, per_page=10)
        for post in posts.items:
            if len(post.content) > 50:
                post.content = post.content[:50] + " ..."
        return render_template('home.html', posts=posts, title='Home', search=search)
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date.desc()).paginate(page=page, per_page=10)
    for post in posts.items:
        if len(post.content) > 50:
            post.content = post.content[:50] + " ..."
    return render_template('home.html', posts=posts, title='Home', search=search)

#-----------------------------------------------------------------------------------------------------------------------

@app.route("/about")
def about():
    return render_template('about.html', title='About')

#-----------------------------------------------------------------------------------------------------------------------
# User Routes
#-----------------------------------------------------------------------------------------------------------------------

def save_picture(form_picture):
    picture_name = secrets.token_hex(8)
    _, pic_ext = os.path.splitext(form_picture.filename)
    fn_pic_name = picture_name + pic_ext
    picture_path = os.path.join(app.root_path, 'static/images', fn_pic_name)
    output_size = (250, 250)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return fn_pic_name

#-----------------------------------------------------------------------------------------------------------------------

@app.route("/account", methods=['GET','POST'])
@login_required
def account():
    form = UpdateAccount()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.img_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your Account Has Been Updated', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    profile_pic = url_for('static', filename='images/' + current_user.img_file)
    return render_template('account.html', title='Account', profile_pic=profile_pic, form=form)

#-----------------------------------------------------------------------------------------------------------------------

@app.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user).order_by(Post.date.desc()).paginate(page=page, per_page=10)
    for post in posts.items:
        if len(post.content) > 50:
            post.content = post.content[:50] + " ..."
    return render_template('user.html', posts=posts, title='User', user=user)

#-----------------------------------------------------------------------------------------------------------------------
# Posts
#-----------------------------------------------------------------------------------------------------------------------

def save_pic(form_picture):
    picture_name = secrets.token_hex(8)
    _, pic_ext = os.path.splitext(form_picture.filename)
    fn_pic_name = picture_name + pic_ext
    picture_path = os.path.join(app.root_path, 'static/images', fn_pic_name)
    output_size = (500, 500)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return fn_pic_name

#-----------------------------------------------------------------------------------------------------------------------

@app.route("/post/new", methods=['GET','POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        if form.animal_pic.data:
            picture_file = save_pic(form.animal_pic.data)
            post = Post(animal_name=form.animal_name.data,  animal_type=form.animal_type.data, animal_gender=form.animal_gender.data, animal_breed=form.animal_breed.data, animal_color=form.animal_color.data, address=form.address.data, content=form.content.data, animal_pic=picture_file, author=current_user)
            db.session.add(post)
            db.session.commit()
            flash('Your post has been made', 'success')
            return redirect(url_for('home'))
        else:
            post = Post(animal_name=form.animal_name.data, animal_type=form.animal_type.data, animal_gender=form.animal_gender.data, animal_breed=form.animal_breed.data, animal_color=form.animal_color.data, address=form.address.data, content=form.content.data, author=current_user)
            db.session.add(post)
            db.session.commit()
            flash('Your post has been made', 'success')
            return redirect(url_for('home'))
    return render_template('new_post.html', title='New Post', form=form, legend='New Post')

#-----------------------------------------------------------------------------------------------------------------------

@app.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.animal_name, post=post)

#-----------------------------------------------------------------------------------------------------------------------

@app.route("/post/<int:post_id>/update", methods=['GET','POST'])
@login_required
def update_post(post_id):
        post = Post.query.get_or_404(post_id)
        if post.author != current_user:
            abort(403)
        form = PostForm()
        if form.validate_on_submit():
            if form.animal_pic.data:
                picture_file = save_pic(form.animal_pic.data)
                post.animal_pic = picture_file
            post.animal_name = form.animal_name.data
            post.animal_type = form.animal_type.data
            post.animal_gender = form.animal_gender.data
            post.animal_breed = form.animal_breed.data
            post.animal_color = form.animal_color.data
            post.address = form.address.data
            post.content = form.content.data
            db.session.commit()
            flash('Your Post Has Been Updated', 'success')
            return redirect(url_for('post', post_id=post.id))
        elif request.method == 'GET':
            form.animal_name.data = post.animal_name
            form.animal_type.data = post.animal_type
            form.animal_gender.data = post.animal_gender
            form.animal_breed.data = post.animal_breed
            form.animal_color.data = post.animal_color
            form.address.data = post.address
            form.content.data = post.content
        return render_template('new_post.html', title='Update Post', post=post, form=form, legend='Update Post')

#-----------------------------------------------------------------------------------------------------------------------

@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
        post = Post.query.get_or_404(post_id)
        if post.author != current_user:
            abort(403)
        db.session.delete(post)
        db.session.commit()
        flash('Your Post Has Been Deleted', 'success')
        return redirect(url_for('home'))

#-----------------------------------------------------------------------------------------------------------------------
# User Management
#-----------------------------------------------------------------------------------------------------------------------

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = Login()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next = request.args.get('next')
            return redirect(next) if next else redirect(url_for('home'))
        else:
            flash('Logged Failed check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)

#-----------------------------------------------------------------------------------------------------------------------

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

#-----------------------------------------------------------------------------------------------------------------------

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = Registration()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account Created For {form.username.data} You Can Now Login', 'success') #This may produce error if version is less than 3.6 and IDE's that dont support it
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

#-----------------------------------------------------------------------------------------------------------------------

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender='Noreply@PetsMail.com', recipients=[user.email])
    msg.body = f'''Reset Password Click The Following Link:
    {url_for('reset_password', token=token, _external=True)}

    If you did not reset your password ignore this email.
    '''
    mail.send(msg)

#-----------------------------------------------------------------------------------------------------------------------

@app.route("/reset_request", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestReset()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('Email Sent For Reset Password', 'info')
        return redirect(url_for('login'))
    return render_template('reset_request.html', title='Reset Password', form=form)

#-----------------------------------------------------------------------------------------------------------------------

@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That Token Has Expired', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPassword()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Account Password Changed You Can Now Login', 'success')
        return redirect(url_for('login'))
    return render_template('reset_password.html', title='Reset Password', form=form)

#-----------------------------------------------------------------------------------------------------------------------

@app.errorhandler(404)
def error_404(error):
    return render_template('404.html'), 404

#-----------------------------------------------------------------------------------------------------------------------

@app.errorhandler(403)
def error_403(error):
    return render_template('403.html'), 403

#-----------------------------------------------------------------------------------------------------------------------

@app.errorhandler(500)
def error_500(error):
    return render_template('404.html'), 500


#-----------------------------------------------------------------------------------------------------------------------
# Autocomplete Dumps
#-----------------------------------------------------------------------------------------------------------------------

@app.route('/names', methods=['GET'])
def names():
    posts = Post.query.order_by(Post.date.desc()).all()
    names = []
    for post in posts:
        if post.animal_name not in names:
            names.append(post.animal_name)
    return Response(json.dumps(names), mimetype='application/json')

#-----------------------------------------------------------------------------------------------------------------------

@app.route('/animals', methods=['GET'])
def animals():
    posts = Post.query.order_by(Post.date.desc()).all()
    animals = []
    for post in posts:
        if post.animal_type not in animals:
            animals.append(post.animal_type)
    return Response(json.dumps(animals), mimetype='application/json')

#-----------------------------------------------------------------------------------------------------------------------

@app.route('/breeds', methods=['GET'])
def breeds():
    posts = Post.query.order_by(Post.date.desc()).all()
    breeds = []
    for post in posts:
        if post.animal_breed not in breeds:
            breeds.append(post.animal_breed)
    return Response(json.dumps(breeds), mimetype='application/json')

#-----------------------------------------------------------------------------------------------------------------------

@app.route('/colors', methods=['GET'])
def colors():
    posts = Post.query.order_by(Post.date.desc()).all()
    colors = []
    for post in posts:
        if post.animal_color not in colors:
            colors.append(post.animal_color)
    return Response(json.dumps(colors), mimetype='application/json')

#-----------------------------------------------------------------------------------------------------------------------

@app.route('/test', methods=['GET', 'POST'])
def index():
    form = SearchForm(request.form)
    return render_template("search.html", form=form)
