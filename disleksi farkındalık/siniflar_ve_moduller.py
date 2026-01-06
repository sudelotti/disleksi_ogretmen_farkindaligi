# Diğer dosyalardan import edilebilecek sınıflar ve modüller
# Fazla kod tekrarı olmasın diye

import tkinter as tk
import time   # Butona bastığımızdan kısa süre bekleyip butonu eski haline geri getirmek için

# Tkinter butonunu özelleştirmek için Canvas (Tuval) kullanılır
class YuvarlakButon(tk.Canvas):
    def __init__(self, ebeveyn, metin, komut, genislik=200, yukseklik=50, kose_yaricapi=20, arkaplan_rengi="#5184B1", yazi_rengi="white", zemin_rengi="#A2C5D8"):
        
        super().__init__(ebeveyn, width=genislik, height=yukseklik, bg=ebeveyn["bg"], highlightthickness=0)
        
        self.komut = komut # command Türkçe
        
        # Renkler
        self.arkaplan_rengi = arkaplan_rengi
        self.golge_rengi = "#607d8b"
        
        # 1. Gölgeyi çiz
        self.yuvarlak_dikdortgen_ciz(4, 4, genislik, yukseklik, kose_yaricapi, self.golge_rengi)
        
        # 2. Ana butonu çiz
        self.ana_sekil = self.yuvarlak_dikdortgen_ciz(0, 0, genislik-4, yukseklik-4, kose_yaricapi, self.arkaplan_rengi)
        
        # 3. Yazıyı ekle
        self.yazi_nesnesi = self.create_text((genislik-4)/2, (yukseklik-4)/2, text=metin, fill=yazi_rengi, font=("Arial", 20))
        
        # Olayları tanımla
        # <Button-1>: Sol Tık, <Enter>: Mouse Geldi, <Leave>: Mouse Gitti
        self.bind("<Button-1>", self.tiklama_olayi) 
        self.bind("<Enter>", self.uzerine_gelince)    
        self.bind("<Leave>", self.ayrilinca) 

    # Köşeleri yuvarlatılmış dikdörtgen çizen fonksiyon
    def yuvarlak_dikdortgen_ciz(self, x1, y1, x2, y2, r, dolgu_rengi):
        koordinatlar = (x1+r, y1, x1+r, y1, x2-r, y1, x2-r, y1, x2, y1, x2, y1+r, x2, y1+r, 
                        x2, y2-r, x2, y2-r, x2, y2, x2-r, y2, x2-r, y2, x1+r, y2, x1+r, y2, 
                        x1, y2, x1, y2-r, x1, y2-r, x1, y1+r, x1, y1+r, x1, y1)
        return self.create_polygon(koordinatlar, fill=dolgu_rengi, smooth=True)

    def tiklama_olayi(self, olay):
        if self.komut:
            # Tıklama efekti (içeri basılır)
            self.move(self.ana_sekil, 2, 2)
            self.move(self.yazi_nesnesi, 2, 2)
            self.update()

            # 2. Çok kısa bekle (Basılma hissi için)
            time.sleep(0.1)

            # (Yukarı Sola geri götürüyoruz)
            self.move(self.ana_sekil, -2, -2)
            self.move(self.yazi_nesnesi, -2, -2)
            self.update()
            
            self.komut() # Fonksiyonu çalıştır

    def uzerine_gelince(self, olay):
        self.configure(cursor="hand2") # Mouse el şeklini alır
        
    def ayrilinca(self, olay):
        self.configure(cursor="")

# Testlerde kullanılan ortak metotlar için
class TemelTest(tk.Frame):
    def __init__(self, ebeveyn, yonetici, katsayi=1.0):
        super().__init__(ebeveyn, bg="#A2C5D8")
        self.yonetici = yonetici
        self.katsayi = katsayi
        self.su_anki_soru_no = 0
        self.yanlis_sayisi = 0
        self.hata_kayitlari = [] # Hata kayıtları için liste
        
        # Ortak "Çıkış" butonu
        YuvarlakButon(self, "<", self.testten_cik, genislik=40, yukseklik=40, 
                     arkaplan_rengi="#95a5a6").place(x=20, y=20) # Sol üste sabitleme

    def testi_sifirla(self):
        self.su_anki_soru_no = 0
        self.yanlis_sayisi = 0
        self.hata_kayitlari = []
        self.soru_yukle()

    def testten_cik(self):
        self.yonetici.su_anki_index = 0
        self.yonetici.sayfa_goster("TestlerSayfasi")
    
    def soru_yukle(self):
        pass # Alt sınıflar bunu doldurmak zorunda (Abstract Method mantığı)

# Veri yönetimi için sınıf
import json
import os
import time
from datetime import datetime

DOSYA_ADI = "ogrenci_verileri.json"

class VeriYoneticisi:
    def __init__(self):
        self.__veriler = self.verileri_yukle()

    def verileri_yukle(self):
        # Eğer dosya yoksa boş bir sözlük oluştur
        if not os.path.exists(DOSYA_ADI):
            return {}
        try:
            # Dosya varsa onu okuma modunda Türkçe karakterleri destekleyecek şekilde aç
            with open(DOSYA_ADI, "r", encoding="utf-8") as dosya:
                # Dosyadaki yazıları Python'un anlayacağı sözlük formatına çevir ve programa yükle
                return json.load(dosya)
        except:
            return {}
    
    def kaydet(self):
        # Dosyayı yazma modunda aç ki dosyanın içeriği en güncel haliyle yazılsın
        with open(DOSYA_ADI, "w", encoding="utf-8") as dosya:
            # İçinde tutulan tüm bilgileri dosyaya aktar
            json.dump(self.__veriler, dosya, ensure_ascii=False, indent=4) # ensure_ascii=False Türkçe harfleri bozmaması için

    def rapor_dosyasina_isles(self, ogr_no, test_adi, puan, hata_kayitlari, toplam_soru, yanlis_sayisi, okuma_suresi=None):
        
        # Bu fonksiyon öğrenciye özel bir metin belgesi oluşturur veya varsa üzerine ekler.
        # Örnek dosya adı: 12_detayli_rapor.txt
  
        dosya_ismi = f"{ogr_no}_detayli_rapor.txt"

        # o anki tarih-saati dizelere dönüştür 
        tarih = datetime.now().strftime("%d.%m.%Y %H:%M:%S")

        # İstatistik hesaplama
        dogru_sayisi = toplam_soru - yanlis_sayisi
        hata_orani = (yanlis_sayisi / toplam_soru * 100) if toplam_soru > 0 else 0
        
        # Rapor Şablonu
        metin = "\n" + "="*60 + "\n"
        metin += f"TARİH: {tarih}\n"
        metin += f"TEST: {test_adi}\n"
        metin += f"DOĞRU:{dogru_sayisi}  YANLIŞ:{yanlis_sayisi}  HATA ORANI: %{hata_orani:.2f}\n"
        # Eğer süre bilgisi gönderildiyse rapora ekle, gönderilmediyse (None ise) bu satırı atla.
        if okuma_suresi is not None:
            metin += f"OKUMA SÜRESİ: {okuma_suresi:.2f} Saniye\n"
        metin += f"ALINAN RİSK PUANI: {puan:.2f}\n" # 2f örn 2.00, 3.60 için
        metin += "-"*30 + "\n"
        metin += "HATA DETAYLARI:\n"
        
        if not hata_kayitlari:
            metin += " * Tebrikler, hata yapılmadı (Tam Başarı).\n"
        else:
            for hata in hata_kayitlari:
                metin += f" * {hata}\n"
        
        metin += "="*60 + "\n\n"

        # Dosyayı "append" (ekleme) modunda açıyoruz, böylece eskiler silinmez
        with open(dosya_ismi, "a", encoding="utf-8") as f:
            f.write(metin)
    
    def anket_sonucu_isles(self, ogr_no, anket_puani):
        dosya_ismi = f"{ogr_no}_detayli_rapor.txt"
        tarih = datetime.now().strftime("%d.%m.%Y %H:%M:%S")

        # 1. Önce Öğrencinin Toplam Test Risk Puanını Hesaplayalım
        toplam_test_riski = 0
        test_detaylari = ""

        if ogr_no in self.__veriler and "testler" in self.__veriler[ogr_no]:
            t = self.__veriler[ogr_no]["testler"]
            # Testlerin puanlarını topla (Çözülmemişse 0 sayar)
            p1 = t.get("fonoloji", 0)
            p2 = t.get("sesler", 0)
            p3 = t.get("siralama", 0)
            p4 = t.get("heceleme", 0)
            p5 = t.get("hizli_okuma", 0)

            toplam_test_riski = p1 + p2 + p3 + p4 + p5

            test_detaylari += f"   - Fonoloji: {p1:.2f}\n"
            test_detaylari += f"   - Ses Farkındalığı: {p2:.2f}\n"
            test_detaylari += f"   - Sıralama: {p3:.2f}\n"
            test_detaylari += f"   - Heceleme: {p4:.2f}\n"
            test_detaylari += f"   - Hızlı Okuma: {p5:.2f}\n"

        metin = "\n" + "#"*60 + "\n"
        metin += f"SONUÇLAR ({tarih})\n"
        metin += "#"*60 + "\n\n"

        metin += "="*60 + "\n"
        metin += f"1. DİJİTAL TESTLER TOPLAM RİSK PUANI: {toplam_test_riski:.2f} / 11.00\n"
        metin += "-"*40 + "\n"
        metin += test_detaylari
        metin += "-"*40 + "\n" 
        metin += f"2. ÖĞRETMEN GÖZLEM ANKETİ PUANI: {anket_puani}\n"
        metin += "="*60 + "\n"

        # Değerlendirme ve tavsiyeler
        if anket_puani < 88 and toplam_test_riski >= 6.5:
            metin += "\n" + "!"*60 + "\n"
            metin += "🔴 DİKKAT: GİZLİ RİSK / TUTARSIZLIK TESPİTİ 🔴\n"
            metin += "!"*60 + "\n\n"
            metin += "Lütfen dikkat: Öğrenci testlerde yüksek risk puanı almıştır ancak anket sonucu düşük risk göstermektedir.\n\n"
            metin += "Olası Sebepler:\n"
            metin += "* Öğrenci test ortamında farklı performans göstermiş olabilir.\n"
            metin += "* Öğrenci üzerindeki gözlemleriniz yetersiz kalmış olabilir.\n\n"
            metin += "Tavsiyeler:\n"
            metin += "* Test verilerini tekrar gözden geçiriniz.\n"
            metin += "* Öğrenci üzerindeki gözlemlerinize devam ediniz.\n"
            metin += "* Verileri, öğrencinin akademik başarısını ve gözlemlerinizi rehberlik servisiyle birlikte değerlendiriniz.\n"
            metin += "\n" + "!"*60 + "\n\n"
        if anket_puani >= 88 and toplam_test_riski >= 6.5:
            metin += "\n" + "!"*60 + "\n\n"
            metin += "⚠️ SONUÇ: YÜKSEK RİSK GRUBU (DİSLEKSİ ŞÜPHESİ)\n"
            metin += "Öğrenci, belirtilen kriterlerin birçoğunda zorluk yaşamaktadır.\n\n"
            metin += "TAVSİYELER:\n"
            metin += "1. Öğrenci, okul rehberlik servisine (PDR) yönlendirilmelidir.\n"
            metin += "2. Aile ile görüşülerek RAM (Rehberlik Araştırma Merkezi) yönlendirmesi düşünülebilir.\n"
            metin += "3. Sınıf içinde öğrenciye daha fazla zaman tanınmalı ve destekleyici materyaller kullanılmalıdır.\n"
            metin += "\n" + "!"*60 + "\n\n"
        if anket_puani >= 88 and toplam_test_riski < 6.5:
            metin += "\n" + "!"*60 + "\n\n"
            metin += "DİKKAT!\n"
            metin += "Gözlemleriniz öğrencide disleksi şüphesi olduğunu göstermektedir.\n"
            metin += "Ancak öğrenci testlerde akranlarıyla aynı seviyede başarı göstermiştir.\n"
            metin += "Bu durum eğer ki öğrencide disleksi ile ilgili bi durum varsa akranlarına yetişmeye başladığını gösteriyor olabilir. Sevindirici.\n"
            metin += "Ancak gözlemleriniz yanlış yönde de olabilir, öğrencinin durumu disleksiden farklı olabilir.\n"
            metin += "Lütfen gözlemlerinizi arttırınız.\n"
            metin += "\n" + "!"*60 + "\n\n"
        if anket_puani < 88 and toplam_test_riski < 6.5:
            metin += "\n" + "!"*60 + "\n\n"
            metin += "✅ SONUÇ: DÜŞÜK RİSK\n"
            metin += "Öğrenci şu an için belirgin bir risk grubunda görünmemektedir.\n"
            metin += "Gözlemlere devam edilmesi önerilir.\n"
            metin += "\n" + "!"*60 + "\n\n"
        
        # YASAL UYARI (Her durumda eklenir)
        metin += "\n" + "!"*60 + "\n\n"
        metin += "YASAL UYARI:\n"
        metin += "Bu rapor ve uygulama tıbbi bir tanı aracı DEĞİLDİR.\n"
        metin += "Sadece eğitsel gözlem ve farkındalık amacı taşır.\n"
        metin += "Kesin tanı için Çocuk Psikiyatristi görüşü gereklidir.\n"
        metin += "\n" + "!"*60 + "\n\n"

        with open(dosya_ismi, "a", encoding="utf-8") as f:
            f.write(metin)
    
    def ogrenci_ekle(self, numara, ad_soyad=""):
        if numara not in self.__veriler:
            # Yeni öğrenci için boş bir karne oluşturuyoruz
            self.__veriler[numara] = {
                "ad": ad_soyad,
                "testler": {}
            }
            self.kaydet()
            return True # Başarılı
        return False # Zaten var

    def ogrenci_sil(self, numara):
        if numara in self.__veriler:
            del self.__veriler[numara]
            self.kaydet()
            return True
        return False

    def ogrenci_var_mi(self, numara):
        return numara in self.__veriler

    def puan_guncelle(self, numara, test_adi, puan):
        if numara in self.__veriler:
            # Eğer 'testler' anahtarı yoksa oluştur (Eski kayıtlarda hata vermemesi için)
            if "testler" not in self.__veriler[numara]:
                self.__veriler[numara]["testler"] = {}
                
            self.__veriler[numara]["testler"][test_adi] = puan
            self.kaydet()

    def tum_ogrencileri_getir(self):
        return self.__veriler
    
# UYGULAMAYI BAŞLAT
if __name__ == "__main__":
    # Döngüsel içe aktarmayı önlemek için burada içe aktarılmalıdır
    from ana3 import DisleksiUygulamasi
    app = DisleksiUygulamasi()
    app.mainloop()
