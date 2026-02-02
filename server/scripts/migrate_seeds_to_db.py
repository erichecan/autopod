import json
import psycopg2
import os

# Configuration
JSON_PATH = "server/data/seed_keywords.json"
DB_URL = "postgresql://neondb_owner:npg_G1ExPZaM4Svw@ep-patient-dawn-ah4w5ax5-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require"

def migrate():
    print(f"Loading seeds from {JSON_PATH}...")
    
    if not os.path.exists(JSON_PATH):
        print(f"Error: File not found: {JSON_PATH}")
        return

    with open(JSON_PATH, 'r') as f:
        data = json.load(f)
        categories = data.get("categories", {})

    try:
        conn = psycopg2.connect(DB_URL)
        cur = conn.cursor()
        
        count = 0
        for category, keywords in categories.items():
            for keyword in keywords:
                # Insert if not exists (using ON CONFLICT DO NOTHING)
                cur.execute("""
                    INSERT INTO seed_keywords (category, keyword)
                    VALUES (%s, %s)
                    ON CONFLICT (keyword) DO NOTHING
                """, (category, keyword))
                count += 1
        
        conn.commit()
        print(f"Successfully processed {count} keywords.")
        
        # Verify count in DB
        cur.execute("SELECT COUNT(*) FROM seed_keywords")
        db_count = cur.fetchone()[0]
        print(f"Total keywords in DB: {db_count}")
        
        cur.close()
        conn.close()
        
    except Exception as e:
        print(f"Database error: {e}")

if __name__ == "__main__":
    migrate()
