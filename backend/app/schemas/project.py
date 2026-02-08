"""
项目 Schema
Pydantic 数据验证模型
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date, datetime
from decimal import Decimal


# ============ 请求 Schema ============

class ProjectCreate(BaseModel):
    """创建项目请求"""
    title: str = Field(..., min_length=1, max_length=100, description="项目标题")
    start_date: date = Field(..., description="开始日期")
    end_date: date = Field(..., description="结束日期")
    budget: Decimal = Field(..., ge=0, description="预算金额")
    member_count: int = Field(1, ge=1, description="参与人数")
    description: Optional[str] = Field(None, max_length=500, description="项目描述")


class ProjectUpdate(BaseModel):
    """更新项目请求"""
    title: Optional[str] = Field(None, min_length=1, max_length=100)
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    budget: Optional[Decimal] = Field(None, ge=0)
    member_count: Optional[int] = Field(None, ge=1)
    status: Optional[str] = Field(None, description="状态: ongoing/completed")
    description: Optional[str] = Field(None, max_length=500)


# ============ 响应 Schema ============

class ProjectRecordResponse(BaseModel):
    """项目关联记录响应"""
    id: int
    type: str
    category_id: int
    category_item_id: int
    amount: Decimal
    date: datetime
    remark: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True


class ProjectResponse(BaseModel):
    """项目响应"""
    id: int
    user_id: int
    title: str
    start_date: date
    end_date: date
    budget: Decimal
    member_count: int
    total_expense: Decimal
    status: str
    description: Optional[str]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class ProjectDetailResponse(ProjectResponse):
    """项目详情响应（包含关联信息）"""
    # 计算字段
    avg_expense: Decimal = Decimal('0')  # 人均费用
    expense_rate: float = 0.0  # 消费率
    
    # 关联记录
    records: List[ProjectRecordResponse] = []


class ProjectListResponse(BaseModel):
    """项目列表响应"""
    projects: List[ProjectResponse] = []
    total: int = 0


class MessageResponse(BaseModel):
    """通用消息响应"""
    message: str
