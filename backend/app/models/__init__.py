"""
数据模型
所有数据库模型的定义
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, Numeric, Text, Date, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database import Base


class User(Base):
    """用户表"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    is_admin = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 关系
    records = relationship("Record", back_populates="user")
    projects = relationship("Project", back_populates="user")


class Category(Base):
    """一级分类表"""
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)
    type = Column(String(10), nullable=False)  # 'expense' 或 'income'
    icon = Column(String(50), default=None)
    sort_order = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 关系
    items = relationship("CategoryItem", back_populates="category", cascade="all, delete")


class CategoryItem(Base):
    """二级分类表"""
    __tablename__ = "category_items"

    id = Column(Integer, primary_key=True, index=True)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    name = Column(String(50), nullable=False)
    icon = Column(String(50), default=None)
    sort_order = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 关系
    category = relationship("Category", back_populates="items")


class PaymentMethod(Base):
    """支付方式表"""
    __tablename__ = "payment_methods"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)
    icon = Column(String(50), default=None)
    sort_order = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Record(Base):
    """记账记录表"""
    __tablename__ = "records"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    type = Column(String(10), nullable=False)  # 'income' 或 'expense'
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    category_item_id = Column(Integer, ForeignKey("category_items.id"), nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    date = Column(DateTime, nullable=False)
    remark = Column(Text, default=None)
    payment_method_id = Column(Integer, ForeignKey("payment_methods.id"), default=None)
    project_id = Column(Integer, ForeignKey("projects.id"), default=None)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 关系
    user = relationship("User", back_populates="records")
    project = relationship("Project", back_populates="records")


class Project(Base):
    """项目表"""
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String(100), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    budget = Column(Numeric(10, 2), nullable=False)
    member_count = Column(Integer, nullable=False)
    total_expense = Column(Numeric(10, 2), default=0)
    status = Column(String(20), default="ongoing")  # 'ongoing' 或 'completed'
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 关系
    user = relationship("User", back_populates="projects")
    records = relationship("Record", back_populates="project")
