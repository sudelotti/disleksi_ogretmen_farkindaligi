# Heceleme testleri

import tkinter as tk
import random
from siniflar_ve_moduller import YuvarlakButon, TemelTest

class HecelemeTesti(TemelTest):
    def __init__(self, ebeveyn, yonetici):
        super().__init__(ebeveyn, yonetici, katsayi=2.0)
        
        # SORU HAVUZU
        self.sorular = [
            {
                "kelime": "KİTAP", 
                "dogru": ["Kİ", "TAP"], 
                "yanlis": ["KİT", "K", "AP", "TA", "İT"]
            },
            {
                "kelime": "ARABA", 
                "dogru": ["A", "RA", "BA"], 
                "yanlis": ["AR", "AB", "ABA", "RAB", "ARA"]
            },
            {
                "kelime": "ALİ", 
                "dogru": ["A", "Lİ"], 
                "yanlis": ["L", "İ", "ALİ", "AL"]
            },
            {
                "kelime": "OKUL", 
                "dogru": ["O", "KUL"], 
                "yanlis": ["OK", "UL", "KU", "OL"]
            },
            {
                "kelime": "EV", 
                "dogru": ["EV"], 
                "yanlis": ["E", "V"]
            },
        ]
        
        self.secilen_heceler = [] # Kullanıcının tıkladığı heceler burada birikecek

        # Hedef Kelime (Örn: KALEM)
        self.lbl_kelime = tk.Label(self, text="...", bg="#A2C5D8",
                                    fg="#2C3E50", font=("Arial", 40, "bold"))
        self.lbl_kelime.pack(pady=40)
        
        # Kullanıcının Oluşturduğu Cevap (Örn: KA - LEM)
        self.lbl_cevap_alani = tk.Label(self, text="?", bg="white", fg="black", width=20, font=("Arial", 24))
        self.lbl_cevap_alani.pack(pady=10, ipady=10)

        # Hecelerin Duracağı Alan (Butonlar buraya gelecek)
        self.hece_frame = tk.Frame(self, bg="#A2C5D8")
        self.hece_frame.pack(pady=20)

        # Alt Butonlar (Temizle ve İleri)
        alt_frame = tk.Frame(self, bg="#A2C5D8")
        alt_frame.pack(side="bottom", pady=30)

        # Temizle Butonu (Yanlış seçerse silsin diye)
        YuvarlakButon(alt_frame, metin="Temizle", genislik=150, yukseklik=50, 
                      arkaplan_rengi="#ac3224",
                      komut=self.cevap_temizle).pack(side="left", pady=20, padx=10)

        # İleri Butonu
        YuvarlakButon(alt_frame, metin="İleri", genislik=150, yukseklik=50, 
                      arkaplan_rengi="#5184B1",
                      komut=self.sonraki_soruya_gec).pack(side="left", pady=20, padx=10)

        # Oyunu Başlat
        self.soru_yukle()

    def soru_yukle(self):
        # Eğer sorular bittiyse sonraki teste geç
        if self.su_anki_soru_no >= len(self.sorular): 
            self.testi_bitir_ve_kaydet()
            return

        # Değişkenleri sıfırla
        self.secilen_heceler = []
        self.lbl_cevap_alani.config(text="...")
        
        # Mevcut soruyu al
        soru = self.sorular[self.su_anki_soru_no]
        self.lbl_kelime.config(text=soru["kelime"])

        # Şıkları oluştur (Doğru + Yanlış heceleri birleştir)
        tum_secenekler = soru["dogru"] + soru["yanlis"]
        random.shuffle(tum_secenekler) # Karıştır ki yeri ezberlenmesin

        # Eski butonları temizle
        for widget in self.hece_frame.winfo_children():
            widget.destroy()

        # Yeni butonları ekrana diz (Yan yana sığdıkça alt satıra geçsin)
        satir = 0
        sutun = 0
        max_sutun = 4 # Yan yana en fazla kaç buton olsun?

        for hece in tum_secenekler:
            tk.Button(self.hece_frame, text=hece, font=("Arial", 16),
                     bg="white", width=6, height=2,
                     # Lambda ile hangi heceye tıklandığını fonksiyona gönderiyoruz
                     command=lambda h=hece: self.hece_sec(h)).grid(row=satir,
                                                             column=sutun, padx=10, pady=10)
            
            sutun += 1
            if sutun >= max_sutun:
                sutun = 0
                satir += 1

    def hece_sec(self, hece):
        # Tıklanan heceyi listeye ekle
        self.secilen_heceler.append(hece)
        # Ekranda göster (Aralara çizgi koyarak)
        gosterilecek_yazi = " - ".join(self.secilen_heceler)
        self.lbl_cevap_alani.config(text=gosterilecek_yazi)

    def cevap_temizle(self):
        self.secilen_heceler = []
        self.lbl_cevap_alani.config(text="...")

    def sonraki_soruya_gec(self):
        soru = self.sorular[self.su_anki_soru_no]

        # Yanlış kontrolü
        if self.secilen_heceler != soru["dogru"]:
            self.yanlis_sayisi += 1
            # Hata kaydı
            yapilan = "-".join(self.secilen_heceler)
            dogrusu = "-".join(soru["dogru"])
            self.hata_kayitlari.append(f"Kelime: {soru['kelime']} -> Yapılan: {yapilan} (Doğrusu: {dogrusu})")
            
        # Doğru da olsa yanlış da olsa bir sonrakine geç
        self.su_anki_soru_no += 1
        self.soru_yukle()

    def testi_bitir_ve_kaydet(self):
        # FORMÜL: (Yanlış / Toplam) * Katsayı
        toplam_soru = len(self.sorular)
        risk_puani = (self.yanlis_sayisi / toplam_soru) * self.katsayi if toplam_soru > 0 else 0
        
        if self.yonetici.aktif_ogrenci_no:
            self.yonetici.veri_yoneticisi.puan_guncelle(self.yonetici.aktif_ogrenci_no, "heceleme", risk_puani)
            # Raporu kaydet
            self.yonetici.veri_yoneticisi.rapor_dosyasina_isles(
                self.yonetici.aktif_ogrenci_no,
                "HECELEME TESTİ",
                risk_puani,
                self.hata_kayitlari,
                toplam_soru,         
                self.yanlis_sayisi
            )

        self.yonetici.siradaki_teste_gec()
    
    def testi_sifirla(self):
        # 1. Bu sınıfa özel temizlikleri yap
        self.secilen_heceler = [] 
        self.lbl_cevap_alani.config(text="...")
        
        # 2. Geri kalan genel temizliği (sayaçları sıfırlamayı) Ata sınıfa bırak
        super().testi_sifirla()

# UYGULAMAYI BAŞLAT
if __name__ == "__main__":
    # Döngüsel içe aktarmayı önlemek için burada içe aktarılmalıdır
    from ana3 import DisleksiUygulamasi
    app = DisleksiUygulamasi()
    app.mainloop()