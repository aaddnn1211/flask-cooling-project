from flask import current_app
import os
import uuid
from werkzeug.utils import secure_filename
from datetime import datetime
from PIL import Image

def allowed_file(filename):
    """Dosya uzantısının izin verilen uzantılardan olup olmadığını kontrol et"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

def save_image(file_data):
    """Resim dosyasını kaydet ve dosya yolunu döndür"""
    if file_data and allowed_file(file_data.filename):
        # Güvenli dosya adı oluştur
        filename = secure_filename(file_data.filename)
        
        # Benzersiz bir dosya adı oluştur
        file_ext = os.path.splitext(filename)[1]
        unique_filename = f"{uuid.uuid4().hex}{file_ext}"
        
        # Dosya yolu oluştur
        upload_folder = current_app.config['UPLOAD_FOLDER']
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)
        
        file_path = os.path.join(upload_folder, unique_filename)
        
        # Resmi kaydet
        file_data.save(file_path)
        
        # Resmi optimize et
        try:
            img = Image.open(file_path)
            img.thumbnail((1200, 1200))  # Maksimum boyut
            img.save(file_path, optimize=True, quality=85)
        except Exception as e:
            print(f"Resim optimize edilirken hata: {e}")
        
        return unique_filename
    
    return None
