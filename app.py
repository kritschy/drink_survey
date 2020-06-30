from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///survey.sqlite3'
db = SQLAlchemy(app)

class Results(db.Model):
     id = db.Column(db.Integer, primary_key=True)
     name = db.Column(db.String(30), nullable=False, unique=True)
     votes = db.Column(db.Integer, default=0, nullable=False)     
     date_created = db.Column(db.DateTime, default=datetime.utcnow)


     


@app.route('/', methods=['POST', 'GET'])
def index():
    results = []
    if request.method == 'POST':
        results.append(request.form['first'])
        results.append(request.form['second'])
        results.append(request.form['third'])


        if results[0] == results[1] or results[0] == results[2] or results[1] == results[2]:
            return 'choosing two times or more the same is forbidden'

        else:
           updateSelection(results)
           return 'thanks'

        # try:
        #     db.session.add(commit_object)
        #     db.session.commit()

        #     return redirect('/')
        # except: 
        #     return 'failed'
    else:

        return render_template('index.html')


def updateSelection(results):
    try:
        first_Selection = results[0]
        second_Selection = results[1]
        third_Selection = results[2]

        first_Selection = Results.query.filter_by(name=first_Selection).first()
        second_Selection = Results.query.filter_by(name=second_Selection).first()
        third_Selection = Results.query.filter_by(name=third_Selection).first()

        print(first_Selection.votes, second_Selection.votes, third_Selection.votes)

        first_Selection.votes = first_Selection.votes + 3
        db.session.commit()
        second_Selection.votes = second_Selection.votes + 2
        db.session.commit()
        third_Selection.votes = third_Selection.votes + 1

        db.session.commit()

    except:
        return 'failed'
    
    

if __name__ == "__main__":
    app.run(debug=True)
