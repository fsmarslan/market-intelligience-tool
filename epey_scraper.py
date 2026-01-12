import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
from datetime import datetime
import time
import os
from dotenv import load_dotenv

# .env dosyasındaki değişkenleri yükle
load_dotenv()

# --- AYARLAR ---
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_telegram_message(message):
    """Telegram üzerinden mesaj gönderir."""
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("❌ Hata: Telegram ayarları bulunamadı! Lütfen .env dosyasını yapılandırın.")
        return

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown",
        "disable_web_page_preview": True
    }
    
    try:
        response = requests.post(url, data=payload, timeout=10)
        if response.status_code == 200:
            print("✅ Telegram mesajı gönderildi.")
        else:
            print(f"❌ Telegram hatası: {response.text}")
    except Exception as e:
        print(f"❌ Telegram gönderim hatası: {e}")

def fiyat_cek(url):
    """Verilen URL'den ürün fiyatını çeker."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status() # HTTP hatalarını yakala
        
        soup = BeautifulSoup(response.content, "html.parser")
        fiyat_etiketi = soup.find("span", class_="urun_fiyat")
        
        if fiyat_etiketi and 'data-sort' in fiyat_etiketi.attrs:
            # data-sort değerini alıp TL'ye çeviriyoruz (Örn: 3500000 -> 35000.00 TL)
            fiyat_raw = int(fiyat_etiketi['data-sort'])
            return float(fiyat_raw) / 100
            
        return None
    except Exception as e:
        print(f"❌ Hata (URL: {url}): {e}")
        return None

def ana_program():
    dosya_adi = 'urunler.json'
    if not os.path.exists(dosya_adi):
        print(f"❌ '{dosya_adi}' dosyası bulunamadı.")
        return

    with open(dosya_adi, 'r', encoding='utf-8') as f:
        urunler = json.load(f)
    
    sonuclar = []
    telegram_mesaji = ""
    simdi = datetime.now()
    tarih_str = simdi.strftime("%d.%m.%Y %H:%M")
    
    print(f"🚀 İşlem başladı: {tarih_str}")
    
    # Rapor Başlığı
    telegram_mesaji += f"📊 *GÜNLÜK FİYAT RAPORU* ({tarih_str})\n\n"

    for urun in urunler:
        urun_adi = urun.get('urun_adi', 'Bilinmeyen Ürün')
        url = urun.get('url')
        
        if not url:
            print(f"⚠️ URL eksik: {urun_adi}")
            continue

        print(f"🔍 {urun_adi} inceleniyor...")
        fiyat = fiyat_cek(url)
        
        if fiyat is not None:
            # Excel için veri hazırla
            sonuclar.append({
                "Tarih": simdi.strftime("%Y-%m-%d %H:%M:%S"),
                "Ürün Adı": urun_adi,
                "Fiyat (TL)": fiyat,
                "Link": url
            })
            
            # Telegram mesajı için formatla
            telegram_mesaji += f"🔹 *{urun_adi}*\n💰 Fiyat: {fiyat:,.2f} TL\n🔗 [Ürüne Git]({url})\n\n"
        else:
            print(f"⚠️ Fiyat alınamadı: {urun_adi}")

        # Her istek arası bekleme
        time.sleep(2)

    # Verileri Excel'e kaydet
    if sonuclar:
        df = pd.DataFrame(sonuclar)
        excel_dosyasi = "fiyat_takip.xlsx"
        
        try:
            if os.path.exists(excel_dosyasi):
                with pd.ExcelWriter(excel_dosyasi, mode='a', if_sheet_exists='overlay', engine='openpyxl') as writer:
                    # Mevcut verinin sonuna eklemek için (header olmadan)
                     # Ancak en garantisi okuyup concat yapmaktır, özellikle sütunlar değişirse.
                     # Prompt "Mevcut varsa üzerine yazma, sonuna ekle" dedi.
                     # En basit ve güvenli yöntem: Oku -> Birleştir -> Yaz
                    mevcut_df = pd.read_excel(excel_dosyasi)
                    guncel_df = pd.concat([mevcut_df, df], ignore_index=True)
                    guncel_df.to_excel(excel_dosyasi, index=False)
            else:
                df.to_excel(excel_dosyasi, index=False)
                
            print(f"✅ Veriler '{excel_dosyasi}' dosyasına başarıyla kaydedildi.")
            
            # Telegram mesajını gönder
            if telegram_mesaji:
                send_telegram_message(telegram_mesaji)
                
        except Exception as e:
             print(f"❌ Excel kayıt hatası: {e}")

    else:
        print("❌ Hiç veri çekilemedi, Excel güncellenmedi.")

if __name__ == "__main__":
    ana_program()
