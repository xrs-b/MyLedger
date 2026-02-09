"""
记账记录 Schema
Pydantic 数据验证模型
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from decimal import Decimal


# ============ 请求 Schema ============

class RecordCreate(BaseModel):
    """创建记账请求"""
    type: str = Field(..., description="类型: income 或 expense")
    category_id: int = Field(..., description="一级分类ID")
    category_item_id: int = Field(..., description="二级分类ID")
    amount: Decimal = Field(..., gt=0, description="金额")
    date: str = Field(..., description="日期 (YYYY-MM-DD)")
    remark: Optional[str] = Field(None, max_length=500, description="备注")
    payment_method_id: Optional[int] = Field(None, description="支付方式ID")
    project_id: Optional[int] = Field(None, description="关联项目ID")


class RecordUpdate(BaseModel):
    """更新记账请求"""
    type: Optional[str] = None
    category_id: Optional[int] = None
    category_item_id: Optional[int] = None
    amount: Optional[Decimal] = Field(None, gt=0)
    date: Optional[datetime] = None
    remark: Optional[str] = Field(None, max_length=500)
    payment_method_id: Optional[int] = None
    project_id: Optional[int] = None


class RecordFilter(BaseModel):
    """记账筛选请求"""
    type: Optional[str] = None
    category_id: Optional[int] = None
    category_item_id: Optional[int] = None
    payment_method_id: Optional[int] = None
    project_id: Optional[int] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None


# ============ 响应 Schema ============

class RecordResponse(BaseModel):
    """记账响应"""
    id: int
    user_id: int
    type: str
    category_id: int
    category_item_id: int
    amount: Decimal
    date: datetime
    remark: Optional[str]
    payment_method_id: Optional[int]
    project_id: Optional[int]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class RecordDetailResponse(RecordResponse):
    """记账详情响应（包含关联信息）"""
    category_name: Optional[str] = None
    category_item_name: Optional[str] = None
    payment_method_name: Optional[str] = None
    project_title: Optional[str] = None


class RecordListResponse(BaseModel):
    """记账列表响应"""
    records: List[RecordDetailResponse] = []
    total: int = 0
    page: int = 1
    page_size: int = 20
    total_pages: int = 1


class RecordStatsResponse(BaseModel):
    """记账统计响应"""
    total_count: int = 0
    total_amount: Decimal = Decimal('0')
    income_count: int = 0
    income_amount: Decimal = Decimal('0')
    expense_count: int = 0
    expense_amount: Decimal = Decimal('0')


class MessageResponse(BaseModel):
    """通用消息响应"""
    message: str
