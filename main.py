import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import json
import os

#Yazılımın hangi adreste olduğunu bulur ve o dosyanın içinde json dosyası açması istenir
adres = os.path.dirname(os.path.abspath(__file__))
gorevler_json_yolu = os.path.join(adres, 'tasks.json')

# Eger dosya bulunamazsa yani yoksa içinde sözlük oluşturacak, varsa da sözlüğü döndürecek bir fonksiyon
def gorevleri_yukle():
    try:
        with open(gorevler_json_yolu, 'r') as dosya:
            return json.load(dosya)
    except FileNotFoundError:
        return {'gorevler': [], 'tamamlananlar': []}
    
# Verileri JSON dosyasının içindeki sözlüğe kaydeden fonksiyon
def gorevleri_kaydet():
    with open(gorevler_json_yolu, 'w') as dosya:
        json.dump({'gorevler': gorevler, 'tamamlananlar': tamamlanan_gorevler}, dosya)

# Metin kutucugundan alınan veriyi gorevler kutucuguna ekleyecek olan fonksiyon
def gorev_ekle():
    gorev = gorev_girisi.get().strip()
    if not gorev:
        messagebox.showerror("Hata", "Görev boş olamaz")
    else:
        gorevler.append(gorev)
        gorev_listesini_guncelle()
        gorev_girisi.delete(0, tk.END)
        gorevleri_kaydet()

#Gorev listesinden seçilen görevi tamamlayıp, tamamlanan verileri başka bir tabloya aktaran bir fonksiyon
def gorevi_tamamla():
    secili_gorev = gorev_listesi.curselection()
    secili_tamamlanan = tamamlanan_gorev_listesi.curselection()

    if secili_gorev:
        tamamlanan_gorevler.append(gorevler[secili_gorev[0]])
        del gorevler[secili_gorev[0]]
        gorev_listesini_guncelle()
        tamamlanan_gorev_listesini_guncelle()
        gorevleri_kaydet()
    elif secili_tamamlanan:
        messagebox.showerror("Hata", "Zaten tamamlanmış bir görevi tamamlayamazsınız.")
    else:
        messagebox.showinfo("Bilgi", "Lütfen tamamlanacak bir görev seçin.")

# Secilen gorevi silen fonksiyon
def gorevi_sil():
    secili_gorev = gorev_listesi.curselection()
    secili_tamamlanan = tamamlanan_gorev_listesi.curselection()

    if secili_gorev:
        onay = messagebox.askyesno("Silme Onayı", "Bu görevi silmek istediğinizden emin misiniz?")
        if onay:
            del gorevler[secili_gorev[0]]
            gorev_listesini_guncelle()
            gorevleri_kaydet()
    elif secili_tamamlanan:
        onay = messagebox.askyesno("Silme Onayı", "Tamamlanmış bu görevi silmek istediğinizden emin misiniz?")
        if onay:
            del tamamlanan_gorevler[secili_tamamlanan[0]]
            tamamlanan_gorev_listesini_guncelle()
            gorevleri_kaydet()
    else:
        messagebox.showerror("Hata", "Silmek için lütfen eleman seçiniz.")


# Gorev listesini güncelleyip ekrana yansıtan fonksiyon
def gorev_listesini_guncelle():
    gorev_listesi.delete(0, tk.END)
    for index,gorev in enumerate(gorevler,start=1):
        gorev_listesi.insert(tk.END, f"{index}) {gorev}")
# Tamamlanmış görevlerin listesini güncelleyip ekrana yansıtan fonksiyon
def tamamlanan_gorev_listesini_guncelle():
    tamamlanan_gorev_listesi.delete(0, tk.END)
    for gorev in tamamlanan_gorevler:
        tamamlanan_gorev_listesi.insert(tk.END, gorev)

#seçilen görevi bir yukarı taşıyan fonksiyon
def gorev_yukari_tasi():
    secili = gorev_listesi.curselection()
    if secili and secili[0] > 0:
        gorev = gorevler.pop(secili[0])
        gorevler.insert(secili[0] - 1, gorev)
        gorev_listesini_guncelle()
        gorev_listesi.selection_set(secili[0] - 1)
#Secilen görevi aşşağı taşıyan fonksiyon
def gorev_asagi_tasi():
    secili = gorev_listesi.curselection()
    if secili and secili[0] < len(gorevler) - 1:
        gorev = gorevler.pop(secili[0])
        gorevler.insert(secili[0] + 1, gorev)
        gorev_listesini_guncelle()
        gorev_listesi.selection_set(secili[0] + 1)

# Buradan sonrası arayüz oluşturma ve etkileşim kodlarıdır,

# Mevcut görevleri yükle
data = gorevleri_yukle()
gorevler = data['gorevler']
tamamlanan_gorevler = data['tamamlananlar']

# Ana pencere
ana_pencere = tk.Tk()
ana_pencere.title("To-Do List")
ana_pencere.geometry("700x800")
ana_pencere.configure(bg='#f0f0f0')  # Arka plan rengini ayarla

# Görev Ekleme Çerçevesi
gorev_ekleme_cercevesi = ttk.LabelFrame(ana_pencere, text="Görev Ekle", padding=(10, 5), relief='groove', borderwidth=2)
gorev_ekleme_cercevesi.pack(fill="x", expand="yes", padx=10, pady=10)
gorev_girisi = ttk.Entry(gorev_ekleme_cercevesi)
gorev_girisi.pack(side="left", expand=True, padx=5, pady=5, fill="x")
gorev_ekle_butonu = ttk.Button(gorev_ekleme_cercevesi, text="Görev Ekle", command=gorev_ekle)
gorev_ekle_butonu.pack(side="right", padx=5, pady=5)

# Görevleri Görüntüleme Çerçevesi
gorevleri_goruntuleme_cercevesi = ttk.LabelFrame(ana_pencere, text="Görevleri Görüntüle", padding=(10, 5), relief='groove', borderwidth=2)
gorevleri_goruntuleme_cercevesi.pack(fill="both", expand="yes", padx=10, pady=10)
gorev_listesi = tk.Listbox(gorevleri_goruntuleme_cercevesi, selectbackground='#cce5ff', background="darksalmon")
gorev_listesi.pack(side="left", expand=True, padx=5, pady=5, fill="both")

# Tamamlanan Görevler Çerçevesi
tamamlanan_gorevler_cercevesi = ttk.LabelFrame(ana_pencere, text="Tamamlanan Görevler", padding=(10, 5), relief='groove', borderwidth=2)
tamamlanan_gorevler_cercevesi.pack(fill="both", expand="yes", padx=10, pady=10)
tamamlanan_gorev_listesi = tk.Listbox(tamamlanan_gorevler_cercevesi, selectbackground='#cce5ff', background='darkolivegreen1')
tamamlanan_gorev_listesi.pack(side="left", expand=True, padx=5, pady=5, fill="both")

# Görev Yönetim Butonları
butonlar_cercevesi = ttk.Frame(ana_pencere, padding=(10, 5))
butonlar_cercevesi.pack(fill="x", padx=10, pady=10, side="bottom")

gorevi_tamamla_butonu = ttk.Button(butonlar_cercevesi, text="Görevi Tamamla", command=gorevi_tamamla)
gorevi_tamamla_butonu.pack(side="left", padx=5, pady=5)
gorevi_sil_butonu = ttk.Button(butonlar_cercevesi, text="Görevi Sil", command=gorevi_sil)
gorevi_sil_butonu.pack(side="left", padx=5, pady=5)

# Yukarı Aşağı Taşıma Butonları
tasima_butonlari_cercevesi = ttk.Frame(gorevleri_goruntuleme_cercevesi)
tasima_butonlari_cercevesi.pack(side="right", fill="y", padx=5, pady=5)

yukari_tasi_butonu = ttk.Button(tasima_butonlari_cercevesi, text="Yukarı Taşı", command=gorev_yukari_tasi)
yukari_tasi_butonu.pack(pady=5)

asagi_tasi_butonu = ttk.Button(tasima_butonlari_cercevesi, text="Aşağı Taşı", command=gorev_asagi_tasi)
asagi_tasi_butonu.pack(pady=5)

# Listbox'ları İlk Güncelleme
gorev_listesini_guncelle()
tamamlanan_gorev_listesini_guncelle()

ana_pencere.mainloop()