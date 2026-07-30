import json
import os
from collections import defaultdict

from sources.freelancer import FreelancerSource
from sources.peopleperhour import PeoplePerHourSource
from sources.reddit import RedditSource


SEEN_JOBS_FILE = "seen_jobs.json"


def normalize_url(url):
    return url.strip().rstrip("/")


def remove_duplicates(jobs):
    unique_jobs = []
    seen_urls = set()

    for job in jobs:
        normalized_url = normalize_url(job.url)

        if not normalized_url:
            continue

        if normalized_url in seen_urls:
            continue

        seen_urls.add(normalized_url)
        unique_jobs.append(job)

    return unique_jobs


def load_seen_jobs():
    if not os.path.exists(SEEN_JOBS_FILE):
        return set()

    try:
        with open(SEEN_JOBS_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

        return set(data)

    except (json.JSONDecodeError, OSError):
        return set()


def save_seen_jobs(seen_urls):
    with open(SEEN_JOBS_FILE, "w", encoding="utf-8") as file:
        json.dump(
            list(seen_urls),
            file,
            ensure_ascii=False,
            indent=4
        )


def remove_seen_jobs(jobs):
    seen_urls = load_seen_jobs()
    new_jobs = []

    for job in jobs:
        normalized_url = normalize_url(job.url)

        if normalized_url in seen_urls:
            continue

        new_jobs.append(job)

    return new_jobs


def select_balanced_jobs(jobs, limit=10):
    jobs_by_source = defaultdict(list)

    for job in jobs:
        jobs_by_source[job.source].append(job)

    selected_jobs = []
    source_names = list(jobs_by_source.keys())

    while len(selected_jobs) < limit:
        job_added = False

        for source_name in source_names:
            source_jobs = jobs_by_source[source_name]

            if source_jobs and len(selected_jobs) < limit:
                selected_jobs.append(source_jobs.pop(0))
                job_added = True

        if not job_added:
            break

    return selected_jobs


def mark_jobs_as_seen(jobs):
    seen_urls = load_seen_jobs()

    for job in jobs:
        seen_urls.add(normalize_url(job.url))

    save_seen_jobs(seen_urls)


def get_all_jobs(limit=10):
    sources = [
        RedditSource(),
        PeoplePerHourSource(),
        FreelancerSource()
    ]

    all_jobs = []

    for source in sources:
        try:
            jobs = source.get_jobs()
            all_jobs.extend(jobs)

            print(
                f"{source.__class__.__name__}: "
                f"отримано {len(jobs)} замовлень"
            )

        except Exception as error:
            print(
                f"Не вдалося отримати дані з "
                f"{source.__class__.__name__}: {error}"
            )

    unique_jobs = remove_duplicates(all_jobs)
    new_jobs = remove_seen_jobs(unique_jobs)

    selected_jobs = select_balanced_jobs(
        new_jobs,
        limit=limit
    )

    print(f"Усього отримано: {len(all_jobs)}")
    print(f"Унікальних: {len(unique_jobs)}")
    print(f"Нових: {len(new_jobs)}")
    print(f"Вибрано для показу: {len(selected_jobs)}")

    return selected_jobs

def clear_seen_jobs():
    save_seen_jobs(set())


def get_seen_jobs_count():
    return len(load_seen_jobs())