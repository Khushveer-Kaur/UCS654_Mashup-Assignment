from flask import Flask, request
import subprocess
import zipfile
import smtplib
from email.message import EmailMessage
import re
import os
import threading

app = Flask(__name__)

# ---------------- EMAIL VALIDATION ----------------
def valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)


# ---------------- HOME PAGE ----------------
@app.route('/')
def home():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Mashup Generator</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background: linear-gradient(to right, #4e73df, #1cc88a);
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
            }
            .container {
                background: white;
                padding: 30px;
                border-radius: 10px;
                box-shadow: 0 4px 15px rgba(0,0,0,0.2);
                width: 350px;
                text-align: center;
            }
            h2 {
                margin-bottom: 20px;
                color: #333;
            }
            input {
                width: 90%;
                padding: 8px;
                margin: 8px 0;
                border-radius: 5px;
                border: 1px solid #ccc;
            }
            button {
                background-color: #4e73df;
                color: white;
                padding: 10px;
                width: 95%;
                border: none;
                border-radius: 5px;
                cursor: pointer;
                font-size: 15px;
            }
            button:hover {
                background-color: #2e59d9;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h2>Mashup Generator</h2>
            <form method="POST" action="/generate">
                <input type="text" name="singer" placeholder="Singer Name" required><br>
                <input type="number" name="videos" placeholder="Number of Videos (>10)" required><br>
                <input type="number" name="duration" placeholder="Duration in Seconds (>20)" required><br>
                <input type="email" name="email" placeholder="Email Address" required><br>
                <button type="submit">Generate Mashup</button>
            </form>
        </div>
    </body>
    </html>
    '''


# ---------------- BACKGROUND FUNCTION ----------------
def run_mashup_and_email(singer, videos, duration, email):
    output_file = "result.mp3"

    try:
        # Run mashup script
        subprocess.run(
            ["python", "102303327.py", singer, videos, duration, output_file]
        )

        # Create ZIP
        zip_name = "mashup.zip"
        with zipfile.ZipFile(zip_name, 'w') as zipf:
            zipf.write(output_file)

        # Send Email
        msg = EmailMessage()
        msg['Subject'] = "Your Mashup File"
        msg['From'] = "kkaur3_be23@thapar.edu"
        msg['To'] = email
        msg.set_content("Your mashup file is attached.")

        with open(zip_name, 'rb') as f:
            msg.add_attachment(
                f.read(),
                maintype='application',
                subtype='zip',
                filename=zip_name
            )

        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login("kkaur3_be23@thapar.edu", "tasnjcdhlfvmmyuo")
        server.send_message(msg)
        server.quit()

        # Cleanup
        if os.path.exists(output_file):
            os.remove(output_file)
        if os.path.exists(zip_name):
            os.remove(zip_name)

        print("Email sent successfully!")

    except Exception as e:
        print("Background Error:", e)


# ---------------- GENERATE ROUTE ----------------
@app.route('/generate', methods=['POST'])
def generate():
    singer = request.form['singer']
    videos = request.form['videos']
    duration = request.form['duration']
    email = request.form['email']

    if not valid_email(email):
        return "<h3 style='color:red;text-align:center;'>Invalid Email ID!</h3>"

    # Start background thread
    thread = threading.Thread(
        target=run_mashup_and_email,
        args=(singer, videos, duration, email)
    )
    thread.start()

    return "<h3 style='color:green;text-align:center;'>Mashup is being generated. You will receive email shortly!</h3>"


# ---------------- RUN APP ----------------
if __name__ == "__main__":
    app.run(debug=False)


