# YouTube Audio Mashup Project

This repository contains a two-part solution developed for the Predictive Analytics assignment (UCS654). The project automates the process of searching for a singer's videos on YouTube, extracting audio segments, and merging them into a single mashup file.

---

## 👤 Author Details
* **Name**: Raj Fatehveer Singh Brar
* **Roll Number**: 102317090
  
---

## 📂 Project Structure

* **Program-1-Script/**: Contains the standalone Python script (`102317090.py`) for command-line execution.
* **Program-2-Web-App/**: Contains the Flask web application (`Mashup-Web-App.py`) for a GUI-based experience.
* **requirements.txt**: Lists all Python dependencies required for the project.
* **.gitignore**: Prevents temporary audio files and MP3 outputs from being uploaded to the repository.
* **Procfile**: Configuration file required for cloud deployment (e.g., Render).

---

## 🚀 Program 1: Local Command Line Script

This script downloads the first N videos of a specified singer, extracts the first X seconds of audio from each, and merges them into one MP3.

### Usage
python Program-1-Script/102317090.py <SingerName> <NumberOfVideos> <DurationInSeconds> <OutputFileName>

**Example:**
python Program-1-Script/102317090.py "Sunidhi Chauhan" 11 25 result.mp3

---

## 🌐 Program 2: Web Service (Flask)

A web-based interface that processes mashup requests and delivers the final output via email.

### Features
* **Interactive Form**: Inputs for Singer, Video Count, Duration, and Recipient Email.
* **Zip Delivery**: The result is compressed and sent as a ZIP attachment.
* **Secure SMTP**: Uses Flask-Mail with Google App Passwords for secure delivery.

### Local Execution
1. Update your credentials in Program-2-Web-App/Mashup-Web-App.py.
2. Run the server: python Program-2-Web-App/Mashup-Web-App.py
3. Open: http://127.0.0.1:5000

## 🌐 Live Web Service
# You can access the live application here: https://mashup-web-app-mi8y.onrender.com
# (Note: If the link is slow to load, the server is "waking up" from its sleep state.)

---

## 🛠️ Installation & Setup

1. **FFmpeg**: Ensure FFmpeg is installed and added to your system environment variables.
2. **Dependencies**: Install the required Python packages:
   pip install -r requirements.txt

The project utilizes: flask, flask-mail, yt-dlp, pydub, and gunicorn.
