from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
import os
from project.config import Config
from markupsafe import Markup

# --- إنشاء تطبيق Flask ---
app = Flask(__name__)
app.config.from_object(Config)
Config.init_app(app)

# --- إنشاء فلتر لتحويل السطر الجديد إلى <br> ---
@app.template_filter('nl2br')
def nl2br_filter(s):
    if not s:
        return ''
    return Markup(s.replace('\n', '<br>'))

# --- إنشاء قاعدة البيانات ---
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# --- إنشاء مدير تسجيل الدخول ---
login_manager = LoginManager(app)
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Bu sayfayı görüntülemek için lütfen giriş yapın.'

# --- استيراد النماذج والطرق بعد تهيئة التطبيق ---
from project.models import user, project, equipment, category, comment, activity
from project.routes import auth, projects, equipment, categories, comments

# --- تسجيل Blueprints ---
app.register_blueprint(auth.bp)
app.register_blueprint(projects.bp)
app.register_blueprint(equipment.bp)
app.register_blueprint(categories.bp)
app.register_blueprint(comments.bp)

# --- الصفحة الرئيسية ---
@app.route('/')
def index():
    return render_template('index.html')
