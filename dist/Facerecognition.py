import os
import pickle
import cv2
import face_recognition
import numpy as np
import cvzone
import firebase_admin
from tkinter import *
import tkinter.messagebox as messagebox
from PIL import ImageTk, Image
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage


cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://faceandidinfo-default-rtdb.firebaseio.com/',
    'storageBucket': 'faceandidinfo.appspot.com'
})

modelInfo = 0
sayac = 0
id = -1
imgUser = []
kronometre = 0
bucket = storage.bucket()



camview = cv2.VideoCapture(0)#kamera kaydını başlatıyor
camview.set(3, 640)# 3 parametresi genişlik değeri alır
camview.set(4, 480)#yükseklik


Backgroundcam = cv2.imread('Resources/backgroundcam.png')
Backgroundresult = cv2.imread('Resources/backgroundresult.png')


ModelPath = 'Resources/Model'
ModelPathList = os.listdir(ModelPath) #Model klosöründeki resimlerin listesi alınıyor
ModelArray = []
for path in ModelPathList:
    ModelArray.append(cv2.imread(os.path.join(ModelPath, path)))
    #resimler imgModeList dizisine ekleniyor.



file = open('PictureFile.p', 'rb') # PictureFile dosyasındaki veriler yüklenir.
ImageAndIdList = pickle.load(file)
file.close()
UserImageList, UserIds = ImageAndIdList



while True:


    success, img = camview.read() # kameradan görüntü oku

    Backgroundcam[162:162 + 480, 55:55 + 640] = img  # Alınan görüntüyü yerleştir.

    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)# görüntüyü RGB formatına dönüştür.

    facelocation = face_recognition.face_locations(imgRGB) # görüntüde yüzleri tespit etme, yüzün konumları bulunur.

    faceVector = face_recognition.face_encodings(imgRGB, facelocation)
    #Kameradan alınan yüzün Derin öğrenme ile yüz özelliği vektörü oluşturur. Bu vektör 128 boyutludur.
    #Her bir boyut yüzün farklı özelliğini veya karakteristiğini temsil eder.



    if facelocation:

        for camFaceVector, faceLoc in zip(faceVector, facelocation):

            match = face_recognition.compare_faces(UserImageList, camFaceVector, 0.55)
            #tolerans 0.6 en iyi performans.
            #listedeki yüzlerle kameradaki yüzleri karşılaştır 'true - false' değeri döner.
            print(match)
            faceDis = face_recognition.face_distance(UserImageList, camFaceVector)
            #listedeli yüzlerle kameradaki yüz arasındaki benzerlik mesafesini hesaplar.
            print(faceDis)
            matchIndex = np.argmin(faceDis) # en düşük benzerlik mesafesi atanır.
                                            # benzerlik mesafesi ne kadar azsa o kadar benzemektedir.
            print(matchIndex)



            if match[matchIndex]:# MatchIndex Listedeki true indeksiyle uyuşuyorsa bloğa gir.
                                    # Yani kameradaki yüz, listedeki yüz ile aynı ise bloğa gir.


                y1, x2, y2, x1 = faceLoc
                bbox = 55 + x1, 162 + y1, x2 - x1, y2 - y1
                Backgroundcam = cvzone.cornerRect(Backgroundcam, bbox, rt=0)  # yüzü dikdörtgen içine alır.
                id = UserIds[matchIndex]
                # y1 = sol üst yüz
                # x2 = sağ üst yüz
                # y2 = sağ alt yüz
                # x1 = sol alt yüz

                if sayac == 0:
                    sayac = 1
                    # modelInfo = 1





            else: # Yabancı bir yüz ise bu bloğa gir
                y1, x2, y2, x1 = faceLoc
                bbox = 55 + x1, 162 + y1, x2 - x1, y2 - y1
                Backgroundcam = cvzone.cornerRect(Backgroundcam, bbox, rt=0)
                kronometre += 1
                if kronometre>=0 and kronometre <=6:
                    if cv2.getWindowProperty("Result", cv2.WND_PROP_VISIBLE) >= 1:
                        cv2.destroyWindow("Result")
                    if cv2.getWindowProperty("Match", cv2.WND_PROP_VISIBLE) >= 1:
                        cv2.destroyWindow("Match")
                    if cv2.getWindowProperty("Waiting Face", cv2.WND_PROP_VISIBLE) >= 1:
                        cv2.destroyWindow("Waiting Face")

                    cv2.imshow("Face Recognation", Backgroundcam)
                    cv2.waitKey(1)
                if kronometre > 6:
                    if cv2.getWindowProperty("Result", cv2.WND_PROP_VISIBLE) >= 1:
                        cv2.destroyWindow("Result")
                    if cv2.getWindowProperty("Face Recognation", cv2.WND_PROP_VISIBLE) >= 1:
                        cv2.destroyWindow("Face Recognation")

                    modelInfo = 3
                    Backgroundresult[0:0 + 633, 0:0 + 414] = ModelArray[modelInfo]
                    cv2.imshow("Not Match!", Backgroundresult)

                    print("Yüz Tanınmıyor")
                    input_key = cv2.waitKey(0)

                    if input_key == 13:
                        break
                    if input_key == 32:
                        sayac = 0
                        continue

        if sayac != 0:

            if sayac == 1:

                userInfo = db.reference(f'User/{id}').get()

                blob = bucket.get_blob(f'Userimg/{id}.png')
                array = np.frombuffer(blob.download_as_string(), np.uint8)# Görüntüyü byte dizisi olarak indirir.
                                                                            #Numpy dizisine dönüştürür.

                imgUser = cv2.imdecode(array, cv2.COLOR_BGRA2BGR) #BGR formatına dönüştürür.
                                                                    #Numpy dizisini görüntü olarak işler.


                sayac = 2




            if sayac >= 2 and sayac <= 10:
                if cv2.getWindowProperty("Result", cv2.WND_PROP_VISIBLE) >= 1:
                    cv2.destroyWindow("Result")
                if cv2.getWindowProperty("Waiting Face", cv2.WND_PROP_VISIBLE) >= 1:
                    cv2.destroyWindow("Waiting Face")
                if cv2.getWindowProperty("Not Match!", cv2.WND_PROP_VISIBLE) >= 1:
                    cv2.destroyWindow("Not Match!")

                cv2.imshow("Face Recognation", Backgroundcam)
                cv2.waitKey(1)

                sayac+=1



            elif sayac >= 11 and sayac <=18:
                if cv2.getWindowProperty("Face Recognation", cv2.WND_PROP_VISIBLE) >= 1:
                    cv2.destroyWindow("Face Recognation")


                modelInfo = 2
                Backgroundresult[0:0 + 633, 0:0 + 414] = ModelArray[modelInfo]

                cv2.imshow("Match", Backgroundresult)
                cv2.waitKey(1)

                sayac+=1


            else:
                if cv2.getWindowProperty("Match", cv2.WND_PROP_VISIBLE) >= 1:
                    cv2.destroyWindow("Match")
                if cv2.getWindowProperty("Not Match!", cv2.WND_PROP_VISIBLE) >= 1:
                    cv2.destroyWindow("Not Match!")


                modelInfo = 1

                Backgroundresult[0:0 + 633, 0:0 + 414] = ModelArray[modelInfo]

                cv2.putText(Backgroundresult, str(userInfo['job']), (113, 455),
                            cv2.FONT_HERSHEY_COMPLEX, 0.5, (50, 50, 50),2 )

                cv2.putText(Backgroundresult, str(userInfo['age']), (113, 398),
                            cv2.FONT_HERSHEY_COMPLEX, 0.5, (50, 50, 50), 2)

                cv2.putText(Backgroundresult, str(userInfo['name']), (113, 342),
                            cv2.FONT_HERSHEY_COMPLEX, 0.5, (50, 50, 50), 2)


                Backgroundresult[35:35 + 260, 75:75 + 260] = imgUser

                cv2.imshow("Result", Backgroundresult)

                input_key = cv2.waitKey(0)

                if input_key == 13:
                    break
                if input_key == 32:
                    sayac = 0
                    continue



    else:
        if cv2.getWindowProperty("Result", cv2.WND_PROP_VISIBLE) >= 1:
            cv2.destroyWindow("Result")

        if cv2.getWindowProperty("Face Recognation", cv2.WND_PROP_VISIBLE) >= 1:
            cv2.destroyWindow("Face Recognation")

        if cv2.getWindowProperty("Match", cv2.WND_PROP_VISIBLE) >= 1:
            cv2.destroyWindow("Match")

        if cv2.getWindowProperty("Not Match!", cv2.WND_PROP_VISIBLE) >= 1:
            cv2.destroyWindow("Not Match!")

        modelInfo =0
        sayac = 0
        kronometre = 0
        Backgroundresult[0:0 + 633, 0:0 + 414] = ModelArray[modelInfo]

        cv2.imshow("Waiting Face", Backgroundresult)
        cv2.waitKey(1)

print(userInfo)
cv2.destroyAllWindows()

window = Tk()
window.title("Giriş")
window.geometry('400x400+600+200')
window.resizable(height=False, width=False)
window.configure(bg='#00abff')

def close_app():
    window.destroy()


def start_main():
    if tc_entry.get() == str(userInfo['tc']) and sifre_entry.get() == str(userInfo['sifre']):
        messagebox.showinfo("Giriş", "Giriş başarılı!")
    else:
        messagebox.showerror("Hata", "TC veya şifreniz hatalı!")

def limit_character(entry):
    value = entry.get()
    if len(value) > 10:
        entry.delete(10, "end")

image_yolu = 'Resources/giris.png'
girisimg = Image.open(image_yolu)
girisimg = girisimg.resize((180, 130), Image.LANCZOS)
girisimg = ImageTk.PhotoImage(girisimg)

image_label = Label(window, image=girisimg)
image_label.image = girisimg
image_label.place(x=120, y=40)

tc_label = Label(window, text="TC:", font=("Helvetica", 12), bg='#00abff')
tc_label.place(x=60, y=200)
tc_entry = Entry(window, font=("Helvetica", 12))
tc_entry.place(x=120, y=200)
tc_entry.bind("<Key>", lambda e: limit_character(tc_entry))  # Her tuşa basıldığında sınırlamayı kontrol et

sifre_label = Label(window, text="Şifre:", font=("Helvetica", 12), bg='#00abff')
sifre_label.place(x=60, y=230)
sifre_entry = Entry(window, show='*', font=("Helvetica", 12))
sifre_entry.place(x=120, y=230)

start_button = Button(window, text="Giriş", command=start_main, font=("Helvetica", 12, "bold"), fg="white", bg="green", width=8, height=1)
start_button.place(x=170, y=270)

close_button = Button(window, text="Kapat", command=close_app, font=("Helvetica", 12, "bold"), fg="white", bg="red",width=8, height=1)
close_button.place(x=170, y=320)


window.mainloop()


