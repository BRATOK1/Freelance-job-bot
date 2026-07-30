from engine import get_all_jobs

jobs = get_all_jobs()

print(f"Знайдено замовлень: {len(jobs)}")

for job in jobs:
    print("=" * 50)
    print(f"Джерело: {job.source}")
    print(f"Назва: {job.title}")
    print(f"Опис: {job.description}")
    print(f"Бюджет: {job.budget}")
    print(f"Посилання: {job.url}")