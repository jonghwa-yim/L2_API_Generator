"""
User Management API 데이터 모델
Pydantic 모델 정의
"""

from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

# ============================================================================
# 기본 모델들
# ============================================================================

class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: str = Field(..., description="사용자 이메일")

class UserCreate(UserBase):
    password: str = Field(..., min_length=8, description="비밀번호")

class UserResponse(UserBase):
    id: int
    is_active: bool = True
    created_at: datetime
    
    class Config:
        from_attributes = True

class ProductBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    price: float = Field(..., gt=0)
    stock_quantity: int = Field(default=0, ge=0)

class ProductCreate(ProductBase):
    category_id: Optional[int] = None

class ProductResponse(ProductBase):
    id: int
    category_id: Optional[int] = None
    is_active: bool = True
    created_at: datetime
    
    class Config:
        from_attributes = True

class CategoryBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None

class CategoryResponse(CategoryBase):
    id: int
    created_at: datetime
    product_count: int = 0
    
    class Config:
        from_attributes = True

class OrderBase(BaseModel):
    user_id: int
    total_amount: float = Field(..., gt=0)
    status: str = Field(default="pending")

class OrderResponse(OrderBase):
    id: str
    order_date: datetime
    items: List[Dict[str, Any]] = []
    
    class Config:
        from_attributes = True

# 인증 관련 모델
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class LoginRequest(BaseModel):
    username: str
    password: str

# 공통 응답 모델
class PaginatedResponse(BaseModel):
    items: List[Dict[str, Any]]
    total: int
    page: int = 1
    size: int = 10
    pages: int

    def calculate_pages(self):
        self.pages = (self.total + self.size - 1) // self.size
        return self
