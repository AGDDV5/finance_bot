from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True)
    language = Column(String, default='uz_lat') # 'uz_lat' or 'uz_cyr'
    created_at = Column(DateTime, default=datetime.utcnow)
    transactions = relationship("Transaction", back_populates="user")

class Transaction(Base):
    __tablename__ = 'transactions'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    type = Column(String) # 'income' or 'expense'
    category = Column(String)
    amount = Column(Float)
    date = Column(DateTime, default=datetime.utcnow)
    user = relationship("User", back_populates="transactions")

# Setup DB
engine = create_engine('sqlite:///finance_bot.db', echo=False)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)