# Ana Sayfa

import tkinter as tk
from tkinter import simpledialog, messagebox
from yonetim import OgrenciYonetimSayfasi
from siniflar_ve_moduller import YuvarlakButon, VeriYoneticisi
from sesler import SeslerTesti
from fonoloji import FonolojiTesti
from heceleme import HecelemeTesti
from hizli_okuma import HizliOkumaTesti
from siralama import SiralamaTesti
from ogretmen_icin import AnketSayfasi
from rapor import RaporSayfasi

# ARA GEÇİŞ EKRANI (Her testten önce çıkacak ekran)
class AraGecisEkrani(tk.Frame):
    def __init__(self, ebeveyn, yonetici):
        super().__init__(ebeveyn, bg="#2C3E50")
        self.lbl_mesaj = tk.Label(self, text="", font=("Arial", 40, "bold"), fg="white", bg="#2C3E50")
        self.lbl_mesaj.pack(expand=True) # Pencere büyüdüğünde aynı oranda büyüsün

# BİTİŞ EKRANI (Hepsi bitince çıkacak)
class BitisEkrani(tk.Frame):
    def __init__(self, ebeveyn, yonetici):
        super().__init__(ebeveyn, bg="#2C3E50")
        
        lbl = tk.Label(self, text="TEBRİKLER!\nTüm Testleri Tamamladın.", 
                       font=("Arial", 35, "bold"), fg="white", bg="#2C3E50", justify="center")
        lbl.pack(expand=True)
        
        # Ana Menüye Dön Butonu
        btn = YuvarlakButon(self, metin="Ana Menüye Dön", genislik=250, yukseklik=50,
                            arkaplan_rengi="#5184B1",
                            komut=lambda: yonetici.sayfa_goster("TestlerSayfasi"))
        btn.pack(side="bottom", pady=30)


# ANA UYGULAMA YÖNETİCİSİ
class DisleksiUygulamasi(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Disleksi")
        self.geometry("900x600")
        self.configure(bg="#A2C5D8")

        self.veri_yoneticisi = VeriYoneticisi() # Veri tabanını başlat
        self.aktif_ogrenci_no = None # Şu an testi çözen kim?

        # Tüm sayfaların üst üste duracağı bir kap (Container) oluştur
        container = tk.Frame(self, bg="#A2C5D8")
        container.pack(side="top", fill="both", expand=True)
        
        # Pencerenin boyutlandırılması durumunda sayfaların da genişlemesi için ayar
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.sayfalar = {}  # Sayfaların hafızada tutulacağı sözlük

        # Tüm sayfaları oluştur ve sözlüğe ekle
        for F in (AnaSayfa, TestlerSayfasi, RaporSayfasi, FonolojiTesti, SeslerTesti, HecelemeTesti, HizliOkumaTesti, SiralamaTesti,
                  AraGecisEkrani, BitisEkrani, OgrenciYonetimSayfasi, AnketSayfasi):
            sayfa_adi = F.__name__
            frame = F(ebeveyn=container, yonetici=self)
            self.sayfalar[sayfa_adi] = frame
            # Tüm sayfaları aynı yere (grid 0,0) koyuyoruz ki üst üste binsinler
            frame.grid(row=0, column=0, sticky="nsew")

        # TEST SIRALAMASI AYARLARI
        # Testlerin açılma sırası
        self.test_listesi = ["FonolojiTesti", "SeslerTesti", "SiralamaTesti", "HecelemeTesti", "HizliOkumaTesti"]
        self.test_isimleri = {
            "FonolojiTesti": "TEST: FONOLOJİ",
            "SeslerTesti": "TEST: FONOLOJİ 2",
            "SiralamaTesti": "TEST: SIRALAMA",
            "HecelemeTesti": "TEST: HECELEME",
            "HizliOkumaTesti": "TEST: HIZLI OKUMA"
        }
        self.su_anki_index = 0
        # İlk açılışta Ana Sayfayı göster
        self.sayfa_goster("AnaSayfa")

    def sayfa_goster(self, sayfa_adi):
        # İstenilen sayfayı en üste çıkar
        frame = self.sayfalar[sayfa_adi]
        frame.tkraise()
    
    # ÖĞRENCİ GİRİŞ KONTROLÜ
    def ogrenci_girisi_yap(self):
        # Ekrana küçük bir kutu açar ve veri ister
        girilen_no = simpledialog.askstring("Öğrenci Girişi", "Lütfen Öğrenci Numaranızı Giriniz:")
        
        if girilen_no: # Eğer bir şey yazıp OK dediyse
            if self.veri_yoneticisi.ogrenci_var_mi(girilen_no):
                self.aktif_ogrenci_no = girilen_no # Giriş başarılı
                messagebox.showinfo("Hoşgeldin", f"Merhaba {girilen_no}, testlere başlayabilirsin.")
                self.sayfa_goster("TestlerSayfasi") # Test seçme ekranına at
            else:
                messagebox.showerror("Hata", "Bu numara kayıtlı değil! Lütfen öğretmeninizle görüşün.")
        # Cancel derse hiçbir şey yapmaz, ana sayfada kalır.

    # Test sürecini başlat
    def test_surecini_baslat(self):
        self.su_anki_index = 0 # Başa sar
        self.siradaki_teste_gec()

    # Bir sonraki teste geç
    def siradaki_teste_gec(self):
        # Eğer listedeki testler bitmediyse
        if self.su_anki_index < len(self.test_listesi):
            gelecek_sayfa_adi = self.test_listesi[self.su_anki_index]
            ekranda_yazacak_isim = self.test_isimleri[gelecek_sayfa_adi]

            # Sayfa açılmadan önce içindeki değişkenleri temizle
            sayfa = self.sayfalar[gelecek_sayfa_adi]
            if hasattr(sayfa, "testi_sifirla"):
                sayfa.testi_sifirla()

            # 1. Önce geçiş ekranını göster
            gecis_sayfasi = self.sayfalar["AraGecisEkrani"]
            gecis_sayfasi.lbl_mesaj.config(text=ekranda_yazacak_isim) # Yazıyı güncelle
            self.sayfa_goster("AraGecisEkrani")
            
            # 2. 2 Saniye (2000 ms) bekle sonra testi aç
            self.after(2000, lambda: self.sayfa_goster(gelecek_sayfa_adi))
            
            # İndeksi bir artır (bir sonraki sefere hazırlık)
            self.su_anki_index += 1
            
        else:
            # Testler bittiyse Bitiş Ekranını göster
            self.sayfa_goster("BitisEkrani")

# SAYFA TASARIMI
class AnaSayfa(tk.Frame):
    def __init__(self, ebeveyn, yonetici):
        super().__init__(ebeveyn, bg="#A2C5D8")
        self.yonetici = yonetici
        
        lbl = tk.Label(self, text="Disleksi Öğretmen Farkındalığı", 
                       bg="#A2C5D8", font=("Times", 30, "bold"))
        lbl.pack(pady=50)

        # Buton kodunun uzun hali
        # Sol üst köşeye profil butonu
        btn_profil = YuvarlakButon(self, metin="👤", 
                               genislik=40, yukseklik=40,
                               arkaplan_rengi="#5184B1", yazi_rengi="black",
                               komut=lambda: yonetici.sayfa_goster("OgrenciYonetimSayfasi"))
        btn_profil.place(x=20, y=20) # Sol üst köşeye sabitler

        # Buton kodunun kısa hali (oluşturacağımız diğer tüm butonlar için böyle olacak)
        # Testler Butonu (Öğrenci Girişi İster)
        YuvarlakButon(self, metin="Testler", genislik=300, yukseklik=80, 
                     arkaplan_rengi="#5184B1", yazi_rengi="black",
                     komut=lambda: yonetici.ogrenci_girisi_yap()).pack(pady=30)
        
        # Rapor Butonu
        YuvarlakButon(self, metin="Öğretmen Raporu", genislik=300, yukseklik=80, 
                     arkaplan_rengi="#5184B1", yazi_rengi="black",
                     komut=lambda: yonetici.sayfa_goster("RaporSayfasi")).pack(pady=20)

class TestlerSayfasi(tk.Frame):
    def __init__(self, ebeveyn, yonetici):
        super().__init__(ebeveyn, bg="#A2C5D8")

        lbl = tk.Label(self, text="Test Seçimi Yapınız", bg="#A2C5D8", font=("Arial", 30, "bold"))
        lbl.pack(pady=50)

        # Öğretmen İçin Butonu
        YuvarlakButon(self, metin="ÖĞRETMEN için", genislik=300, yukseklik=80, 
                     arkaplan_rengi="#5184B1", yazi_rengi="black", 
                     komut=lambda: yonetici.sayfa_goster("AnketSayfasi")).pack(pady=30)

        # Öğrenci İçin Butonu
        YuvarlakButon(self, metin="ÖĞRENCİ için", genislik=300, yukseklik=80, 
                     arkaplan_rengi="#5184B1", yazi_rengi="black",
                     # Testi başlat
                     komut=lambda: yonetici.test_surecini_baslat()).pack(pady=20)

        # Geri Dön Butonu
        YuvarlakButon(self, metin="Geri Dön", 
                     arkaplan_rengi="#5184B1", yazi_rengi="black",
                     komut=lambda: yonetici.sayfa_goster("AnaSayfa")).pack(side="bottom", pady=30)

if __name__ == "__main__":
    app = DisleksiUygulamasi()
    app.mainloop()