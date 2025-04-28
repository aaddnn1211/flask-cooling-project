@echo off
echo Merkezi Sogutma Projeleri Yonetim Sistemi baslatiliyor...
echo.

REM Python yüklü mü kontrol et
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python bulunamadi! Lutfen Python 3.10 veya daha yeni bir surumu yukleyin.
    echo https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Sanal ortam var mı kontrol et
if not exist venv (
    echo Sanal ortam bulunamadi. Yeni bir sanal ortam olusturuluyor...
    python -m venv venv
    if %errorlevel% neq 0 (
        echo Sanal ortam olusturulamadi!
        pause
        exit /b 1
    )
)

REM Sanal ortamı etkinleştir ve bağımlılıkları yükle
echo Sanal ortam etkinlestiriliyor ve gerekli kutuphaneler yukleniyor...
call venv\Scripts\activate.bat
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo Kutuphaneler yuklenemedi!
    pause
    exit /b 1
)

REM Veritabanını başlat (eğer yoksa)
if not exist project\app.db (
    echo Veritabani olusturuluyor ve ornek veriler ekleniyor...
    python project\init_db.py
)

REM Uygulamayı başlat
echo.
echo Uygulama baslatiliyor...
echo Tarayicinizda http://localhost:5000 adresine gidin
echo Uygulamayi durdurmak icin bu pencereyi kapatin veya Ctrl+C tusuna basin
echo.
python project\run.py

REM Sanal ortamdan çık
call venv\Scripts\deactivate.bat
