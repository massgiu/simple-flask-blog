from flask import Flask, render_template, url_for
app = Flask(__name__) #var

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
def hello():
    return render_template('home.html',posts = posts)

@app.route("/about")
def about():
    return render_template('about.html', title='about')

# if __name__ == "__main__":
#     app.run(debug=True)