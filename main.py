from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
import sqlite3

app = Flask(__name__)
Bootstrap(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Books.db'
db = SQLAlchemy(app)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


class Books(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    author = db.Column(db.String(250), unique=False, nullable=True)
    rating = db.Column(db.Float, nullable=False)

with app.app_context():
    db.create_all()



@app.route('/')
def home():
    all_books = db.session.query(Books).all()
    return render_template('index.html', books=all_books, count = len(all_books))


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        new_book = Books(title=request.form["title"], author=request.form["author"], rating=request.form["rating"])
        db.session.add(new_book)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('add.html')

@app.route("/edit", methods = ["GET", "POST"])
def edit():
    if request.method == "POST":
        id = request.form["id"]
        book = Books.query.filter_by(id=id).first()
        book.rating = request.form["new_rating"]
        db.session.commit()
        return redirect(url_for('home'))
    id = request.args.get('id')
    book = Books.query.filter_by(id=id).first()
    return render_template('edit.html', book=book)

@app.route("/delete")
def delete():
    book_id = request.args.get('id')
    book_to_delete = Books.query.get(book_id)
    db.session.delete(book_to_delete)
    db.session.commit()
    return redirect(url_for('home'))



if __name__ == "__main__":
    app.run(debug=True)

