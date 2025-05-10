# app/models.py
from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    nickname = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    score = db.Column(db.Integer, default=0)  # untuk leaderboard

    def __repr__(self):
        return f'<User {self.username}>'

    # Metode yang diperlukan Flask-Login
    def is_active(self):
        return True  # Kamu bisa sesuaikan jika ada logika khusus

    def is_authenticated(self):
        return True  # Cek apakah pengguna telah login, biasanya ini True jika pengguna berhasil login

    def is_anonymous(self):
        return False  # Jika tidak menggunakan mode anonim, ini False

    def get_id(self):
        return str(self.id)  # Flask-Login membutuhkan metode ini untuk mendapatkan ID pengguna

class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(200), nullable=False)
    options = db.Column(db.PickleType, nullable=False)
    answer = db.Column(db.String(100), nullable=False)

class Score(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    score = db.Column(db.Integer, default=0)
