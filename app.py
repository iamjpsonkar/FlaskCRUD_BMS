from email.policy import default
from flask import Flask, jsonify, request
from flask.views import MethodView

app = Flask(__name__)

"""
Book Model: Each book should have the following attributes:

id (Unique identifier)
title (Title of the book)
author (Author of the book)
published_date
"""

BOOKS = {
    "1": {
        "id": 1,
        "title": "title1",
        "author": "author1",
        "published_date": "10/11/2021",
    },
    "2": {
        "id": 2,
        "title": "title2",
        "author": "author2",
        "published_date": "12/11/2021",
    },
    "3": {
        "id": 3,
        "title": "title3",
        "author": "author3",
        "published_date": "14/11/2021",
    },
}


class Home(MethodView):
    def get(self):
        return """
        <html>
            <head>
                <title>Book Management System</title>
            </head>
            <body>
                <h1>Welcome to Book Management System!</h1>
                <a href="/books/">List of Books</a>
            </body>
        </html>
        """


class BookManagementSystem(MethodView):
    def get(self, id=None):
        if id:
            return jsonify(BOOKS.get(str(id)))
        else:
            return jsonify(BOOKS)

    def post(self):
        book = request.json
        if book:
            if book.get("id") in BOOKS:
                return jsonify({"status": 500, "message": "Book ID already exist"})
            else:
                if book.get("id"):
                    BOOKS[str(book.get("id"))] = book
                    return jsonify({"status": 200, "message": "Book added to DB"})
                else:
                    return jsonify({"status": 400, "message": "missing book id"})
        else:
            return jsonify({"status": 400, "message": "missing book details"})

    def put(self, id=None):
        book = request.json
        if id and str(id) in BOOKS and book:
            BOOKS[str(id)] = book
            return jsonify({"status": 200, "message": "Book updated in DB"})
        elif id and book:
            BOOKS[str(id)] = book
            return jsonify({"status": 200, "message": "Book added in DB"})
        else:
            return jsonify({"status": 400, "message": "missing book details/not found"})

    def delete(self, id=None):
        if id:
            BOOKS.pop(str(id))
            return jsonify({"status": 200, "message": "Book deleted from DB"})
        else:
            return jsonify({"status": 400, "message": "missing book missing"})


home_view = Home.as_view("home")
book_view = BookManagementSystem.as_view("book_api")


app.add_url_rule("/", view_func=home_view, methods=["GET"])
app.add_url_rule("/books/<int:id>/", view_func=book_view, methods=["GET"])
app.add_url_rule("/books/", view_func=book_view, methods=["POST"])
app.add_url_rule("/books/", defaults={"id": None}, view_func=book_view, methods=["GET"])
app.add_url_rule("/books/<int:id>/", view_func=book_view, methods=["PUT"])
app.add_url_rule("/books/<int:id>/", view_func=book_view, methods=["DELETE"])


if __name__ == "__main__":
    app.run(debug=True)
