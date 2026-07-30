import requests

from models.job import Job
from models.source import Source


class FreelancerSource(Source):

    def get_jobs(self):
        url = (
            "https://www.freelancer.com/api/projects/0.1/"
            "projects/active/"
        )

        params = {
            "compact": "true",
            "limit": 20,
            "job_details": "true",
            "full_description": "true",
            "sort_field": "time_updated",
            "or_search_query": (
                "python html css javascript "
                "telegram bot sql website landing page"
            )
        }

        headers = {
            "User-Agent": "FreelanceBot/1.0"
        }

        response = requests.get(
            url,
            params=params,
            headers=headers,
            timeout=15
        )

        # Якщо сервер повернув помилку — Python її покаже.
        response.raise_for_status()

        data = response.json()

        projects = data.get("result", {}).get("projects", [])

        jobs = []

        for project in projects:
            project_id = project.get("id")

            title = project.get(
                "title",
                "Без назви"
            )

            description = project.get(
                "description",
                "Опис відсутній"
            )

            budget_data = project.get("budget", {})

            minimum = budget_data.get("minimum")
            maximum = budget_data.get("maximum")

            currency_data = project.get("currency", {})

            currency_code = currency_data.get(
                "code",
                ""
            )

            if minimum is not None and maximum is not None:
                budget = (
                    f"{minimum}–{maximum} "
                    f"{currency_code}"
                )
            else:
                budget = "Look in description"

            job_url = (
                f"https://www.freelancer.com/projects/"
                f"{project_id}"
            )

            jobs.append(
                Job(
                    title=title,
                    description=description[:700],
                    budget=budget,
                    url=job_url,
                    source="Freelancer"
                )
            )

        return jobs