from datetime import datetime

def format_date(date):
    """Tarihi DD.MM.YYYY - HH:MM formatına dönüştür"""
    if isinstance(date, datetime):
        return date.strftime('%d.%m.%Y - %H:%M')
    return date

def get_file_extension(filename):
    """Dosya uzantısını al"""
    return filename.rsplit('.', 1)[1].lower() if '.' in filename else ''

def truncate_text(text, length=100):
    """Metni belirli bir uzunlukta kısalt"""
    if text and len(text) > length:
        return text[:length] + '...'
    return text if text else ''
