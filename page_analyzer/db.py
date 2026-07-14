"""Модуль для работы с базой данных"""

import os
import psycopg
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")


def init_db():
    """Создание таблиц при запуске приложения"""
    with get_connection() as conn:
        with conn.cursor() as cur:
            # Проверяем, существует ли таблица urls
            cur.execute("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables
                    WHERE table_name = 'urls'
                );
            """)
            table_exists = cur.fetchone()[0]

            if not table_exists:
                print("📦 Создание таблиц базы данных...")
                cur.execute("""
                    CREATE TABLE urls (
                        id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
                        name VARCHAR(255) UNIQUE NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    );
                """)
                cur.execute("""
                    CREATE TABLE url_checks (
                        id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
                        url_id BIGINT REFERENCES urls(id) ON DELETE CASCADE,
                        status_code INTEGER,
                        h1 VARCHAR(255),
                        title VARCHAR(255),
                        description TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    );
                """)
                cur.execute("CREATE INDEX idx_url_checks_url_id ON url_checks(url_id);")
                cur.execute("CREATE INDEX idx_urls_name ON urls(name);")
                conn.commit()
                print("✅ Таблицы созданы успешно!")
            else:
                print("✅ Таблицы уже существуют")


def get_connection():
    """Получение соединения с БД"""
    return psycopg.connect(DATABASE_URL)


def get_all_urls():
    """Получение всех URL с последней проверкой"""
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT
                    urls.id,
                    urls.name,
                    urls.created_at,
                    MAX(url_checks.created_at) as last_check,
                    url_checks.status_code
                FROM urls
                LEFT JOIN url_checks ON urls.id = url_checks.url_id
                GROUP BY urls.id, urls.name, urls.created_at, url_checks.status_code
                ORDER BY urls.id DESC
            """)
            return cur.fetchall()


def get_url_by_id(url_id):
    """Получение URL по ID"""
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT id, name, created_at FROM urls WHERE id = %s", (url_id,)
            )
            return cur.fetchone()


def get_url_by_name(name):
    """Получение URL по имени"""
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT id, name, created_at FROM urls WHERE name = %s", (name,)
            )
            return cur.fetchone()


def add_url(name):
    """Добавление нового URL"""
    with get_connection() as conn:
        with conn.cursor() as cur:
            created_at = datetime.now()
            cur.execute(
                """
                INSERT INTO urls (name, created_at)
                VALUES (%s, %s)
                RETURNING id
                """,
                (name, created_at),
            )
            url_id = cur.fetchone()[0]
            conn.commit()
            return url_id


def get_url_checks(url_id):
    """Получение всех проверок для URL"""
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT
                    id,
                    created_at,
                    status_code,
                    h1,
                    title,
                    description
                FROM url_checks
                WHERE url_id = %s
                ORDER BY id DESC
            """,
                (url_id,),
            )
            return cur.fetchall()


def add_url_check(url_id, status_code, h1, title, description):
    """Добавление результата проверки URL"""
    with get_connection() as conn:
        with conn.cursor() as cur:
            created_at = datetime.now()
            cur.execute(
                """
                INSERT INTO url_checks (
                    url_id,
                    created_at,
                    status_code,
                    h1,
                    title,
                    description
                )
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                (url_id, created_at, status_code, h1, title, description),
            )
            conn.commit()
