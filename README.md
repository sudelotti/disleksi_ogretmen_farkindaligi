# 🧩 Disleksi Öğretmen Farkındalığı ve Ön Tarama Aracı
Merhabalar ben Ankara Üniversitesi Bilgisayar ve Öğretim Teknolojileri Öğretmenliği 2. sınıf öğrencisi Sude Kaya. BOZ213 Nesne Tabanlı Programlama dersi final projemi sizlere tanıtmak isterim.

# 📖 Proje Hakkında
Bu proje, sınıf ortamında gözden kaçabilen Özgül Öğrenme Güçlüğü (Disleksi) riskini erken aşamada tespit etmek amacıyla geliştirilmiş bir masaüstü uygulamasıdır. Öğretmenlere, öğrencilerin işitsel, görsel ve bilişsel becerilerini ölçebilecekleri dijital bir araç sunar.

Uygulama, öğrencinin çözdüğü 5 farklı interaktif test ile öğretmenin doldurduğu gözlem anketini birleştirerek bir risk analizi yapar ve detaylı raporlar sunar.

🎮 **Oyunlaştırılmış 5 Test Modülü:**

* Fonoloji (İşitsel) Testi: Harf-ses farkındalığı.

* Ses Sayma Testi: Görseldeki varlığın ses sayısını bulma.

* Sıralama Testi: Olay oluş sırası, örüntü ve yön bulma.

* Heceleme Testi: Karışık hecelerden anlamlı kelime türetme.

* Hızlı Okuma Testi: Okuma süresi ve anlama ölçümü.

📊 **Akıllı Raporlama:** Test puanları ve öğretmen gözlemini karşılaştırarak "Gizli Risk" veya "Yüksek Risk" tespiti.

💾 **Veri Yönetimi:** JSON tabanlı yerel veritabanı ile öğrenci kaydı ve takibi.

📈 **Detaylı Analiz:** Her öğrenci için .txt formatında hata dökümü ve gelişim raporu çıktısı.

## 🛠️ Teknik Mimari ve Özellikler

* **Programlama Dili:** Python 3.12
  
* **Kullanılan Kütüphaneler:** Pygame, Tkinter, OS, Random, Time, Platform, Pillow, Json, Datetime
  
* **OOP Mimari:** `TemelTeset` ata sınıfı üzerinden kalıtım (inheritance) ve metod ezme (overriding) kullanılmıştır.
  
* **Veri Yönetimi:** Öğrenci verileri JSON formatında dinamik olarak yönetilmektedir.

# 📂 Proje Yapısı
```bash
📂 disleksi_ogretmen_farkindaligi
├── 📄 ana3.py                  # Uygulamanın ana giriş noktası (Main)
├── 📄 siniflar_ve_moduller.py  # Temel sınıflar (TemelTest, YuvarlakButon, VeriYoneticisi)
├── 📄 testler.py               # Test seçim ekranı
├── 📄 fonoloji.py              # Ses farkındalığı testi
├── 📄 sesler.py                # Kelime içi ses sayma testi
├── 📄 heceleme.py              # Hece birleştirme testi
├── 📄 siralama.py              # Mantıksal sıralama ve yön bulma testi
├── 📄 hizli_okuma.py           # Okuma hızı ve anlama testi
├── 📄 ogretmen_icin.py         # Öğretmen gözlem anketi modülü
├── 📄 rapor.py                 # Rapor görüntüleme ekranı
├── 📄 yonetim.py               # Öğrenci ekleme/silme paneli
├── 📄 ogrenci_verileri.json    # Veritabanı dosyası
└── 📂 assets                   # Resim ve ses dosyalarının bulunduğu klasör
```

# 🚀 Kurulum ve Başlatma
Projeyi kendi bilgisayarınıza indirmek için terminale şu komutu yazın:
```bash
git clone https://github.com/sudelotti/disleksi_ogretmen_farkindaligi.git
```

Projenin bulunduğu konuma gitmek için terminale şu komutu yazın:
```bash
cd disleksi_ogretmen_farkindaligi
```

Uygulamayı çalıştırmak için terminale şu komutu yazın:
```bash
python ana3.py
```
# ⚠️ Yapılması Gerekenler
Uygulamada `pygame` kullanıldığı için Python 11.x veya Python 12.x kurmalısınız. Yoksa pygame kurulumunda hata verilecektir. `Python`ı işletim sisteminiz Windows ise Microsoft Store'den indirebilirsiniz.
Ayrıca `pillow` kütüphanesini terminale `pip install pillow` yazarak kurmayı unutmayın.

## ⚖️ Etik ve Yasal Sorumluluk Beyanı

Bu yazılım, **Ankara Üniversitesi BOZ213 Nesne Yönelimli Programlama** dersi kapsamında eğitim ve farkındalık amacıyla geliştirilmiştir. Kullanıcılar ve geliştiriciler aşağıdaki hususları kabul etmiş sayılır:

1.  **🚫 Tıbbi Tanı Aracı Değildir:** Bu uygulama bir tıbbi cihaz veya profesyonel tanı aracı **DEĞİLDİR**. Algoritmaların ürettiği "Risk Puanı" ve raporlar yalnızca istatistiksel bir ön değerlendirmedir. Kesin tanı için öğrenci mutlaka **Rehberlik ve Araştırma Merkezlerine (RAM)** veya çocuk psikiyatristine yönlendirilmelidir.
2.  **🏷️ Etiketlemeden Kaçınma:** Uygulama sonuçları çocuğun "başarısız" veya "yetersiz" olduğu anlamına gelmez; yalnızca fonolojik veya görsel algı alanlarında desteğe ihtiyaç duyabileceğini gösterir. Sonuçlar öğrenciyi etiketlemek için kullanılmamalıdır.
3.  **🔒 Veri Mahremiyeti:** Uygulama, öğrenci verilerini şifrelemeden, yerel bir JSON dosyasında (`ogrenci_verileri.json`) saklar. Veriler herhangi bir bulut sunucusuna gönderilmez. Ancak, bu verilerin güvenliğinden ve KVKK (Kişisel Verilerin Korunması Kanunu) uyumluluğundan yazılımı kullanan kişi (öğretmen) sorumludur.
