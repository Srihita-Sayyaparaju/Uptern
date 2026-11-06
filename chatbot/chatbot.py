from groq import Groq
from dotenv import load_dotenv
from urllib.parse import quote
import sqlite3
import os
import re

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

# ---------------- Skill Recommendation Map ---------------- #

skill_map = {

    "python": [
        "python",
        "django",
        "flask",
        "backend",
        "data science",
        "machine learning"
    ],

    "java": [
        "java",
        "spring boot",
        "backend",
        "software engineer"
    ],

    "javascript": [
        "javascript",
        "react",
        "node js",
        "frontend",
        "full stack"
    ],

    "react": [
        "react",
        "frontend",
        "javascript",
        "full stack"
    ],

    "html": [
        "frontend",
        "web developer",
        "html",
        "css"
    ],

    "css": [
        "frontend",
        "web developer",
        "css"
    ],

    "sql": [
        "sql",
        "database",
        "data analyst",
        "backend"
    ],

    "machine learning": [
        "machine learning",
        "artificial intelligence",
        "deep learning",
        "computer vision",
        "nlp"
    ],

    "ai": [
        "artificial intelligence",
        "machine learning",
        "deep learning",
        "nlp"
    ],

    "cyber security": [
        "cyber security",
        "information security",
        "network"
    ],

    "cloud": [
        "cloud",
        "devops",
        "aws"
    ],
    "c": [
        "c",
        "embedded",
        "firmware",
        "iot"
    ],

    "c++": [
        "c++",
        "software engineer",
        "game developer"
    ],

    "node js": [
        "node js",
        "backend",
        "full stack",
        "express"
    ],

    "flask": [
        "python",
        "flask",
        "backend"
    ],

    "django": [
        "python",
        "django",
        "backend"
    ],

    "android": [
        "android",
        "kotlin",
        "java"
    ],

    "ui ux": [
        "ui",
        "ux",
        "designer"
    ],

    "data science": [
        "python",
        "machine learning",
        "sql",
        "data analyst"
    ],

    "php": [
    "php",
    "laravel",
    "backend",
    "web developer"
    ],

    "laravel": [
        "laravel",
        "php",
        "backend"
    ],

    "ruby": [
    "ruby",
    "ruby on rails",
    "backend"
    ],

    "ruby on rails": [
        "ruby on rails",
        "ruby",
        "backend"
    ],

    "go": [
        "go",
        "golang",
        "backend"
    ],

    "golang": [
        "golang",
        "go",
        "backend"
    ],

    "rust": [
        "rust",
        "systems programming",
        "backend"
    ],

    "scala": [
        "scala",
        "backend",
        "data engineering"
    ],

    "perl": [
        "perl",
        "backend"
    ],

    "r": [
        "r",
        "data science",
        "data analyst"
    ],

    "numpy": [
        "numpy",
        "python",
        "machine learning"
    ],

    "pandas": [
        "pandas",
        "python",
        "data science"
    ],

    "matplotlib": [
        "matplotlib",
        "python",
        "data visualization"
    ],

    "tensorflow": [
        "tensorflow",
        "machine learning",
        "deep learning"
    ],

    "pytorch": [
        "pytorch",
        "machine learning",
        "deep learning"
    ],

    "hadoop": [
        "hadoop",
        "big data",
        "data engineering"
    ],

    "spark": [
        "apache spark",
        "big data",
        "data engineering"
    ],

    "etl": [
        "etl",
        "data engineering",
        "sql"
    ],

    "api": [
        "api",
        "backend",
        "web developer"
    ],

    "rest api": [
        "rest api",
        "backend",
        "api"
    ],

    "graphql": [
        "graphql",
        "backend",
        "api"
    ],

    "microservices": [
        "microservices",
        "backend",
        "java"
    ],

    "oracle": [
        "oracle",
        "sql",
        "database"
    ],

    "postgresql": [
        "postgresql",
        "database",
        "sql"
    ],

    "firebase": [
        "firebase",
        "android",
        "flutter"
    ],

    "figma": [
        "figma",
        "ui",
        "ux",
        "designer"
    ],

    "photoshop": [
        "photoshop",
        "designer",
        "ui"
    ],

    "canva": [
        "canva",
        "designer",
        "ui"
    ],

    "blockchain": [
        "blockchain",
        "web3",
        "solidity"
    ],

    "web3": [
        "web3",
        "blockchain",
        "solidity"
    ],

    "solidity": [
        "solidity",
        "blockchain",
        "web3"
    ],

    "robotics": [
        "robotics",
        "embedded",
        "iot"
    ],

    "iot": [
        "iot",
        "embedded",
        "electronics"
    ],

    "mysql": [
        "mysql",
        "database",
        "sql",
        "backend"
    ],

    "mongodb": [
        "mongodb",
        "database",
        "backend"
    ],

    "express": [
        "express",
        "node js",
        "backend"
    ],

    "angular": [
        "angular",
        "frontend",
        "javascript"
    ],

    "vue": [
        "vue",
        "frontend",
        "javascript"
    ],

    "bootstrap": [
        "bootstrap",
        "frontend",
        "web developer"
    ],

    "tailwind": [
        "tailwind",
        "frontend",
        "web developer"
    ],

    "full stack": [
        "full stack",
        "frontend",
        "backend",
        "react",
        "node js"
    ],

    "backend": [
        "backend",
        "python",
        "java",
        "node js"
    ],

    "frontend": [
        "frontend",
        "react",
        "html",
        "css",
        "javascript"
    ],

    "web development": [
        "web developer",
        "frontend",
        "backend",
        "full stack"
    ],

    "app development": [
        "android",
        "mobile",
        "kotlin",
        "java"
    ],

    "kotlin": [
        "kotlin",
        "android",
        "mobile"
    ],

    "swift": [
        "swift",
        "ios",
        "mobile"
    ],

    "ios": [
        "ios",
        "swift",
        "mobile"
    ],

    "flutter": [
        "flutter",
        "dart",
        "mobile"
    ],

    "dart": [
        "dart",
        "flutter",
        "mobile"
    ],

    "devops": [
        "devops",
        "aws",
        "docker",
        "kubernetes"
    ],

    "aws": [
        "aws",
        "cloud",
        "devops"
    ],

    "azure": [
        "azure",
        "cloud",
        "devops"
    ],

    "docker": [
        "docker",
        "devops",
        "cloud"
    ],

    "kubernetes": [
        "kubernetes",
        "docker",
        "devops"
    ],

    "git": [
        "git",
        "github",
        "software engineer"
    ],

    "github": [
        "github",
        "git",
        "software engineer"
    ],

    "data analyst": [
        "data analyst",
        "sql",
        "excel",
        "power bi"
    ],

    "excel": [
        "excel",
        "data analyst",
        "business analyst"
    ],

    "power bi": [
        "power bi",
        "data analyst",
        "business intelligence"
    ],

    "tableau": [
        "tableau",
        "data analyst",
        "business intelligence"
    ],

    "business analyst": [
        "business analyst",
        "sql",
        "excel"
    ],

    "artificial intelligence": [
        "artificial intelligence",
        "machine learning",
        "deep learning",
        "nlp"
    ],

    "deep learning": [
        "deep learning",
        "machine learning",
        "artificial intelligence"
    ],

    "computer vision": [
        "computer vision",
        "machine learning",
        "artificial intelligence"
    ],

    "nlp": [
        "nlp",
        "machine learning",
        "artificial intelligence"
    ],

    "data engineering": [
        "data engineer",
        "python",
        "sql",
        "etl"
    ],

    "testing": [
        "qa",
        "testing",
        "software tester"
    ],

    "qa": [
        "qa",
        "software tester",
        "testing"
    ],

    "automation testing": [
        "automation testing",
        "selenium",
        "qa"
    ],

    "selenium": [
        "selenium",
        "automation testing",
        "qa"
    ],
    "dsa": [
    "software engineer",
    "software developer",
    "backend",
    "java",
    "python",
    "c++",
    "algorithm",
    "data structures"
    ],

    "data structures": [
        "software engineer",
        "backend",
        "algorithm"
    ],

    "algorithms": [
        "software engineer",
        "backend",
        "algorithm"
    ],
    "networking": [
        "network",
        "cyber security",
        "system administrator"
    ],

    "linux": [
        "linux",
        "devops",
        "system administrator"
    ],

    "operating systems": [
        "linux",
        "system programming",
        "software engineer"
    ],

    "game development": [
        "unity",
        "unreal",
        "c++",
        "game developer"
    ],

    "unity": [
        "unity",
        "game developer",
        "c#"
    ],

    "unreal": [
        "unreal",
        "game developer",
        "c++"
    ],

    "c#": [
        "c#",
        "unity",
        "software engineer"
    ]
}


def ask_ai(question):

    conn = sqlite3.connect("database/internships.db")
    cursor = conn.cursor()

    question_lower = question.lower()
    question_lower = re.sub(r"[^\w\s]", " ", question_lower)
    # ---------- Check if user asked about a company ----------

    # ---------- Check if user asked about a company ----------

    cursor.execute("""
    SELECT company_name,
        industry,
        linkedin_jobs_url,
        careers_url
    FROM companies
    """)

    companies = cursor.fetchall()

    company_descriptions = {
        "microsoft": "Microsoft is a global technology company known for Windows, Azure, Microsoft 365, GitHub, and AI technologies.",
        "google": "Google is a global technology company known for Search, Android, Chrome, Gmail, Google Cloud, and Gemini AI.",
        "amazon": "Amazon is a leading e-commerce and cloud computing company, offering services through Amazon Web Services (AWS).",
        "adobe": "Adobe develops creative software such as Photoshop, Illustrator, Premiere Pro, and Acrobat.",
        "flipkart": "Flipkart is one of India's largest e-commerce companies, offering technology, logistics, and retail solutions.",
        "meesho": "Meesho is an Indian e-commerce platform that enables online shopping and social commerce.",
        "zomato": "Zomato is an Indian food delivery and restaurant discovery platform with opportunities in technology and operations.",
        "swiggy": "Swiggy is a leading food delivery and quick commerce company in India.",
        "infosys": "Infosys is a global IT consulting and digital services company headquartered in India.",
        "tcs": "TCS (Tata Consultancy Services) is one of the world's largest IT services and consulting companies.",
        "wipro": "Wipro is a multinational IT services, consulting, and business solutions company.",
        "accenture": "Accenture is a global professional services company specializing in consulting, technology, and digital transformation.",
        "ibm": "IBM is a multinational technology company focusing on cloud computing, AI, consulting, and enterprise software.",
        "oracle": "Oracle develops enterprise software, cloud infrastructure, and database technologies.",
        "nvidia": "NVIDIA is a leader in GPUs, artificial intelligence, gaming, robotics, and high-performance computing.",
        "capgemini": "Capgemini is a global IT consulting and digital transformation company.",
        "cognizant": "Cognizant provides IT consulting, digital engineering, cloud, and AI solutions.",
        "tech mahindra": "Tech Mahindra is an Indian multinational IT services and consulting company.",
        "hcltech": "HCLTech is a global technology company providing IT services, engineering, and cloud solutions.",
        "deloitte": "Deloitte is one of the world's largest consulting and professional services firms.",
        "ey": "EY (Ernst & Young) provides consulting, assurance, tax, and strategy services.",
        "kpmg": "KPMG is a global professional services network offering audit, tax, and advisory services.",
        "pwc": "PwC provides consulting, assurance, tax, and business advisory services worldwide.",
        "sap": "SAP develops enterprise software and ERP solutions used by organizations around the world.",
        "salesforce": "Salesforce is a global leader in CRM software and cloud-based business applications.",
        "intel": "Intel designs processors, semiconductor technologies, and AI hardware.",
        "qualcomm": "Qualcomm develops wireless communication technologies, mobile processors, and AI solutions.",
        "cisco": "Cisco is a global networking, cybersecurity, and cloud technology company.",
        "paytm": "Paytm is an Indian fintech company providing digital payments and financial services.",
        "phonepe": "PhonePe is one of India's largest digital payments and fintech platforms.",
        "razorpay": "Razorpay provides payment gateway and fintech solutions for businesses.",
        "freshworks": "Freshworks develops customer engagement and business software solutions.",
        "zoho": "Zoho develops business software including CRM, email, accounting, and productivity applications.",
        "atlassian": "Atlassian develops collaboration tools such as Jira, Confluence, and Trello.",
        "jp morgan chase": "JPMorgan Chase is one of the world's largest banking and financial services companies."
    }

    company_results = []

    question_words = set(question_lower.split())

    for company in companies:

        company_name = company[0].lower()
        company_words = company_name.split()

        if (
            company_name in question_lower
            or all(word in question_words for word in company_words)
        ):

            description = company_descriptions.get(
                company_name,
                "A leading company offering excellent career opportunities."
            )

            company_results.append(f"""
🏢 {company[0]}

📖 About:
{description}

🏷 Industry:
{company[1]}

🔗 LinkedIn Jobs:
{company[2]}

🌐 Official Careers:
{company[3]}

💡 Tip:
Visit the Official Careers page for the latest internship openings, graduate programs, and full-time opportunities.
""")

    if company_results:
        conn.close()
        return ("\n" + "=" * 60 + "\n").join(company_results)

    stop_words = {
        "can", "could", "would", "should",
        "please", "show", "find", "give",
        "recommend", "suggest", "looking",
        "for", "me", "my", "i", "know",
        "skills", "skill", "based", "on",
        "want", "need", "an", "a", "the",
        "to", "with", "of", "in", "is",
        "are", "internship", "internships"
    }

    keywords = []

    for word in question_lower.split():

        if word not in stop_words:
            keywords.append(word)

    # ---------- Expand skills ----------

    expanded_keywords = keywords.copy()

    for skill, related in skill_map.items():

        if skill in question_lower:

            expanded_keywords.extend(related)

    # Remove duplicates
    expanded_keywords = list(dict.fromkeys(expanded_keywords))

    if not expanded_keywords:
        expanded_keywords = ["intern"]

    query = """
    SELECT
        title,
        company,
        location,
        category,
        salary,
        duration,
        description,
        apply_url
    FROM internships
    WHERE
    """

    conditions = []
    values = []

    for word in expanded_keywords:

        conditions.append("""
            title LIKE ?
            OR company LIKE ?
            OR location LIKE ?
            OR category LIKE ?
            OR duration LIKE ?
            OR description LIKE ?
        """)

        values.extend([
            f"%{word}%",
            f"%{word}%",
            f"%{word}%",
            f"%{word}%",
            f"%{word}%",
            f"%{word}%"
        ])

    query += " OR ".join(f"({c})" for c in conditions)
    query += " LIMIT 20"

    cursor.execute(query, values)

    jobs = cursor.fetchall()

    conn.close()

    context = ""

    skill_detected = []

    for skill in skill_map.keys():
        if skill in question_lower:
            skill_detected.append(skill.title())

    for job in jobs:

        title = job[0]
        company = job[1]
        location = job[2]
        category = job[3]
        stipend = job[4]
        duration = job[5]
        description = job[6]
        apply_link = job[7]

        if not duration:
            duration = "Not Specified"

        if not apply_link or apply_link.strip() == "":
            apply_link = (
                "https://www.linkedin.com/jobs/search/?keywords="
                + quote(f"{company} {title}")
            )

        context += f"""
Title: {title}
Company: {company}
Location: {location}
Category: {category}
Monthly Stipend: {stipend}
Duration: {duration}
Description: {description}
Apply Link: {apply_link}

-------------------------
"""

    skill_text = ""

    if skill_detected:
        skill_text = (
            "The user mentioned these skills: "
            + ", ".join(skill_detected)
            + ". Recommend internships that best match these skills."
        )

    prompt = f"""
You are Uptern AI, a friendly AI internship assistant.

Your goal is to help students discover internships.

{skill_text}

Rules:

- Be friendly and professional.
- Recommend internships ONLY from the database below.
- Never invent internships.
- If the user mentions skills (for example Python, Java, React, SQL, AI, Machine Learning, HTML, CSS, JavaScript), prioritize internships related to those skills.
- Explain briefly why each internship matches the user's skills.
- If multiple internships are available, recommend the most relevant ones first.
- If no internship exactly matches, recommend the closest internships based on the user's skills.
- You are ONLY an internship and career assistant.
- Answer questions related to internships, jobs, companies, careers, skills, resumes, interview preparation, placements, learning paths, and career guidance.
- If the user asks anything unrelated (movies, games, politics, sports, recipes, jokes, celebrities, shopping, etc.), politely refuse and guide them back to internship or career topics.
- Never answer unrelated questions.
If the user's message is casual (like "okay", "thanks", "hi", "hello"),
respond naturally instead of asking for skills again.

Continue the conversation naturally.

Examples:
User: okay
Assistant: Great! Let me know if you'd like recommendations based on your skills, preferred role, company, or location.

User: thanks
Assistant: You're welcome! 😊 Feel free to ask anytime if you're looking for internships or career guidance.

User: hi
Assistant: Hi! 👋 I'm Uptern AI. Tell me your skills or the type of internship you're looking for, and I'll help you find relevant opportunities.
- If the Apply Link is a LinkedIn Jobs search link, that's acceptable.

Always use this format:

💼 Internship:
<Title>

🏢 Company:
<Company>

📍 Location:
<Location>

📅 Duration:
<Duration>

💰 Monthly Stipend:
<Monthly Stipend>

🏷 Category:
<Category>

⭐ Why it matches:
1-2 lines explaining why it suits the user's skills.

📝 Description:
Summarize in 2-3 short lines.

🔗 Apply Here:
<Apply Link>

----------------------------------------

Internships:

{context}

User Question:

{question}
"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content