import sqlalchemy.types
from flask import Flask, request, redirect
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
import random


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///C:\\Users\\Haris Bence\\PycharmProjects\\LangCert\\database.db'
database = SQLAlchemy(app)


class Question(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    title = database.Column(database.String(30), nullable=False)
    A = database.Column(database.String, nullable=False)
    B = database.Column(database.String, nullable=False)
    C = database.Column(database.String, nullable=False)
    D = database.Column(database.String, nullable=False)
    answer_good = database.Column(database.String, nullable=False)

    def __repr__(self):
        return '<Question %r>' % self.id


def generate_array(quest_num):
    letters = ['A', 'B', 'C', 'D']
    choices = list()
    for i in range(quest_num):
        past = []
        shuffled = []
        while True:
            num = random.randint(0,3)
            if num not in past:
                shuffled.append(letters[num])
            past.append(num)
            if len(shuffled) == 4:
                break
        choices.append(shuffled)
    return choices


@app.route('/', methods=["POST", "GET"])
def hello_world():
    questions = Question.query.all()
    if request.method == "POST":
        score = 0
        answers = list()
        for i in range(len(questions)):
            options = []
            right = questions[i].answer_good
            for j in range(4):
                print(f"{str(i+1)}.{str(j)}")
                if request.form.get(f"{str(i+1)}.{str(j)}") is not None:
                    options.append(request.form.get(f"{str(i+1)}.{str(j)}"))
            print(options)
            if len(options) < 1:
                return render_template("bad.html", desc="You really missed some?")
            elif len(options) > 1:
                return render_template("bad.html", desc="You really marked more than one options?")
            else:
                answers.append(options[0])
                print(f'{right}:{right}')
                if right == options[0]:
                    score += 1
        print("POSTED")
        print(answers)
        print(f"Score: {str(score)}")

        perc = round(score/len(questions)*100)
        if score > 7.2:
            result="Passed"
        else:
            result="Failed"

        return render_template("congrats.html", result=result, perc=perc)
    else:

        orders = generate_array(len(questions))
        return render_template("index.html", questions=questions, orders=orders)


if __name__ == '__main__':
    app.run()
