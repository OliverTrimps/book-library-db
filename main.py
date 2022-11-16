from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///new-books-collection.db"
db = SQLAlchemy(app)
all_books = []


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    rating = db.Column(db.Float, nullable=False)


with app.app_context():
    db.create_all()


@app.route('/')
def home():
    with app.app_context():
        books = db.session.query(Book).all()
    # if len(books) < 1:
    #     return render_template("index.html", book_list="Library is empty.")
    # # if len(all_books) < 1:
    # #     return render_template("index.html", book_list="Library is empty.")
    # else:
    #     # return render_template("index.html", book_list=all_books)
    return render_template("index.html", book_list=books)


@app.route("/add", methods=["POST", "GET"])
def add():
    # message = None
    # book_library = {}
    if request.method == 'POST':
        data = request.form
        # book_library['Name'] = data['book_name']
        # book_library['Author'] = data['book_author']
        # book_library['Rating'] = float(data['book_rating'])
        # all_books.append(book_library)
        # # return url_for('home')
        # print(all_books)
        with app.app_context():
            # db.create_all()
            new_book = Book(title=data['book_name'], author=data['book_author'], rating=data['book_rating'])
            db.session.add(new_book)
            db.session.commit()
        # message = "Added!"
        # return render_template("add.html", msg=message)
        return redirect("/")
    return render_template("add.html")


@app.route("/edit", methods=["POST", "GET"])
def rating():
    if request.method == "POST":
        data = request.form
        with app.app_context():
            book_id = data['id']
            book_to_update = Book.query.get(book_id)
            book_to_update.rating = data['book_rating']
            db.session.commit()
            return redirect(url_for('home'))
    book_id = request.args.get('id')  # id value gotten from index.html a href link
    book_selected = Book.query.get(book_id)
    return render_template("rating.html", book=book_selected)


@app.route("/delete", methods=["GET", "POST"])
def delete():
    book_id = request.args.get('id')
    with app.app_context():
        book_to_delete = Book.query.get(book_id)
        db.session.delete(book_to_delete)
        db.session.commit()
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)

