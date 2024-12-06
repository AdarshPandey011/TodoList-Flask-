from datetime import datetime
from flask import Flask,render_template,url_for,request,redirect

from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy import Nullable

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Todos(db.Model):
  
  id = db.Column(db.Integer, primary_key=True)
  content = db.Column(db.String(200), nullable=False)
  completed = db.Column(db.Integer,default = 0)
  date_created = db.Column(db.DateTime,default=datetime.utcnow)

@app.route('/',methods=['POST','GET'])
def index():
  if request.method == 'POST':
    task_content = request.form['content']
    new_task = Todos(content=task_content)
    # print('form',task_con tent)
    try:
      db.session.add(new_task)
      db.session.commit()
      return redirect('/')
    except:
      return 'There was an error adding your task'
    
  else:
    tasks = Todos.query.order_by(Todos.date_created).all()
    return render_template('index.html',task=tasks)
  
@app.route('/delete/<int:id>')
def delete(id):
  to_delete = Todos.query.get_or_404(id)
  print('-------------------');
  print(to_delete,id)
    
  try:
    
    db.session.delete(to_delete)
    db.session.commit()
    return redirect('/')
  except:
    return 'There was a problem deleting that task'
  
@app.route('/update/<int:id>',methods=['GET','POST'])
def update(id):
  task = Todos.query.get_or_404(id)

  if request.method == 'POST':
    task.content = request.form['content']

    try:
      db.session.commit()
      return redirect('/')
    except:
      return 'Something wrong'

  else:
    return render_template('update.html',task=task)
    

def __repr__(self):
  return '<Task %r>' % self.id

if __name__ == '__main__':
  app.run(debug=True)


# from datetime import datetime
# from flask import Flask, render_template, url_for
# from flask_sqlalchemy import SQLAlchemy

# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
# db = SQLAlchemy(app)

# class Todos(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     content = db.Column(db.String(200), nullable=False)
#     completed = db.Column(db.Integer, default=0)
#     date_created = db.Column(db.DateTime, default=datetime.utcnow)

#     def __repr__(self):
#         return '<Task %r>' % self.id

# @app.route('/')
# def index():
#     return render_template('index.html')

# if __name__ == '__main__':
#     with app.app_context():
#         db.create_all()
#     app.run(debug=True)