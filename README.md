# Market Intelligence Tool

Bu araç, belirlenen ürünlerin fiyatlarını Epey.com üzerinden takip eder, Excel dosyasına kaydeder ve Telegram üzerinden raporlar.

## Kurulum ve Güvenlik

Bu projede hassas bilgiler (API anahtarları vb.) `.env` dosyasında saklanmaktadır. Projeyi çalıştırmadan önce aşağıdaki adımları izleyin:

1.  **Gereksinimleri Yükleyin:**
    termianl
    pip install -r requirements.txt
    

2.  **Ortam Değişkenlerini Ayarlayın:**
    *   Proje klasöründe `.env` adında yeni bir dosya oluşturun.
    *   `.env.example` dosyasındaki içeriği `.env` dosyasına kopyalayın.
    *   `TELEGRAM_BOT_TOKEN` ve `TELEGRAM_CHAT_ID` yerine kendi bilgilerinizi yazın.

    Örnek `.env` içeriği:
    text
    TELEGRAM_BOT_TOKEN="123456789:ABCDefGHIjkLmnOPQRstuVWxyz"
    TELEGRAM_CHAT_ID="987654321"
    

    *Not: `.env` dosyası gizli bilgilerinizi içerdiği için Git geçmişine (GitHub'a) yüklenmez. `.gitignore` dosyasında engellenmiştir.*

3.  **GitHub Actions / Canlı Ortam:**
    Eğer bu projeyi GitHub Actions veya bir sunucuda çalıştıracaksanız, bu değişkenleri ilgili platformun "Secrets" veya "Environment Variables" bölümüne eklemelisiniz:
    *   **GitHub:** Repo Settings > Secrets and variables > Actions > New repository secret yolunu izleyerek `TELEGRAM_BOT_TOKEN` ve `TELEGRAM_CHAT_ID` anahtarlarını ekleyin.

## Kullanım

Scripti çalıştırmak için:
bash
python epey_scraper.py
