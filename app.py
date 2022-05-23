from flask import Flask, render_template, Response , request , url_for,redirect,flash
from Frame import get_frame
import psycopg2
import psycopg2.extras
from StudentData import auth_users
from TeacherData import auth_admin
from attendance import add_attendance , attendance_sheet , making_table
app = Flask(__name__)
app.secret_key = "meowmeowandolymewo"
 
DB_HOST = "localhost"
DB_NAME = "SampleDB"
DB_USER = "postgres"
DB_PASS = "ROOT"
 
user_list = auth_users()
admin_list = auth_admin() 
conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/login", methods = ['POST','GET'])
def login():
    if request.method == "POST":
        user = request.form['uname']
        psw = request.form['psw']
        user = str(user).capitalize()
        if (user , psw) in user_list.items():
            return redirect(url_for('student'))
        elif (user , psw) in admin_list.items():
            return redirect(url_for('teacher'))
        else:
            flash("Enter the correct Password")
            return redirect(url_for('index'))
        
        
@app.route('/Index')
def Index():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    s = f"SELECT * FROM {attendance_sheet}"
    cur.execute(s) # Execute the SQL
    list_users = cur.fetchall()
    return render_template('system.html', list_users = list_users)
 
@app.route('/add_student', methods=['POST'])
def add_student():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method == 'POST':
        name = request.form['name']
        time = request.form['time']
        date = request.form['date']
        cur.execute("ROLLBACK")
        conn.commit()
        print(time , date)
        add_attendance(name,time,date)
        flash('Student Added successfully')
        return redirect(url_for('Index'))
 
 
@app.route('/video')
def video():
    return Response(get_frame(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/student')
def student():
    return render_template('student.html')

@app.route('/home')
def home():
    get_frame(False)
    return render_template('index.html')

@app.route('/teacher')
def teacher():
    return render_template('teacher.html')



if __name__ == "__main__":
    app.run(debug=True ,port=8080,use_reloader=False)
    
