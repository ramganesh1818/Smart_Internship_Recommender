import csv
import random
from pathlib import Path


DATA_DIR = Path(__file__).resolve().parent.parent / "data"
DATA_FILE = DATA_DIR / "internships_1000.csv"


SECTORS = [
    "IT",
    "Finance",
    "Agriculture",
    "Healthcare",
    "Design",
    "Media",
    "Tourism",
    "Law",
    "Logistics",
    "Cybersecurity",
    "Data Analytics",
    "Education",
    "Public Policy",
    "Renewable Energy",
    "GIS",
    "E-Governance",
    "Blockchain",
    "AIML",
    "Full Stack",
    "Data Science",
    "Web Development",
]

LOCATIONS = [
    "Remote",
    "Delhi",
    "Mumbai",
    "Bengaluru",
    "Hyderabad",
    "Chennai",
    "Pune",
    "Kolkata",
    "Jaipur",
    "Lucknow",
    "Bhopal",
    "Chandigarh",
    "Patna",
    "Kochi",
    "Guwahati",
    "Visakhapatnam",
    "Indore",
    "Raipur",
    "Ranchi",
    "Surat",
    "Ahmedabad",
    "Nagpur",
    "Noida",
    "Gurugram",
    "Mysuru",
    "Thiruvananthapuram",
]

SKILLS_POOL = [
    "Excel",
    "Python",
    "SQL",
    "Power BI",
    "Tableau",
    "HTML",
    "CSS",
    "JavaScript",
    "React",
    "Java",
    "C",
    "C++",
    "Canva",
    "Photoshop",
    "Illustrator",
    "Figma",
    "AutoCAD",
    "SolidWorks",
    "QGIS",
    "ArcGIS",
    "Research",
    "Tally",
    "GST",
    "Digital Marketing",
    "SEO",
    "Content Writing",
    "SPSS",
    "R",
    "UI/UX",
    "Networking",
    "Linux",
    "Data Entry",
    "Typing",
    "Solidity",
    "Ethereum",
    "Web3",
    "Smart Contracts",
    "Blockchain",
    "TensorFlow",
    "PyTorch",
    "Machine Learning",
    "Deep Learning",
    "NLP",
    "Computer Vision",
    "Node.js",
    "Express",
    "MongoDB",
    "PostgreSQL",
    "Docker",
    "Git",
    "REST API",
    "GraphQL",
    "Pandas",
    "NumPy",
    "Scikit-learn",
    "Jupyter",
    "Vue.js",
    "Angular",
    "TypeScript",
    "Next.js",
    "Django",
    "Flask",
    "AWS",
    "Azure",
]

DURATIONS = ["1 month", "2 months", "3 months", "6 months"]
TYPES = ["Govt", "NGO", "PSU", "Startup", "Private"]
MODES = ["Online", "Offline", "Hybrid"]


def _random_skills(sector: str) -> list[str]:
    focus_map = {
        "IT": ["Python", "JavaScript", "React", "Java", "HTML", "CSS", "SQL", "Linux"],
        "Finance": ["Excel", "Power BI", "SQL", "Tally", "GST", "Python"],
        "Agriculture": ["Research", "Data Entry", "Excel", "SPSS"],
        "Healthcare": ["Research", "Excel", "SPSS", "Python"],
        "Design": ["Canva", "Photoshop", "Illustrator", "Figma", "UI/UX"],
        "Media": ["Content Writing", "Digital Marketing", "SEO", "Canva"],
        "Tourism": ["Content Writing", "Digital Marketing", "Excel"],
        "Law": ["Research", "Content Writing"],
        "Logistics": ["Excel", "SQL", "Power BI"],
        "Cybersecurity": ["Networking", "Linux", "Python"],
        "Data Analytics": ["Python", "SQL", "Power BI", "Tableau", "Excel", "R"],
        "Education": ["Content Writing", "Research", "Excel"],
        "Public Policy": ["Research", "Content Writing", "Excel"],
        "Renewable Energy": ["Research", "Excel", "AutoCAD"],
        "GIS": ["QGIS", "ArcGIS", "Excel"],
        "E-Governance": ["Excel", "Python", "SQL", "Research"],
        "Blockchain": ["Solidity", "Ethereum", "Web3", "Smart Contracts", "Blockchain", "Python", "JavaScript", "Node.js"],
        "AIML": ["Python", "TensorFlow", "PyTorch", "Machine Learning", "Deep Learning", "NLP", "Computer Vision", "Scikit-learn", "Pandas", "NumPy"],
        "Full Stack": ["JavaScript", "React", "Node.js", "Express", "MongoDB", "PostgreSQL", "HTML", "CSS", "REST API", "Git", "Docker"],
        "Data Science": ["Python", "SQL", "Pandas", "NumPy", "Scikit-learn", "TensorFlow", "Jupyter", "R", "Tableau", "Power BI", "Machine Learning"],
        "Web Development": ["HTML", "CSS", "JavaScript", "React", "Vue.js", "Angular", "TypeScript", "Node.js", "Next.js", "Django", "Flask", "REST API"],
    }
    base_skills = focus_map.get(sector, [])
    count = random.randint(3, 6)
    skills = set(random.sample(SKILLS_POOL, count))
    while len(skills) < count and base_skills:
        skills.add(random.choice(base_skills))
    skills.update(random.sample(base_skills, min(len(base_skills), random.randint(1, 3))))
    return sorted(skills)


def _random_title(sector: str) -> str:
    role_map = {
        "IT": ["Software Intern", "Full Stack Intern", "IT Support Intern"],
        "Finance": ["Finance Analyst Intern", "Investment Research Intern"],
        "Agriculture": ["Agri Research Intern", "Field Operations Intern"],
        "Healthcare": ["Healthcare Data Intern", "Clinical Research Intern"],
        "Design": ["Graphic Design Intern", "Product Design Intern"],
        "Media": ["Content Strategist Intern", "Social Media Intern"],
        "Tourism": ["Travel Operations Intern", "Tour Planning Intern"],
        "Law": ["Legal Research Intern", "Compliance Intern"],
        "Logistics": ["Supply Chain Intern", "Operations Intern"],
        "Cybersecurity": ["Security Analyst Intern", "Cyber Risk Intern"],
        "Data Analytics": ["Data Analyst Intern", "Business Intelligence Intern"],
        "Education": ["Learning Design Intern", "Academic Research Intern"],
        "Public Policy": ["Policy Research Intern", "Governance Analyst Intern"],
        "Renewable Energy": ["Sustainability Intern", "Solar Projects Intern"],
        "GIS": ["GIS Mapping Intern", "Spatial Data Intern"],
        "E-Governance": ["Digital Governance Intern", "Civic Tech Intern"],
        "Blockchain": ["Blockchain Developer Intern", "Smart Contract Intern", "Web3 Developer Intern"],
        "AIML": ["AI/ML Engineer Intern", "Machine Learning Intern", "Deep Learning Intern", "NLP Intern"],
        "Full Stack": ["Full Stack Developer Intern", "MERN Stack Intern", "MEAN Stack Intern"],
        "Data Science": ["Data Scientist Intern", "Data Science Analyst Intern", "ML Data Science Intern"],
        "Web Development": ["Frontend Developer Intern", "Backend Developer Intern", "Web Developer Intern"],
    }
    generic = ["Program Intern", "Operations Intern", "Strategy Intern"]
    titles = role_map.get(sector, generic)
    return random.choice(titles)


def generate_dataset(path: Path = DATA_FILE, total: int = 1000) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    organizations = [
        "Innovate Labs",
        "FutureWave Tech",
        "GreenGrowth Initiatives",
        "UrbanRise Solutions",
        "EduBridge Alliance",
        "PolicyWorks India",
        "BrightPath Designs",
        "HealthSphere Analytics",
        "AgriNova Collective",
        "CivicLink Foundation",
        "Spectrum Media House",
        "NextGen Logistics",
        "SecureNet Systems",
        "Insight Finance Group",
        "EcoVision Energy",
        "MapCraft GIS",
        "TourEase Travels",
        "LexGuard Associates",
        "Skyline Innovations",
        "DataPulse Analytics",
    ]

    seen_titles = {}

    with path.open("w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([
            "id",
            "title",
            "organization",
            "sector",
            "location",
            "skills",
            "duration",
            "stipend",
            "type",
            "mode",
        ])

        for idx in range(1, total + 1):
            sector = random.choice(SECTORS)
            location = random.choice(LOCATIONS)
            skills = _random_skills(sector)
            duration = random.choice(DURATIONS)
            stipend = random.randrange(3000, 15001, 500)
            org = random.choice(organizations)
            internship_type = random.choice(TYPES)
            mode = random.choice(MODES)
            title = _random_title(sector)

            key = (title, org, sector, location)
            suffix = seen_titles.get(key, 0)
            seen_titles[key] = suffix + 1
            if suffix:
                title = f"{title} ({suffix + 1})"

            writer.writerow([
                idx,
                title,
                org,
                sector,
                location,
                "|".join(skills),
                duration,
                stipend,
                internship_type,
                mode,
            ])


if __name__ == "__main__":
    generate_dataset()

