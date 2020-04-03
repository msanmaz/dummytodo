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
        
    def __repr__(self):  # debugging repr method
        return f'<Todo {self.id} {self.description}>'



@app.route('/todos/list/create', methods=['POST'])   
def list_create():
    try:
        listUpdate = request.get_json()['list']
        todoList = TodoList(name=listUpdate)
        db.session.add(todoList)
        db.session.commit()
    except:
        db.session.rollback()
    finally:
        db.session.close()
    if error:
        abort(400)
    else:
        return jsonify(body)





@app.route('/todos/create', methods=['POST'])
def create_todo():
    error = False
    body = {}
    try:
        # request.get.json body json response
        description = request.get_json()['description']
        list_id = request.get_json()['list_id']
        todo = Todo(description=description, completed=False)
        active_list = TodoList.query.get(list_id)
        todo.list = active_list  # db update
        db.session.add(todo)
        db.session.commit()
    except ValueError:
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
    return redirect(url_for('list_number', todo_list=1))



@app.route('/lists/<todo_list>')
def list_number(todo_list):
    return render_template('index.html', 
    lists=TodoList.query.all(),
    active_list=TodoList.query.get(todo_list),
    todos=Todo.query.filter_by(todo_list=todo_list).order_by('id').all()
    )




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
