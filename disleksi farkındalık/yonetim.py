# Öğretmen Paneli Arayüzü, öğrenci ekle-sil kısmı

import tkinter as tk
from tkinter import messagebox
from siniflar_ve_moduller import YuvarlakButon, VeriYoneticisi

class OgrenciYonetimSayfasi(tk.Frame):
    def __init__(self, ebeveyn, yonetici):
        super().__init__(ebeveyn, bg="#2C3E50")
        self.yonetici = yonetici
        # Eklenen öğrenci anında giriş ekranında da kaydedilsin
        self.veri_yoneticisi = self.yonetici.veri_yoneticisi

        # Başlık
        lbl = tk.Label(self, text="Sınıf Yönetim Paneli", bg="#2C3E50", fg="white", font=("Arial", 24, "bold"))
        lbl.pack(pady=50)

        # Açıklama
        lbl_bilgi = tk.Label(self, text="Buradan sınıfınızdaki öğrencileri sisteme ekleyip çıkartabilirsiniz.", 
                             bg="#2C3E50", fg="#bdc3c7", font=("Arial", 12))
        lbl_bilgi.pack(pady=10)

        # Ekleme Bölümü
        frame_ekle = tk.Frame(self, bg="#34495e", padx=20, pady=20)
        frame_ekle.pack(pady=20)

        tk.Label(frame_ekle, text="Öğrenci No:", bg="#34495e", fg="white", font=("Arial", 12, "bold")).pack(side="left", padx=5)
        
        self.entry_no = tk.Entry(frame_ekle, font=("Arial", 12), width=10)
        self.entry_no.pack(side="left", padx=5)

        btn_ekle = tk.Button(frame_ekle, text="+ Ekle", bg="#2C3E50", fg="white", font=("Arial", 11, "bold"),
                             command=self.ogrenci_ekle)
        btn_ekle.pack(side="left", padx=10)

        # Liste Bölümü
        tk.Label(self, text="Kayıtlı Öğrenci Listesi", bg="#2C3E50", fg="white", font=("Arial", 14)).pack(pady=(20,5))
        
        self.liste_kutusu = tk.Listbox(self, font=("Arial", 14), width=30, height=6)
        self.liste_kutusu.pack(pady=5)
        
        # Silme Butonu
        btn_sil = tk.Button(self, text="Seçili Öğrenciyi Sil", bg="#c0392b", fg="white", font=("Arial", 11),
                            command=self.ogrenci_sil)
        btn_sil.pack(pady=5)

        self.listeyi_guncelle()

        # Ana Menüye Dön Butonu
        YuvarlakButon(self, metin="<", genislik=40, yukseklik=40, 
                     arkaplan_rengi="#95a5a6", # Gri tonu
                     komut=lambda: yonetici.sayfa_goster("AnaSayfa")).place(x=20, y=20) # Sol üste sabitledik

    def ogrenci_ekle(self):
        no = self.entry_no.get().strip()
        # Bilgilendirme mesaj kutusunu gösterir
        if no:
            if self.veri_yoneticisi.ogrenci_ekle(no):
                messagebox.showinfo("Başarılı", f"{no} numaralı öğrenci eklendi.")
                self.entry_no.delete(0, tk.END)
                self.listeyi_guncelle()
            else:
                messagebox.showwarning("Hata", "Bu numara zaten kayıtlı!")
        else:
            messagebox.showwarning("Hata", "Lütfen bir numara girin.")

    def ogrenci_sil(self):
        secili = self.liste_kutusu.curselection()
        if secili:
            veri = self.liste_kutusu.get(secili)
            no = veri.split(" - ")[0]
            if messagebox.askyesno("Onay", f"{no} numaralı öğrenciyi silmek istediğine emin misin?"):
                self.veri_yoneticisi.ogrenci_sil(no)
                self.listeyi_guncelle()
        else: # Öğrenci seçilmeden silme butonuna basılırsa
            messagebox.showwarning("Uyarı", "Silinecek öğrenciyi seçin.")

    def listeyi_guncelle(self):
        self.liste_kutusu.delete(0, tk.END)
        veriler = self.veri_yoneticisi.tum_ogrencileri_getir()
        for no in veriler:
            self.liste_kutusu.insert(tk.END, f"{no}")

# UYGULAMAYI BAŞLAT
if __name__ == "__main__":
    # Döngüsel içe aktarmayı önlemek için burada içe aktarılmalıdır
    from ana3 import DisleksiUygulamasi
    app = DisleksiUygulamasi()
    app.mainloop()