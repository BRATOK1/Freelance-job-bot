import html
import re

import feedparser

from urllib.parse import quote_plus
from models.job import Job
from models.source import Source


class PeoplePerHourSource(Source):

    def get_jobs(self):
        # За кожним словом PeoplePerHour поверне окрему RSS-стрічку.
        search_terms = [
            "html",
            "css",
            "javascript",
            "python",
            "telegram bot",
            "sql"
        ]

        jobs = []
        added_urls = set()

        for term in search_terms:
            encoded_term = quote_plus(term)
            url = f"https://www.peopleperhour.com/feed/jobs?term={encoded_term}"

            feed = feedparser.parse(
                url,
                request_headers={
                    "User-Agent": "SnirKuryer/0.1"
                }
            )

            if feed.bozo and not feed.entries:
                print(
                    f"PeoplePerHour не завантажив '{term}': "
                    f"{feed.bozo_exception}"
                )
                continue

            for entry in feed.entries:
                job_url = entry.get("link", "")

                # Одне замовлення може потрапити в кілька пошуків.
                # Так ми не покажемо його декілька разів.
                if not job_url or job_url in added_urls:
                    continue

                added_urls.add(job_url)

                title = entry.get("title", "Без назви")
                description_html = entry.get(
                    "summary",
                    entry.get("description", "")
                )

                # Прибираємо HTML-теги з опису.
                description = re.sub(
                    r"<[^>]+>",
                    " ",
                    description_html
                )

                description = html.unescape(description)
                description = " ".join(description.split())

                # Намагаємося знайти бюджет у назві або описі.
                full_text = f"{title} {description}"

                budget_match = re.search(
                    r"(?:£|\$|€)\s?\d+(?:[.,]\d+)?"
                    r"(?:\s?[-–]\s?(?:£|\$|€)?\s?\d+(?:[.,]\d+)?)?",
                    full_text
                )

                if budget_match:
                    budget = budget_match.group(0)
                else:
                    budget = "Look in description"

                jobs.append(
                    Job(
                        title=title,
                        description=description[:700],
                        budget=budget,
                        url=job_url,
                        source="PeoplePerHour"
                    )
                )

        return jobs