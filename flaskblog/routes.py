import secrets, os
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from flaskblog import app, db, bcrypt
from flaskblog.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm
from flaskblog.models import User, Post
from flask_login import login_user, logout_user, current_user, login_required

@app.route("/")
@app.route("/home")
def home():
    posts = Post.query.all()
    return render_template('home.html',posts = posts)

@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        #create instance of user
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        #insert instance in db
        db.session.add(user)
        db.session.commit()
        flash(f'Your accont has been created successfully!','success')
        return redirect(url_for('login')) #redirect to the function

    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user,remember=form.remember.data)
            next_page = request.args.get('next') #get next parameter in the url
            #if next parameter exists in the url redirect to account page, else to home page
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Check your email and password','danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return (redirect(url_for('home')))

def save_picture(form_picture):
    #randomize name so we don't have collisions
    random_hex = secrets.token_hex(8)
    #grab file extension in order to keep for image saved
    f_name, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex+f_ext #new filename
    picture_path = os.path.join(app.root_path,'static/profile_pics',picture_fn) #destination directory for profile pics
    #resizing
    output_size = (125,125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn

@app.route("/account", methods=['GET','POST'])
@login_required
def account():
    form = UpdateAccountForm()
    #on update button
    if form.validate_on_submit():
        if form.picture.data: #if are there any new data
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        #update data on db
        db.session.commit()
        flash('Your account has been updated!','success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        #fill form with existing data
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/'+current_user.image_file) #profile_pics is a dir
    return render_template('account.html', title='Account', image_file=image_file, form=form)

@app.route("/post/new", methods=['GET','POST']) #accepting POST and GET request
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        # insert instance in db
        db.session.add(post)
        db.session.commit()
        flash('You post has been created','success')
        return redirect(url_for('home'))
    return render_template('create_post.html', title='New Post', form= form,legend='New Post')

#route to get spefic post
@app.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id) #if the post with that id doesn't exist-> 404
    return render_template('post.html', title=post.title, post=post)

@app.route("/post/<int:post_id>/update", methods=['GET','POST'])
@login_required #this recall login
def update_post(post_id):
    post = Post.query.get_or_404(post_id) #if the post with that id doesn't exist-> 404
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated', 'success')
        return redirect(url_for('post', post_id=post.id)) #redirect specific post
    elif request.method == 'GET':
        #Fill form with old title/content
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post', form=form, legend='Updated Post')

@app.route("/post/<int:post_id>/delete", methods=['POST','GET'])
@login_required #this recall login
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)  # if the post with that id doesn't exist-> 404
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('home'))
