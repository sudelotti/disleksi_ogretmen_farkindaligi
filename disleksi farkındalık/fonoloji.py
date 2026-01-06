# Fonoloji testleri (işitme kısmı)

import tkinter as tk
from tkinter import messagebox
import random
import os
from siniflar_ve_moduller import YuvarlakButon, TemelTest

try:
    import pygame
except ImportError:
    pygame = None

class FonolojiTesti(TemelTest):
    def __init__(self, ebeveyn, yonetici):
        # TemelTest sınıfındaki özellikleri miras al
        super().__init__(ebeveyn, yonetici, katsayi=3.0)
        
        # SORU HAVUZU
        self.sorular = [
            {
                "ses_dosyasi": "balık.mp3",
                "soru": "Duyduğun kelime hangi harfle başlıyor?",
                "dogru": "b",
                "siklar": ["b", "d"]
            },
            {
                "ses_dosyasi": "mavi.mp3",
                "soru": "Duyduğun kelime hangi harfle başlıyor?",
                "dogru": "m",
                "siklar": ["m", "w"]
            },
            {
                "ses_dosyasi": "nasıl.mp3",
                "soru": "Duyduğun kelime hangi harfle başlıyor?",
                "dogru": "n",
                "siklar": ["n", "u"]
            },
            {
                "ses_dosyasi": "para.mp3",
                "soru": "Duyduğun kelime hangi harfle başlıyor?",
                "dogru": "p",
                "siklar": ["p", "q"]
            },
            {
                "ses_dosyasi": "sakız.mp3",
                "soru": "Duyduğun kelime hangi harfle başlıyor?",
                "dogru": "S",
                "siklar": ["S", "Ƨ"]
            },
            {
                "ses_dosyasi": "kitap.mp3",
                "soru": "Duyduğun kelime hangi harfle bitiyor?",
                "dogru": "p",
                "siklar": ["b", "p"]
            },
            {
                "ses_dosyasi": "yok.mp3",
                "soru": "Duyduğun kelimeyi işaretle.",
                "dogru": "yok",
                "siklar": ["koy", "yok"]
            },
            {
                "ses_dosyasi": "ev.mp3",
                "soru": "Duyduğun kelimeyi işaretle.",
                "dogru": "ev",
                "siklar": ["ev", "ve"]
            }
        ]
        
        self.yanlis_sayisi = 0 # Yanlışlar sayılacak
        self.hata_kayitlari = [] # Hata kayıtları için liste

        # ARAYÜZ
        self.lbl_soru = tk.Label(self, text="...", bg="#A2C5D8", font=("Arial", 18))
        self.lbl_soru.pack(pady=50)

        # Ses Butonu
        self.btn_ses = YuvarlakButon(self, "🔊", self.sesi_cal, genislik=80, yukseklik=80)
        self.btn_ses.pack(pady=30)

        # 3. Durum Bilgisi (Dosya yoksa uyarmak için)
        self.lbl_bilgi = tk.Label(self, text="", bg="#A2C5D8", fg="red", font=("Arial", 12))
        self.lbl_bilgi.pack()

        # lbl oluştuktan sonra pygame durumunu bildir
        if pygame is None:
            self.pygame_available = False
            self.lbl_bilgi.config(text="Ses için pygame yüklü değil. Terminalde: pip install pygame", fg="red")
        else:
            self.pygame_available = True
            try:
                if not pygame.get_init():
                    pygame.init()
                if not pygame.mixer.get_init():
                    pygame.mixer.init()
            except Exception as e:
                # pygame başlatılamazsa durumu bildir ve ses fonksiyonunu devre dışı bırak
                self.pygame_available = False
                self.lbl_bilgi.config(text=f"Pygame başlatılamadı: {e}", fg="red")

        # 4. Şıklar Alanı
        self.siklar_frame = tk.Frame(self, bg="#A2C5D8")
        self.siklar_frame.pack(pady=20)

        self.soru_yukle()

    def soru_yukle(self):
        if self.su_anki_soru_no >= len(self.sorular):
            # Sorular bittiğinde önce puanı hesaplayıp kaydet
            self.testi_bitir_ve_kaydet()
            # Temizle: şıkları kaldır ve ses butonunu devre dışı bırak
            for widget in self.siklar_frame.winfo_children():
                widget.destroy()
            try:
                self.btn_ses.config(state="disabled")
            except Exception:
                pass
            self.lbl_soru.config(text="Test tamamlandı.")
            return

        soru = self.sorular[self.su_anki_soru_no]
        self.lbl_soru.config(text=soru["soru"])
        self.lbl_bilgi.config(text="") # Hata mesajını temizle

        # ŞIKLARI OLUŞTUR
        for widget in self.siklar_frame.winfo_children():
            widget.destroy()

        secenekler = soru["siklar"].copy()
        random.shuffle(secenekler)

        for secenek in secenekler:
            YuvarlakButon(self.siklar_frame, metin=secenek, genislik=100, yukseklik=60,
                         komut=lambda s=secenek: self.kontrol_et(s)).pack(side="left", padx=20)

    # Yerel ses dosyasını çalma fonksiyonu
    def sesi_cal(self):
        dosya_adi = self.sorular[self.su_anki_soru_no]["ses_dosyasi"]
        dosya_yolu = f"assets/{dosya_adi}" # assets klasörüne bakar

        if not getattr(self, "pygame_available", False):
            # Kullanıcıyı ses için pygame'in eksikliği hakkında bilgilendir
            try:
                self.lbl_bilgi.config(text="Ses oynatılamıyor: pygame yüklü değil.")
            except Exception:
                pass
            return

        if os.path.exists(dosya_yolu):
            try:
                # Varsa eski çalanı durdur
                if pygame.mixer.music.get_busy():
                    pygame.mixer.music.stop()
                # Bazı pygame sürümlerinde unload fonksiyonu mevcut olabilir
                if hasattr(pygame.mixer.music, "unload"):
                    pygame.mixer.music.unload()

                # Yeni dosyayı yükle ve çal
                pygame.mixer.music.load(dosya_yolu)
                pygame.mixer.music.play()
            except Exception as e:
                self.lbl_bilgi.config(text=f"Ses Hatası: {e}", fg="red")
        else:
            self.lbl_bilgi.config(text=f"DOSYA BULUNAMADI: {dosya_adi}", fg="red")

    def kontrol_et(self, secilen_cevap):
        # Eğer test sona ermiş veya indeks dışındaysa girişi yoksay
        if self.su_anki_soru_no >= len(self.sorular):
            return

        dogru_cevap = self.sorular[self.su_anki_soru_no]["dogru"]
        # Yanlış yaptıysa sayacı artır
        if secilen_cevap != dogru_cevap:
            self.yanlis_sayisi += 1
            # Hatayı kaydet
            hata_mesaji = f"Dosya: {self.sorular[self.su_anki_soru_no]['ses_dosyasi']} -> Öğrenci '{secilen_cevap}' dedi. (Doğrusu: {dogru_cevap})"
            self.hata_kayitlari.append(hata_mesaji)

        # İleriye geç
        self.su_anki_soru_no += 1

        # Soru geçmeden önce sesi durdur (sadece pygame kullanılabiliyorsa)
        if getattr(self, "pygame_available", False):
            try:
                if pygame.mixer.music.get_busy():
                    pygame.mixer.music.stop()
                if hasattr(pygame.mixer.music, "unload"):
                    pygame.mixer.music.unload()
            except Exception:
                pass
        self.soru_yukle()

    def testi_bitir_ve_kaydet(self):
        # FORMÜL: (Yanlış Sayısı / Toplam Soru) * Katsayı
        toplam_soru = len(self.sorular)
        if toplam_soru > 0:
            risk_puani = (self.yanlis_sayisi / toplam_soru) * self.katsayi
        else:
            risk_puani = 0
            
        # Veritabanına kaydet
        if self.yonetici.aktif_ogrenci_no:
            self.yonetici.veri_yoneticisi.puan_guncelle(self.yonetici.aktif_ogrenci_no, "fonoloji", risk_puani)
            
        self.yonetici.veri_yoneticisi.rapor_dosyasina_isles(
                self.yonetici.aktif_ogrenci_no,
                "FONOLOJİ (İŞİTSEL) TESTİ",
                risk_puani,
                self.hata_kayitlari,
                toplam_soru,         
                self.yanlis_sayisi
            )
        
        self.yonetici.siradaki_teste_gec()

    # Testten çıkma fonksiyonu
    # Testten_cik metodunu silmeyip, "Override" (Ezme) yapıyoruz:
    def testten_cik(self):
        if getattr(self, "pygame_available", False):
            try:
                if pygame.mixer.music.get_busy():
                    pygame.mixer.music.stop()
                if hasattr(pygame.mixer.music, "unload"):
                    pygame.mixer.music.unload()
            except Exception:
                pass
        # İşimiz bitince Atadaki standart çıkış işlemini çağırıyoruz
        super().testten_cik()

# UYGULAMAYI BAŞLAT
if __name__ == "__main__":
    # Döngüsel içe aktarmayı önlemek için burada içe aktarılmalıdır
    from ana3 import DisleksiUygulamasi
    app = DisleksiUygulamasi()
    app.mainloop()