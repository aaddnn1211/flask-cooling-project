import os

class Config:
    # Temel yapılandırma
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'gizli-anahtar-merkezi-sogutma-projesi'
    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    
    # Veritabanı yapılandırması
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(BASEDIR, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Dosya yükleme yapılandırması
    UPLOAD_FOLDER = os.path.join(BASEDIR, 'static/uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB maksimum dosya boyutu
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    
    # Uygulama yapılandırması
    APP_NAME = "Merkezi Soğutma Projeleri Yönetim Sistemi"
    ITEMS_PER_PAGE = 10
    
    @staticmethod
    def init_app(app):
        # Uygulama başlatma sırasında yapılacak ek yapılandırmalar
        if not os.path.exists(Config.UPLOAD_FOLDER):
            os.makedirs(Config.UPLOAD_FOLDER)
