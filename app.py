from flask import Flask, jsonify, request
import psycopg2
import os

def create_app():
    app = Flask(__name__)

    def get_db_connection():
        conn = psycopg2.connect(
            host=os.environ.get("POSTGRES_HOST", "localhost"),
            port=int(os.environ.get("POSTGRES_PORT", "5432")),
            database=os.environ.get("POSTGRES_DB", "library_test_db"),
            user=os.environ.get("POSTGRES_USER", "postgres"),
            password=os.environ.get("POSTGRES_PASSWORD", "secret"),
        )
        return conn

    @app.route("/api/authors", methods=["GET"])
    def get_authors():
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, name FROM authors ORDER BY id")
        authors = [{"id": row[0], "name": row[1]} for row in cur.fetchall()]
        cur.close()
        conn.close()
        return jsonify(authors)

    @app.route("/api/authors", methods=["POST"])
    def create_author():
        data = request.get_json()
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO authors (name) VALUES (%s) RETURNING id", (data["name"],))
        author_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"id": author_id, "name": data["name"]}), 201

    @app.route("/api/authors/<int:author_id>", methods=["GET"])
    def get_author(author_id):
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, name FROM authors WHERE id = %s", (author_id,))
        row = cur.fetchone()
        cur.close()
        conn.close()
        if row:
            return jsonify({"id": row[0], "name": row[1]})
        return jsonify({"error": "Author not found"}), 404

    @app.route("/api/authors/<int:author_id>", methods=["PUT"])
    def update_author(author_id):
        data = request.get_json()
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("UPDATE authors SET name = %s WHERE id = %s", (data["name"], author_id))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"id": author_id, "name": data["name"]})

    @app.route("/api/authors/<int:author_id>", methods=["DELETE"])
    def delete_author(author_id):
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM authors WHERE id = %s", (author_id,))
        conn.commit()
        cur.close()
        conn.close()
        return "", 204

    @app.route("/api/books", methods=["GET"])
    def get_books():
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, title, author_id, status FROM books ORDER BY id")
        books = [{"id": row[0], "title": row[1], "author_id": row[2], "status": row[3]} for row in cur.fetchall()]
        cur.close()
        conn.close()
        return jsonify(books)

    @app.route("/api/books", methods=["POST"])
    def create_book():
        data = request.get_json()
        conn = get_db_connection()
        cur = conn.cursor()
        status = data.get("status", "available")
        cur.execute(
            "INSERT INTO books (title, author_id, status) VALUES (%s, %s, %s) RETURNING id",
            (data["title"], data.get("author_id"), status)
        )
        book_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"id": book_id, "title": data["title"], "author_id": data.get("author_id"), "status": status}), 201

    @app.route("/api/books/<int:book_id>", methods=["GET"])
    def get_book(book_id):
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, title, author_id, status FROM books WHERE id = %s", (book_id,))
        row = cur.fetchone()
        cur.close()
        conn.close()
        if row:
            return jsonify({"id": row[0], "title": row[1], "author_id": row[2], "status": row[3]})
        return jsonify({"error": "Book not found"}), 404

    @app.route("/api/books/<int:book_id>", methods=["PUT"])
    def update_book(book_id):
        data = request.get_json()
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            "UPDATE books SET title = %s, author_id = %s, status = %s WHERE id = %s",
            (data["title"], data.get("author_id"), data.get("status", "available"), book_id)
        )
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"id": book_id, "title": data["title"], "author_id": data.get("author_id"), "status": data.get("status", "available")})

    @app.route("/api/books/<int:book_id>", methods=["DELETE"])
    def delete_book(book_id):
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM books WHERE id = %s", (book_id,))
        conn.commit()
        cur.close()
        conn.close()
        return "", 204

    return app