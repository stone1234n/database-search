import sqlite3
import tkinter as tk
from tkinter import filedialog
from ttkthemes import ThemedTk

def veritabani_sec():
    dosya_adi = filedialog.askopenfilename(title="Veritabanı Seç", filetypes=[("Metin dosyaları", "*.txt"), ("SQLite veritabanları", "*.db")])
    veritabani_dosyasi.set(dosya_adi)

def sql_veritabani_arama(sorgu):
    baglanti = sqlite3.connect(veritabani_dosyasi.get())
    imlec = baglanti.cursor()
    imlec.execute(sorgu)
    sonuclar = imlec.fetchall()
    baglanti.close()
    return sonuclar

def txt_veritabani_arama(sorgu):
    with open(veritabani_dosyasi.get(), 'r') as dosya:
        sonuclar = [satir.strip() for satir in dosya if sorgu in satir]
    return sonuclar

def ara():
    sorgu = giris_alani.get()
    if veritabani_tipi.get() == 'SQL':
        try:
            sonuclar = sql_veritabani_arama(sorgu)
            sonuc_metni.set("Arama Sonuçları:")
            sonuc_liste.delete(0, tk.END)
            for satir in sonuclar:
                sonuc_liste.insert(tk.END, satir)
        except sqlite3.OperationalError as e:
            sonuc_metni.set("SQL Arama Hatası: " + str(e))
    elif veritabani_tipi.get() == 'TXT':
        sonuclar = txt_veritabani_arama(sorgu)
        sonuc_metni.set("Arama Sonuçları:")
        sonuc_liste.delete(0, tk.END)
        for satir in sonuclar:
            sonuc_liste.insert(tk.END, satir)
    else:
        sonuc_metni.set("Geçersiz veritabanı tipi. Lütfen SQL veya TXT seçiniz.")

def say_hello():
    greeting = f"Hello, {name_entry.get()}!"
    greeting_label.config(text=greeting)

root = ThemedTk(theme="dark")  
root.title("Database Searcher")
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.geometry(f"{int(screen_width * 0.8)}x{int(screen_height * 0.8)}+{int(screen_width * 0.1)}+{int(screen_height * 0.1)}")


background_image = tk.PhotoImage(file="background1.png")
background_label = tk.Label(root, image=background_image)
background_label.place(relwidth=1, relheight=1)

veritabani_dosyasi = tk.StringVar()
veritabani_sec_buton = tk.Button(root, text="Veritabanı Seç", command=veritabani_sec, bg="black", fg="green")
veritabani_sec_buton.place(x=50, y=50)

veritabani_tipi = tk.StringVar()
veritabani_tipi.set("SQL")
sql_radio = tk.Radiobutton(root, text="SQL", variable=veritabani_tipi, value="SQL", bg="black", fg="green")
sql_radio.place(x=200, y=50)
txt_radio = tk.Radiobutton(root, text="TXT", variable=veritabani_tipi, value="TXT", bg="black", fg="green")
txt_radio.place(x=250, y=50)

giris_alani = tk.Entry(root)
giris_alani.place(x=50, y=100)

giris_butonu = tk.Button(root, text="Ara", command=ara, bg="black", fg="green")
giris_butonu.place(x=200, y=100)

sonuc_metni = tk.StringVar()
sonuc_metni.set("Arama Sonuçları:")
sonuc_label = tk.Label(root, textvariable=sonuc_metni, bg="black", fg="green")
sonuc_label.place(x=50, y=150)


listbox_frame = tk.Frame(root, bg="black")
listbox_frame.place(x=50, y=200)


sonuc_liste = tk.Listbox(listbox_frame, height=30, width=175, bg="black", fg="green")
sonuc_liste.pack(side="left", fill="both", expand=True)


horiz_scrollbar = tk.Scrollbar(listbox_frame, orient="horizontal", command=sonuc_liste.xview)
horiz_scrollbar.pack(side="bottom", fill="x")
vert_scrollbar = tk.Scrollbar(listbox_frame, orient="vertical", command=sonuc_liste.yview)
vert_scrollbar.pack(side="right", fill="y")


sonuc_liste.config(xscrollcommand=horiz_scrollbar.set, yscrollcommand=vert_scrollbar.set)




root.mainloop()