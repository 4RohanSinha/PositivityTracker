from flask import Flask, render_template, jsonify, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import datetime
import SentimentAnalysis

app = Flask(__name__)
ENV = 'prod'
if ENV == 'dev':
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1234@localhost/PositivityTracker'
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://ullcptfjqacwlx:c83dece25764d848c8fd8139a9a755f0ca414a95261bb9346cf3b28f3f1cb34f@ec2-52-71-23-11.compute-1.amazonaws.com:5432/ddj95docf728de'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Student(db.Model):
    __tablename__ = "students"
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(), nullable=False)
    lastName = db.Column(db.String(), nullable=False)
    entries = db.relationship('DiaryEntry', backref='student', lazy=True, cascade='all, delete-orphan')

class DiaryEntry(db.Model):
    __tablename__ = "diaryentries"
    id = db.Column(db.Integer, primary_key=True)
    entry = db.Column(db.Text, nullable=False)
    sentimentLevel = db.Column(db.Float)
    date_written = db.Column(db.DateTime, nullable=False)
    date_last_updated = db.Column(db.DateTime, nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)


db.create_all()

#****************************ROUTES**********************************

@app.route('/')
def home_page():
    return render_template('home.html', users=Student.query.all())

@app.route('/createuser')
def create_user_page():
    return render_template('newUser.html')

@app.route('/finishcreateuser', methods=['POST'])
def create_new_user():
    newUser = Student()
    newUser.firstName = request.form['firstName']
    newUser.lastName = request.form['lastName']
    db.session.add(newUser)
    db.session.commit()
    return redirect(url_for("home_page"))

@app.route('/deleteuser/<user_id>')
def delete_user(user_id):
    user = Student.query.get(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for("home_page"))

@app.route('/users/<user_id>')
def user_page(user_id):
    user = Student.query.filter_by(id=user_id).first()
    return render_template('user.html', user=user)

@app.route('/users/<user_id>/entries')
def return_entries(user_id):
    user = Student.query.filter_by(id=user_id).first()
    entries = {}
    max_time_since = datetime.datetime.now()-datetime.datetime.now()
    for i in user.entries:
        entries[i.id] = {}
        entries[i.id]["entry"] = i.entry
        entries[i.id]["date_written"] = i.date_written
        entries[i.id]["date_last_updated"] = i.date_last_updated
        entries[i.id]["sentimentLevel"] = i.sentimentLevel

        time_since = datetime.datetime.now()-i.date_written
        if (time_since > max_time_since):
            max_time_since = time_since

    for j in entries.keys():
        entries[j]["time_since"] = max_time_since.days

    return jsonify(entries)

@app.route('/users/<user_id>/addEntry')
def addEntry(user_id):
    return render_template('newEntry.html', user_id=user_id)

@app.route('/users/<user_id>/submitAddedEntry', methods=['POST'])
def submitNewEntry(user_id):

    newEntry = DiaryEntry()
    newEntry.entry = request.form["diary_entry"]
    if newEntry.entry.strip() != "":
        newEntry.sentimentLevel = getSentimentPositivityOf(newEntry.entry)
    else:
        newEntry.sentimentLevel = 0.0
    newEntry.date_written = datetime.datetime.now()
    newEntry.date_last_updated = newEntry.date_written
    newEntry.student_id = user_id
    db.session.add(newEntry)
    db.session.commit()

    return redirect(url_for("user_page", user_id=user_id))


@app.route('/users/<user_id>/submitAddedEntryFromDiary', methods=['POST'])
def submitNewEntryFromDiary(user_id):

    newEntry = DiaryEntry()
    newEntry.entry = request.form["diary_entry"]
    if newEntry.entry.strip() != "":
        newEntry.sentimentLevel = getSentimentPositivityOf(newEntry.entry)
    else:
        newEntry.sentimentLevel = 0.0
    newEntry.date_written = datetime.datetime.now()
    newEntry.date_last_updated = newEntry.date_written
    newEntry.student_id = user_id
    db.session.add(newEntry)
    db.session.commit()

    return redirect(url_for("show_entire_diary", user_id=user_id))

@app.route('/users/<user_id>/diary')
def show_entire_diary(user_id):
    user = Student.query.filter_by(id=user_id).first()
    return render_template('full_diary.html', user=user)

@app.route('/users/<user_id>/view_entry/<entry_id>')
def entry_page(user_id, entry_id):
    user = Student.query.filter_by(id=user_id).first()
    entry = DiaryEntry.query.filter_by(id=entry_id).first()
    return render_template("viewEntry.html", user=user, entry=entry)

@app.route('/users/<user_id>/edit_entry/<entry_id>')
def edit_entry_page(user_id, entry_id):
    entry = DiaryEntry.query.filter_by(id=entry_id).first()
    return render_template("editEntry.html", user_id=user_id, entry=entry)

@app.route('/users/<user_id>/submitEntryEdits/<entry_id>', methods=['POST'])
def submitEntryEdits(user_id, entry_id):

    entry = DiaryEntry.query.filter_by(id=entry_id).first()
    entry.entry = request.form["diary_entry"]
    entry.sentimentLevel = (2*(float(request.form["sentimentLevel"])/100))-1
    print(entry.sentimentLevel)
    if ("conductSentimentAnalysisAgain" in request.args):
        entry.sentimentLevel = getSentimentPositivityOf(entry.entry)
    entry.date_last_updated = datetime.datetime.now()
    db.session.commit()

    return redirect(url_for("entry_page", user_id=user_id, entry_id=entry_id))

def deleteEntry(entry_id):
    entry = DiaryEntry.query.get(entry_id)
    db.session.delete(entry)
    db.session.commit()

@app.route('/users/<user_id>/delete_entry/<entry_id>')
def deleteEntryFromDashboard(user_id, entry_id):
    deleteEntry(entry_id)

    return redirect(url_for("user_page", user_id=user_id))

@app.route('/users/<user_id>/delete_entry_from_diary/<entry_id>')
def deleteEntryFromDiaryView(user_id, entry_id):
    deleteEntry(entry_id)

    return redirect(url_for("show_entire_diary", user_id=user_id))
#***********************APPLY FUNCTION FROM SENTIMENT ANALYSIS*****************
def getSentimentPositivityOf(entry):
    return SentimentAnalysis.sentiment_analysis(entry)
