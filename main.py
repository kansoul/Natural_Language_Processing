import tkinter as tk
from tkinter import ttk
from tkinter import *
from PIL import Image, ImageTk
import mysql.connector
import cv2
import sqlite3
import os
import numpy as np
import unidecode
import tkinter.messagebox
from tkinter.messagebox import showinfo

def logged_destroy():
    logged_message.destroy()


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
def logged():
    global logged_message
    logged_message = Toplevel(window)
    logged_message.title("Welcome")
    logged_message.geometry("500x100")
    Label(logged_message, text="Login Successfully!...Welcome {} ".format(email.get()), fg="green", font="bold").pack()
    Label(logged_message, text="").pack()
    Button(logged_message, text="Logout", bg="blue", fg='white', relief="groove", font=('arial', 12, 'bold'), command=logs).pack()

def login_verification():
    connectiondb = mysql.connector.connect(host="localhost", user="root", passwd="", database="diemdanh")
    cursordb = connectiondb.cursor()
    user_verification = email.get()
    pass_verification = password.get()
    sql = "select * from admin where user = %s and password = %s"
    cursordb.execute(sql, [(user_verification), (pass_verification)])
    results = cursordb.fetchall()
    if results:
        for i in results:
            logs()
            break
    else:
        failed()

def logs():
    def item_selected(event):

        selected = tree.focus()
        values = tree.item(selected, 'values')


        def opencamera():
            id = values[0]
            name = values[2]
            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
            cap = cv2.VideoCapture(0)
            # lay du lieu tu camera
            sampleNum = 0
            while (True):
                ret, frame = cap.read()  # frame: data camera
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # convert to gray pricture

                # ket hop face_cascade vs webcam de cho ra gia tri khuon mat
                faces = face_cascade.detectMultiScale(gray, 1.3, 5)  # image,scaleFactor,minNeighbor

                for (x, y, w, h) in faces:
                    # ve hinh vuong nhan dien khuon mat
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

                    directory = remove_accent(name)
                    parent_dir = "dataSet"
                    path = os.path.join(parent_dir, directory)

                    # if not os.path.exists(directory):
                    os.makedirs(path, exist_ok=True)

                    # tang id
                    sampleNum += 1
                    url = 'dataSet/' + u"" + remove_accent(name) + '/' + str(id) + '-' + str(sampleNum) + '.jpg'
                    # save the captured face in the dataset folder
                    cv2.imwrite(url,
                                gray[y:y + h, x:x + w])

                cv2.imshow('frame', frame)
                cv2.waitKey(1)
                # break if the sample number is morethan 20
                if sampleNum > 100:
                    cap.release()
                    cv2.destroyAllWindows()
                    break;
            cap.release()
            cv2.destroyAllWindows()

        def traindata():
            recognizer = cv2.face.LBPHFaceRecognizer_create()
            path = 'dataSet'

            def getImageWithID(path):
                # imagePaths=[os.path.join(path, f) for f in os.listdir(path)]
                imagePaths = []
                for root, dirs, files in os.walk(path):
                    # imagePaths.append(files)
                    for f in files:
                        imagePaths.append(os.path.join(root, f))
                # print(imagePaths) #: list url
                faces = []
                IDs = []

                for imagePath in imagePaths:
                    # loading the image and converting it to gray scale
                    faceImg = Image.open(imagePath).convert('L')
                    # converting the PIL image into numpy array
                    faceNp = np.array(faceImg, 'uint8')
                    # print(faceNp) #: list matrix pixel

                    # split to get ID of the image
                    ID = int(imagePath.split('\\')[2].split('-')[0])
                    # print(os.path.split(imagePath)) => [dataSet, url]

                    # add to array
                    faces.append(faceNp)
                    IDs.append(ID)

                    cv2.imshow("traning", faceNp)
                    cv2.waitKey(10)

                return IDs, faces

            Ids, faces = getImageWithID(path)
            recognizer.train(faces, np.array(Ids))
            if not os.path.exists('recognizer'):
                os.makedirs('recognizer')
            recognizer.save('recognizer/trainningData.yml')
            cv2.destroyAllWindows()


        def ca23():
            opencamera()
            traindata()

        ca23()



    log = tk.Toplevel(window)
    logo = PhotoImage(file='images/iconbitmap.gif')
    #log.call('wm', 'iconphoto', log._w, logo)
    log.title('Danh sách sinh viên')

    log.geometry("862x519")
    log.configure(bg="#94CDF6")
    canvas1 = Canvas(log, bg="#94CDF6", height=519, width=862, bd=0, highlightthickness=0, relief="ridge")
    canvas1.place(x=0, y=0)

    hello1 = Label(log, text="Welcome {}".format(email.get()), fg="black", font="Calibri 15",bg="#94CDF6", highlightthickness=0)
    hello1.place(x=80, y=20)


    chon = Label(log, text="Danh sách sinh viên", fg="black", font="Calibri 30", bg="#94CDF6",
                  highlightthickness=0)
    chon.place(x=280, y=70)



    # setup treeview
    columns = ('ID', 'Mã sinh viên', 'Họ và tên', 'Class')
    tree = ttk.Treeview(log, height=10, columns=columns, show='headings')
    tree.place(x=210, y=150)
    sb = tk.Scrollbar(log, orient=tk.VERTICAL, command=tree.yview)
    sb.place(x=210 + 401 + 2, y=150, height=206 + 20)
    tree.config(yscrollcommand=sb.set)
    tree.bind('<Double-1>', item_selected)
    # exit
    btn = tk.Button(log, text='Đăng xuất', command=log.destroy, width=10, bd=2, fg='#eb4d4b')
    btn.place(x=780, y=10)

    # setup columns attributes
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=100, anchor=tk.CENTER)

    # fetch data
    con = mysql.connector.connect(host="localhost", user="root", passwd="", database="diemdanh")
    c = con.cursor()
    sql = "SELECT dssv.id, dssv.masv, dssv.ten, dslop.name FROM dssv INNER JOIN dslop ON dssv.idlop=dslop.id"
    c.execute(sql)
    # populate data to treeview
    for rec in c:
        tree.insert('', 'end', value=rec)
    log.transient(window)

def remove_accent(text):
    return unidecode.unidecode(text)








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

canvas.create_text(519.0, 210.0, text="User", fill="#515486", font=("Arial-BoldMT", int(13.0)))
canvas.create_text(518.5, 310.5, text="      Password", fill="#515486", font=("Arial-BoldMT", int(13.0)))

canvas.create_text(646.5, 130.0, text="Đăng Nhập Admin", fill="#515486", font=("Arial-BoldMT", int(22.0)))

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


