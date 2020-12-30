from flask import Flask, render_template, url_for, flash, redirect
from src.forms import RegistrationForm, LoginForm
app = Flask(__name__) #var

#Set secret  cookie
app.config['SECRET_KEY']='e4f3b857d3c940c8a2683afa6055ad29'

posts = [
    {
        'author': 'M. Giunchi',
        'title': 'Blog post 1',
        'content': 'First post',
        'date_posted' : 'June 1 2020'
    },
    {
        'author': 'M. Giunchi',
        'title': 'Blog post 2',
        'content': 'Second post',
        'date_posted' : 'June 2 2020'
    }
]

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html',posts = posts)

@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Accont created for {form.username.data}!','success')
        return redirect(url_for('home')) #redirect to the function

    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have been logged in!','success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Check your username and password','danger')
    return render_template('login.html', title='Login', form=form)

# if __name__ == "__main__":
#     app.run(debug=True)