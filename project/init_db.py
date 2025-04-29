from project.app import db, app
from project.models.user import User
from project.models.category import Category
from werkzeug.security import generate_password_hash
import os


# Veritabanını oluştur
with app.app_context():
    # Veritabanı tablolarını oluştur
    db.create_all()
    
    # Yönetici kullanıcıları oluştur
    admin_users = [
        {
            'username': 'admin1',
            'email': 'admin1@example.com',
            'full_name': 'Yönetici Bir',
            'password': 'admin123',
            'role': 'admin'
        },
        {
            'username': 'admin2',
            'email': 'admin2@example.com',
            'full_name': 'Yönetici İki',
            'password': 'admin123',
            'role': 'admin'
        },
        {
            'username': 'admin3',
            'email': 'admin3@example.com',
            'full_name': 'Yönetici Üç',
            'password': 'admin123',
            'role': 'admin'
        },
        {
            'username': 'admin4',
            'email': 'admin4@example.com',
            'full_name': 'Yönetici Dört',
            'password': 'admin123',
            'role': 'admin'
        },
        {
            'username': 'admin5',
            'email': 'admin5@example.com',
            'full_name': 'Yönetici Beş',
            'password': 'admin123',
            'role': 'admin'
        }
    ]
    
    # Normal kullanıcıları oluştur
    regular_users = [
        {
            'username': 'user1',
            'email': 'user1@example.com',
            'full_name': 'Kullanıcı Bir',
            'password': 'user123',
            'role': 'user'
        },
        {
            'username': 'user2',
            'email': 'user2@example.com',
            'full_name': 'Kullanıcı İki',
            'password': 'user123',
            'role': 'user'
        },
        {
            'username': 'user3',
            'email': 'user3@example.com',
            'full_name': 'Kullanıcı Üç',
            'password': 'user123',
            'role': 'user'
        },
        {
            'username': 'user4',
            'email': 'user4@example.com',
            'full_name': 'Kullanıcı Dört',
            'password': 'user123',
            'role': 'user'
        }
    ]
    
    # Kullanıcıları veritabanına ekle
    for user_data in admin_users + regular_users:
        # Kullanıcı zaten var mı kontrol et
        existing_user = User.query.filter_by(username=user_data['username']).first()
        if not existing_user:
            user = User(
                username=user_data['username'],
                email=user_data['email'],
                full_name=user_data['full_name'],
                password=user_data['password'],
                role=user_data['role']
            )
            db.session.add(user)
    
    # Temel kategorileri oluştur
    categories = [
        {'name': 'Evaporatörler', 'description': 'Soğutucu akışkanın buharlaştığı ısı değiştiricileri'},
        {'name': 'Kompresörler', 'description': 'Soğutucu akışkanı sıkıştıran cihazlar'},
        {'name': 'Kondensatörler', 'description': 'Soğutucu akışkanın yoğunlaştığı ısı değiştiricileri'},
        {'name': 'Genleşme Valfleri', 'description': 'Soğutucu akışkanın basıncını düşüren cihazlar'},
        {'name': 'Borular ve Bağlantılar', 'description': 'Soğutucu akışkanın dolaştığı borular ve bağlantı elemanları'},
        {'name': 'Kontrol Sistemleri', 'description': 'Soğutma sistemini kontrol eden elektronik cihazlar'}
    ]
    
    # Kategorileri veritabanına ekle
    for category_data in categories:
        # Kategori zaten var mı kontrol et
        existing_category = Category.query.filter_by(name=category_data['name']).first()
        if not existing_category:
            category = Category(
                name=category_data['name'],
                description=category_data['description']
            )
            db.session.add(category)
    
    # Değişiklikleri kaydet
    db.session.commit()
    
    print("Veritabanı başarıyla oluşturuldu ve örnek veriler eklendi.")
    print("Yönetici kullanıcıları: admin1, admin2, admin3, admin4, admin5 (şifre: admin123)")
    print("Normal kullanıcılar: user1, user2, user3, user4 (şifre: user123)")
