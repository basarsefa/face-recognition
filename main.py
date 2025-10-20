from tkinter import *
from tkinter import filedialog
from PIL import Image
import shutil
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import tkinter.messagebox as messagebox


cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL' : 'https://faceandidinfo-default-rtdb.firebaseio.com/'
})

img_name = None
dosya_name = None
ref = db.reference('User')

def save_to_firebase():

    if not name_entry.get() or not job_entry.get() or not age_entry.get() or not img_name or not tc_entry.get() or not sifre_entry.get() :
        # Eğer herhangi bir alan boşsa veya resim seçilmediyse hata mesajı göster
        messagebox.showerror("Hata", "Lütfen tüm alanları doldurun ve bir resim seçin.")
        return

    if tc_entry.get() and not tc_entry.get().isdigit():
        messagebox.showerror("Hata", "TC'de harf bulunamaz! Lütfen geçerli bir TC girin.")
        return
    existing_tc = ref.order_by_child('tc').equal_to(tc_entry.get()).get()
    if existing_tc:
        messagebox.showerror("Hata", "Bu TC zaten kullanımda.")
        return


    user_id = img_name
    name = name_entry.get()
    job = job_entry.get()
    age = age_entry.get()
    tc = tc_entry.get()
    sifre = sifre_entry.get()

    data = {


            "name": name,
            "job": job,
            "age": age,
            "tc" : tc,
            "sifre": sifre
    }
    shutil.copy(dosya_name, "./Userimg")  # Resmi Userimg klasörüne kopyala
    print("Resim başarıyla seçildi ve Images klasörüne kaydedildi:", os.path.basename(dosya_name))

    ref.child(user_id).set(data)
    print("Veri Firebase'e başarıyla kaydedildi.")
    # FaceGenerator.py dosyasının tam yolunu alın
    script_path = "FaceGenerator.py"

    # FaceGenerator.py dosyasını çalıştırın
    os.system("python {}".format(script_path))


def browse_image():
    initial_dir = "C:/Users/basar/OneDrive/Masaüstü/fotolar"
    filename = filedialog.askopenfilename(initialdir=initial_dir, title="Resim Seç", filetypes=(("Image Files", "*.jpg *.jpeg *.png *.gif"), ("All Files", "*.*")))
    messagebox.showinfo("Uyarı", "Lütfen resmin 260x260 piksel boyutunda olduğundan emin olun.")

    if filename:

        _, ext = os.path.splitext(filename)
        if ext.lower() != ".png":
            messagebox.showwarning("Uyarı", "Lütfen PNG formatında bir resim seçin.")
            return

        global dosya_name
        dosya_name = filename

        dosya_adi = os.path.basename(filename)
        global img_name
        img_name = dosya_adi.split('.')[0]
        print(img_name)

def close_app():
    window.destroy()
def limit_character(entry):
    value = entry.get()
    if len(value) > 10:
        entry.delete(10, "end")








# Tkinter penceresi oluşturun
window = Tk()
window.title("Register")
window.geometry('400x400+600+200')
window.resizable(height=False, width=False)
window.configure(bg='#468499')


# İsim etiketi ve giriş kutusu
name_label = Label(window,font=("Corbel", 12), bg='#468499',fg='white',text="Ad Soyad:")
name_label.place(x=45, y=40)
name_entry = Entry(window,font=("Corbel", 12),width=22)
name_entry.place(x=130, y=40)

# Bölüm etiketi ve giriş kutusu
job_label = Label(window, font=("Corbel", 12),bg='#468499', fg='white', text="Meslek:")
job_label.place(x=60, y=145)
job_entry = Entry(window, font=("Corbel", 12),width=22)
job_entry.place(x=130, y=145)

# Yaş etiketi ve giriş kutusu
age_label = Label(window, font=("Corbel", 12),bg='#468499',fg='white',text="Yaş:")
age_label.place(x=80, y=180)
age_entry = Entry(window, font=("Corbel", 12), width=22)
age_entry.place(x=130, y=180)

tc_label = Label(window,font=("Corbel", 12), bg='#468499',fg='white',text="TC:")
tc_label.place(x=83, y=75)
tc_entry = Entry(window,font=("Corbel", 12),width=22)
tc_entry.place(x=130, y=75)
tc_entry.bind("<Key>", lambda e: limit_character(tc_entry))

sifre_label = Label(window,font=("Corbel", 12),bg='#468499',fg='white', text="Şifre:")
sifre_label.place(x=75, y=110)
sifre_entry = Entry(window,show='*',font=("Corbel", 12),width=22)
sifre_entry.place(x=130, y=110)

browse_button = Button(window, text="Resim Seç", command=browse_image, bg='#80c5ca',fg='white')
browse_button.place(x=250, y=220)


# Kaydet butonu
save_button = Button(window, text="Kaydet", command=save_to_firebase,font=("Helvetica", 12), width=10, height=1,bg='#80c5ca',fg='white')
save_button.place(x=160, y=270)

def start_main():
    window.destroy()
    script_path = "Facerecognition.py"

    os.system("python {}".format(script_path))

start_button = Button(window, text="Başlat", command=start_main,font=("Helvetica", 12), width=10, height=1, bg='#3ae965', fg='white')
start_button.place(x=60, y=350)

close_button = Button(window, text="Kapat", command=close_app,font=("Helvetica", 12), width=10, height=1, bg='#f30505', fg='white')
close_button.place(x=240, y=350)




# Tkinter penceresini çalıştırın
window.mainloop()
