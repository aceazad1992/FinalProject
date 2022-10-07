from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///uni.db'
app.config['SECRET_KEY'] = 'the random string'

db = SQLAlchemy(app)

class Teacher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    subjects = db.relationship('Subject', backref='teacher', lazy=True)

    def __repr__(self):
        return '<Teacher %r>' % self.name

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    subjects = db.relationship('Subject', backref='student', lazy=True)

    def __repr__(self):
        return '<Student %r>' % self.name

class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject_name = db.Column(db.String(80), unique=True, nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)

    def __repr__(self):
        return '<Subject %r>' % self.name

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/teachers')
def teachers():
    teachers = Teacher.query.all()
    return render_template('teachers.html', teachers=teachers)

@app.route('/students')
def students():
    students = Student.query.all()
    return render_template('students.html', students=students)

@app.route('/subjects')
def classes():
    subjects = Subject.query.all()
    return render_template('subjects.html', subjects=subjects)

@app.route('/teacher/new', methods=['GET', 'POST'])
def new_teacher():
    if request.method == 'POST':
        name = form.name.data
        #name = request.form['name'].value
        email = form.email.data
        #email = request.form['email'].value
        subjects = form.subjects.data
        #subjects = request.form['subjects'].value
        teacher = form.teacher.data
        #teacher = Teacher(name, email, subjects).value

        flash('Record was successfully added')
        db.session.add(teacher)
        db.session.commit()

        return redirect(url_for('teachers'))
    return render_template('index.html')

@app.route('/student/new', methods=['GET', 'POST'])
def new_student():
    if request.method == 'POST':
        if not request.form['name']:
            flash('Please enter all the fields', 'error')
        else:
            student = Student(name=request.form['name'], email=request.form['email'])
            db.session.add(student)
            db.session.commit()
            flash('Record was successfully added')
            return redirect(url_for('students'))
    return render_template('index.html')

@app.route('/subject/new', methods=['GET', 'POST'])
def new_class():
    if request.method == 'POST':
        if not request.form['name']:
            flash('Please enter all the fields', 'error')
        else:
            _subject = Subject(name=request.form['name'].data)
            db.session.add(_subject)
            db.session.commit()
            flash('Record was successfully added')
            return redirect(url_for('subjects'))
    return render_template('index.html')

@app.route('/teacher/<int:teacher_id>/edit', methods=['GET', 'POST'])
def edit_teacher(teacher_id):
    teacher = Teacher.query.get_or_404(teacher_id)
    if request.method == 'POST':
        if not request.form['name']:
            flash('Please enter all the fields', 'error')
        else:
            teacher.name = request.form['name']
            db.session.commit()
            flash('Record was successfully edited')
            return redirect(url_for('teachers'))
    return render_template('index.html', teacher=teacher)

@app.route('/student/<int:student_id>/edit', methods=['GET', 'POST'])
def edit_student(student_id):
    student = Student.query.get_or_404(student_id)
    if request.method == 'POST':
        if not request.form['name']:
            flash('Please enter all the fields', 'error')
        else:
            student.name = request.form['name']
            db.session.commit()
            flash('Record was successfully edited')
            return redirect(url_for('students'))
    return render_template('index.html', student=student)

@app.route('/subject/<int:class_id>/edit', methods=['GET', 'POST'])
def edit_subject(subject_id):
    _subject = Subject.query.get_or_404(subject_id)
    if request.method == 'POST':
        if not request.form['name']:
            flash('Please enter all the fields', 'error')
        else:
            _subject.name = request.form['name']
            db.session.commit()
            flash('Record was successfully edited')
            return redirect(url_for('subject'))
    return render_template('index.html', _subject=_subject)

@app.route('/teacher/<int:teacher_id>/delete', methods=['POST'])
def delete_teacher(teacher_id):
    teacher = Teacher.query.get_or_404(teacher_id)
    db.session.delete(teacher)
    db.session.commit()
    flash('Record was successfully deleted')
    return redirect(url_for('index'))

@app.route('/student/<int:student_id>/delete', methods=['POST'])
def delete_student(student_id):
    student = Student.query.get_or_404(student_id)
    db.session.delete(student)
    db.session.commit()
    flash('Record was successfully deleted')
    return redirect(url_for('index'))

@app.route('/subject/<int:subject_id>/delete', methods=['POST'])
def delete_class(subject_id):
    _class = Subject.query.get_or_404(subject_id)
    db.session.delete(_subject)
    db.session.commit()
    flash('Record was successfully deleted')
    return redirect(url_for('index'))

@app.before_first_request
def createdatabase():
    db.create_all()


if __name__ == '__main__':
    app.run(port=8000, debug=True, host='0.0.0.0')
