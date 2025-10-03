from flask import Flask, render_template
import os

app = Flask(__name__)

@app.route('/')
def index():
    context = {
        'backend_url': os.getenv('BACKEND_URL', 'http://localhost:8080')
    }
    return render_template('./index.html', context=context)

@app.route('/users')
def users():
    context = {
        'backend_url': os.getenv('BACKEND_URL', 'http://localhost:8080')
    }
    return render_template('./users.html', context=context)

if __name__ == '__main__':
    app.run(debug=True, template_folder='./templates')