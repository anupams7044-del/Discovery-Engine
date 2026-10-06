"""
Initialize database tables.
Run: python -m database.init_db
"""
import sys
import io

# Ensure UTF-8 output on Windows consoles
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from database.database import engine, SessionLocal
from database.models import Base, IssueCategory
from config.constants import ISSUE_CATEGORIES

def init_database():
    """Create all tables."""
    Base.metadata.create_all(bind=engine)
    print("[SUCCESS] Database tables created successfully.")

    # Seed issue categories
    db = SessionLocal()
    try:
        for name, info in ISSUE_CATEGORIES.items():
            existing = db.query(IssueCategory).filter_by(name=name).first()
            if not existing:
                db.add(IssueCategory(
                    name=name,
                    display_name=info["display_name"],
                    description=info["description"],
                ))
        db.commit()
        print(f"[SUCCESS] {len(ISSUE_CATEGORIES)} issue categories seeded.")
    finally:
        db.close()

if __name__ == "__main__":
    init_database()
