import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
from datetime import datetime
import time

def fiyat_cek(url):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.content, "html.parser")
        fiyat_etiketi = soup.find("span", class_="urun_fiyat")
        
        if fiyat_etiketi:
            # data-sort değerini alıp TL'ye çeviriyoruz
            return int(fiyat_etiketi['data-sort']) / 100
        return None
    except Exception as e:
        print(f"Hata (URL: {url}): {e}")
        return None

def ana_program():
    # 1. JSON dosyasını oku
    with open('urunler.json', 'r', encoding='utf-8') as f:
        urunler = json.load(f)
    
    sonuclar = []
    tarih = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print(f"🚀 İşlem başladı: {tarih}")
    
    for urun in urunler:
        print(f"🔍 {urun['urun_adi']} inceleniyor...")
        fiyat = fiyat_cek(urun['urun_url'])
        
        if fiyat:
            sonuclar.append({
                "Tarih": tarih,
                "Ürün Adı": urun['urun_adi'],
                "Fiyat (TL)": fiyat,
                "Link": urun['urun_url']
            })
        
        # Epey'in bizi engellememesi için her ürün arası kısa bir bekleme (opsiyonel)
        time.sleep(2)

    # 2. Verileri DataFrame'e dönüştür ve Excel'e kaydet
    if sonuclar:
        df = pd.DataFrame(sonuclar)
        
        # Dosya varsa üstüne eklemek (append) için veya yeni dosya oluşturmak için:
        try:
            # Mevcut bir excel varsa onu oku ve yeni verileri ekle
            mevcut_df = pd.read_excel("fiyat_takip.xlsx")
            guncel_df = pd.concat([mevcut_df, df], ignore_index=True)
            guncel_df.to_excel("fiyat_takip.xlsx", index=False)
        except FileNotFoundError:
            # Dosya yoksa sıfırdan oluştur
            df.to_excel("fiyat_takip.xlsx", index=False)
            
        print("✅ Veriler 'fiyat_takip.xlsx' dosyasına başarıyla kaydedildi.")
    else:
        print("❌ Hiç veri çekilemedi.")

if __name__ == "__main__":
    ana_program()