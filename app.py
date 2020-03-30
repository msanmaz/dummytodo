from flask import Flask, render_template, request, redirect, url_for, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
import sys


app = Flask(__name__)
# db login
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://m@localhost:5432/todosapp'
db = SQLAlchemy(app)


# database model
class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)  # id of db's columns
    description = db.Column(db.String(), nullable=False)  # data itself

    def __repr__(self):  # debugging repr method
        return f'<Todo {self.id} {self.description}>'


@app.route('/todos/create', methods=['POST'])
def create_todo():
    error = False
    body = {}
    try:
        # request.get.json body json response
        description = request.get_json()['description']
        todo = Todo(description=description)  # db update
        db.session.add(todo)
        db.session.commit()
        body['description'] = todo.description
    except:
        error = True
        db.session.rollback()
        print(sys.ext_info())
    finally:
        db.session.close()
    if error:
        abort (400)
    else:
        return jsonify(body)


@app.route('/')
def index():
    return render_template('index.html', data=Todo.query.all()) ##include data from data base

