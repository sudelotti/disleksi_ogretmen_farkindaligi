# Sıralama testleri

import tkinter as tk
import random
import os
from siniflar_ve_moduller import YuvarlakButon, TemelTest
from PIL import Image, ImageTk


class SiralamaTesti(TemelTest):
    def __init__(self, ebeveyn, yonetici):
        super().__init__(ebeveyn, yonetici, katsayi=2.0)
        
        # SORU HAVUZU
        self.sorular = [
            # TÜR 1: METİN TAMAMLAMA (Günler, Aylar, Sayılar)
            {
                "tur": "metin",
                "soru": "Sıradaki boşluğa hangisi gelmelidir?",
                "icerik": "Pazartesi ➔ Salı ➔ Çarşamba ➔ ...?...",
                "dogru": "Perşembe",
                "siklar": ["Cuma", "Perşembe", "Pazar"]
            },
            {
                "tur": "metin",
                "soru": "Sıradaki boşluğa hangisi gelmelidir?",
                "icerik": "Mart ➔ Nisan ➔ Mayıs ➔ ...?...",
                "dogru": "Haziran",
                "siklar": ["Temmuz", "Haziran", "Ağustos"]
            },
            {
                "tur": "metin",
                "soru": "Örüntüde sıradaki sayı kaçtır?",
                "icerik": "5 - 7 - 9 - ...?...",
                "dogru": "11",
                "siklar": ["10", "11", "12"]
            },
            {
                "tur": "metin",
                "soru": "Örüntüde sıradaki sayı kaçtır?",
                "icerik": "2 - 3 - 4 - ...?...",
                "dogru": "5",
                "siklar": ["1", "5", "6"]
            },

            # TÜR 2: GÖRSEL SIRALAMA (Oluş Sırası)
            # Resim isimleri: 1.png, 2.png, 3.png, 4.png (assets klasöründe olmalı)
            {
                "tur": "gorsel_siralama",
                "soru": "Görselleri zaman sırasına göre seç.",
                # Doğru sıralama listesi (Dosya adları)
                "dogru_sira": ["1.png", "2.png", "3.png", "4.png"] 
            },
            # Resim isimleri: yumurta.png, tırtıl.png, koza.png, kelebek.png (assets klasöründe olmalı)
            {
                "tur": "gorsel_siralama",
                "soru": "Kelebeğin oluşum evrelerini sıraya diz.",
                "dogru_sira": ["yumurta.png", "tırtıl.png", "koza.png", "kelebek.png"] 
            },
            
            # TÜR 3: YÖN BULMA (Kroki)
            {
                "tur": "yon_bulma",
                "soru": "Adamı işaretli yere götürmek için oklara sırasıyla dokun. (5 adım)",
                "resim": "kroki.png",
                "dogru_yol": ["sag", "asagi", "sol", "asagi", "sag"] 
            }
        ]
        
        self.secilen_resim_sirasi = [] # Görsel sorusu için
        self.secilen_yonler = [] # Yön sorusu için

        # ARAYÜZ
        self.lbl_soru = tk.Label(self, text="...", bg="#A2C5D8", font=("Arial", 19))
        self.lbl_soru.pack(pady=50)

        # İçerik Alanı (Değişken olacak)
        self.icerik_frame = tk.Frame(self, bg="#A2C5D8")
        self.icerik_frame.pack(expand=True, fill="both", pady=10)

        # Oyunu Başlat
        self.soru_yukle()

    def soru_yukle(self):
        # Temizlik
        for widget in self.icerik_frame.winfo_children():
            widget.destroy()
        self.secilen_resim_sirasi = []
        self.secilen_yonler = []

        if self.su_anki_soru_no >= len(self.sorular):
            self.testi_bitir_ve_kaydet()
            return

        soru = self.sorular[self.su_anki_soru_no]
        self.lbl_soru.config(text=soru["soru"])

        # Türüne göre ekranı çiz
        if soru["tur"] == "metin":
            self.yukle_metin_sorusu(soru)
        elif soru["tur"] == "gorsel_siralama":
            self.yukle_gorsel_siralama(soru)
        elif soru["tur"] == "yon_bulma":
            self.yukle_yon_bulma(soru)

    # TÜR 1: METİN SORUSU
    def yukle_metin_sorusu(self, soru):
        # 1. Örüntü Metni
        tk.Label(self.icerik_frame, text=soru["icerik"], 
                 font=("Arial", 30, "bold"), bg="#A2C5D8", fg="#2C3E50").pack(pady=30)
        
        # 2. Şıklar
        btn_frame = tk.Frame(self.icerik_frame, bg="#A2C5D8")
        btn_frame.pack(pady=20)
        
        secenekler = soru["siklar"].copy()
        random.shuffle(secenekler)
        
        for sec in secenekler:
            YuvarlakButon(btn_frame, metin=sec, genislik=150, yukseklik=60,
                          arkaplan_rengi="#5184B1",
                          komut=lambda s=sec: self.cevap_kontrol_metin(s)).pack(side="left", padx=15)

    def cevap_kontrol_metin(self, secilen):
        dogru = self.sorular[self.su_anki_soru_no]["dogru"]
        if secilen != dogru:
            self.yanlis_sayisi += 1

            self.hata_kayitlari.append(f"Soru: {self.sorular[self.su_anki_soru_no]['icerik']} -> Seçilen: {secilen} (Doğrusu: {dogru})")
        
        self.su_anki_soru_no += 1
        self.soru_yukle()

    # TÜR 2: GÖRSEL SIRALAMA
    def yukle_gorsel_siralama(self, soru):
        # Resimlerin listesini al ve karıştır
        resimler = soru["dogru_sira"].copy()
        random.shuffle(resimler)
        
        # Resimlerin gösterileceği alan
        resim_alani = tk.Frame(self.icerik_frame, bg="#A2C5D8")
        resim_alani.pack(pady=20)

        # Resimleri buton olarak ekle
        for dosya_adi in resimler:
            frame_kutu = tk.Frame(resim_alani, bg="#A2C5D8", padx=10)
            frame_kutu.pack(side="left")

            # Resim Yükleme (Yoksa Yazı Göster)
            yol = f"assets/{dosya_adi}"
            if os.path.exists(yol):
                try:
                    # 1. Pillow ile aç
                    pil_img = Image.open(yol)
                    # 2. Buton için uygun boyuta getir (Örn: 300x300)
                    pil_img.thumbnail((200, 200), Image.LANCZOS)
                    # 3. Tkinter resmine çevir
                    img = ImageTk.PhotoImage(pil_img)

                    btn = tk.Button(frame_kutu, image=img, bg="white",
                                    command=lambda d=dosya_adi, b=frame_kutu: self.resim_sec(d, b))
                    btn.image = img # Çöp toplayıcı (Garbage Collector) silmesin diye referans tutuyoruz
                    btn.pack()
                except:
                     tk.Label(frame_kutu, text="Hata").pack()
            else:
                btn = tk.Button(frame_kutu, text=f"{dosya_adi}\n(Resim Yok)", width=15, height=5, bg="white",
                                command=lambda d=dosya_adi, b=frame_kutu: self.resim_sec(d, b))
                btn.pack()

        YuvarlakButon(self.icerik_frame, metin="Baştan Seç", 
                      arkaplan_rengi="#ac3224", 
                      komut=self.soru_yukle).pack(side="bottom", pady=30)
    
    def cevap_temizle(self):
        self.secilen_heceler = []
        self.lbl_cevap_alani.config(text="...")

    def resim_sec(self, dosya_adi, buton_frame):
        # Aynı resme tekrar tıklamayı engellemek için kontrol edebiliriz
        if dosya_adi in self.secilen_resim_sirasi:
            return 

        self.secilen_resim_sirasi.append(dosya_adi)
        
        # Görsel olarak seçildiğini belli et (Örn: Çerçeve rengi değişsin veya etiket koy)
        tk.Label(buton_frame, text=f"{len(self.secilen_resim_sirasi)}. Sırada", bg="yellow").pack()

        # Eğer tüm resimler seçildiyse kontrol et
        dogru_liste = self.sorular[self.su_anki_soru_no]["dogru_sira"]
        if len(self.secilen_resim_sirasi) == len(dogru_liste):
            if self.secilen_resim_sirasi != dogru_liste:
                self.yanlis_sayisi += 1

                self.hata_kayitlari.append(f"Görsel Sıralama Yanlış: {self.sorular[self.su_anki_soru_no]['soru']}")
            
            self.after(500, self.sonraki_soruya_gec)

    # TÜR 3: YÖN BULMA (KROKİ)
    def yukle_yon_bulma(self, soru):
        # 1. SOL PANEL (Kroki için) -> Sola yasla, tüm alanı kapla
        sol_frame = tk.Frame(self.icerik_frame, bg="#A2C5D8")
        sol_frame.pack(side="left", expand=True, fill="both", padx=20)

        # 2. SAĞ PANEL (Tuşlar için) -> Sağa yasla, tüm alanı kapla
        sag_frame = tk.Frame(self.icerik_frame, bg="#A2C5D8")
        sag_frame.pack(side="right", expand=True, fill="both", padx=20)
        
        # Sol taraf / Kroki Resmi
        yol = f"assets/{soru['resim']}"
        if os.path.exists(yol):
            try:
                # 1. Pillow ile aç
                pil_img = Image.open(yol)
                # 2. Harita boyutuna getir (Örn: 400x400)
                pil_img.thumbnail((400, 400), Image.LANCZOS)
                # 3. Tkinter resmine çevir
                img = ImageTk.PhotoImage(pil_img)
                
                lbl_img = tk.Label(sol_frame, image=img, bg="#A2C5D8")
                lbl_img.image = img
                lbl_img.pack(expand=True) # Ortala
            except:
                 tk.Label(sol_frame, text="Resim Hatası").pack(expand=True)
        else:
            tk.Label(sol_frame, text=f"[KROKİ RESMİ BURAYA: {soru['resim']}]", 
                     bg="white", width=40, height=10).pack(expand=True)

        # Sağ taraf / Tuşlar ve Butonlar
        # Tuşları ve butonları dikeyde ortalamak için bir "container"
        center_sag = tk.Frame(sag_frame, bg="#A2C5D8")
        center_sag.pack(expand=True)
        
        # Ok Tuşları
        oklar_frame = tk.Frame(center_sag, bg="#A2C5D8")
        oklar_frame.pack(pady=10)

        # Ok Butonları (Grid ile yerleştirelim ki klavye gibi dursun)
        #       Yukarı
        #  Sol  Aşağı  Sağ
        
        btn_yukari = tk.Button(oklar_frame, text="🡹", font=("Arial", 20), width=4, command=lambda: self.yon_ekle("yukari"))
        btn_yukari.grid(row=0, column=1, padx=5, pady=5)

        btn_sol = tk.Button(oklar_frame, text="🡸", font=("Arial", 20), width=4, command=lambda: self.yon_ekle("sol"))
        btn_sol.grid(row=1, column=0, padx=5, pady=5)

        btn_asagi = tk.Button(oklar_frame, text="🡻", font=("Arial", 20), width=4, command=lambda: self.yon_ekle("asagi"))
        btn_asagi.grid(row=1, column=1, padx=5, pady=5)

        btn_sag = tk.Button(oklar_frame, text="🡺", font=("Arial", 20), width=4, command=lambda: self.yon_ekle("sag"))
        btn_sag.grid(row=1, column=2, padx=5, pady=5)

        # Seçilen Yol Göstergesi
        self.lbl_yol = tk.Label(center_sag, text="Yol: Başlangıç", bg="#A2C5D8", font=("Arial", 12))
        self.lbl_yol.pack(pady=5)

        # Alt Butonlar (Yan yana düzgün durması için ayrı frame)
        aksiyon_frame = tk.Frame(center_sag, bg="#A2C5D8")
        aksiyon_frame.pack(pady=20)

        # Temizle Butonu
        YuvarlakButon(aksiyon_frame, metin="Temizle", genislik=150, yukseklik=50, 
                     arkaplan_rengi="#ac3224", 
                     komut=self.soru_yukle).pack(side="left", padx=10)

        # Kontrol Et Butonu
        YuvarlakButon(aksiyon_frame, metin="Git", genislik=150, yukseklik=50,
                     arkaplan_rengi="#5184B1",
                     komut=self.cevap_kontrol_yon).pack(side="left", pady=10 , padx=10)

    def yon_ekle(self, yon):
        self.secilen_yonler.append(yon)
        # Ok işaretine çevirip ekranda gösterelim
        semboller = {"yukari": "🡹", "asagi": "🡻", "sag": "🡺", "sol": "🡸"}
        yol_str = " ".join([semboller[y] for y in self.secilen_yonler])
        self.lbl_yol.config(text=f"Yol: {yol_str}")

    def cevap_kontrol_yon(self):
        dogru_yol = self.sorular[self.su_anki_soru_no]["dogru_yol"]
        if self.secilen_yonler != dogru_yol:
            self.yanlis_sayisi += 1

            self.hata_kayitlari.append(f"Yön Hatası: {self.sorular[self.su_anki_soru_no]['soru']} -> Seçilen: {(self.secilen_yonler)} (Doğrusu: sağ(🡺), aşağı(🡻), sol(🡸), aşağı(🡻), sağ(🡺))")
        
        self.sonraki_soruya_gec()

    def sonraki_soruya_gec(self):
        self.su_anki_soru_no += 1
        self.soru_yukle()

    def testi_bitir_ve_kaydet(self):
        # FORMÜL: (Yanlış / Toplam) * Katsayı
        toplam_soru = len(self.sorular)
        risk_puani = (self.yanlis_sayisi / toplam_soru) * self.katsayi if toplam_soru > 0 else 0
        
        if self.yonetici.aktif_ogrenci_no:
            self.yonetici.veri_yoneticisi.puan_guncelle(self.yonetici.aktif_ogrenci_no, "siralama", risk_puani)

            self.yonetici.veri_yoneticisi.rapor_dosyasina_isles(
                self.yonetici.aktif_ogrenci_no,
                "SIRALAMA TESTİ",
                risk_puani,
                self.hata_kayitlari,
                toplam_soru,         
                self.yanlis_sayisi
            )

        self.yonetici.siradaki_teste_gec()    

    def testi_sifirla(self):
        self.secilen_resim_sirasi = []
        self.secilen_yonler = []
        super().testi_sifirla()

# UYGULAMAYI BAŞLAT
if __name__ == "__main__":
    # Döngüsel içe aktarmayı önlemek için burada içe aktarılmalıdır
    from ana3 import DisleksiUygulamasi
    app = DisleksiUygulamasi()
    app.mainloop()