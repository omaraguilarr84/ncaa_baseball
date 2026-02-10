from backend.db import ping_db

if __name__ == "__main__":
    print("DB ping:", ping_db())