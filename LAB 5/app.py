import os
from flask import Flask
from flask import render_template
from flask import request, redirect
from flask_sqlalchemy import SQLAlchemy
current_dir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.path.join(current_dir, "database.sqlite3") 
db = SQLAlchemy()
db.init_app(app)
app.app_context().push()

#Model
class Student(db.Model):
    __tablename__ = "student"
    student_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    roll_number = db.Column(db.String, unique=True, nullable=False)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String)

class Course(db.Model):
    __tablename__ = "course"
    course_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    course_code = db.Column(db.String, unique=True, nullable=False)
    course_name = db.Column(db.String, nullable=False)
    course_description = db.Column(db.String)

class Enrollments(db.Model):
    __tablename__ = "enrollments"
    enrollment_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    estudent_id = db.Column(db.Integer,   db.ForeignKey("student.student_id"), nullable=False)
    ecourse_id = db.Column(db.Integer,  db.ForeignKey("course.course_id"), nullable=False)



@app.route("/")
def index():
    all_student = Student.query.all()
    enrollment = Enrollments.query.all()

    #for i in enrollment:
    #    print(i.estudent_id,i.ecourse_id)
    return render_template("index.html", all_student=all_student)


@app.route("/student/create", methods=['GET', 'POST'])
def create():
    if request.method == "POST":
        try:
            first_name = request.form.get("f_name")
            last_name = request.form.get("l_name")
            roll_no = request.form.get("roll")
            update_student_db = Student(roll_number=roll_no, first_name=first_name, last_name=last_name)
            db.session.add(update_student_db)
            db.session.flush()
            #db enrollment
            courses = request.form.getlist("courses")
            for course in courses:
                enroll = Enrollments(estudent_id=update_student_db.student_id, ecourse_id=int(course))
                db.session.add(enroll)
        except:
            db.session.rollback()
            return render_template("error.html")
        else:
            db.session.commit()
            return redirect("/") 
    elif request.method == "GET":
        return render_template("create.html")

@app.route("/student/<int:student_id>/update", methods=['GET', 'POST'])
def update(student_id):
    if request.method == "GET":
        stud = Student.query.get(student_id)
        #enroll = Enrollments.query.get(estudent_id=student_id)
        enrollment = Enrollments.query.all()
        course = []
        for i in enrollment:
            if i.estudent_id == student_id:
                course.append(i.ecourse_id)
        print(course)

        return render_template("update.html", student=stud, course=course)
    elif request.method == "POST":
        first_name = request.form.get("f_name")
        last_name = request.form.get("l_name")

        stud = Student.query.get(student_id)
        stud.first_name = first_name
        stud.last_name = last_name
        #db enrollment
        Enrollments.query.filter_by(estudent_id=student_id).delete()
        db.session.flush()
        courses = request.form.getlist("courses")
        for course in courses:
            enroll = Enrollments(estudent_id=student_id, ecourse_id=int(course))
            db.session.add(enroll)

        db.session.commit()
        return redirect("/")

@app.route("/student/<int:student_id>/delete")
def Delete(student_id):
    Enrollments.query.filter_by(estudent_id=student_id).delete()
    Student.query.filter_by(student_id=student_id).delete()
    db.session.flush()
    db.session.commit()
    return redirect("/")


@app.route("/student/<int:student_id>")
def student(student_id):
    stud = Student.query.get(student_id)
    enrollment = Enrollments.query.all()
    course = []
    for i in enrollment:
        if i.estudent_id == student_id:
            course.append(i.ecourse_id)
    course_table = Course.query.all()
    #print(course_table)
    return render_template("student.html",student=stud, course_table=course_table, course_list=course)



if __name__ == '__main__':
    app.run(debug=True)