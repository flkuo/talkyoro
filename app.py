import os
# Get the database URL from Render environment variables
# If it doesn't exist (local), use the local site.db file
database_url = os.environ.get('DATABASE_URL')
if database_url and database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

app = Flask(__name__)

# --- Configuration ---
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SECRET_KEY'] = 'professional-info-web-2026'
app.config['SQLALCHEMY_DATABASE_URI'] = database_url or 'sqlite:///' + os.path.join(basedir, 'instance', 'site.db')
app.config['UPLOAD_FOLDER'] = os.path.join(basedir, 'static', 'uploads')

db = SQLAlchemy(app)
with app.app_context():
    db.create_all()
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# --- Database Model ---
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    image_file = db.Column(db.String(100), nullable=True)
    link_url = db.Column(db.String(500), nullable=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=True)
    subcategories = db.relationship('Category', backref=db.backref('parent', remote_side=[id]), lazy=True)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# --- Routes ---
@app.route('/')
def index():
    # Fetch top-level categories for the main grid/menu
    main_cats = Category.query.filter_by(parent_id=None).all()
    return render_template('index.html', categories=main_cats)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form.get('username')).first()
        if user and check_password_hash(user.password, request.form.get('password')):
            login_user(user)
            return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/add_category', methods=['GET', 'POST'])
@login_required
def add_category():
    if request.method == 'POST':
        file = request.files.get('image')
        filename = secure_filename(file.filename) if file and file.filename != '' else None
        if filename:
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        new_cat = Category(
            name=request.form.get('name'),
            parent_id=int(request.form.get('parent_id')) if request.form.get('parent_id') else None,
            image_file=filename,
            link_url=request.form.get('link_url')
        )
        db.session.add(new_cat)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_category.html', categories=Category.query.all())

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        if not User.query.filter_by(username='admin').first():
            db.session.add(User(username='admin', password=generate_password_hash('1234')))
            db.session.commit()
    app.run(debug=True)