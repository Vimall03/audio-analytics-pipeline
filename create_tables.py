from app.db.base import Base
from app.db.session import engine
import app.db.models
from app.core.logger import logger

def main():
    logger.info("Creating all tables...")
    Base.metadata.create_all(bind=engine)
    logger.info("Done!!")

if __name__ == "__main__":
    main()
