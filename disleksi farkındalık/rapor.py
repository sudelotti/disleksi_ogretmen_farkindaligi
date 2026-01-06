# Öğretmenin testlerden ve anketlerden gelen verileri göreceği sayfa

import tkinter as tk
import platform
import os
from tkinter import messagebox
from siniflar_ve_moduller import YuvarlakButon


class RaporSayfasi(tk.Frame): 
     def __init__(self, ebeveyn, yonetici):
        super().__init__(ebeveyn, bg="#A2C5D8")
        self.yonetici = yonetici

        lbl_baslik = tk.Label(self, text="Öğrenci Risk Raporu", bg="#A2C5D8", font=("Arial", 24, "bold"))
        lbl_baslik.pack(pady=30)
        
        self.lbl_rapor = tk.Label(self, text="...", bg="white", font=("Courier", 12), justify="left", padx=20, pady=20)
        self.lbl_rapor.pack(pady=20)

        # Bilgilendirme
        info_lbl = tk.Label(self, text="Öğrencinin detaylı test geçmişini ve hata analizlerini\ngörmek için numarasını girip butona basınız.",
                            bg="#A2C5D8", font=("Arial", 12)).pack(pady=10)
        
        # Öğrenci No Giriş Alanı
        lbl_no = tk.Label(self, text="Öğrenci No:", bg="#A2C5D8", font=("Arial", 14, "bold"))
        lbl_no.pack(pady=(20, 5))
        
        self.entry_no = tk.Entry(self, font=("Arial", 14), justify="center")
        self.entry_no.pack(pady=5, ipady=5)

        # Raporu İndir/Aç Butonu
        YuvarlakButon(self, metin="Detaylı Raporu Aç", arkaplan_rengi="#5184B1", yazi_rengi="black",
                      genislik=320, komut=self.raporu_goster).pack(pady=20)
        
        YuvarlakButon(self, metin="Geri Dön", arkaplan_rengi="#5184B1", yazi_rengi="black",
                     komut=lambda: yonetici.sayfa_goster("AnaSayfa")).pack(side="bottom", pady=30)

     def raporu_goster(self):
         ogr_no = self.yonetici.aktif_ogrenci_no
         if not ogr_no:
             self.lbl_rapor.config(text="Lütfen önce öğrenci girişi yapınız.")
             return
         
         dosya_adi = f"{ogr_no}_detayli_rapor.txt"

         if os.path.exists(dosya_adi):
             try:
                 # İşletim sistemine göre dosyayı açma komutu
                 if platform.system() == 'Darwin':       # macOS
                     os.system(f'open "{dosya_adi}"')
                 elif platform.system() == 'Windows':    # Windows
                     os.startfile(dosya_adi)
                 else:                                   # Linux
                     os.system(f'xdg-open "{dosya_adi}"')
             except Exception as e:
                 messagebox.showerror("Hata", f"Dosya açılamadı: {e}")
         else:
             messagebox.showerror("Bulunamadı", f"{ogr_no} numaralı öğrenciye ait bir rapor geçmişi bulunamadı.\nHenüz test çözmemiş olabilir.")

# UYGULAMAYI BAŞLAT
if __name__ == "__main__":
    # Döngüsel içe aktarmayı önlemek için burada içe aktarılmalıdır
    from ana3 import DisleksiUygulamasi
    app = DisleksiUygulamasi()
    app.mainloop()