# Öğretmenin öğrenci gözlem anketi

import tkinter as tk
from tkinter import messagebox
from siniflar_ve_moduller import YuvarlakButon

class AnketSayfasi(tk.Frame):
    def __init__(self, ebeveyn, yonetici):
        super().__init__(ebeveyn, bg="#A2C5D8") 
        self.yonetici = yonetici

        # 1. BAŞLIK KISMI
        baslik_frame = tk.Frame(self, bg="#2C3E50", height=60)
        baslik_frame.pack(side="top", fill="x")

        # Geri Dön Butonu
        YuvarlakButon(baslik_frame, metin="<", genislik=40, yukseklik=40, 
                     arkaplan_rengi="#95a5a6",
                     # Başlığın sol tarafına, dikeyde ortalayarak yerleştiriyoruz
                     komut=lambda: yonetici.sayfa_goster("TestlerSayfasi")).place(x=15, y=15) 
          
        lbl_baslik = tk.Label(baslik_frame, text="Öğrenme Bozukluğu Belirti Tarama Testi", 
                              bg="#2C3E50", fg="white", font=("Arial", 16, "bold"))
        lbl_baslik.pack(pady=15)

        # 2. KAYDIRILABİLİR ALAN (SCROLLBAR)
        self.canvas = tk.Canvas(self, bg="#1e1e1e", highlightthickness=0)
        scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)

        self.scrollable_frame = tk.Frame(self.canvas, bg="#A2C5D8")

        # Dikey kaydırma ayarı
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        # Pencere ID'sini alıyoruz
        self.canvas_window = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True, padx=20, pady=20)
        scrollbar.pack(side="right", fill="y")

        # Pencere genişledikçe içerdeki çerçeveyi de genişlet
        self.canvas.bind("<Configure>", self.cerceve_genisligini_ayarla)

        # Fare alanın üzerine gelince tekerleği dinle, ayrılınca dinlemeyi bırak
        self.canvas.bind_all("<MouseWheel>", self.tekerlek_hareketi)
        
        # 3. SORULAR
        self.sorular = [
            "1. Bir çok alanda zeki görünmesine karşın okul başarısı düşüktür.",
            "2. Başarı durumu günden güne hatta saatten saate değişiklik gösterir.",
            "3. Bazı ders/alanlarda başarısı normal hatta normalin üstünde iken, bazı ders/alanlarda düşüktür.",
            "4. Okuması yaşıtları seviyesinin altındadır.",
            "5. Okumayı sevmez.",
            "6. Yaşıtlarından daha yavaş okur.",
            "7. Bazı harflerin seslerini öğrenemez (harfin şekli ile sesini birleştiremez).",
            "8. Sessiz ya da sesli okurken kelimeleri parmağıyla izler.",
            "9. Sınıf düzeyinde bir parça okurken satır, kelime ya da harf atlar ya da tekrar okur.",
            "10. Okurken anlamı bozacak kelimeleri parçadakilerin yerine koyar (ne zaman yerine, nerede gibi).",
            "11. Kelimeleri hecelerken ya da harflerine ayırırken zorlanır.",
            "12. Sınıf düzeyinde bir parçayı okuduğunda anlamakta zorlanır (eğer başka birisi okursa daha iyi anlar).",
            "13. Okurken bazı harf ya da sayıları karıştırır, ters okur (b-d, b-p, 6-9 vb.).",
            "14. Gördüğü şeyleri aklında tutmakta zorlanır (görsel belleği zayıftır).",
            "15. Nesnelerin boyutlarını, şekillerini, uzaklıklarını kavrayamaz (uzaklık, derinlik, boyut algısı zayıftır).",
            "16. Eşyaları, resimleri, şekilleri eşleştirmekte güçlük çeker, belirli bir şeklin benzerini bulmakta zorlanır.",
            "17. Bazı harf, sayı ve kelimeleri yanlış duyar, karıştırır (m-n, f-v, b-m, kaş-koş, soba-sopa vb.).",
            "18. Sözle verilen yönergeleri anlamakta güçlük çeker (ne söylediğini anlamaz).",
            "19. Söyleneni dinliyormuş gibi görünür (başkaları söyleneni yapmaya başladığı halde o yönergelerin tekrarlanmasını ister).",
            "20. Birkaç şey birden söylendiğinde en az birini unutur (işitsel belleği zayıftır).",
            "21. Aynı zamanda işittiği 2-3 sesten birini duymaz (müzik dinlerken telefon sesini, kendisine seslenildiğini duymaz).",
            "22. Yaşıtlarına oranla el yazısı okunaksız ve çirkindir.",
            "23. Yazı yazmayı sevmez.",
            "24. Sınıf düzeyine göre yazı yazması yavaştır.",
            "25. Yazarken bazı harf ve sayıları ters yazar, karıştırır (b-p, m-n, ı-i, 2-5, d-t, g-ğ gibi).",
            "26. Yazarken bazı harfleri atlar ya da harf ekler.",
            "27. Sınıf düzeyine göre yazılı imla ve noktalama hataları yapar (küçük harf-büyük harf, noktalama hataları).",
            "28. Yazarken sayfayı düzenli kullanamaz (gereksiz satır atlar, boşluk bırakır).",
            "29. Yaşıtlarına oranla çizgileri kötü, dalgalıdır.",
            "30. Yaşıtlarına oranla insan resmi çizimleri kötüdür.",
            "31. Aritmetikte zorlanır (dört işlemi yaparken yavaştır, parmak sayar, yanlış yapar).",
            "32. Sınıf düzeyine göre çarpım tablosu öğrenmede yaşıtları seviyesinin altındadır.",
            "33. Bazı aritmetik sembolleri öğrenmekte zorlanır, karıştırır (+, x, -).",
            "34. Ev ödevlerini almaz, eksik kalır.",
            "35. Ev ödevlerini yaparken yavaş ve verimsizdir.",
            "36. Ders çalışırken sık sık ara verir, çabuk sıkılır.",
            "37. Ders çalışmayı sevmez.",
            "38. Ödevlerini yalnız başına yapmaz.",
            "39. Odası, çantası ve eşyaları, giysileri dağınıktır.",
            "40. Defter, kitaplarını kötü kullanır, yırtar.",
            "41. Defter, kalem ve diğer araçlarını kaybeder.",
            "42. Zamanını ayarlamakta zorluk çeker (bir işi yaparken ne kadar zaman geçirdiğini tahmin edemez).",
            "43. Üzerine aldığı işleri düzenlemekte zorluk çeker, nereden başlayacağını bilemez.",
            "44. Sağ-sol karıştırır.",
            "45. Yönünü bulmakta zorlanır (doğu-batı, kuzey-güney kavramlarını karıştırır).",
            "46. Burada, şurada, orada gibi işaret sözcüklerini karıştırır.",
            "47. Alt-üst, ön-arka gibi kavramları karıştırır.",
            "48. Zaman kavramlarını karıştırır (dün-bugün, önce-sonra gibi).",
            "49. Yıl, ay, gün, mevsim kavramlarını karıştırır.",
            "50. Saati öğrenmekte zorlanır.",
            "51. Gözü kapalı iken avucuna çizilen sayı, harfi anlayamaz.",
            "52. Gözü kapalı iken hangi parmağına dokunulduğunu anlayamaz.",
            "53. Dinlediği, okuduğu bir öyküyü anlatması istendiğinde öykünün başını sonunu karıştırır.",
            "54. Haftanın günlerini ya da ayları sırayla sayabilir ama karışık sorulduğunda bir sonrakini bilemez.",
            "55. Okulda öğrendiklerini ya da çalıştıklarını çabuk unutur.",
            "56. Duygu ve düşüncelerini sözel olarak ifade etmekte zorlanır.",
            "57. Serbest konuşurken düzgün cümleler kuramaz.",
            "58. Kalabalıkta konuşurken heyecanlanır, takılır, şaşırır.",
            "59. Bazı harflerin seslerini doğru olarak telaffuz edemez (r, ş, j gibi harfleri söyleyemez).",
            "60. Konuşması yabancılar tarafından zor anlaşılır.",
            "61. Top yakalama, ip atlama gibi işlerde yaşıtları seviyesinin altındadır.",
            "62. Sakardır, düşer, yaralanır, istemeden bir şeyler kırar.",
            "63. Çatal, kaşık kullanmakta zorlanır.",
            "64. Ayakkabı, kravat bağlamayı beceremez.",
            "65. El becerilerine dayalı işlerde zorluk çeker (düğme ilikleme, makas kullanma, boncuk dizme gibi).",
            "66. Düşünmeden aniden aklına eseni yapar.",
            "67. İstedikleri yapılmadığında aşırı tepki gösterir, öfkelenir.",
            "68. Eleştirildiğinde aşırı tepki gösterir, öfkelenir ya da dikkate almaz (eleştiriye toleransı azdır).",
            "69. Daha çok yalnız olmayı tercih eder, fazla arkadaşı yoktur.",
            "70. Arkadaş ilişkileri iyi değildir.",
            "71. Yaşıtları yerine daha çok yetişkinlerle ya da kendinden küçüklerle birlikte olmaktan keyif alır.",
            "72. Hayal kurar, dalgındır, sınıfta uyur.",
            "73. Yaşıtlarına oranla sınıf ya da okul kurallarına uymakta zorluk çeker.",
            "74. Değişikliklere zor uyum sağlar.",
            "75. Duygu durumu çok sık değişir (neşeli iken aniden öfkelenebilir).",
            "76. Kendisine güveni azdır.",
            "77. Gergin ya da huzursuzdur (dudaklarını ısırır, sık tuvalete gider, saçıyla oynar).",
            "78. Kendisini fiziksel olarak beğenmez.",
            "79. Hızlı hareket eder, hızlı konuşur.",
            "80. Aşırı hareketlidir (eli ayağı oynar, kıpırdanır, mırıldanır).",
            "81. Uzun süre yerinde duramaz.",
            "82. Yoğun görsel dikkat gerektiren işlerden kaçınır.",
            "83. Dikkatini ayrıntılara veremez, dikkatsizce hatalar yapar.",
            "84. Dikkati kolayca dağılır (başkasının sesinden, hareketinden dahi dikkati dağılır).",
            "85. İşlerini bitirmede yavaştır, oyalanır, nadiren başladığı işi bitirir.",
            "86. Başarılı olamadığı zaman çok çabuk vazgeçer.",
            "87. Okulla ilgili ya da başka faaliyetlere katılmak istemez.",
            "88. Okulda hevessizdir. Çok az çaba gösterir."
        ]

        self.cevap_degiskenleri = [] 
        self.label_listesi = [] # Yazıların wraplength'ini güncellemek için tutuyoruz

        for index, soru_metni in enumerate(self.sorular):
            self.soru_olustur(index + 1, soru_metni)

        # Butonları yan yana koymak için bir çerçeve (Frame)
        buton_frame = tk.Frame(self.scrollable_frame, bg="#A2C5D8")
        buton_frame.pack(pady=30)

        # Temizle Butonu
        YuvarlakButon(buton_frame, metin="Temizle", genislik=200, yukseklik=50,
                      arkaplan_rengi="#ac3224",
                      komut=self.formu_temizle).pack(side="left", padx=20)

        # Bitir Butonu
        YuvarlakButon(buton_frame, metin="Testi Bitir", genislik=200, yukseklik=50,
                      arkaplan_rengi="#5184B1", 
                      komut=self.sonuclari_hesapla).pack(side="left", padx=20)

    # Fare tekerleği ile kaydırma için
    def tekerlek_hareketi(self, olay):
        try:
            self.canvas.yview_scroll(int(-1*(olay.delta/120)), "units")
        except:
            pass # Hata olursa (örn: sayfa kapalıysa) görmezden gel

    def cerceve_genisligini_ayarla(self, olay):
        # Canvas içindeki pencerenin genişliğini, canvas'ın yeni genişliğine eşitleme
        canvas = olay.widget
        canvas.itemconfig(self.canvas_window, width=olay.width)

        # Yazıların pencere genişliğine göre alt satıra geçmesini sağla
        yeni_wraplength = olay.width - 60 # Kenar boşlukları için biraz düşürüldü
        for lbl in self.label_listesi:
            lbl.config(wraplength=yeni_wraplength)

    def soru_olustur(self, soru_no, metin):
        # Frame
        soru_kutusu = tk.Frame(self.scrollable_frame, bg="#2b2b2b", bd=1, relief="flat")
        soru_kutusu.pack(fill="x", pady=5, ipadx=10, ipady=5)

        # Soru Metni
        lbl = tk.Label(soru_kutusu, text=f"{metin}", 
                         bg="#2b2b2b", fg="white", font=("Arial", 11), 
                         justify="left", anchor="w")
        
        # Başlangıç wraplength (Sonra event ile değişecek)
        lbl.pack(anchor="w", padx=10, pady=5, fill="x")
        self.label_listesi.append(lbl)

        # Değişken
        var = tk.IntVar(value=-1) 
        self.cevap_degiskenleri.append(var)

        # Şıklar Frame
        siklar_frame = tk.Frame(soru_kutusu, bg="#2b2b2b")
        siklar_frame.pack(anchor="w", padx=10)

        stiller = [("Hiçbir Zaman", 0), ("Bazen", 1), ("Sıklıkla", 2), ("Her Zaman", 3)]
        
        for yazi, puan in stiller:
            tk.Radiobutton(siklar_frame, text=yazi, variable=var, value=puan,
                                bg="#2b2b2b", fg="#aaaaaa", selectcolor="#1e1e1e",
                                activebackground="#2b2b2b", activeforeground="white",
                                font=("Arial", 10)).pack(side="left", padx=10)
    
    def formu_temizle(self):
        # Kullanıcıya soralım, yanlışlıkla basmış olabilir
        cevap = messagebox.askyesno("Temizle", "Tüm işaretlemeler silinecek ve sıfırlanacak.\nEmin misiniz?")
        
        if cevap:
            # Tüm değişkenleri döngüye alıp 0 yapıyoruz
            for var in self.cevap_degiskenleri:
                var.set(-1)
            
            # Sayfayı en yukarı kaydır
            self.canvas.yview_moveto(0)
    
    def sonuclari_hesapla(self):
        # Boş soru kontrolü
        bos_sorular = []
        for index, var in enumerate(self.cevap_degiskenleri):
            # Eğer değeri -1 ise, öğretmen o soruya dokunmamış demektir
            if var.get() == -1:
                bos_sorular.append(str(index + 1)) # Sorunun numarasını not et

        # Eğer boş soru listesi doluysa uyarı ver ve işlemi durdur
        if bos_sorular:
            uyari_mesaji = f"Lütfen tüm soruları cevaplayınız.\n\nBoş Bırakılan Sorular:\n{', '.join(bos_sorular[:10])}"
            if len(bos_sorular) > 10:
                uyari_mesaji += f"\n... ve {len(bos_sorular)-10} soru daha."
            
            messagebox.showwarning("Eksik Cevap", uyari_mesaji)
            return # Fonksiyondan çık, kaydetme!
        
        # 1. Puanı Hesapla
        toplam_puan = 0
        for var in self.cevap_degiskenleri:
            toplam_puan += var.get()

        # 2. Aktif Öğrenciyi Kontrol Et
        aktif_ogrenci = self.yonetici.aktif_ogrenci_no
        
        if aktif_ogrenci:
            # 3. Veritabanına Kaydet
            self.yonetici.veri_yoneticisi.puan_guncelle(aktif_ogrenci, "anket_puani", toplam_puan)
            
            self.yonetici.veri_yoneticisi.anket_sonucu_isles(aktif_ogrenci, toplam_puan)
            
            # 4. Mesaj Metnini Hazırla
            mesaj = f"Anket Tamamlandı.\nÖğrenci: {aktif_ogrenci}\nToplam Puan: {toplam_puan}\n\n"
            
            if toplam_puan >= 88:
                mesaj += "⚠️ DİKKAT: YÜKSEK RİSK GRUBU\n"
                mesaj += "Bu puan, öğrencinin disleksi belirtileri gösterdiğine işaret edebilir.\n\n"
            else:
                mesaj += "Risk seviyesi eşik değerin (88) altındadır.\n\n"
            
            # 5. Yasal/Pedagojik Uyarı (Her durumda gösterilir)
            mesaj += ("-"*40 + "\n"
                      "ÖNEMLİ BİLGİLENDİRME:\n"
                      "Bu uygulama tıbbi bir tanı aracı DEĞİLDİR.\n"
                      "Elde edilen sonuç sadece bir ön değerlendirmedir.\n"
                      "Kesin sonuç için öğrencinin Rehberlik Servisine veya\n"
                      "bir çocuk psikiyatristine yönlendirilmesi önerilir.\n"
                      "Lütfen gözlemlerinizi arttırarak takibe devam ediniz.")

            messagebox.showinfo("Değerlendirme Sonucu", mesaj)
            
            # İşlem bitince testler sayfasına dön
            self.yonetici.sayfa_goster("TestlerSayfasi")
            
        else:
            messagebox.showerror("Hata", "Öğrenci girişi yapılmamış! Puan kaydedilemedi.")

# UYGULAMAYI BAŞLAT
if __name__ == "__main__":
    # Döngüsel içe aktarmayı önlemek için burada içe aktarılmalıdır
    from ana3 import DisleksiUygulamasi
    app = DisleksiUygulamasi()
    app.mainloop()