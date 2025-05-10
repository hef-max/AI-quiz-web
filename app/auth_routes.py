from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from app.models import User, Quiz, Score
from app import db, login_manager
from sqlalchemy.exc import IntegrityError
import random

auth = Blueprint('auth', __name__)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

questions = [
    {
        "question": "Apa itu Artificial Intelligence (AI)?",
        "options": ["Sistem pintar buatan manusia", "Robot mainan", "Situs web", "Aplikasi biasa"],
        "answer": "Sistem pintar buatan manusia",
        "explanation": "AI adalah sistem yang dirancang untuk meniru kecerdasan manusia dalam menyelesaikan tugas."
    },
    {
        "question": "Library Python apa yang sering digunakan untuk AI?",
        "options": ["Pandas", "TensorFlow", "Django", "Matplotlib"],
        "answer": "TensorFlow",
        "explanation": "TensorFlow adalah library machine learning yang dikembangkan oleh Google untuk AI."
    },
    {
        "question": "Apa itu NLP?",
        "options": ["Neuro Language Python", "Natural Language Processing", "New Language Process", "Node Learning Protocol"],
        "answer": "Natural Language Processing",
        "explanation": "NLP adalah cabang AI yang fokus pada interaksi antara komputer dan bahasa manusia."
    },
    {
        "question": "Contoh AI dalam kehidupan sehari-hari adalah...",
        "options": ["Mesin pencuci", "Smartphone dengan Siri/Google Assistant", "Gelas pintar", "Jam tangan biasa"],
        "answer": "Smartphone dengan Siri/Google Assistant",
        "explanation": "Asisten virtual seperti Siri dan Google Assistant menggunakan teknologi AI untuk memahami dan merespons perintah."
    },
    {
        "question": "Apa hubungan antara machine learning dan AI?",
        "options": ["Keduanya sama persis", "Machine learning adalah subset dari AI", "AI adalah subset dari machine learning", "Keduanya tidak berhubungan"],
        "answer": "Machine learning adalah subset dari AI",
        "explanation": "Machine learning adalah cabang dari AI yang memungkinkan sistem belajar dari data."
    }
]

@auth.route('/quiz', methods=['GET', 'POST'])
@login_required
def quiz():
    # Gunakan session untuk menyimpan status quiz
    if 'quiz_stats' not in session:
        session['quiz_stats'] = {
            'correct': 0,
            'total': 0,
            'asked_questions': []
        }
    
    # Jika sudah menjawab, tampilkan hasil
    if request.method == 'POST':
        user_answer = request.form.get('answer')
        question_idx = int(request.form.get('question_idx'))
        current_question = questions[question_idx]
        
        is_correct = (user_answer == current_question['answer'])
        
        # Update statistik quiz
        session['quiz_stats']['total'] += 1
        if is_correct:
            session['quiz_stats']['correct'] += 1
            current_user.score += 1
            db.session.commit()
            flash("Jawaban Benar! " + current_question['explanation'], "success")
        else:
            flash(f"Jawaban Salah! Jawaban yang benar adalah: {current_question['answer']}. " + 
                  current_question['explanation'], "danger")
        
        # Tambahkan ke daftar pertanyaan yang sudah ditanyakan
        session['quiz_stats']['asked_questions'].append(question_idx)
        session.modified = True
        
        # Redirect ke halaman result
        return render_template('quiz_result.html', 
                              is_correct=is_correct,
                              question=current_question,
                              user_answer=user_answer,
                              stats=session['quiz_stats'])

    # Filter pertanyaan yang belum ditanyakan
    available_questions = [i for i in range(len(questions)) 
                         if i not in session.get('quiz_stats', {}).get('asked_questions', [])]
    
    # Jika semua pertanyaan sudah ditanyakan, reset
    if not available_questions:
        flash("Anda telah menyelesaikan semua pertanyaan! Memulai set baru.", "info")
        session['quiz_stats']['asked_questions'] = []
        available_questions = list(range(len(questions)))
    
    # Pilih pertanyaan secara acak
    question_idx = random.choice(available_questions)
    question = questions[question_idx]
    
    # Acak urutan pilihan jawaban
    options = question['options'].copy()
    random.shuffle(options)

    return render_template('quiz.html', 
                          question=question, 
                          options=options, 
                          question_idx=question_idx,
                          stats=session['quiz_stats'])


@auth.route('/reset_quiz')
@login_required
def reset_quiz():
    # Reset statistik quiz
    session.pop('quiz_stats', None)
    flash("Quiz telah direset!", "info")
    return redirect(url_for('auth.quiz'))


@auth.route('/leaderboard')
def leaderboard():
    # Dapatkan semua pengguna diurutkan berdasarkan skor tertinggi
    users = User.query.order_by(User.score.desc()).all()
    return render_template('leaderboard.html', users=users)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        nickname = request.form['nickname']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            flash('Konfirmasi sandi tidak cocok', 'error')
            return redirect(url_for('auth.register'))

        hashed_password = generate_password_hash(password)
        user = User(username=username, nickname=nickname, password=hashed_password)

        try:
            db.session.add(user)
            db.session.commit()
            flash('Akun berhasil dibuat! Silakan login.', 'success')
            return redirect(url_for('auth.login'))
        except IntegrityError:
            db.session.rollback()
            flash('Username sudah terdaftar. Coba yang lain.', 'error')
            return redirect(url_for('auth.register'))

    return render_template('register.html')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Cari pengguna berdasarkan username
        user = User.query.filter_by(username=username).first()

        # Cek apakah pengguna ada dan passwordnya cocok
        if user and check_password_hash(user.password, password):
            # Jika password benar, login pengguna
            login_user(user)
            flash('Berhasil login!', 'success')
            return redirect(url_for('main.home'))  # redirect ke halaman utama setelah login
        else:
            flash('Username atau password salah!', 'error')
            return redirect(url_for('auth.login'))  # jika login gagal, kembali ke halaman login

    return render_template('login.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Berhasil logout!', 'success')
    return redirect(url_for('main.home'))  # pastikan main.home eksis