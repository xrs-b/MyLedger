"""
记账记录路由
记账 CRUD API
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from datetime import datetime

from ..database import get_db
from ..models import Record, User
from ..schemas.record import (
    RecordCreate, RecordUpdate, RecordResponse,
    RecordDetailResponse, RecordListResponse, RecordStatsResponse,
    MessageResponse
)
from .auth import get_current_user

router = APIRouter(prefix="/api/v1/records", tags=["记账"])


@router.get("", response_model=RecordListResponse, summary="获取记账列表")
async def get_records(
    type: Optional[str] = Query(None, description="类型: income/expense"),
    category_id: Optional[int] = Query(None, description="一级分类ID"),
    category_item_id: Optional[int] = Query(None, description="二级分类ID"),
    payment_method_id: Optional[int] = Query(None, description="支付方式ID"),
    project_id: Optional[int] = Query(None, description="项目ID"),
    start_date: Optional[datetime] = Query(None, description="开始日期"),
    end_date: Optional[datetime] = Query(None, description="结束日期"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    获取当前用户的记账列表
    
    支持多条件筛选：
    - type: 收入/支出
    - category_id/category_item_id: 分类筛选
    - payment_method_id: 支付方式筛选
    - project_id: 项目筛选
    - start_date/end_date: 日期范围筛选
    """
    # 构建查询
    query = db.query(Record).filter(Record.user_id == current_user.id)
    
    # 条件筛选
    if type:
        query = query.filter(Record.type == type)
    if category_id:
        query = query.filter(Record.category_id == category_id)
    if category_item_id:
        query = query.filter(Record.category_item_id == category_item_id)
    if payment_method_id:
        query = query.filter(Record.payment_method_id == payment_method_id)
    if project_id:
        query = query.filter(Record.project_id == project_id)
    if start_date:
        query = query.filter(Record.date >= start_date)
    if end_date:
        query = query.filter(Record.date <= end_date)
    
    # 获取总数
    total = query.count()
    
    # 分页
    offset = (page - 1) * page_size
    records = query.order_by(Record.date.desc()).offset(offset).limit(page_size).all()
    
    # 构建响应
    record_responses = []
    for record in records:
        # 获取关联信息
        category = record.category_id  # 这里可以通过关联获取
        payment_method = record.payment_method_id
        
        record_responses.append(RecordDetailResponse(
            **{
                'id': record.id,
                'user_id': record.user_id,
                'type': record.type,
                'category_id': record.category_id,
                'category_item_id': record.category_item_id,
                'amount': record.amount,
                'date': record.date,
                'remark': record.remark,
                'payment_method_id': record.payment_method_id,
                'project_id': record.project_id,
                'created_at': record.created_at,
                'updated_at': record.updated_at,
            }
        ))
    
    return {
        "records": record_responses,
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": (total + page_size - 1) // page_size
    }


@router.get("/{record_id}", response_model=RecordDetailResponse, summary="获取记账详情")
async def get_record(
    record_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取记账详情"""
    record = db.query(Record).filter(
        Record.id == record_id,
        Record.user_id == current_user.id
    ).first()
    
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="记账记录不存在"
        )
    
    return RecordDetailResponse(
        **{
            'id': record.id,
            'user_id': record.user_id,
            'type': record.type,
            'category_id': record.category_id,
            'category_item_id': record.category_item_id,
            'amount': record.amount,
            'date': record.date,
            'remark': record.remark,
            'payment_method_id': record.payment_method_id,
            'project_id': record.project_id,
            'created_at': record.created_at,
            'updated_at': record.updated_at,
        }
    )


@router.post("", response_model=RecordDetailResponse, summary="创建记账")
async def create_record(
    record: RecordCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """创建新记账"""
    # 验证分类存在
    from ..models import Category, CategoryItem
    
    category = db.query(Category).filter(Category.id == record.category_id).first()
    if not category:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="一级分类不存在"
        )
    
    item = db.query(CategoryItem).filter(
        CategoryItem.id == record.category_item_id,
        CategoryItem.category_id == record.category_id
    ).first()
    if not item:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="二级分类不存在"
        )
    
    # 如果指定了项目，验证项目存在且属于当前用户
    if record.project_id:
        from ..models import Project
        project = db.query(Project).filter(
            Project.id == record.project_id,
            Project.user_id == current_user.id
        ).first()
        if not project:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="项目不存在"
            )
    
    # 创建记录
    db_record = Record(
        user_id=current_user.id,
        type=record.type,
        category_id=record.category_id,
        category_item_id=record.category_item_id,
        amount=record.amount,
        date=record.date,
        remark=record.remark,
        payment_method_id=record.payment_method_id,
        project_id=record.project_id
    )
    
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    
    # 如果关联了项目，更新项目总消费
    if record.project_id:
        from ..models import Project
        project = db.query(Project).filter(Project.id == record.project_id).first()
        if project:
            total = db.query(func.sum(Record.amount)).filter(
                Record.project_id == record.project_id
            ).scalar() or 0
            project.total_expense = total
            db.commit()
    
    return RecordDetailResponse(
        **{
            'id': db_record.id,
            'user_id': db_record.user_id,
            'type': db_record.type,
            'category_id': db_record.category_id,
            'category_item_id': db_record.category_item_id,
            'amount': db_record.amount,
            'date': db_record.date,
            'remark': db_record.remark,
            'payment_method_id': db_record.payment_method_id,
            'project_id': db_record.project_id,
            'created_at': db_record.created_at,
            'updated_at': db_record.updated_at,
        }
    )


@router.put("/{record_id}", response_model=RecordDetailResponse, summary="更新记账")
async def update_record(
    record_id: int,
    record_update: RecordUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """更新记账"""
    record = db.query(Record).filter(
        Record.id == record_id,
        Record.user_id == current_user.id
    ).first()
    
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="记账记录不存在"
        )
    
    # 更新字段
    update_data = record_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(record, field, value)
    
    db.commit()
    db.refresh(record)
    
    # 如果项目有变化，更新项目总消费
    if record.project_id:
        from ..models import Project
        total = db.query(func.sum(Record.amount)).filter(
            Record.project_id == record.project_id
        ).scalar() or 0
        project = db.query(Project).filter(Project.id == record.project_id).first()
        if project:
            project.total_expense = total
            db.commit()
    
    return RecordDetailResponse(
        **{
            'id': record.id,
            'user_id': record.user_id,
            'type': record.type,
            'category_id': record.category_id,
            'category_item_id': record.category_item_id,
            'amount': record.amount,
            'date': record.date,
            'remark': record.remark,
            'payment_method_id': record.payment_method_id,
            'project_id': record.project_id,
            'created_at': record.created_at,
            'updated_at': record.updated_at,
        }
    )


@router.delete("/{record_id}", response_model=MessageResponse, summary="删除记账")
async def delete_record(
    record_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """删除记账"""
    record = db.query(Record).filter(
        Record.id == record_id,
        Record.user_id == current_user.id
    ).first()
    
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="记账记录不存在"
        )
    
    project_id = record.project_id
    
    db.delete(record)
    db.commit()
    
    # 更新项目总消费
    if project_id:
        from ..models import Project
        total = db.query(func.sum(Record.amount)).filter(
            Record.project_id == project_id
        ).scalar() or 0
        project = db.query(Project).filter(Project.id == project_id).first()
        if project:
            project.total_expense = total
            db.commit()
    
    return MessageResponse(message="删除成功")


@router.get("/stats/summary", response_model=RecordStatsResponse, summary="获取统计摘要")
async def get_stats_summary(
    start_date: Optional[datetime] = Query(None, description="开始日期"),
    end_date: Optional[datetime] = Query(None, description="结束日期"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取记账统计摘要"""
    # 总数
    total_count = db.query(func.count(Record.id)).filter(
        Record.user_id == current_user.id
    ).scalar()
    
    total_amount = db.query(func.sum(Record.amount)).filter(
        Record.user_id == current_user.id
    ).scalar() or 0
    
    # 收入
    income_count = db.query(func.count(Record.id)).filter(
        Record.user_id == current_user.id,
        Record.type == 'income'
    ).scalar()
    
    income_amount = db.query(func.sum(Record.amount)).filter(
        Record.user_id == current_user.id,
        Record.type == 'income'
    ).scalar() or 0
    
    # 支出
    expense_count = db.query(func.count(Record.id)).filter(
        Record.user_id == current_user.id,
        Record.type == 'expense'
    ).scalar()
    
    expense_amount = db.query(func.sum(Record.amount)).filter(
        Record.user_id == current_user.id,
        Record.type == 'expense'
    ).scalar() or 0
    
    return RecordStatsResponse(
        total_count=total_count,
        total_amount=total_amount,
        income_count=income_count,
        income_amount=income_amount,
        expense_count=expense_count,
        expense_amount=expense_amount
    )
