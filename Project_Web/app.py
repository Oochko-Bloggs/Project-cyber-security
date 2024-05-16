from flask import Flask, render_template, session, request, flash, redirect, url_for, make_response
import os
import io
import re
import sqlite3
import hashlib
import builtwith
import pyotp
import qrcode
import base64
import sys
sys.path.insert(0, '../IP_Location')
from ip_to_geo import IPtoGeo


def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    match = re.match(pattern, email)
    return match is not None


def is_valid_ip(ip_address):
    pattern = r'^(\d{1,3}\.){3}\d{1,3}$'
    match = re.match(pattern, ip_address)
    return True if match else False


def is_valid_password(password):
    if len(password) < 8:
        return False
    if not any(char.isdigit() for char in password):
        return False
    if not any(char.isupper() for char in password):
        return False
    if not any(char.islower() for char in password):
        return False
    return True


def database_connect():
    conn = sqlite3.connect("userdata.db")
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS userdata (
        id INTEGER PRIMARY KEY,
        username VARCHAR(255) NOT NULL,
        password VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL,
        secret_key VARCHAR(255)
    )
    """)
    return conn, c


app = Flask(__name__, template_folder='templates')
app.config['SECRET_KEY'] = b'\xd9\xb0\xdfa\x94\xc4\xb1\x9d\xb6\xec\xc7\xb6\x8c\x12a-'
# os.urandom(16)

SECRET_KEY = 'Bi-huurhun-urjdeg-ni-1000'


@app.route('/', methods=['GET'])
def index():
    if 'email' in session and 'verified' in session:
        return render_template('index.html')
    elif 'email' in session:
        return redirect(url_for('twofactor'))
    else:
        return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        conn, c = database_connect()

        c.execute("SELECT password FROM userdata WHERE email=?", (email,))
        result = c.fetchone()

        if result is None:
            return render_template("login.html", error='Invalid login credentials')

        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        if hashed_password == result[0]:
            # session.permanent = remember_me  # Set session to be permanent if "remember me" is checked
            session['email'] = email
            return redirect(url_for('twofactor'))
        else:
            flash('Invalid login credentials', 'error')
            return redirect(url_for('login'))
    # if GET request
    return render_template("login.html")


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        repeat_password = request.form['repeat_password']

        # Server-side validation
        if not username or not email or not password or not repeat_password:
            flash('Please fill in all fields.', 'error')
            return redirect(url_for('login'))

        elif password != repeat_password:
            flash('Passwords do not match.', 'error')
            return redirect(url_for('login'))

        elif not is_valid_email(email):
            flash('Please enter a valid email address.', 'error')
            return redirect(url_for('login'))

        elif not is_valid_password(password):
            flash('Password must contain at least 8 characters and include at least one uppercase letter, one lowercase letter, and one number.', 'error')
            return redirect(url_for('login'))

        try:
            conn, c = database_connect()

            c.execute("SELECT email FROM userdata WHERE email=?", (email,))
            result = c.fetchone()
            if result:
                flash('Email already registered.', 'error')
                return redirect(url_for('register'))

            hashed_password = hashlib.sha256(password.encode()).hexdigest()

            # Insert the new user
            c.execute("INSERT INTO userdata (username, email, password) VALUES (?, ?, ?)", (username, email, hashed_password))
            conn.commit()
            conn.close()

            # Notify the user and redirect to login page
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))

        except Exception as e:
            flash('An error occurred. Please try again later.', 'error')
            return redirect(url_for('register'))

    return render_template('login.html')


@app.route('/logout', methods=['POST'])
def logout():
    # Clear the user's session to log them out
    session.clear()
    return redirect('/')


@app.route('/twofactor', methods=['GET', 'POST'])
def twofactor():
    if request.method == 'POST':
        otp_code = request.form['otp']
        # get email from session. I couldn't find a way to send login form values to /twofactor when redirecting :((
        email = session.get('email')
        try:
            conn, c = database_connect()
            c.execute("SELECT secret_key FROM userdata WHERE email=?", (email,))
            secret_key = c.fetchone()

        except Exception as e:
            flash('An error occurred. Please try again later.', 'error')
            return redirect(url_for('twofactor'))

        if secret_key == (None,):
            flash("You should scan the QRcode!", 'error')
            return redirect(url_for('twofactor'))

        totp = pyotp.TOTP(secret_key[0])

        if totp.verify(otp_code):
            session['verified'] = True
            return redirect('/')
        else:
            flash('Invalid OTP code', 'error')
            return redirect(url_for('twofactor'))

    else:
        email = session.get('email')
        try:
            conn, c = database_connect()
            c.execute("SELECT secret_key FROM userdata WHERE email=?", (email,))
            secret_key = c.fetchone()

        except Exception as e:
            flash('An error occurred. Please try again later.', 'error')
            return redirect(url_for('twofactor'))

        if secret_key == (None,):
            # Generate a new secret key for the user
            secret_key = pyotp.random_base32()
            c.execute("UPDATE userdata SET secret_key = ? WHERE email = ?", (secret_key, email))
            conn.commit()
            conn.close()
            # Generate a provisioning URI for the user to scan with their authenticator app
            provisioning_uri = pyotp.totp.TOTP(secret_key).provisioning_uri(name='Hicheejiinoo', issuer_name='SICT')
            qr_code = qrcode.make(provisioning_uri)
            # Convert the image to a base64-encoded string
            qr_code_io = io.BytesIO()
            qr_code.save(qr_code_io, 'PNG')
            qr_code_io.seek(0)
            qr_code_b64 = base64.b64encode(qr_code_io.getvalue()).decode('utf-8')
            return render_template('base.html', qr_code=qr_code_b64)
        return render_template('base.html')


@app.route('/ipgeo', methods=['POST'])
def ipgeo():
    ip_address = request.form['ip_address']
    if not is_valid_ip(ip_address):
        location = IPtoGeo(ip_address)
        country = location.country
        city = location.city
        time_zone = location.time_zone
        latitude = location.latitude
        longitude = location.longitude

        maps_url = f"https://www.openstreetmap.org/?mlat={location.latitude}&mlon={location.longitude}"
        return render_template('index.html', time_zone=time_zone, latitude=latitude, longitude=longitude, city=city, country=country, maps_url=maps_url)
    flash("Invalid IP address!", 'error')
    return redirect('/')


@app.route('/webtech', methods=['POST'])
def webtech():
    url = request.form['ip_address']
    results = builtwith.builtwith(url)
    return render_template('index.html', results=results.items())


if __name__ == '__main__':
    app.run(debug=True)
