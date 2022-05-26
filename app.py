from flask import Flask, render_template, Response, request, url_for, redirect, flash
from Frame import get_frame
import numpy as np
import cv2
from keras.models import load_model
import sys
import psycopg2
import psycopg2.extras
from StudentData import auth_users
from TeacherData import auth_admin
from attendance import add_attendance, attendance_sheet, making_table
from animals import main_frames
from driver_drowsiness import drowss
from canvas import canvas

app = Flask(__name__)
app.secret_key = "meowmeowandolymewo"

DB_HOST = "localhost"
DB_NAME = "Attendance"
DB_USER = "postgres"
DB_PASS = "ROOT"

user_list = auth_users()
admin_list = auth_admin()
conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER,
                        password=DB_PASS, host=DB_HOST)

#front Page
@app.route('/')
def index():
    return render_template('index.html')

#login Redirect Student
@app.route("/login", methods=['POST', 'GET'])
def login():
    if request.method == "POST":
        user = request.form['uname']
        psw = request.form['psw']
        user = str(user).capitalize()
        if (user, psw) in user_list.items():
            return redirect(url_for('student'))
        else:
            flash("Enter the correct Password")
            return redirect(url_for('index'))

#login Redirect Student
@app.route("/logint", methods=['POST', 'GET'])
def logint():
    if request.method == "POST":
        user = request.form['uname']
        psw = request.form['psw']
        user = str(user).capitalize()
        if (user, psw) in admin_list.items():
            making_table()
            return redirect(url_for('teacher'))
        else:
            flash("Enter the correct Password")
            return redirect(url_for('index'))

#attendance Managment Page
@app.route('/Index')
def Index():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    s = f"SELECT * FROM {attendance_sheet}"
    cur.execute(s)
    list_users = cur.fetchall()
    return render_template('system.html', list_users=list_users)

#Adding Student
@app.route('/add_student', methods=['POST'])
def add_student():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method == 'POST':
        name = request.form['name']
        time = request.form['time']
        date = request.form['date']
        cur.execute("ROLLBACK")
        conn.commit()
        print(time, date)
        add_attendance(name, time, date)
        flash('Student Added successfully')
        return redirect(url_for('Index'))

#vedio at attendance page
@app.route('/video')
def video():
    return Response(get_frame(), mimetype='multipart/x-mixed-replace; boundary=frame')

#student.html
@app.route('/student')
def student():
    return render_template('student.html')

#homepage redirect
@app.route('/home')
def home():
    get_frame(False)
    return render_template('index.html')

#veiw attendance page
@app.route('/teacher')
def teacher():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    z = f"SELECT COUNT(*) FROM {attendance_sheet}"
    cur.execute(z)
    z1 = cur.fetchall()
    p = z1[0][0]
    t = len(user_list)
    a = t - p
    return render_template('teacher.html', a=a, p=p, t=t)

#about us page
@app.route('/about')
def about():
    return render_template('about.html')

#contact page
@app.route('/contact')
def contact():
    return render_template('contact.html')

# ---- Fun Zone 

@app.route("/funzone")
def funzone():
    return render_template('funzone.html')



# Emotion detection
@app.route('/collecting')
def collecting():
    return render_template('collecting.html')


@app.route('/predict', methods=['GET', 'POST'])
def predict():
    image = request.files['select_file']
    image.save('./static/file.jpg')
    image = cv2.imread('static/file.jpg')
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt2.xml')
    faces = cascade.detectMultiScale(gray, 1.1, 3)
    for x, y, w, h in faces:
        cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cropped = image[y:y+h, x:x+w]
    cv2.imwrite('static/after.jpg', image)
    try:
        cv2.imwrite('static/cropped.jpg', cropped)
    except:
        pass
    try:
        img = cv2.imread('static/cropped.jpg', 0)
    except:
        img = cv2.imread('static/file.jpg', 0)
    img = cv2.resize(img, (48, 48))
    img = img/255
    img = img.reshape(1, 48, 48, 1)
    model = load_model('model.h5')
    pred = model.predict(img)
    label_map = ['Anger', 'Neutral', 'Fear', 'Happy', 'Sad', 'Surprise']
    pred = np.argmax(pred)
    final_pred = label_map[pred]
    return render_template('predict.html', data=final_pred)




# Animal app
@app.route('/animals')
def animals():
    return render_template('animals.html')


@app.route('/video_feed/1')
def video_feed_dog():
    print(request.base_url, file=sys.stdout)
    return Response(main_frames('dog'),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/video_feed/2')
def video_feed_pig():
    print(request.base_url, file=sys.stdout)
    return Response(main_frames('pig'),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/video_feed/3')
def video_feed_panda():
    print(request.base_url, file=sys.stdout)
    return Response(main_frames('panda'),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/video_feed/4')
def video_feed_snake():
    print(request.base_url, file=sys.stdout)
    return Response(main_frames('snake'),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/pig')
def pig():
    return render_template('pig.html')


@app.route('/dog')
def dog():
    return render_template('dog.html')


@app.route('/panda')
def panda():
    return render_template('panda.html')


@app.route('/snake')
def snake():
    return render_template('snake.html')




# Drowsness
@app.route('/drows')
def drows():
    return Response(drowss(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/drowsness')
def drowsness():
    return render_template('drowsness.html')



# Air Canvas
@app.route("/canvass")
def canvass():
    return render_template("canvas.html")


@app.route('/canvasvedio')
def canvasvedio():
    return Response(canvas(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == "__main__":
    app.run(debug=True, port=8000, use_reloader=False)
