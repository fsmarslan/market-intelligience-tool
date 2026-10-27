# Market Intelligence Tool

E-ticarette ürün fiyatlarını takip etmek için geliştirilmiş Python aracı. `urunler.json` dosyasında tanımlanan ürünlerin Epey.com üzerindeki fiyatını okumayı dener ve sonuçları tek bir Telegram raporunda toplar.

## Neler yapar?

- Ürün listesi üzerinden fiyat sorgular.
- İlan metninde yenilenmiş, outlet, teşhir veya ikinci el gibi ifadeler gördüğünde ilgili sonucu atlar.
- Bulduğu fiyatları ürün bağlantılarıyla birlikte Telegram'a gönderir.
- İstekler arasında iki saniye bekler ve bağlantı isteklerine zaman aşımı uygular.

Mevcut sürüm fiyat geçmişi tutmaz ve Excel dosyası üretmez. Fiyatı okunamayan ürünler konsolda bildirilir.

## Kurulum

Depoyu indirip proje dizininde bir sanal ortam oluşturun:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Windows'ta sanal ortamı `.venv\Scripts\activate` ile etkinleştirebilirsiniz.

`.env.example` dosyasını `.env` adıyla kopyalayın ve kendi Telegram bilgilerinizi girin:

```dotenv
TELEGRAM_BOT_TOKEN="kendi_bot_tokeniniz"
TELEGRAM_CHAT_ID="kendi_chat_id_degeriniz"
```

`.env` dosyasını Git'e eklemeyin. Bir sunucu veya otomasyon ortamında bu değerleri ortam değişkenleri olarak sağlayabilirsiniz.

## Ürün listesini düzenleme

`urunler.json` dosyası bir JSON listesi içerir. Her ürün için `urun_adi` ve `url` alanlarını tanımlayın; URL olarak takip etmek istediğiniz Epey ürün sayfasını kullanın.

## Çalıştırma

Proje dizininde:

```bash
python epey_scraper.py
```

Program bir kez çalışır ve raporu gönderir. Düzenli çalıştırma için ayrıca bir zamanlayıcı yapılandırılması gerekir; depoda hazır bir GitHub Actions iş akışı bulunmaz.

## Sınırlamalar

- Fiyat ayrıştırma, sayfadaki `span.urun_fiyat` ve `data-sort` yapısına bağlıdır. Site yapısı değişirse güncelleme gerekir.
- Filtreyi geçen ilk fiyat kullanılır; tüm satıcılar arasında en düşük fiyatı bulma garantisi yoktur.
- Telegram raporu tek mesaj olarak gönderilir; uzun ürün listelerinde mesaj boyutu sınırına takılabilir.
- Zamanlar uygulamanın çalıştığı ortamın yerel saatine göre yazılır.

## Geliştirme planı

- Fiyat geçmişini saklama ve değişim karşılaştırması.
- CSV / Excel dışa aktarımı.
- Ayrıştırıcı için kayıtlı HTML örnekleriyle testler.
- Uzun raporları birden fazla Telegram mesajına bölme.
