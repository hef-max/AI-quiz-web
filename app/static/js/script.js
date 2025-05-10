// File: static/js/script.js

// Fungsi untuk menampilkan pesan cuaca di halaman home
function showWeatherInfo() {
    let weatherInfo = document.getElementById("weather-info");
    weatherInfo.style.display = 'block';
}

// Fungsi untuk mengacak urutan soal kuis
function shuffleAnswers() {
    let answers = document.querySelectorAll("input[type='radio']");
    let answersArray = Array.from(answers);
    answersArray.sort(() => Math.random() - 0.5);
    answersArray.forEach(answer => {
        answer.parentElement.appendChild(answer);
    });
}

// Event Listener untuk menangani tombol submit di form login
document.querySelector("#login-form").addEventListener("submit", function(event) {
    // Validasi form jika diperlukan
    let username = document.getElementById("username").value;
    let password = document.getElementById("password").value;
    if (!username || !password) {
        alert("Mohon isi semua kolom!");
        event.preventDefault();
    }
});
