import tkinter as tk
from tkinter import ttk
from tkinter import *
from PIL import Image, ImageTk
import mysql.connector
import tkinter.messagebox
from tkinter.messagebox import showinfo
from datetime import date
import cv2
import unidecode
import json
import random
import os
import playsound
import speech_recognition as sr
import time
import sys
import ctypes
import wikipedia
import datetime
import json
import re
import webbrowser
import smtplib
import requests
import urllib
import urllib.request as urllib2
from time import strftime
from gtts import gTTS
from youtube_search import YoutubeSearch


language = 'vi'
    #giongnoi
def speak(text):



        tts = gTTS(text=text, lang=language, slow=False)
        tts.save('sound.mp3')
        playsound.playsound('sound.mp3', False)
        os.remove("sound.mp3")

def ai(name):
    #     name = get_text()
    if name:
     speak("Chào bạn {}".format(name))



def remove_accent(text):
    return unidecode.unidecode(text)
def failed():
    global failed_message
    failed_message = Toplevel(window)
    failed_message.title("Invalid Message")
    failed_message.geometry("500x100")
    Label(failed_message, text="Invalid Username or Password", fg="red", font="bold").pack()
    Label(failed_message, text="").pack()
    Button(failed_message,text="Ok", bg="blue", fg='white', relief="groove", font=('arial', 12, 'bold'), command=failed_destroy).pack()

def failed_destroy():
    failed_message.destroy()

def login_verification():
    connectiondb = mysql.connector.connect(host="localhost", user="root", passwd="", database="diemdanh")
    cursordb = connectiondb.cursor()
    user_verification = email.get()
    pass_verification = password.get()
    sql = "select * from giaovien where email = %s and password = %s"
    cursordb.execute(sql, [(user_verification), (pass_verification)])
    results = cursordb.fetchall()
    if results:
        for i in results:
            logs()
            break
    else:
        failed()

def logs():
    log = tk.Toplevel(window)
    logo = PhotoImage(file='images/iconbitmap.gif')
    #log.call('wm', 'iconphoto', log._w, logo)
    log.title('Thời khóa biểu')

    log.geometry("862x519")
    log.configure(bg="#94CDF6")
    canvas1 = Canvas(log, bg="#94CDF6", height=519, width=862, bd=0, highlightthickness=0, relief="ridge")
    canvas1.place(x=0, y=0)

    hello1 = Label(log, text="Welcome {}".format(email.get()), fg="black", font="Calibri 15",bg="red", highlightthickness=0)
    hello1.place(x=10, y=20)


    chon = Label(log, text="Thời khóa biểu hôm nay", fg="black", font="Calibri 30", bg="#94CDF6",
                  highlightthickness=0)
    chon.place(x=200, y=50)



    def treeview():
        # click
        def item_selected(event):
            selected = tree.focus()
            values = tree.item(selected, 'values')

            def openreco():
                # tranning hinh anh nhan dien vs Thu vien nhan dien khuon mat
                face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
                recognizer = cv2.face.LBPHFaceRecognizer_create()

                # read file tranning
                recognizer.read('recognizer/trainningData.yml')

                # get profile by id from datatbase
                def getProfile(id):
                    connectiondb = mysql.connector.connect(host="localhost", user="root", passwd="",
                                                           database="diemdanh")
                    cursor = connectiondb.cursor()

                    sql = "select ten, masv from dssv  WHERE ID=" + str(id)
                    cursor.execute(sql)


                    profile = None
                    for row in cursor:
                        profile = row

                    return profile

                def check(ngaythang, masv, lop, monhoc, giaovien):
                    connectiondb = mysql.connector.connect(host="localhost", user="root", passwd="",
                                                           database="diemdanh")
                    cursor = connectiondb.cursor()
                    sql = "UPDATE diemdanh SET tinhtrang=0 WHERE ngaythang=%s AND masv=%s AND lop=%s AND monhoc=%s AND giaovien=%s"
                    dulieu=(ngaythang, masv, lop, monhoc, giaovien)

                    cursor.execute(sql,dulieu)
                    connectiondb.commit()

                def checkchao(ngaythang, masv, lop, monhoc, giaovien):
                    connectiondb = mysql.connector.connect(host="localhost", user="root", passwd="",
                                                           database="diemdanh")
                    cursor = connectiondb.cursor()
                    sql = "SELECT ten,tinhtrang FROM diemdanh WHERE ngaythang=%s AND masv=%s AND lop=%s AND monhoc=%s AND giaovien=%s"
                    dulieu = (ngaythang, masv, lop, monhoc, giaovien)

                    cursor.execute(sql, dulieu)
                    profile1 = None
                    for row in cursor:
                        profile1 = row

                    return profile1
                # lop = input("Nhap lop: ")
                # ngay = input("Nhap ngay(dd-mm-yyyy): ")
                # taobangngay(ngay, lop)

                # use webcam

                # set text style
                def mocamera():
                    today = date.today()
                    ngay = today.strftime("%Y/%m/%d")
                    lop=values[1]
                    monhoc = values[3]
                    giaovien = values[4]

                    fontface = cv2.FONT_HERSHEY_SIMPLEX

                    cap = cv2.VideoCapture(0)
                    while (True):
                        ret, frame = cap.read()
                        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

                        for (x, y, w, h) in faces:
                            # rectangle: hinh chu nhat
                            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                            roi_gray = gray[y:y + h, x:x + w]  # cut anh xam de so sanh voi dataTrain
                            # roi_color = frame[y:y+h, x:x+w]

                            nbr_predicted, confidence = recognizer.predict(roi_gray)  # du doan anh voi data exists

                            print(c)
                            if confidence < 30:
                                profile = getProfile(nbr_predicted)

                                if (profile != None):
                                    b= round(confidence, 2)
                                    a=profile[0]+"-"+str(b)
                                    cv2.putText(frame, "" + remove_accent(str(a)), (x + 10, y + h + 30),
                                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)


                                    profile1=checkchao(ngay, profile[1], lop, monhoc,giaovien)
                                    if(profile1[1]==1):
                                        ai(profile1[0])
                                        check(ngay, profile[1], lop, monhoc, giaovien)

                            else:
                                cv2.putText(frame, "Unknown", (x + 10, y + h + 30), fontface, 1, (0, 0, 255), 2);

                        cv2.imshow('photograph', frame)
                        if (cv2.waitKey(1) == ord('q')):
                            break
                        if cv2.getWindowProperty('photograph', 4) < 1:
                            break

                    cap.release()
                    cv2.destroyAllWindows()

                mocamera()

            openreco()

       # setup treeview
        columns = ('ID', 'Lớp', 'Khóa', 'Môn', 'Giáo viên', 'Tiết học')
        tree = ttk.Treeview(log, height=10, columns=columns, show='headings')
        tree.place(x=120, y=150)
        sb = tk.Scrollbar(log, orient=tk.VERTICAL, command=tree.yview)
        sb.place(x=121 + 600 + 2, y=150, height=206 + 20)
        tree.config(yscrollcommand=sb.set)
        tree.bind('<Double-1>', item_selected)
       # exit
        btn = tk.Button(log, text='Thoát', command=log.destroy, width=10, bd=2, fg='#eb4d4b')
        btn.place(x=780, y=10)



       # setup columns attributes
        for col in columns:
           tree.heading(col, text=col)
           tree.column(col, width=100, anchor=tk.CENTER)

       # fetch data
        con = mysql.connector.connect(host="localhost", user="root", passwd="", database="diemdanh")
        c = con.cursor()
        today=date.today()
        d1=today.strftime("%Y/%m/%d")
        sql="SELECT (@cnt := @cnt + 1) AS rowNumber, dslop.name, dslop.khoa, monhoc.ten, giaovien.name, thoikhoabieu.tiethoc FROM thoikhoabieu CROSS JOIN (SELECT @cnt := 0) AS dummy INNER JOIN monhoc ON thoikhoabieu.monhoc_id=monhoc.id INNER JOIN dslop ON thoikhoabieu.idlop=dslop.id INNER JOIN giaovien ON monhoc.giaovien=giaovien.id WHERE giaovien.email= %s AND thoikhoabieu.ngaythang= %s"
        abc=("{}".format(email.get()),d1)
        c.execute(sql, abc)
        results = c.fetchall()
        arr=[("Hôm", "Nay","Không","Có","Lịch","Học")]
        if results:
            for i in results:
                tree.insert('', 'end', value=i)


        else:

            for j in arr:
                tree.insert('','end',value=j)

       # populate data to treeview


    treeview()
    log.transient(window)







window = Tk()
logo = PhotoImage(file='images/iconbitmap.gif')
window.call('wm', 'iconphoto', window._w, logo)
window.title("LOGIN PAGE")


window.geometry("862x519")
window.configure(bg="#94CDF6")
canvas = Canvas(window, bg="#94CDF6", height=519, width=862, bd=0, highlightthickness=0, relief="ridge")
canvas.place(x=0, y=0)
canvas.create_rectangle(401, 0, 431 + 431, 0 + 519, fill="#FCFCFC", outline="")
canvas.create_rectangle(30, 160, 40 + 100, 160 + 5, fill="#FCFCFC", outline="")

text_box_bg = PhotoImage(file=f"images/TextBox_Bg.png")
token_entry_img = canvas.create_image(650.5, 230, image=text_box_bg)
URL_entry_img = canvas.create_image(650.5, 330, image=text_box_bg)

email = Entry(bd=0, bg="#F6F7F9", font="Calibri 15", highlightthickness=0)
email.place(x=490.0, y=197 + 30, width=321.0, height=35)
email.focus()

password = Entry(bd=0, bg="#F6F7F9", font="Calibri 15", show="*", highlightthickness=0)
password.place(x=490.0, y=290 + 30, width=321.0, height=35)

canvas.create_text(519.0, 210.0, text="Email", fill="#515486", font=("Arial-BoldMT", int(13.0)))
canvas.create_text(518.5, 310.5, text="      Password", fill="#515486", font=("Arial-BoldMT", int(13.0)))

canvas.create_text(646.5, 130.0, text="Đăng Nhập", fill="#515486", font=("Arial-BoldMT", int(22.0)))

logo = PhotoImage(file="./images/img_5.png")
generate_btn1 = Button(image=logo, borderwidth=0, highlightthickness=0,relief="flat")
generate_btn1.place(x=770, y=10,width=65, height=55)


title = Label(text="Welcome to My App", bg="#94CDF6", fg="white", font=("Arial-BoldMT", int(20.0)))
title.place(x=27.0, y=120.0)


info_text = Label(text="Design by Hồ Đoan."

                      ,
                      bg="#94CDF6", fg="white", justify="left", font=("Georgia", int(10.0)))

info_text.place(x=10.0, y=490.0)

generate_btn_img = PhotoImage(file="./images/img_4.png")
generate_btn = Button(image=generate_btn_img, borderwidth=0, highlightthickness=0, command=login_verification,
                          relief="flat")
generate_btn.place(x=557, y=401, width=160, height=55)
window.resizable(False, False)
window.mainloop()


