from flask import Flask, render_template, request, flash, redirect, url_for
import os
from dotenv import load_dotenv
from urllib.parse import urlparse
import validators
from page_analyzer.analyzer import analyze_url
from page_analyzer.db import init_db

from page_analyzer.db import (
    add_url,
    get_all_urls,
    get_url_by_id,
    get_url_by_name,
    get_url_checks,
    add_url_check
)

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')

# Создаем таблицы при первом запросе, а не при импорте
_tables_created = False

@app.before_request
def create_tables():
    global _tables_created
    if not _tables_created:
        init_db()
        _tables_created = True


def normalize_url(url):
    """Нормализация URL (удаление протокола и приведение к единому виду)"""
    parsed = urlparse(url)
    return f"{parsed.scheme}://{parsed.netloc}"


def validate_url(url):
    """Валидация URL"""
    errors = []

    if not url or len(url.strip()) == 0:
        errors.append('URL обязателен для заполнения')
    elif len(url) > 255:
        errors.append('URL превышает 255 символов')
    elif not validators.url(url):
        errors.append('Некорректный URL')

    return errors


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/urls', methods=['POST'])
def post_url():
    """Добавление нового URL"""
    url = request.form.get('url', '').strip()

    # Валидация
    errors = validate_url(url)
    if errors:
        for error in errors:
            flash(error, 'danger')
        return render_template('index.html', url_input=url), 422

    # Нормализация URL
    normalized_url = normalize_url(url)

    # Проверка, существует ли URL
    existing_url = get_url_by_name(normalized_url)
    if existing_url:
        flash('Страница уже существует', 'info')
        return redirect(url_for('show_url', id=existing_url[0]))

    # Добавление URL в БД
    try:
        url_id = add_url(normalized_url)
        flash('Страница успешно добавлена', 'success')
        return redirect(url_for('show_url', id=url_id))
    except Exception as e:
        flash(f'Ошибка при добавлении: {str(e)}', 'danger')
        return render_template('index.html', url_input=url), 500


@app.route('/urls')
def show_urls():
    """Список всех URL"""
    urls = get_all_urls()
    return render_template('urls.html', urls=urls)


@app.route('/urls/<int:id>')
def show_url(id):
    """Страница конкретного URL"""
    url_data = get_url_by_id(id)
    if not url_data:
        flash('Страница не найдена', 'danger')
        return redirect(url_for('index'))

    checks = get_url_checks(id)
    return render_template('url.html', url=url_data, checks=checks)


@app.route('/urls/<int:id>/checks', methods=['POST'])
def check_url(id):
    """Запуск проверки URL"""

    url_data = get_url_by_id(id)
    if not url_data:
        flash('Страница не найдена', 'danger')
        return redirect(url_for('index'))

    try:
        # Анализ URL
        result = analyze_url(url_data[1])  # name
        add_url_check(
            id,
            result['status_code'],
            result['h1'],
            result['title'],
            result['description']
        )
        flash('Страница успешно проверена', 'success')
    except Exception as e:
        flash(f'Ошибка при проверке: {str(e)}', 'danger')

    return redirect(url_for('show_url', id=id))


@app.route('/health')
def health():
    return 'OK', 200


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True)
