import html
import re

import feedparser

from models.job import Job
from models.source import Source


class RedditSource(Source):

    def get_jobs(self):
        # RSS-стрічка нових постів r/forhire
        url = "https://www.reddit.com/r/forhire/new/.rss"

        feed = feedparser.parse(
            url,
            request_headers={
                "User-Agent": "SnirKuryer/0.1 by Chirikson"
            }
        )

        # Якщо RSS не завантажився — показуємо нормальну помилку
        if feed.bozo and not feed.entries:
            raise RuntimeError(f"Помилка Reddit RSS: {feed.bozo_exception}")

        jobs = []

        for entry in feed.entries:
            title = entry.get("title", "Без назви")

            # У r/forhire нас цікавлять ті, хто шукає виконавця,
            # а не фрілансери, які пропонують свої послуги
            if "[hiring]" not in title.lower():
                continue

            description_html = entry.get("summary", "")

            # Прибираємо HTML-теги з опису
            description = re.sub(r"<[^>]+>", " ", description_html)
            description = html.unescape(description)
            description = " ".join(description.split())

            jobs.append(
                Job(
                    title=title,
                    description=description[:700],
                    budget="Look in description",
                    url=entry.get("link", ""),
                    source="Reddit r/forhire"
                )
            )

        return jobs