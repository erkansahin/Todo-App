# Author: Erkan Şahin
# A basic Todo App using flask orm SQL Alchemy.

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import Flask,render_template,redirect,url_for,request

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/Erkan/Desktop/todo app/todo.db'
db = SQLAlchemy(app)

@app.route('/')
def index():
    todos = Todo.query.all()
    return render_template('index.html',todos = todos)

# This method adds a new task that the clients want to add to the database. 
@app.route('/add',methods= ['POST'])
def add_todo():
    title = request.form.get('title')
    newTodo = Todo(title = title,complete = False)
    db.session.add(newTodo)
    db.session.commit()
    return redirect(url_for('index'))

# The state of the task is kept here. The state is true if the task is completed.
@app.route('/complete/<string:id>')
def completeTodo(id):
    todo = Todo.query.filter_by(id=id).first()
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for('index'))    

# This method removes a task that the clients want to remove from the database. 
@app.route('/delete/<string:id>')
def removeTodo(id):
    todo = Todo.query.filter_by(id=id).first()
    db.session.delete(todo)
    db.session.commit()

    return redirect(url_for('index'))
         

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    complete = db.Column(db.Boolean)

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
