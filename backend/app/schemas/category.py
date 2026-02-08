"""
分类 Schema
Pydantic 数据验证模型
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


# ============ 请求 Schema ============

class CategoryCreate(BaseModel):
    """创建分类请求"""
    name: str = Field(..., min_length=1, max_length=50, description="分类名称")
    type: str = Field(..., description="类型: expense 或 income")
    icon: Optional[str] = Field(None, description="图标")
    sort_order: int = Field(0, ge=0, description="排序")


class CategoryUpdate(BaseModel):
    """更新分类请求"""
    name: Optional[str] = Field(None, min_length=1, max_length=50)
    icon: Optional[str] = None
    sort_order: Optional[int] = Field(None, ge=0)


class CategoryItemCreate(BaseModel):
    """创建二级分类请求"""
    category_id: int = Field(..., description="一级分类ID")
    name: str = Field(..., min_length=1, max_length=50, description="二级分类名称")
    icon: Optional[str] = Field(None, description="图标")
    sort_order: int = Field(0, ge=0, description="排序")


class CategoryItemUpdate(BaseModel):
    """更新二级分类请求"""
    name: Optional[str] = Field(None, min_length=1, max_length=50)
    icon: Optional[str] = None
    sort_order: Optional[int] = Field(None, ge=0)


class PaymentMethodCreate(BaseModel):
    """创建支付方式请求"""
    name: str = Field(..., min_length=1, max_length=50, description="支付方式名称")
    icon: Optional[str] = Field(None, description="图标")
    sort_order: int = Field(0, ge=0, description="排序")


class PaymentMethodUpdate(BaseModel):
    """更新支付方式请求"""
    name: Optional[str] = Field(None, min_length=1, max_length=50)
    icon: Optional[str] = None
    sort_order: Optional[int] = Field(None, ge=0)


# ============ 响应 Schema ============

class CategoryResponse(BaseModel):
    """分类响应"""
    id: int
    name: str
    type: str
    icon: Optional[str]
    sort_order: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class CategoryWithItemsResponse(CategoryResponse):
    """带二级分类的分类响应"""
    items: List['CategoryItemResponse'] = []


class CategoryItemResponse(BaseModel):
    """二级分类响应"""
    id: int
    category_id: int
    name: str
    icon: Optional[str]
    sort_order: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class PaymentMethodResponse(BaseModel):
    """支付方式响应"""
    id: int
    name: str
    icon: Optional[str]
    sort_order: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class CategoriesListResponse(BaseModel):
    """分类列表响应"""
    expense: List[CategoryWithItemsResponse] = []
    income: List[CategoryWithItemsResponse] = []


class MessageResponse(BaseModel):
    """通用消息响应"""
    message: str
