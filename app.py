from flask import Flask, url_for, request, redirect, session
from flask.templating import render_template
from werkzeug.security import generate_password_hash, check_password_hash
import os
from database import get_database


app =Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)

def get_current_user():
    user = None
    if 'user' in session:
        user = session['user']
    return user


# mydb = mysql.connector.connect(**config)
# my_cursor = mydb.cursor(dictionary=True)
# my_cursor1 = mydb.cursor(dictionary=True)
# my_cursor.execute(" SELECT table_name FROM information_schema.tables WHERE table_schema ='University_Data' ")
# my_result = my_cursor.fetchall()




@app.route('/')
def index():
    return render_template('firsthome.html')

@app.route('/firstindex')
def firstindex():
    user = get_current_user()
    return render_template('home.html', user = user)

@app.route('/login' , methods= ["POST", "GET"])
def login():
    error = None
    db = get_database()
    if request.method == "POST":
        name = request.form['name']
        password = request.form['password']
        query = "select * from users where user_name = ?"
        myres = db.execute(query, (name,))
        user = myres.fetchone()

        if user:
            if check_password_hash(user['user_password'], password):
                session['user'] = user['user_name']
                return redirect(url_for('firstindex'))
            else:
                error = "**Password did not match. Try again!"
                return render_template('login.html', loginerror = error)
        else:
            error = "**Username did not match. Try again!"
            return render_template('login.html', loginerror = error)
    return render_template('login.html')

@app.route('/register', methods= ["POST", "GET"])
def register():
    if request.method == "POST":
        name = request.form['name']
        password = request.form['password']
        hash_password = generate_password_hash(password)

        db = get_database()
        query_user = "select * from users where user_name = ?"
        my_user = db.execute(query_user, (name,))
        user = my_user.fetchone()

        # query = "select * from users where user_name = %s"
        # my_cursor.execute(query, (name,))
        # user = my_cursor.fetchone()

        if user:
            error = "**Username already takem. Try a different one!"
            return render_template('register.html', loginerror = error)

        query = "INSERT INTO users (user_name, user_password) VALUES (?, ?)"
        #my_cursor.execute(query, (name, hash_password))
        db.execute(query, (name, hash_password))

        db.commit()
        session['user'] = name

        return redirect(url_for('firstindex'))
    return render_template('register.html')

@app.route('/departmentdashboard')
def departmentdashboard():
    user = get_current_user()
    db = get_database()
    myres = db.execute(" SELECT * FROM department_information ")
    my_result = myres.fetchall()
    return render_template('department_dashboard.html', records = my_result, user = user)

@app.route('/studentdashboard')
def studentdashboard():
    user = get_current_user()
    db = get_database()
    myres = db.execute(" SELECT * FROM student_information ")
    my_result = myres.fetchall()
    return render_template('studentdashboard.html', records = my_result, user = user)

@app.route('/addnewdepartment', methods= ["POST", "GET"])
def addnewdepartment():
    user = get_current_user()
    if request.method == "POST":
        department_id = request.form['department_id']
        department_name = request.form['department_name']
        date_of_est = request.form['date_of_est']
        db = get_database()
        query = "INSERT INTO department_information (department_id, department_name, date_of_est) VALUES (?, ?, ?)"
        db.execute(query, (department_id, department_name, date_of_est))

        db.commit()
        return redirect(url_for('departmentdashboard'))

    return render_template('addnewdepartment.html', user = user)

@app.route('/singlemployeeprofile')
def singlemployeeprofile():
    return render_template('singlemployee.html')

@app.route('/updateemployee')
def updateemployee():
    return render_template('updateemployee.html')

@app.route('/addnewstudent', methods= ["POST", "GET"])
def addnewstudent():
    user = get_current_user()
    if request.method == "POST":
        student_id = request.form['student_id']
        department = request.form['department']
        date_of_birth = request.form['date_of_birth']
        date_of_admission = request.form['date_of_admission']
        db = get_database()

        query = "INSERT INTO student_information (student_id, department_admission, date_of_birth, date_of_admission) VALUES (?, ?, ?, ?)"
        db.execute(query, (student_id, department, date_of_birth, date_of_admission))

        db.commit()
        return redirect(url_for('studentdashboard'))

    return render_template('addnewstudent.html', user = user)

@app.route('/singlstudentprofile/<string:student_id>')
def singlestudentprofile(student_id):
    user = get_current_user()
    db = get_database()
    query = " SELECT * FROM student_information where Student_ID = ? "
    myres = db.execute(query, (student_id,))
    my_result = myres.fetchone()

    query2 = "select * from studentPercentage where Student_ID = ?"

    myres = db.execute(query2, (student_id,))
    percentage = myres.fetchone()
    print(percentage)

    return render_template('singlestudent.html', student=my_result, percentage= percentage)


@app.route('/deletedepartment/<string:department_id>')
def deletedepartment(department_id):
    db = get_database()
    query = "delete from department_information where Department_ID = ?"
    db.execute(query, (department_id,))
    db.commit()
    return redirect(url_for('departmentdashboard'))

@app.route('/fetchdept/<string:department_id>')
def fetchdept(department_id):
    user = get_current_user()
    db = get_database()
    query = " SELECT * FROM department_information where Department_ID = ? "
    myres = db.execute(query, (department_id,))
    my_result = myres.fetchone()
    
    return render_template( 'updatedepartment.html', records = my_result, user = user)

@app. route('/updatedepartment' , methods = ["POST", "GET"])
def updatedepartment():
    user = get_current_user()
    db = get_database()
    if request.method == 'POST':
        department_id = request.form['department_id']
        department_name = request.form['department_name']
        date_of_est = request.form['date_of_est']

        query = "UPDATE department_information SET department_name = ?,  date_of_est = ? where department_ID = ?"
        db.execute(query, ( department_name, date_of_est, department_id))

        db.commit()
        return redirect(url_for('departmentdashboard'))

    return render_template('updatedepartment.html', user = user)

@app.route('/fetchstudent/<string:student_id>')
def fetchstudent(student_id):
    user = get_current_user()
    db = get_database()
    query = " SELECT * FROM student_information where Student_ID = ? "
    myres = db.execute(query, (student_id,))
    my_result = myres.fetchone()
    
    return render_template( 'updatestudent.html', records = my_result, user = user)

@app. route('/updatestudent' , methods = ["POST", "GET"])
def updatestudent():
    user = get_current_user()
    db = get_database()
    if request.method == 'POST':
        student_id = request.form['student_id']
        department = request.form['department']
        date_of_birth = request.form['date_of_birth']
        date_of_admission = request.form['date_of_admission']

        query = "UPDATE student_information SET department_Admission = ?,  date_of_birth = ?, date_of_Admission = ? where student_ID = ?"
        db.execute(query, ( department, date_of_birth, date_of_admission, student_id))

        db.commit()
        return redirect(url_for('studentdashboard'))

    return render_template('updatestudent.html', user = user)

@app.route('/deletestudent/<string:student_id>')
def deletestudent(student_id):
    db = get_database()
    query = "delete from student_information where Student_ID = ?"
    db.execute(query, (student_id,))
    db.commit()
    return redirect(url_for('studentdashboard'))

@app.route('/studentperformance')
def studentperformance():
    user = get_current_user()
    db = get_database()
    myres = db.execute(" SELECT *  FROM student_performance_data limit 1000")
    my_result = myres.fetchall()
    return render_template('studentperformance.html', records = my_result, user = user)

@app.route('/fetchstudentscore/<string:student_id>/<string:semester>/<string:paper>')
def fetchstudentscore(student_id, semester, paper):
    user = get_current_user()
    db = get_database()
    query = " SELECT * FROM student_performance_data where Student_ID = ? and Semster_Name = ? and Paper_ID = ? "
    myres = db.execute(query, (student_id, semester, paper))
    my_result = myres.fetchone()
    
    return render_template( 'updatestudentperformance.html', records = my_result, user = user)

@app. route('/updatestudentperformance' , methods = ["POST", "GET"])
def updatestudentperformance():
    user = get_current_user()
    db = get_database()
    if request.method == 'POST':
        student_id = request.form['student_id']
        semester = request.form['semester']
        paper = request.form['paper']
        score = request.form['score']

        query = "UPDATE student_performance_data SET Marks = ? where student_ID = ? and Semster_Name = ? and Paper_ID = ?"
        myres = db.execute(query, ( score, student_id, semester, paper))

        db.commit()
        return redirect(url_for('studentperformance'))

    return render_template('updatestudentperformance.html', user = user)

def logout():
    render_template('home.html')

if __name__ =='__main__':
    app.run(debug = True)

