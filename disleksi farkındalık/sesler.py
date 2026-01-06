# Fonoloji 2 testleri (ses sayma)

import tkinter as tk
import random
import os
from siniflar_ve_moduller import YuvarlakButon, TemelTest
from PIL import Image, ImageTk

class SeslerTesti(TemelTest):
    def __init__(self, ebeveyn, yonetici):
        super().__init__(ebeveyn, yonetici, katsayi=3.0)
        
        # SORU HAVUZU
        self.sorular = [
            {
                "resim": "elma.png",      
                "soru": "Görseldeki varlık kaç sesten/harften oluşuyor?",
                "dogru": "4",
                "siklar": ["2", "3", "4"]
            },
            {
                "resim": "köpek.png",
                "soru": "Görseldeki varlık kaç sesten/harften oluşuyor?",
                "dogru": "5",
                "siklar": ["4", "5", "6"]
            },
            {
                "resim": "ev.png",
                "soru": "Görseldeki varlık kaç sesten/harften oluşuyor?",
                "dogru": "2",
                "siklar": ["2", "3", "1"]
            },
        ]

        # ARAYÜZ
        # 1. Soru Metni
        self.lbl_soru = tk.Label(self, text="...", bg="#A2C5D8", font=("Arial", 18))
        self.lbl_soru.pack(pady=(50,20))

        # 2. Resim Alanı
        # Resmi tutacak bir Label. Başlangıçta boş.
        self.lbl_resim = tk.Label(self, text="[Resim Yükleniyor...]", bg="#A2C5D8", font=("Arial", 20, "bold"), fg="#2C3E50")
        self.lbl_resim.pack(pady=15)

        # 3. Şıklar Alanı (Butonlar buraya gelecek)
        self.siklar_frame = tk.Frame(self, bg="#A2C5D8")
        self.siklar_frame.pack(pady=20)

        # İlk soruyu yükle
        self.soru_yukle()

    def soru_yukle(self):
        # Sorular bittiyse testi bitir ve diğer aşamaya geç
        if self.su_anki_soru_no >= len(self.sorular):
            self.testi_bitir_ve_kaydet()
            return

        soru = self.sorular[self.su_anki_soru_no]
        
        # Soru Metnini Güncelle
        self.lbl_soru.config(text=soru["soru"])

        # RESİM YÜKLEME
        resim_yolu = f"assets/{soru['resim']}" # assets klasörüne bakar
        
        if os.path.exists(resim_yolu):
            try:
                # 1. Resmi Pillow ile aç
                pil_resim = Image.open(resim_yolu)
                
                # 2. Boyutlandır (Kaliteyi koruyarak: LANCZOS filtresi)
                # Maksimum 300x300 piksel olsun ama oranı bozulmasın
                pil_resim.thumbnail((300, 300), Image.LANCZOS)
                
                # 3. Tkinter formatına çevir
                self.tk_resim = ImageTk.PhotoImage(pil_resim)
                
                self.lbl_resim.config(image=self.tk_resim, text="")
            except Exception as e:
                self.lbl_resim.config(image="", text=f"HATA: {soru['resim']} açılamadı")
        else:
            # Resim yoksa dosya adını yazı olarak göster
            self.lbl_resim.config(image="", text=f"[RESİM EKSİK: {soru['resim']}]")

        # ŞIKLARI OLUŞTUR
        # Önce eski butonları temizle
        for widget in self.siklar_frame.winfo_children():
            widget.destroy()

        # Şıkları karıştır
        secenekler = soru["siklar"].copy()
        random.shuffle(secenekler)

        # Butonları diz
        for secenek in secenekler:
            YuvarlakButon(self.siklar_frame, metin=secenek, genislik=100, yukseklik=60,
                         arkaplan_rengi="#5184B1",
                         komut=lambda s=secenek: self.kontrol_et(s)).pack(side="left", padx=20)

    def kontrol_et(self, secilen_cevap):
        dogru_cevap = self.sorular[self.su_anki_soru_no]["dogru"]

        if secilen_cevap != dogru_cevap:
            self.yanlis_sayisi += 1
            # Hatayı kaydet
            hata_mesaji = f"Resim: {self.sorular[self.su_anki_soru_no]['resim']} -> Seçilen: {secilen_cevap} (Doğrusu: {dogru_cevap})"
            self.hata_kayitlari.append(hata_mesaji)

        self.su_anki_soru_no += 1
        self.soru_yukle()    

    def testi_bitir_ve_kaydet(self):
        # FORMÜL: (Yanlış / Toplam) * Katsayı
        toplam_soru = len(self.sorular)
        risk_puani = (self.yanlis_sayisi / toplam_soru) * self.katsayi if toplam_soru > 0 else 0
        
        if self.yonetici.aktif_ogrenci_no:
            # Puanı JSON veritabanına kaydet
            self.yonetici.veri_yoneticisi.puan_guncelle(self.yonetici.aktif_ogrenci_no, "sesler", risk_puani)

            self.yonetici.veri_yoneticisi.rapor_dosyasina_isles(
                self.yonetici.aktif_ogrenci_no,
                "FONOLOJİ 2 TESTİ",
                risk_puani,
                self.hata_kayitlari,
                toplam_soru,         
                self.yanlis_sayisi
            )

        self.yonetici.siradaki_teste_gec()

# UYGULAMAYI BAŞLAT
if __name__ == "__main__":
    # Döngüsel içe aktarmayı önlemek için burada içe aktarılmalıdır
    from ana3 import DisleksiUygulamasi
    app = DisleksiUygulamasi()
    app.mainloop()