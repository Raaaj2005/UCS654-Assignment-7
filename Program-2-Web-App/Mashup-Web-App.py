import os
import sys
import zipfile
from flask import Flask, render_template_string, request, flash
from flask_mail import Mail, Message
from yt_dlp import YoutubeDL
from pydub import AudioSegment

app = Flask(__name__)
app.secret_key = "secret_key"

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'rbrar_be23@thapar.edu'
app.config['MAIL_PASSWORD'] = 'cfvm efgd dhpj orf'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)

HTML_FORM = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Audio Mashup Service</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            margin: 0;
        }
        .container {
            background: rgba(255, 255, 255, 0.9);
            padding: 40px;
            border-radius: 15px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.2);
            width: 400px;
            text-align: center;
        }
        h2 { color: #4a4a4a; margin-bottom: 25px; }
        .form-group { margin-bottom: 15px; text-align: left; }
        label { display: block; margin-bottom: 5px; color: #666; font-weight: 600; }
        input[type="text"], input[type="number"], input[type="email"] {
            width: 100%;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 5px;
            box-sizing: border-box;
        }
        input[type="submit"] {
            background-color: #f39c12;
            color: white;
            padding: 12px 20px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            width: 100%;
            font-size: 16px;
            font-weight: bold;
            margin-top: 10px;
            transition: background 0.3s;
        }
        input[type="submit"]:hover { background-color: #e67e22; }
        .flash-message {
            margin-top: 20px;
            padding: 10px;
            background-color: #d4edda;
            color: #155724;
            border-radius: 5px;
            font-size: 14px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h2>Mashup Generator</h2>
        <form method="POST">
            <div class="form-group">
                <label>Singer Name</label>
                <input type="text" name="singer" placeholder="e.g. Sharry Mann" required>
            </div>
            <div class="form-group">
                <label>Number of Videos</label>
                <input type="number" name="count" value="20" min="11" required>
            </div>
            <div class="form-group">
                <label>Duration of Each (sec)</label>
                <input type="number" name="duration" value="30" min="21" required>
            </div>
            <div class="form-group">
                <label>Your Email Address</label>
                <input type="email" name="email" placeholder="email@example.com" required>
            </div>
            <input type="submit" value="Generate & Send Email">
        </form>
        {% with messages = get_flashed_messages() %}
          {% if messages %}
            {% for message in messages %}
              <div class="flash-message"><strong>{{ message }}</strong></div>
            {% endfor %}
          {% endif %}
        {% endwith %}
    </div>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        singer = request.form['singer']
        count = int(request.form['count'])
        duration = int(request.form['duration'])
        recipient = request.form['email']
        
        output_mp3 = "result.mp3"
        output_zip = "result.zip"
        
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': 'temp_%(id)s.%(ext)s',
            'quiet': True,
        }
        
        temp_files = []
        try:
            with YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(f"ytsearch{count}:{singer}", download=True)
                for entry in info['entries']:
                    temp_files.append(f"temp_{entry['id']}.mp3")
            
            combined = AudioSegment.empty()
            for file in temp_files:
                if os.path.exists(file):
                    audio = AudioSegment.from_file(file)
                    combined += audio[:duration * 1000]
            
            combined.export(output_mp3, format="mp3")
            
            with zipfile.ZipFile(output_zip, 'w') as zf:
                zf.write(output_mp3)
            
            msg = Message("Your Mashup Result", sender=app.config['MAIL_USERNAME'], recipients=[recipient])
            msg.body = "Please find your requested mashup attached as a zip file."
            with app.open_resource(output_zip) as fp:
                msg.attach(output_zip, "application/zip", fp.read())
            
            mail.send(msg)
            flash("Success! ZIP file sent to your email.")
            
        except Exception as e:
            flash(f"Error: {str(e)}")
        finally:
            for file in temp_files + [output_mp3, output_zip]:
                if os.path.exists(file):
                    os.remove(file)
                    
    return render_template_string(HTML_FORM)

if __name__ == '__main__':
    app.run(debug=True)
