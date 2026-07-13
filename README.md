# Анализатор страниц

## Статус:
[![Actions Status](https://github.com/artemcherepanov2357/python-project-83/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/artemcherepanov2357/python-project-83/actions)

---

## Демо:
[Посмотреть на Render.com](https://python-project-83-2enb.onrender.com/)

---

## Описание:
**Анализатор страниц** – это веб-приложение, разработанное с использованием Flask, которое позволяет пользователям быстро и бесплатно проверять веб-сайты на SEO-пригодность.

---

## Установка:
### Клонируем репозиторий
```
git clone https://github.com/artemcherepanov2357/python-project-83.git
cd python-project-83
```
### Установка uv (если не установлен):
```
curl -LsSf https://astral.sh/uv/install.sh | sh
```
### Установите зависимости:
```
make install
```
### Создайте .env файл и настройте как в примере:
```
SECRET_KEY=ваш_секретный_ключ
DATABASE_URL=postgresql://пользователь:пароль@localhost:5432/имя_базы
```
### Создайте таблицы в базе данных:
```
make db-init
```
### Запустите приложение на локальном сервере:
```commandline
make dev
```
