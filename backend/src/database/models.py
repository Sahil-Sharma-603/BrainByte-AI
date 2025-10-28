from sqlalchemy import Column, Integer, String, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# we can modify here to use Cloud database like PostgreSQL, MySQL, etc.
# by changing the connection string in create_engine function
# For now, we are using file-based SQLite database for simplicity
engine = create_engine('sqlite:///database.db', echo=True)
Base = declarative_base()


# Define a Challenge Model: 
class Challenge(Base):
    __tablename__ = 'challenges'
    
    id = Column(Integer, primary_key=True)
    difficulty = Column(String, nullable=False)
    date_created = Column(DateTime, default=datetime.utcnow)
    created_by = Column(String, nullable=False) 
    title = Column(String, nullable=False)
    options = Column(String, nullable=False)
    correct_answer_id = Column(Integer, nullable=False)
    explanation = Column(String, nullable=False)

# Define ChallengeQuota Model - allows to store how many challenges left for a day
class ChallengeQuota(Base):
    __tablename__ = 'challenge_quotas'
    id = Column(Integer, primary_key=True)
    user_id = Column(String, nullable=False, unique=True)
    last_reset_date = Column(DateTime, default=datetime.utcnow)
    quota_remaining = Column(Integer, default=50)  # Default quota per day


# convert the python classess into SQL tables
Base.metadata.create_all(engine)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


