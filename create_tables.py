from app.db.base import Base
from app.db.session import engine
import app.db.models 

def main():
    print("Creating all tables...")
    Base.metadata.create_all(bind=engine)
    print("Done!!")

if __name__ == "__main__":
    main()
