"""
postgresql 데이터베이스 설정
SQLAlchemy 기반
"""

from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, Float, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator
from datetime import datetime
import os

# 데이터베이스 설정
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/dbname")

# SQLAlchemy 설정
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# 데이터베이스 모델
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class Product(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False, index=True)
    description = Column(Text)
    price = Column(Float, nullable=False)
    stock_quantity = Column(Integer, default=0)
    category_id = Column(Integer)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class Category(Base):
    __tablename__ = "categories"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

def get_db() -> Generator:
    """데이터베이스 세션 의존성"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """데이터베이스 초기화"""
    Base.metadata.create_all(bind=engine)

def create_sample_data():
    """샘플 데이터 생성"""
    db = SessionLocal()
    try:
        # 카테고리 생성
        if not db.query(Category).first():
            categories = [
                Category(name="Electronics", description="전자제품"),
                Category(name="Books", description="도서"),
                Category(name="Clothing", description="의류"),
            ]
            for category in categories:
                db.add(category)
            db.commit()
            
        # 상품 생성
        if not db.query(Product).first():
            products = [
                Product(name="스마트폰", description="최신 스마트폰", price=799.99, stock_quantity=50, category_id=1),
                Product(name="프로그래밍 책", description="Python 학습서", price=29.99, stock_quantity=100, category_id=2),
                Product(name="티셔츠", description="편안한 면 티셔츠", price=19.99, stock_quantity=200, category_id=3),
            ]
            for product in products:
                db.add(product)
            db.commit()
            
    except Exception as e:
        print(f"샘플 데이터 생성 오류: {e}")
        db.rollback()
    finally:
        db.close()
