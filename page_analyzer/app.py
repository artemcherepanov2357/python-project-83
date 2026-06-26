from flask import Flask, render_template, request, flash, redirect, url_for
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/urls', methods=['POST'])
def post_url():
    url = request.form.get('url')

    if not url or not url.startswith(('http://', 'https://')):
        flash('Некорректный URL. Введите адрес, начинающийся с http:// или https://', 'danger')
        return render_template('index.html', url_input=url), 422

    flash(f'Страница {url} добавлена', 'success')
    return redirect(url_for('index'))


@app.route('/health')
def health():
    return 'OK', 200


if __name__ == '__main__':
    app.run(debug=True)
