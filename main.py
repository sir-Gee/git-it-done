from flask import Flask, request, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import select

app = Flask(__name__)

app.config['DEBUG'] = True      # displays runtime errors in the browser, too
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:qwerty@localhost:3306/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True


db = SQLAlchemy(app)


class Task(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))

    def __init__(self, name):
        self.name = name


# tasks = []
# results = db.session.execute(select([Task]))

# tasks = []

tasks = []

# for i in results:
#     tasks.append(i[1])
    # print(i[1])


@app.route('/', methods=['POST', 'GET'])
def index():

    if request.method == 'POST':
        task = request.form['task']

        if task in tasks:
            return redirect("/?error=You have this task on the list")

        db.session.add(Task(str(task)))
        db.session.commit()
        results = db.session.execute(select([Task]))
        tasks.clear()
        for item in results:
            tasks.append(item[1])

    if request.method == 'GET':
        results = db.session.execute(select([Task]))
        tasks.clear()
        for item in results:
            tasks.append(item[1])

    return render_template('todos.html', title="Get It Done!", tasks=tasks, errorTask=request.args.get("error"))


if __name__ == '__main__':
    app.run()
