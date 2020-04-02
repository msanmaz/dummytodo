from flask import Flask, render_template, request, redirect, url_for, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
import sys
from flask_migrate import Migrate


app = Flask(__name__)
# db login
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://m@localhost:5432/todosapp'
db = SQLAlchemy(app)

migrate = Migrate(app, db)


# database model
class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)  # id of db's columns
    description = db.Column(db.String(), nullable=False)  # data itself
    completed = db.Column(db.Boolean, nullable=False, default=False)
    todo_list = db.Column(db.Integer, db.ForeignKey('todolists.id'), nullable=False)

    def __repr__(self):  # debugging repr method
        return f'<Todo {self.id} {self.description}>'


class TodoList(db.Model):
    __tablename__ = 'todolists'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    todos = db.relationship('Todo', backref='list', lazy=True)

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
    finally:
        db.session.close()
    if error:
        abort(400)
    else:
        return jsonify(body)


@app.route('/')
def index():
    # include data from data base
    return render_template('index.html', data=Todo.query.all())


@app.route('/todos/<todo_id>/set-completed', methods=['POST'])
def setcomp(todo_id):
    try:
        completed = request.get_json()['completed']
        print('completed', completed)
        todo = Todo.query.get(todo_id)
        todo.completed = completed
        db.session.commit()
    except ValueError:
        db.session.rollback()
    finally:
        db.session.close()
    return redirect(url_for('index'))


@app.route('/todos/<deletedId>/delete', methods=['DELETE'])
def delete(deletedId):
    try:
        Todo.query.filter_by(id=deletedId).delete()
        db.session.commit()
    except:
        db.session.rollback()
    finally:
        db.session.close()
    return jsonify({'success': True})
