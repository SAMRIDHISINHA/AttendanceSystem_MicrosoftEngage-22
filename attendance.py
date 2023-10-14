import psycopg2  # pip install psycopg2
import psycopg2.extras
from datetime import datetime
from database_credential import DB_HOST , DB_NAME , DB_PASS , DB_USER

#establishing connection with the database
conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER,
                        password=DB_PASS, host=DB_HOST)
#taking system's current date and time
time_now = datetime.now()
tStr = time_now.strftime('%H:%M:%S')
dStr = time_now.strftime('%d_%m_%Y')
attendance_sheet = "Attendance_" + dStr

#cur is used for writing sql queries//,treat it like a blank sheet
cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

#making table if it is not there in the database
def making_table():
    cur.execute(
        f"CREATE TABLE IF NOT EXISTS {attendance_sheet} (name VARCHAR ( 40 ) PRIMARY KEY,time VARCHAR ( 40 ) ,date VARCHAR ( 40 ));")
  #queries are being run and saved
    conn.commit()
  #blank page restored, queries wiped off
    cur.execute("ROLLBACK")
  
    conn.commit()
  #it will make table if it does not exist

# Adding attendance to the data base

# default value =none
def add_attendance(name, time=None, date=None):
    making_table()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    name = str(name)
    name = name.capitalize()
    time_now = datetime.now()
  #manual addition of attendance
    if time == '' or time == None:
        time = time_now.strftime('%H:%M:%S')
    if date == '' or date == None:
        date = time_now.strftime('%d_%m_%Y')
    try:
      #insertion of attendance in database
        cur.execute(
            f"INSERT INTO {attendance_sheet} (name, time, date) VALUES (%s,%s,%s)", (name, time, date))
        conn.commit()
    except:
        cur.execute("ROLLBACK")
        conn.commit()
