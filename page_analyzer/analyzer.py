"""Модуль для анализа страниц"""

import requests
import bs4
from requests import ConnectionError, HTTPError


def analyze_url(url):
    """Анализ URL: получение status_code, h1, title, description"""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        soup = bs4.BeautifulSoup(response.text, "html.parser")

        # Извлечение данных
        h1 = soup.find("h1").get_text().strip() if soup.find("h1") else ""
        title = soup.find("title").get_text().strip() if soup.find("title") else ""

        description = ""
        meta_desc = soup.find("meta", attrs={"name": "description"})
        if meta_desc and meta_desc.get("content"):
            description = meta_desc.get("content").strip()

        return {
            "status_code": response.status_code,
            "h1": h1[:255] if h1 else "",  # Ограничиваем длину
            "title": title[:255] if title else "",
            "description": description[:255] if description else "",
        }

    except (ConnectionError, HTTPError, requests.RequestException) as e:
        raise Exception(f"Ошибка при анализе страницы: {str(e)}")
