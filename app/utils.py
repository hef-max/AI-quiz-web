import random
from app.models import User
import requests
from datetime import datetime, timedelta
import pytz

import requests
from datetime import datetime, timedelta
import pytz

def get_weather(city):
    API_KEY = "e353144d7e824bb091ca97ef790c4ae0"  # ganti dengan API key kamu dari OpenWeatherMap
    BASE_URL = "https://api.openweathermap.org/data/2.5/forecast"

    try:
        params = {
            'q': city,
            'appid': API_KEY,
            'units': 'metric',
            'lang': 'id'  # Dapatkan deskripsi cuaca dalam bahasa Indonesia
        }

        response = requests.get(BASE_URL, params=params)
        data = response.json()

        if response.status_code != 200 or 'list' not in data:
            print(f"[ERROR] Weather API returned status code {response.status_code}")
            if 'message' in data:
                print(f"[ERROR] API message: {data['message']}")
            return None

        # Kalkulasi ramalan cuaca untuk 3 hari
        weather_by_day = {}
        now = datetime.now(pytz.timezone('Asia/Jakarta'))
        today = now.strftime('%Y-%m-%d')
        
        # Dapatkan tanggal untuk 3 hari ke depan
        forecast_dates = [
            (now + timedelta(days=i)).strftime('%Y-%m-%d') 
            for i in range(3)
        ]
        
        day_names_id = {
            'Monday': 'Senin',
            'Tuesday': 'Selasa',
            'Wednesday': 'Rabu',
            'Thursday': 'Kamis',
            'Friday': 'Jumat',
            'Saturday': 'Sabtu',
            'Sunday': 'Minggu'
        }

        # Inisialisasi dictionary untuk menyimpan data tiap hari
        for date in forecast_dates:
            weather_by_day[date] = {
                'day_temps': [],    # Suhu siang (6:00-18:00)
                'night_temps': [],  # Suhu malam (18:00-6:00)
                'descriptions': []  # Deskripsi cuaca
            }

        # Mengisi data dari API
        for entry in data['list']:
            dt_txt = entry['dt_txt']
            date = dt_txt.split()[0]
            time = dt_txt.split()[1]
            
            # Hanya proses data untuk 3 hari ke depan
            if date in forecast_dates:
                temp = entry['main']['temp']
                desc = entry['weather'][0]['description']
                
                # Tentukan apakah siang atau malam berdasarkan waktu
                hour = int(time.split(':')[0])
                if 6 <= hour < 18:  # Siang hari (6:00-18:00)
                    weather_by_day[date]['day_temps'].append(temp)
                else:  # Malam hari (18:00-6:00)
                    weather_by_day[date]['night_temps'].append(temp)
                
                weather_by_day[date]['descriptions'].append(desc)

        # Membuat hasil akhir
        result = []
        for i, date in enumerate(forecast_dates):
            day_temps = weather_by_day[date]['day_temps']
            night_temps = weather_by_day[date]['night_temps']
            descriptions = weather_by_day[date]['descriptions']
            
            # Jika tidak ada data untuk siang/malam, gunakan data yang tersedia
            if not day_temps and night_temps:
                day_temps = night_temps
            elif not night_temps and day_temps:
                night_temps = day_temps
            
            # Jika tidak ada data sama sekali untuk hari tertentu, lanjutkan ke hari berikutnya
            if not day_temps and not night_temps:
                continue
                
            # Hitung suhu rata-rata atau gunakan nilai default
            avg_day_temp = round(sum(day_temps) / len(day_temps), 1) if day_temps else None
            avg_night_temp = round(sum(night_temps) / len(night_temps), 1) if night_temps else None
            
            # Tentukan deskripsi cuaca yang paling sering muncul
            if descriptions:
                desc_count = {}
                for desc in descriptions:
                    if desc in desc_count:
                        desc_count[desc] += 1
                    else:
                        desc_count[desc] = 1
                most_common_desc = max(desc_count, key=desc_count.get)
            else:
                most_common_desc = "Tidak ada data"
            
            # Dapatkan nama hari dalam bahasa Indonesia
            day_name_en = (now + timedelta(days=i)).strftime('%A')
            day_name = day_names_id.get(day_name_en, day_name_en)
            
            result.append({
                'date': date,
                'day_name': day_name,
                'temp_day': avg_day_temp if avg_day_temp is not None else 0,
                'temp_night': avg_night_temp if avg_night_temp is not None else 0,
                'description': most_common_desc
            })

        return result

    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Network error: {e}")
        return None
    except KeyError as e:
        print(f"[ERROR] Invalid API response structure. Missing key: {e}")
        return None
    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}")
        return None


# Fungsi untuk mengacak urutan jawaban kuis
def shuffle_answers(answers):
    """
    Mengacak urutan jawaban dalam sebuah list.
    """
    random.shuffle(answers)
    return answers

# Fungsi untuk memformat tanggal dalam format yang lebih ramah pengguna
def format_date(date):
    """
    Memformat tanggal dalam format yang lebih mudah dibaca: "Senin, 1 Januari 2023"
    """
    return date.strftime('%A, %d %B %Y')

# Fungsi untuk validasi apakah input username unik (contoh sederhana)
def is_username_unique(username, db_session):
    """
    Mengecek apakah username sudah digunakan di database.
    """
    user = db_session.query(User).filter_by(username=username).first()
    return user is None
