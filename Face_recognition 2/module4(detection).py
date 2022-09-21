#.................................face_recognition(person)............................................#
import os
import time
import cv2
import face_recognition
import numpy as np
from skimage import io
from sklearn import svm
from joblib import dump, load
from PIL import Image, ImageDraw
from sklearn.metrics import classification_report,accuracy_score
import mysql.connector
mydb = mysql.connector.connect(user='root', password='root',host='localhost',database='web_school_web')
mycursor = mydb.cursor()
from datetime import datetime
import send_email as se
class myclass:

    path = 'C:/Users/Gaurav/Desktop/Bus_Face/face_recogniton/Dataset/'

    folders = []

    # r=root, d=directories, f = files
    for r, d, f in os.walk(path):
        for folder in d:
            folders.append(folder)
    known_face_encodings=[]
    known_face_names=[]
    for f in folders:
        ifile=f'Dataset/{f}/{f}_0.jpg'
        ru_image = face_recognition.load_image_file(ifile)
        ru_face_encoding = face_recognition.face_encodings(ru_image)[0]
        known_face_encodings.append(ru_face_encoding)
        known_face_names.append(f)

    clf = svm.SVC(gamma='scale')
    clf.fit(known_face_encodings,known_face_names)
    dump(clf,'SVM.Model')
    unknown_count=0
    timer=0
    TestData="Test"
    while True:
        
        usns=[]
        for(direcpath,direcnames,files) in os.walk(TestData):
            f=open('new_user.txt')
            data = f.read()
            f.close()
            if data != '':
                print(data)
                f=open('new_user.txt','w')
                f.write('')
                f.close() 
        
                ru_image = face_recognition.load_image_file(f'Dataset/{data}/{data}.jpg')
                ru_face_encoding = face_recognition.face_encodings(ru_image)[0]
                known_face_encodings.append(ru_face_encoding)
                known_face_names.append(data)
            f=open('readdata.txt')
            data = f.read()
            f.close()
            timer = timer+ 1
            fn='Unknown.jpg'
            f=open('unkn.txt','r')
            fd=f.read()
            f.close()
            print(timer)
            if timer>60 and fd!='':
                se.sendeMail(fd)
                timer=0
                f=open('unkn.txt','w')
                f.write('')
                f.close()



            if data == 'read':
                print(data)
                f=open('readdata.txt','w')
                f.write('busy')
                f.close()
                time.sleep(2)
                exists = os.path.isfile(TestData+'//a.jpg')
                if exists:
                    try:
                        frame = (TestData+'//a.jpg')

                        unknown_image = face_recognition.load_image_file(frame)
                        face_locations = face_recognition.face_locations(unknown_image)
                        face_encodings = face_recognition.face_encodings(unknown_image, face_locations)

                        pil_image = Image.fromarray(unknown_image)
                        draw = ImageDraw.Draw(pil_image)
                        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
                            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                            name = "Unknown Person"
                            unknown_count += 1
                            
                            
                            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                            best_match_index = np.argmin(face_distances)
                            if matches[best_match_index]:
                                name = known_face_names[best_match_index]
                            draw.rectangle(((left, top), (right, bottom)), outline=(0, 0, 255))
                            text_width, text_height = draw.textsize(name)
                            print("The Person is:",name)
                            f = open("output.txt","w")
                            print((name),file = f)
                            f.close()
                            if name == "Unknown Person":
                                path = (TestData+'//a.jpg')
                                un_image = cv2.imread(path)
                                cv2.imwrite("Unknown.jpg",un_image)
                                f=open('unkn.txt','w')
                                f.write('Unknown.jpg')
                                f.close()
                                #pil_image.save("Unknown.jpg")
                                f=open("result.txt","w")
                                print(("unknown"),file = f)
                                f.close()
                            else:
                                f=open("result.txt","w")
                                str1=f'face_matched:{name}'
                                print(str1,file = f)
                                f.close()
                                usns.append(name)

                            draw.rectangle(((left, bottom - text_height - 10), (right, bottom)), fill=(0, 0, 255), outline=(0, 0, 255))
                            draw.text((left + 6, bottom - text_height - 5), name, fill=(255, 255, 255, 255))

                        del draw
                        #pil_image.show()
                        pil_image.save("recognition/output.jpg")
                        os.remove(TestData+'//a.jpg')
                        time.sleep(5)
                        f=open('readdata.txt','w')
                        f.write('') 
                        f.close()
                        f=open('task.txt','r')
                        st=f.read()
                        f.close()
                        for i in usns:
                            print(i)
                            
                            sql="SELECT course, branch, sem FROM student_details where usn=%s"
                            val=(i,)
                            mycursor.execute(sql, val)
                            myresult = mycursor.fetchall()
                            for x in myresult:
                                print(x) 
                            now=datetime.now()
                            date=now.strftime("%d %m %Y")
                            time1=now.strftime("%H:%M:%S")
                            print(date,time1)
                            sql = "INSERT INTO entry_exit_record (usn, status,course,branch,sem,adate,atime) VALUES (%s, %s,%s, %s,%s, %s,%s)"
                            val = (i,st,x[0],x[1],x[2],date,time1)
                            mycursor.execute(sql, val)
                            mydb.commit()
                            sql="SELECT status FROM usn_status where usn=%s"
                            val = (i,)
                            mycursor.execute(sql, val)
                            myresult = mycursor.fetchall()
                            print('myresult',myresult)
                            
                            
                            if len(myresult)==0:
                                sql = "INSERT INTO usn_status (usn, status) VALUES (%s, %s)"
                                val = (i,st)
                                mycursor.execute(sql, val)
                                mydb.commit()
                            else:
                                print('already present')
                                sql="update usn_status set status=%s where usn=%s"
                                val = (st,i)
                                print(sql,val)
                                mycursor.execute(sql, val)
                                mydb.commit()


                    except:
                        print('could not read')
                        f=open('readdata.txt','w')
                        f.write('')
                        f.close()   


