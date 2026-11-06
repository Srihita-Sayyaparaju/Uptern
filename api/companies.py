import sqlite3

conn = sqlite3.connect("database/internships.db")
cursor = conn.cursor()

companies = [
    ("Microsoft", "Technology",
     "https://www.linkedin.com/jobs/search/?keywords=Microsoft&location=India",
     "https://careers.microsoft.com/"),

    ("Google", "Technology",
     "https://www.linkedin.com/jobs/search/?keywords=Google&location=India",
     "https://careers.google.com/"),

    ("Amazon", "E-Commerce & Cloud",
     "https://www.linkedin.com/jobs/search/?keywords=Amazon&location=India",
     "https://www.amazon.jobs/"),

    ("Adobe", "Software",
     "https://www.linkedin.com/jobs/search/?keywords=Adobe&location=India",
     "https://careers.adobe.com/"),

    ("Flipkart", "E-Commerce",
     "https://www.linkedin.com/jobs/search/?keywords=Flipkart&location=India",
     "https://www.flipkartcareers.com/"),

    ("Meesho", "E-Commerce",
     "https://www.linkedin.com/jobs/search/?keywords=Meesho&location=India",
     "https://careers.meesho.com/"),

    ("Zomato", "Food Delivery",
     "https://www.linkedin.com/jobs/search/?keywords=Zomato&location=India",
     "https://www.zomato.com/careers"),

    ("Swiggy", "Food Delivery",
     "https://www.linkedin.com/jobs/search/?keywords=Swiggy&location=India",
     "https://careers.swiggy.com/"),

    ("Infosys", "IT Services",
     "https://www.linkedin.com/jobs/search/?keywords=Infosys&location=India",
     "https://career.infosys.com/"),

    ("TCS", "IT Services",
     "https://www.linkedin.com/jobs/search/?keywords=TCS&location=India",
     "https://www.tcs.com/careers"),

    ("Wipro", "IT Services",
     "https://www.linkedin.com/jobs/search/?keywords=Wipro&location=India",
     "https://careers.wipro.com/"),

    ("Accenture", "Consulting",
     "https://www.linkedin.com/jobs/search/?keywords=Accenture&location=India",
     "https://www.accenture.com/in-en/careers"),

    ("IBM", "Technology",
     "https://www.linkedin.com/jobs/search/?keywords=IBM&location=India",
     "https://www.ibm.com/careers"),

    ("Oracle", "Technology",
     "https://www.linkedin.com/jobs/search/?keywords=Oracle&location=India",
     "https://careers.oracle.com/"),

    ("NVIDIA", "Technology",
     "https://www.linkedin.com/jobs/search/?keywords=NVIDIA&location=India",
     "https://www.nvidia.com/en-us/about-nvidia/careers/"),

    ("Capgemini", "IT Services",
    "https://www.linkedin.com/jobs/search/?keywords=Capgemini&location=India",
    "https://www.capgemini.com/in-en/careers/"),

    ("Cognizant", "IT Services",
    "https://www.linkedin.com/jobs/search/?keywords=Cognizant&location=India",
    "https://careers.cognizant.com/"),

    ("Tech Mahindra", "IT Services",
    "https://www.linkedin.com/jobs/search/?keywords=Tech%20Mahindra&location=India",
    "https://careers.techmahindra.com/"),

    ("HCLTech", "IT Services",
    "https://www.linkedin.com/jobs/search/?keywords=HCLTech&location=India",
    "https://www.hcltech.com/careers"),

    ("Deloitte", "Consulting",
    "https://www.linkedin.com/jobs/search/?keywords=Deloitte&location=India",
    "https://www2.deloitte.com/in/en/careers.html"),

    ("EY", "Consulting",
    "https://www.linkedin.com/jobs/search/?keywords=EY&location=India",
    "https://www.ey.com/en_in/careers"),

    ("KPMG", "Consulting",
    "https://www.linkedin.com/jobs/search/?keywords=KPMG&location=India",
    "https://kpmg.com/in/en/home/careers.html"),

    ("PwC", "Consulting",
    "https://www.linkedin.com/jobs/search/?keywords=PwC&location=India",
    "https://www.pwc.in/careers.html"),

    ("SAP", "Enterprise Software",
    "https://www.linkedin.com/jobs/search/?keywords=SAP&location=India",
    "https://www.sap.com/about/careers.html"),

    ("Salesforce", "Cloud Software",
    "https://www.linkedin.com/jobs/search/?keywords=Salesforce&location=India",
    "https://careers.salesforce.com/"),

    ("Intel", "Semiconductors",
    "https://www.linkedin.com/jobs/search/?keywords=Intel&location=India",
    "https://jobs.intel.com/"),

    ("Qualcomm", "Semiconductors",
    "https://www.linkedin.com/jobs/search/?keywords=Qualcomm&location=India",
    "https://www.qualcomm.com/company/careers"),

    ("Cisco", "Networking",
    "https://www.linkedin.com/jobs/search/?keywords=Cisco&location=India",
    "https://jobs.cisco.com/"),

    ("Paytm", "FinTech",
    "https://www.linkedin.com/jobs/search/?keywords=Paytm&location=India",
    "https://paytm.com/careers"),

    ("PhonePe", "FinTech",
    "https://www.linkedin.com/jobs/search/?keywords=PhonePe&location=India",
    "https://www.phonepe.com/careers/"),

    ("Razorpay", "FinTech",
    "https://www.linkedin.com/jobs/search/?keywords=Razorpay&location=India",
    "https://razorpay.com/jobs/"),

    ("Freshworks", "Software",
    "https://www.linkedin.com/jobs/search/?keywords=Freshworks&location=India",
    "https://www.freshworks.com/company/careers/"),

    ("Zoho", "Software",
    "https://www.linkedin.com/jobs/search/?keywords=Zoho&location=India",
    "https://www.zoho.com/careers/"),

    ("Atlassian", "Software",
    "https://www.linkedin.com/jobs/search/?keywords=Atlassian&location=India",
    "https://www.atlassian.com/company/careers"),

    ("JP Morgan Chase", "Banking & Finance",
    "https://www.linkedin.com/jobs/search/?keywords=JP%20Morgan&location=India",
    "https://careers.jpmorgan.com/")
]

cursor.executemany("""
INSERT INTO companies
(company_name, industry, linkedin_jobs_url, careers_url)
VALUES (?, ?, ?, ?)
""", companies)

conn.commit()
conn.close()

print("✅ 15 companies inserted successfully!")