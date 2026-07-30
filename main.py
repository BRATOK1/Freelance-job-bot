import asyncio
import random

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import (
    Message,
    CallbackQuery,
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

from config import BOT_TOKEN
from engine import (
    get_all_jobs,
    mark_jobs_as_seen,
    clear_seen_jobs,
    get_seen_jobs_count,
)


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


user_jobs = {}
user_job_indexes = {}


main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🔎 Find Jobs"),
            KeyboardButton(text="🗑 Clear History"),
        ],
        [
            KeyboardButton(text="📊 Statistics"),
            KeyboardButton(text="ℹ️ Help"),
        ],
    ],
    resize_keyboard=True,
)


def create_job_text(job, index, total):
    description = job.description or "No description provided."

    if len(description) > 1000:
        description = description[:1000] + "..."

    budget = job.budget or "Not specified"

    return (
        f"📄 Job {index + 1} of {total}\n\n"
        f"🌐 Platform: {job.source}\n"
        f"📌 Title: {job.title}\n"
        f"💰 Budget: {budget}\n\n"
        f"📝 Description:\n{description}"
    )


def create_job_keyboard(job):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="⬅️ Previous",
                    callback_data="previous_job",
                ),
                InlineKeyboardButton(
                    text="➡️ Next",
                    callback_data="next_job",
                ),
            ],
            [
                InlineKeyboardButton(
                    text="🌐 Open Job",
                    url=job.url,
                )
            ],
        ]
    )


@dp.message(CommandStart())
async def start_handler(message: Message):
    greetings = [
        "👋 Welcome!",
        "👋 Hello!",
        "👋 Ready to find freelance jobs?",
    ]

    text = (
        f"{random.choice(greetings)}\n\n"
        "I'm your freelance job assistant.\n\n"
        "I collect freelance projects from multiple platforms "
        "and show them in one place.\n\n"
        'Press "🔎 Find Jobs" to get started.'
    )

    await message.answer(
        text,
        reply_markup=main_keyboard,
    )


@dp.message(F.text == "🔎 Find Jobs")
async def find_jobs_handler(message: Message):
    await message.answer("🔍 Searching for new freelance jobs...")

    try:
        jobs = get_all_jobs(limit=10)
    except Exception as error:
        print(f"Job search error: {error}")

        await message.answer(
            "❌ Something went wrong while searching for jobs.\n"
            "Please try again later."
        )
        return

    if not jobs:
        await message.answer(
            "📭 No new jobs found.\n\n"
            "Try again later or clear your viewing history."
        )
        return

    user_id = message.from_user.id

    user_jobs[user_id] = jobs
    user_job_indexes[user_id] = 0

    first_job = jobs[0]

    await message.answer(
        create_job_text(
            first_job,
            0,
            len(jobs),
        ),
        reply_markup=create_job_keyboard(first_job),
    )

    mark_jobs_as_seen(jobs)


@dp.callback_query(F.data == "next_job")
async def next_job_handler(callback: CallbackQuery):
    user_id = callback.from_user.id

    if user_id not in user_jobs:
        await callback.answer(
            "Please search for jobs first.",
            show_alert=True,
        )
        return

    jobs = user_jobs[user_id]
    current_index = user_job_indexes[user_id]

    new_index = (current_index + 1) % len(jobs)
    user_job_indexes[user_id] = new_index

    job = jobs[new_index]

    await callback.message.edit_text(
        create_job_text(
            job,
            new_index,
            len(jobs),
        ),
        reply_markup=create_job_keyboard(job),
    )

    await callback.answer()


@dp.callback_query(F.data == "previous_job")
async def previous_job_handler(callback: CallbackQuery):
    user_id = callback.from_user.id

    if user_id not in user_jobs:
        await callback.answer(
            "Please search for jobs first.",
            show_alert=True,
        )
        return

    jobs = user_jobs[user_id]
    current_index = user_job_indexes[user_id]

    new_index = (current_index - 1) % len(jobs)
    user_job_indexes[user_id] = new_index

    job = jobs[new_index]

    await callback.message.edit_text(
        create_job_text(
            job,
            new_index,
            len(jobs),
        ),
        reply_markup=create_job_keyboard(job),
    )

    await callback.answer()


@dp.message(F.text == "🗑 Clear History")
async def clear_history_handler(message: Message):
    clear_seen_jobs()

    user_id = message.from_user.id
    user_jobs.pop(user_id, None)
    user_job_indexes.pop(user_id, None)

    await message.answer(
        "✅ Viewing history has been cleared.\n\n"
        "Previously viewed jobs can now appear again."
    )


@dp.message(F.text == "📊 Statistics")
async def statistics_handler(message: Message):
    viewed_jobs = get_seen_jobs_count()

    await message.answer(
        "📊 Statistics\n\n"
        f"👁 Viewed jobs: {viewed_jobs}\n"
        "🌐 Connected platforms: 3\n\n"
        "• Reddit\n"
        "• PeoplePerHour\n"
        "• Freelancer"
    )


@dp.message(F.text == "ℹ️ Help")
async def help_handler(message: Message):
    await message.answer(
        "ℹ️ Help\n\n"
        '🔎 "Find Jobs" searches for new freelance projects.\n\n'
        '⬅️ "Previous" and ➡️ "Next" let you browse jobs.\n\n'
        '🌐 "Open Job" opens the original project page.\n\n'
        '🗑 "Clear History" allows previously viewed jobs '
        "to appear again.\n\n"
        '📊 "Statistics" shows the number of viewed jobs.'
    )


async def main():
    print("Freelance Job Bot is running...")

    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot stopped.")