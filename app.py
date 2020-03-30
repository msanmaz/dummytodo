from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://m@localhost:5432/todosapp' ##db login
db = SQLAlchemy(app)


##database model
class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True) ##id of db's columns
    description = db.Column(db.String(), nullable=False) ##data itself

    def __repr__(self): ##debugging repr method
        return f'<Todo {self.id} {self.description}>'

db.create_all() ##



@app.route('/')
def index():
    return render_template('index.html', data=Todo.query.all()) ##include data from data base


@app.route('/todos/create', methods=['POST'])
def create_todo():
  description = request.form.get('description', '') ##request.form.get grabs form
  todo = Todo(description=description) ##db update
  db.session.add(todo)
  db.session.commit()
  return redirect(url_for('index')) ##redirect


if(__name__)== '__main__': 
    app.run()