from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# Setting up postgres database

app.config.update(
    SECRET_KEY='flima_is_laura',
    SQLALCHEMY_DATABASE_URI='postgresql://postgres:flima_is_laura@localhost/catalog_db',
    SQLACHEMY_TRACK_MODIFICATIONS=False
)

db = SQLAlchemy(app)


# Basic routes

@app.route('/')
def hello_laura() -> str:
    return 'Hello sweet Laura! How are things in Melbourne?'


@app.route('/new/')
def query_strings(greeting='Laura, now and always') -> str:
    query_val = request.args.get('greeting', greeting)
    return '<h1> the greeting is: {0} <h1>'.format(query_val)


@app.route('/user')
@app.route('/user/<name>')
def no_query_strings(name='Lovely Laurette') -> str:
    return '<h1> Hello my {} <h1>'.format(name)


# Strings
@app.route('/text/<string:name>')
def working_with_strings(name):
    return '<h1> Finding love in Melbourne is:' + name + '<h1>'.format(name)


# Numbers1
@app.route('/numbers/<int:num>')
def working_with_numbers(num) -> int:
    return '<h1> Her age shall be: ' + str(num) + '<h1>'


# Numbers2
@app.route('/add/<int:num1>/<int:num2>')
def adding_integers(num1, num2) -> int:
    return '</h1> The total price is: {}'.format(num1 + num2) + '</h1>'


# Floats
@app.route('/product/<float:num1>/<float:num2>')
def multiply_floats(num1, num2) -> float:
    return '<h1> Your weekly earning is : {}'.format(num1 * num2) + '</h1>'


# Using templates
@app.route('/welcome')
def using_templates() -> 'html':
    return render_template('welcome.html')


# Jinja Templates
@app.route('/watch')
def top_movies():
    movie_list = ['About a boy',
                  'Home Alone',
                  'Along came Polly',
                  'The Proposal',
                  'Bad Santa',
                  'Miracle in Melbourne',
                  'Two seeds on the edge']

    return render_template('movies.html',
                           movies=movie_list,
                           name='Laura')


@app.route('/table')
def movies_details():
    movies_dict = {'About a boy': 1.41,
                   'Home Alone': 1.43,
                   'Along came Polly': 1.30,
                   'The Proposal': 1.48,
                   'Bad Santa': 1.31,
                   'Miracle in Melbourne': 2.36,
                   'Two seeds on the edge': 3.15}
    return render_template('table_data.html',
                           movies=movies_dict,
                           name='Laura')


class Publication(db.Model):
    __tablename__ = 'publication'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)

    def __init__(self, name) -> None:
        self.name = name

    def __repr__(self) -> str:
        return 'The Publisher is {}'.format(self.name)


class Book(db.Model):
    __tablename__ = 'book'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(500), nullable=False, index=True)
    author = db.Column(db.String(350))
    avg_rating = db.Column(db.Float)
    book_format = db.Column(db.String(50))
    image = db.Column(db.String(100), unique=True)
    num_pages = db.Column(db.Integer)
    pub_date = db.Column(db.DateTime, default=datetime.utcnow())

    # Relationship
    pub_id = db.Column(db.Integer, db.ForeignKey('publication.id'))

    def __init__(self, title, author, avg_rating, book_format, image, num_pages, pub_id):
        self.title = title
        self.author = author
        self.avg_rating = avg_rating
        self.book_format = book_format

        self.image = image
        self.num_pages = num_pages
        self.pub_id = pub_id

    def __repr__(self):
        return '{} by {}'.format(self.title, self.author)


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
