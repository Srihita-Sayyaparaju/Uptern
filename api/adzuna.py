import os
import re
import sqlite3
import requests
from dotenv import load_dotenv

load_dotenv()

APP_ID = os.getenv("ADZUNA_APP_ID")
APP_KEY = os.getenv("ADZUNA_APP_KEY")

DATABASE = "database/internships.db"

queries = [
    "intern",
    "software intern",
    "software engineer intern",
    "software developer intern",
    "python intern",
    "java intern",
    "frontend intern",
    "backend intern",
    "full stack intern",
    "web developer intern",
    "machine learning intern",
    "artificial intelligence intern",
    "data science intern",
    "data analyst intern",
    "cyber security intern",
    "cloud intern",
    "devops intern",
    "ui ux intern",
    "android intern",
    "ios intern",
    "react intern",
    "node js intern",
    "django intern",
    "flask intern",
    "spring boot intern",
    "sql intern",
    "database intern",
    "embedded systems intern",
    "electronics intern",
    "qa intern",
    "testing intern",
    "automation intern",
    "business analyst intern",
    "product management intern",
    "blockchain intern",
    "game developer intern",
    "computer vision intern",
    "nlp intern",
    "deep learning intern",
    "robotics intern",
    "network engineer intern",
    "information security intern"
]

conn = sqlite3.connect(DATABASE)
cursor = conn.cursor()

all_jobs = []
seen_jobs = set()

for query in queries:

    print(f"\n========== Searching: {query} ==========")

    for page in range(1, 4):

        print(f"Fetching page {page}...")

        url = f"https://api.adzuna.com/v1/api/jobs/in/search/{page}"

        params = {
            "app_id": APP_ID,
            "app_key": APP_KEY,
            "results_per_page": 20,
            "what": query
        }

        try:
            response = requests.get(url, params=params, timeout=15)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"Error fetching data: {e}")
            continue

        data = response.json()
        results = data.get("results", [])

        print(f"Found {len(results)} jobs")

        if len(results) == 0:
            break

        for job in results:

            title = job.get("title", "")

            title_lower = title.lower()

            intern_keywords = [
                "intern",
                "internship",
                "trainee",
                "apprentice"
            ]

            if not any(keyword in title_lower for keyword in intern_keywords):
                continue

            company = job.get("company", {}).get("display_name", "")
            location = job.get("location", {}).get("display_name", "")
            category = job.get("category", {}).get("label", "")
            description = job.get("description", "")

            # ---------------- Duration ----------------

            duration = "Not Specified"

            patterns = [
                r'(\d+)\s*months?',
                r'(\d+)\s*weeks?',
                r'(\d+)\s*days?'
            ]

            for pattern in patterns:
                match = re.search(pattern, description, re.IGNORECASE)
                if match:
                    duration = match.group(0).title()
                    break

            if duration == "Not Specified":
                if re.search(r"summer internship", description, re.IGNORECASE):
                    duration = "Summer Internship"
                elif re.search(r"winter internship", description, re.IGNORECASE):
                    duration = "Winter Internship"

            # ---------------- Stipend ----------------

            salary_min = job.get("salary_min")
            salary_max = job.get("salary_max")

            if salary_min is not None and salary_max is not None:

                monthly_min = salary_min / 12
                monthly_max = salary_max / 12

                salary = f"₹{monthly_min:,.0f}/month - ₹{monthly_max:,.0f}/month"

            elif salary_min is not None:

                monthly_min = salary_min / 12
                salary = f"From ₹{monthly_min:,.0f}/month"

            elif salary_max is not None:

                monthly_max = salary_max / 12
                salary = f"Up to ₹{monthly_max:,.0f}/month"

            else:

                salary = "Stipend Not Disclosed"

            apply_url = job.get("redirect_url", "")
            source = "Adzuna"

            job_key = (
                title.lower().strip(),
                company.lower().strip(),
                location.lower().strip()
            )

            if job_key in seen_jobs:
                continue

            seen_jobs.add(job_key)

            all_jobs.append((
                title,
                company,
                location,
                category,
                salary,
                duration,
                description,
                apply_url,
                source
            ))
            # Only update database if internships were fetched
if all_jobs:

    print(f"\nFetched {len(all_jobs)} unique internships.")
    print("Updating database...")

    cursor.execute("DELETE FROM internships")

    cursor.executemany("""
        INSERT INTO internships
        (
            title,
            company,
            location,
            category,
            salary,
            duration,
            description,
            apply_url,
            source
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, all_jobs)

    conn.commit()

    print(f"✅ Database updated successfully with {len(all_jobs)} internships.")

else:

    print("❌ No internships fetched.")
    print("Keeping existing internships in the database.")

conn.close()