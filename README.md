<h1 align="center">
Attendance Tracker
</h1>

<p align="center">
  <a href="#introduction">Introduction</a> •
  <a href="#key-features">Key Features</a> •
  <a href="#how-to-use">How To Use</a> •
  <a href="#tech-stack">Tech Stack</a> •
  <a href="#documentation">Documentation </a> •
  <a href="#video">Video </a> •
  <a href="#snapshots">Snapshots</a>
</p>

## Introduction

Attendance Tracker Application is a school portal for both students and teachers. It automates the manual work of taking attendance using face recognition technology .It also contains some fun features for students including emotion detection ,sleep detection ,air canvas ,and animal filter . The project is based upon computer vision applications and pre-built machine learning models.Flask is used in the backend.
<br/>

## Key Features

- Sign in for student
- Sign in for the teacher
- Records attendance via face recognition technology
- Displays the total number of presentees and absentees
- Database management system where the name, time, and dates of the entries are shown
- Manual input of the attendance
- Funzone for students including OpenCV applications
  - Air canvas
  - Sleep detection
  - Emotion detection
  - Animal filter

## How To Use
Detailed tutorial [Installation Guide](https://drive.google.com/file/d/1aPQdOk-N_pYdEbr5lDBfDDrmgapDO06y/view?usp=sharing)
- Download Python 3.10.4 (https://www.python.org/downloads/)
- Install PostgreSQL Database (https://www.enterprisedb.com/downloads/postgres-postgresql-downloads)
- Open cmd and excecute the following command
  ```
  git clone https://github.com/SAMRIDHISINHA/AttendanceSystem_MicrosoftEngage-22.git
  ```
  ```
  createdb -h localhost -U postgres Attendance
  ```
  ```
  cd AttendanceSystem_MicrosoftEngage-22
  ```
  ```
  pip install --upgrade pip --user
  ```
  ```
  pip install cmake --user
  ```
  ```
  pip install wheel --user
  ```
  ```
  pip install dlib-19.22.99-cp39-cp39-win_amd64.whl --user
  ```
  ```
  pip install -r requirements.txt --user
  ```
- Now run the app 
  ```
  python app.py
  ```
- Run the app on browser
  ```
  http://127.0.0.1:8000/
  ```

## Tech Stack

- Python : Server Side Language
- Flask : Backend FrameWork
- Postgres : To store Attendance
- OpenCv : Face Recognition
- Tensorflow : Emotion Detection


## [Attendance Tracker Documentation](https://drive.google.com/file/d/1rz7N8xlutr-pbDitrxpo55koGYyt6_9A/view?usp=sharing)

## [Video](https://youtu.be/gKh8em37Otg)

<div align="center">

## Snapshots

![ezgif com-resize](https://github.com/SAMRIDHISINHA/AttendanceSystem_MicrosoftEngage-22/blob/main/DemoGIF.gif)

</div>

<h2 align="center">
  Microsoft Engage Mentorship Program
</h2>
