# Merkezi Soğutma Projeleri Yönetim Sistemi

Bu belge, Merkezi Soğutma Projeleri Yönetim Sistemi'nin kurulum ve kullanım kılavuzudur.

## Sistem Gereksinimleri

- Python 3.10 veya daha yeni bir sürüm
- Windows, Linux veya macOS işletim sistemi
- İnternet bağlantısı (ilk kurulum için)

## Kurulum ve Çalıştırma

### Windows

1. Dosyaları bilgisayarınıza çıkarın
2. `setup.bat` dosyasına çift tıklayın
3. Tarayıcınızda `http://localhost:5000` adresine gidin

### Linux/macOS

1. Dosyaları bilgisayarınıza çıkarın
2. Terminal açın ve proje klasörüne gidin
3. Sanal ortamı oluşturun: `python3 -m venv venv`
4. Sanal ortamı etkinleştirin: `source venv/bin/activate`
5. Bağımlılıkları yükleyin: `pip install -r requirements.txt`
6. Veritabanını oluşturun: `python project/init_db.py`
7. Uygulamayı başlatın: `python project/run.py`
8. Tarayıcınızda `http://localhost:5000` adresine gidin

## Varsayılan Kullanıcılar

### Yönetici Hesapları

| Kullanıcı Adı | Şifre    |
|---------------|----------|
| admin1        | admin123 |
| admin2        | admin123 |
| admin3        | admin123 |
| admin4        | admin123 |
| admin5        | admin123 |

### Normal Kullanıcı Hesapları

| Kullanıcı Adı | Şifre   |
|---------------|---------|
| user1         | user123 |
| user2         | user123 |
| user3         | user123 |
| user4         | user123 |

## Sistem Özellikleri

- Proje yönetimi (ekleme, düzenleme, silme)
- Ekipman yönetimi (ekleme, düzenleme, silme, resim yükleme)
- Kategori yönetimi (ekleme, düzenleme, silme)
- Yorum sistemi
- Aktivite kaydı
- Kullanıcı yetkilendirme sistemi (admin/normal kullanıcı)
- Duyarlı tasarım (mobil uyumlu)

## Kullanıcı Rolleri

### Yönetici (Admin)

- Tüm projeleri, ekipmanları, kategorileri görüntüleyebilir
- Yeni proje, ekipman, kategori ekleyebilir
- Mevcut projeleri, ekipmanları, kategorileri düzenleyebilir ve silebilir
- Yorum ekleyebilir ve silebilir
- Tüm aktivite kayıtlarını görüntüleyebilir

### Normal Kullanıcı

- Tüm projeleri ve ekipmanları görüntüleyebilir
- Yeni proje ve ekipman ekleyebilir
- Sadece kendi eklediği projeleri ve ekipmanları düzenleyebilir
- Yorum ekleyebilir ve kendi yorumlarını silebilir
- Aktivite kayıtlarını görüntüleyebilir

## Dosya Yapısı

```
project/
│
├── static/
│   └── uploads/         ← Ekipman resimleri
│   └── css/             ← CSS dosyaları
│   └── js/              ← JavaScript dosyaları
│
├── templates/           ← HTML şablonları
│
├── models/              ← Veritabanı modelleri
├── routes/              ← Uygulama rotaları
├── forms/               ← Form tanımları
├── utils/               ← Yardımcı fonksiyonlar
│
├── config.py            ← Uygulama yapılandırması
├── app.py               ← Uygulama tanımı
├── run.py               ← Uygulama başlatıcı
└── init_db.py           ← Veritabanı başlatıcı
```

## Sorun Giderme

- **Uygulama başlatılamıyor**: Python'un doğru sürümünün yüklü olduğundan emin olun
- **Veritabanı hatası**: `project/app.db` dosyasını silip `python project/init_db.py` komutunu çalıştırın
- **Resim yükleme sorunu**: `project/static/uploads` klasörünün yazma izinlerine sahip olduğundan emin olun

## İletişim

Herhangi bir sorun veya öneri için lütfen iletişime geçin.
