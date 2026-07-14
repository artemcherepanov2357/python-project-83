"""Модуль для анализа страниц"""

import requests
import bs4
from requests import RequestException


def analyze_url(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        soup = bs4.BeautifulSoup(response.text, "html.parser")

        h1_tag = soup.find("h1")
        h1 = h1_tag.get_text().strip() if h1_tag else ""

        title_tag = soup.find("title")
        title = title_tag.get_text().strip() if title_tag else ""

        description = ""
        meta_desc = soup.find("meta", attrs={"name": "description"})
        if meta_desc and meta_desc.get("content"):
            description = meta_desc.get("content").strip()

        return {
            "status_code": response.status_code,
            "h1": h1[:255] if h1 else "",
            "title": title[:255] if title else "",
            "description": description[:255] if description else "",
        }

    except RequestException as e:
        print(f"❌ Ошибка: {e}")
        raise Exception(str(e))
