# Hızlı okuma ve okuduğunu anlama testleri

import tkinter as tk
import time
from siniflar_ve_moduller import YuvarlakButon, TemelTest

class HizliOkumaTesti(TemelTest):
    def __init__(self, ebeveyn, yonetici):
        super().__init__(ebeveyn, yonetici, katsayi=1.0)
        self.yonetici = yonetici

        # Okunacak metin
        self.okuma_metni = "Ali sabah odasını topladı.\nAyşe resim çizmeyi çok sever."

        # SORU HAVUZU
        self.sorular = [
            {
                "soru": "Ali odasını ne zaman topladı?",
                "siklar": ["Sabah", "Öğle", "Akşam"],
                "dogru": "Sabah"
            },
            {
                "soru": "Ayşe ne yapmayı çok sever?",
                "siklar": ["Yemek yapmak", "Resim Yapmak", "Yüzmek"],
                "dogru": "Resim Yapmak"
            }
        ]

        self.okuma_suresi = 0
        self.baslangic_zamani = 0

        # ARAYÜZ ELEMANLARI
        # İçerik Alanı
        self.icerik_frame = tk.Frame(self, bg="#A2C5D8")
        self.icerik_frame.pack(expand=True, fill="both", padx=60, pady=20)

        # Testi Başlat (Metni Göster)
        self.metni_goster()

    def metni_goster(self):
        # Önce ekranı temizle
        for widget in self.icerik_frame.winfo_children():
            widget.destroy()

        # Metni Ekrana Yaz
        lbl_metin = tk.Label(self.icerik_frame, text=self.okuma_metni, 
                             bg="#A2C5D8", fg="#2C3E50",
                             font=("Arial", 28, "bold"), justify="center", wraplength=800)
        lbl_metin.pack(pady=(180, 40))

        # İleri Butonu
        YuvarlakButon(self.icerik_frame, metin="İleri", genislik=250, yukseklik=60,
                                  arkaplan_rengi="#5184B1",
                                  komut=self.okumayi_bitir).pack(side="bottom", pady=30)

        # Sayacı Başlat
        self.baslangic_zamani = time.time()

    def okumayi_bitir(self):
        # Süreyi Hesapla
        bitis_zamani = time.time()
        self.okuma_suresi = bitis_zamani - self.baslangic_zamani
        
        # Sorulara Geç
        self.soru_yukle()

    def soru_yukle(self):
        # Sorular bittiyse testi bitir
        if self.su_anki_soru_no >= len(self.sorular): 
            self.testi_bitir_ve_kaydet()
            return

        # Ekranı temizle
        for widget in self.icerik_frame.winfo_children():
            widget.destroy()

        soru_verisi = self.sorular[self.su_anki_soru_no]

        # Soruyu Yaz
        lbl_soru = tk.Label(self.icerik_frame, text=soru_verisi["soru"],
                            bg="#A2C5D8", fg="#2C3E50",
                            font=("Arial", 24, "bold"), wraplength=800)
        lbl_soru.pack(pady=(180, 25))

        # Şıkları Yaz (Butonlar)
        siklar_frame = tk.Frame(self.icerik_frame, bg="#A2C5D8")
        siklar_frame.pack(pady=20)

        for secenek in soru_verisi["siklar"]:
            YuvarlakButon(siklar_frame, metin=secenek, genislik=230, 
                         yukseklik=60, arkaplan_rengi="#5184B1",
                         komut=lambda s=secenek: self.kontrol_et(s)).pack(side="left", padx=15)

    def kontrol_et(self, secilen_sik):
        dogru_cevap = self.sorular[self.su_anki_soru_no]["dogru"]
        
        # Yanlış Kontrolü
        if secilen_sik != dogru_cevap:
            self.yanlis_sayisi += 1
            # Hatayı kaydet
            hata_cumlesi = f"Öğrenci '{secilen_sik}' dedi. (Doğrusu: {dogru_cevap})"
            self.hata_kayitlari.append(hata_cumlesi)
        
        # Diğer soruya geç
        self.su_anki_soru_no += 1
        self.soru_yukle()

    def testi_bitir_ve_kaydet(self):
        # FORMÜL: (Yanlış / Toplam) * Katsayı
        toplam_soru = len(self.sorular)
        risk_puani = (self.yanlis_sayisi / toplam_soru) * self.katsayi if toplam_soru > 0 else 0
        # Puanı JSON'a kaydet
        if self.yonetici.aktif_ogrenci_no:
            self.yonetici.veri_yoneticisi.puan_guncelle(self.yonetici.aktif_ogrenci_no, "hizli_okuma", risk_puani)
        
        #  Detaylı raporu txt dosyasına kaydet
        self.yonetici.veri_yoneticisi.rapor_dosyasina_isles(
                self.yonetici.aktif_ogrenci_no, 
                "HIZLI OKUMA TESTİ", 
                risk_puani,
                self.hata_kayitlari,
                toplam_soru,         
                self.yanlis_sayisi,
                self.okuma_suresi
            )
        
        self.yonetici.siradaki_teste_gec()

    def testi_sifirla(self):
        self.su_anki_soru_no = 0
        self.yanlis_sayisi = 0
        self.hata_kayitlari = [] # Listeyi temizle
        self.okuma_suresi = 0
        self.baslangic_zamani = 0
        # Test sıfırlanınca önce okuma metnini göster
        self.metni_goster()

    # ÇIKIŞ FONKSİYONU
    def testten_cik(self):
        # Yönetici indeksini sıfırla
        self.yonetici.su_anki_index = 0
        # Çıkış yap
        self.yonetici.sayfa_goster("TestlerSayfasi")

# UYGULAMAYI BAŞLAT
if __name__ == "__main__":
    # Döngüsel içe aktarmayı önlemek için burada içe aktarılmalıdır
    from ana3 import DisleksiUygulamasi
    app = DisleksiUygulamasi()
    app.mainloop()