from flask import Blueprint, render_template, request, session, redirect, url_for
from app.utils import get_weather  # pastikan ada fungsi ini di utils.py
from flask_login import login_required

main = Blueprint('main', __name__)

@main.route('/',  methods=['GET', 'POST'])
def home():
    weather_info = None
    city = None
    
    if request.method == 'POST':
        city = request.form.get('city')
        if city:
            weather_info = get_weather(city)
            print(f"Weather data received: {weather_info}")  # Debug info
    
    return render_template('home.html', weather_info=weather_info, city=city)