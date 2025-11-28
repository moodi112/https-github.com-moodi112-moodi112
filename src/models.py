from sqlalchemy import create_engine, Column, Integer, String, Date, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime

DATABASE_URL = "sqlite:///./events.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Event(Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True)
    date = Column(Date)
    location = Column(String(100))
    summary = Column(Text)
    details = Column(Text)

def init_db():
    Base.metadata.create_all(bind=engine)
    # Seed data if DB empty
    db = SessionLocal()
    if db.query(Event).count() == 0:
        db.add_all([
            Event(
                name="Muscat Festival",
                date=datetime.date(2025, 1, 15),
                location="Muscat",
                summary="Cultural and entertainment festival held annually in Muscat.",
                details="The Muscat Festival showcases Omani heritage, performances, food, and entertainment."
            ),
            Event(
                name="Salalah Tourism Festival",
                date=datetime.date(2025, 7, 15),
                location="Salalah",
                summary="Tourism festival attracting thousands to Salalah’s cool climate.",
                details="Features music, folklore, food, and cultural exhibitions."
            )
        ])
        db.commit()
    db.close()