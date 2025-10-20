import os
import face_recognition
import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage
import cv2

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://faceandidinfo-default-rtdb.firebaseio.com/',
    'storageBucket': 'faceandidinfo.appspot.com'
})


import pickle


folderPath = 'Userimg'
PathList = os.listdir(folderPath)

imgList = []
userIds = []
for path in PathList:
    imgList.append(cv2.imread(os.path.join(folderPath,path)))#Images/32051.png veriyi imgliste atar
    userIds.append(os.path.splitext(path)[0])#dosyanın uzantısız adı elde etmek

    fileName = f'{folderPath}/{path}'#Images/34324.png şeklinde firebase kaydeder.
    bucket = storage.bucket()
    blob = bucket.blob(fileName)
    blob.upload_from_filename(fileName)
    print(userIds)




def findEncodings(imagesList):
    encodeList = []

    for img in imagesList:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)#face_recognition kütüphanesi için RGB formatına dönüştürülüyor.
        encode = face_recognition.face_encodings(img)[0]# Görüntü içindeki yüz kodlarını bulur.
        # 0 indeksi birden fazla yüz olduğunda sadece ilk olan yüzü alır.
        encodeList.append(encode)


    return encodeList

print("Encoding Started . . .")
encodeListKnown = findEncodings(imgList)
encodeListKnownWithIds = [encodeListKnown, userIds] # Görüntülerin yüz kodları ve öğrenci id'leri
print("Encoding Complete")


file = open("PictureFile.p", 'wb')
pickle.dump(encodeListKnownWithIds, file) # binary modunda dosyaya yazılır ve kaydedilir.
file.close()
print("File saved")
