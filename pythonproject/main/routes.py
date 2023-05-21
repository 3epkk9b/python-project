from flask import render_template, request, Blueprint, abort, flash, redirect, url_for
from flask_login import login_required, current_user
from pythonproject.models import Post, Student, db

main = Blueprint('main', __name__)

@main.route("/")
@main.route("/home")
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts)

@main.route("/about")
def about():
    return render_template('about.html', title='About')

@main.route('/database', methods=['GET', 'POST'])
@login_required
def database():
    if current_user.role != 'teacher':
        abort(403)

    if request.method == 'POST':
        # Checkboxes are submitted as a list of values
        # Get the selected genders from the form
        selected_genders = request.form.getlist('gender')
        selected_group = request.form.get('group')

        # Query students based on the selected genders and group
        if selected_genders:
            students = Student.query.filter(Student.gender.in_(selected_genders)).all()
        elif selected_group and selected_group != 'all':
            students = Student.query.filter_by(group=selected_group).all()
        else:
            students = Student.query.all()

        flash('Filtered database based on selected genders and group.', 'success')
        return render_template('database.html', students=students, groups=get_all_groups())

    students = Student.query.all()
    return render_template('database.html', students=students, groups=get_all_groups())

def get_all_groups():
    return [group[0] for group in db.session.query(Student.group.distinct()).all()]

@main.route('/add_student', methods=['GET', 'POST'])
@login_required
def add_student():
    if current_user.role != 'teacher':
        abort(403)

    if request.method == 'POST':
        # Handle the form submission
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        group = request.form['group']
        gender = request.form['gender']

        # Process the form data and add the student to the database
        student = Student(name=name, email=email, phone=phone, group=group, gender=gender)
        db.session.add(student)
        db.session.commit()

        flash('Student added successfully.', 'success')
        return redirect(url_for('main.database'))

    return render_template('add_student.html', groups=get_all_groups())

@main.route('/delete-student/<int:student_id>', methods=['GET', 'POST'])
def delete_student(student_id):
    student = Student.query.get(student_id)
    if not student:
        flash('Student not found.', 'error')
        return redirect(url_for('main.database'))
    db.session.delete(student)
    db.session.commit()
    flash('Student deleted successfully.', 'success')
    return redirect(url_for('main.database'))

@main.route('/update-student/<int:student_id>', methods=['GET'])
def update_student(student_id):
    student = Student.query.get(student_id)
    return render_template('update.html', student=student, groups=get_all_groups())

@main.route('/update-student/<int:student_id>', methods=['POST'])
def process_update_student(student_id):
    student = Student.query.get(student_id)
    if not student:
        flash('Student not found.', 'error')
        return redirect(url_for('main.database'))

    student.name = request.form['name']
    student.email = request.form['email']
    student.phone = request.form['phone']
    student.group = request.form['group']
    student.gender = request.form['gender']

    db.session.commit()
    flash('Student updated successfully.', 'success')
    return redirect(url_for('main.database'))

@main.route('/search_student', methods=['GET'])
def search_student():
    gender = request.args.get('gender')

    if gender == 'male':
        students = Student.query.filter_by(gender='male').all()
    elif gender == 'female':
        students = Student.query.filter_by(gender='female').all()
    else:
        students = Student.query.all()

    return render_template('database.html', students=students, groups=get_all_groups())
