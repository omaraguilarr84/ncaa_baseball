from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.environ["DATABASE_URL"]

engine = create_engine(DATABASE_URL)

def seed_clemson():
    with engine.begin() as conn:
        conn.execute(
            text("""
                INSERT INTO teams (name, short_name, conference)
                VALUES (:name, :short_name, :conference)
                ON DUPLICATE KEY UPDATE name=name
            """),
            {
                "name": "Clemson",
                "short_name": "Clemson",
                "conference": "ACC"
            }
        )

if __name__ == "__main__":
    seed_clemson()
    print("Clemson seeded 🌱")
