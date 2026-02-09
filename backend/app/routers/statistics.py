"""
统计路由
多维度统计 API
"""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, case
from typing import Optional, List
from datetime import datetime, timedelta
from decimal import Decimal

from ..database import get_db
from ..models import Record, User, Category, CategoryItem
from .auth import get_current_user

router = APIRouter(prefix="/api/v1/statistics", tags=["统计"])


def parse_date(date_str: str) -> Optional[datetime]:
    """解析日期字符串"""
    if not date_str:
        return None
    try:
        return datetime.strptime(date_str, '%Y-%m-%d')
    except:
        return None


@router.get("/summary", summary="获取统计摘要")
async def get_summary(
    start_date: Optional[str] = Query(None, description="开始日期 YYYY-MM-DD"),
    end_date: Optional[str] = Query(None, description="结束日期 YYYY-MM-DD"),
    category_id: Optional[int] = Query(None, description="一级分类ID"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    获取统计摘要
    - 按日期范围筛选
    - 按分类筛选
    - 包含日常记账 + 项目关联记账
    """
    # 构建查询
    query = db.query(
        func.count(Record.id).label('total_count'),
        func.sum(Record.amount).label('total_amount'),
        func.sum(case((Record.type == 'income', Record.amount), else_=0)).label('income_amount'),
        func.count(case((Record.type == 'income', Record.id))).label('income_count'),
        func.sum(case((Record.type == 'expense', Record.amount), else_=0)).label('expense_amount'),
        func.count(case((Record.type == 'expense', Record.id))).label('expense_count')
    ).filter(Record.user_id == current_user.id)
    
    # 日期筛选
    if start_date:
        start = parse_date(start_date)
        if start:
            query = query.filter(Record.date >= start)
    
    if end_date:
        end = parse_date(end_date)
        if end:
            end = end + timedelta(days=1)  # 包含结束日期当天
            query = query.filter(Record.date < end)
    
    # 分类筛选
    if category_id:
        query = query.filter(Record.category_id == category_id)
    
    result = query.first()
    
    return {
        "total_count": result.total_count or 0,
        "total_amount": float(result.total_amount) if result.total_amount else 0,
        "income_count": result.income_count or 0,
        "income_amount": float(result.income_amount) if result.income_amount else 0,
        "expense_count": result.expense_count or 0,
        "expense_amount": float(result.expense_amount) if result.expense_amount else 0,
        "net_amount": float(result.income_amount - result.expense_amount) if result.income_amount and result.expense_amount else float(result.income_amount or 0) - float(result.expense_amount or 0)
    }


@router.get("/by-category", summary="按分类统计")
async def get_by_category(
    start_date: Optional[str] = Query(None, description="开始日期"),
    end_date: Optional[str] = Query(None, description="结束日期"),
    record_type: Optional[str] = Query(None, alias="type", description="类型: income/expense"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    按分类统计
    - 返回一级分类汇总
    - 包含各分类的金额和占比
    """
    # 子查询：按分类汇总
    subquery = db.query(
        Record.category_id,
        func.sum(Record.amount).label('amount'),
        func.count(Record.id).label('count')
    ).filter(Record.user_id == current_user.id)
    
    # 日期筛选
    if start_date:
        start = parse_date(start_date)
        if start:
            subquery = subquery.filter(Record.date >= start)
    
    if end_date:
        end = parse_date(end_date)
        if end:
            end = end + timedelta(days=1)
            subquery = subquery.filter(Record.date < end)
    
    if record_type:
        subquery = subquery.filter(Record.type == record_type)
    
    subquery = subquery.group_by(Record.category_id).subquery()
    
    # 关联分类信息
    results = db.query(
        Category.id,
        Category.name,
        Category.icon,
        func.coalesce(subquery.c.amount, 0).label('amount'),
        func.coalesce(subquery.c.count, 0).label('count')
    ).outerjoin(subquery, Category.id == subquery.c.category_id).all()
    
    # 计算总数
    total_amount = sum(float(r.amount) for r in results if r.amount) or 1
    
    # 构建响应
    categories = []
    for r in results:
        amount = float(r.amount) if r.amount else 0
        categories.append({
            "id": r.id,
            "name": r.name,
            "icon": r.icon,
            "amount": amount,
            "count": r.count,
            "percentage": round(amount / total_amount * 100, 2) if total_amount > 0 else 0
        })
    
    # 按金额排序
    categories.sort(key=lambda x: x['amount'], reverse=True)
    
    return {
        "categories": categories,
        "total_amount": total_amount,
        "total_count": sum(c['count'] for c in categories)
    }


@router.get("/by-day", summary="按日统计")
async def get_by_day(
    start_date: Optional[str] = Query(None, description="开始日期"),
    end_date: Optional[str] = Query(None, description="结束日期"),
    record_type: Optional[str] = Query(None, alias="type", description="类型"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    按日统计
    - 返回每日收支汇总
    - 用于折线图
    """
    # 按日期分组查询
    query = db.query(
        func.date(Record.date).label('date'),
        func.sum(case((Record.type == 'income', Record.amount), else_=0)).label('income'),
        func.sum(case((Record.type == 'expense', Record.amount), else_=0)).label('expense')
    ).filter(Record.user_id == current_user.id)
    
    # 日期筛选
    if start_date:
        start = parse_date(start_date)
        if start:
            query = query.filter(Record.date >= start)
    
    if end_date:
        end = parse_date(end_date)
        if end:
            end = end + timedelta(days=1)
            query = query.filter(Record.date < end)
    
    if record_type:
        query = query.filter(Record.type == record_type)
    
    query = query.group_by(func.date(Record.date)).order_by(func.date(Record.date))
    
    results = query.all()
    
    # 构建响应
    daily_data = []
    for r in results:
        daily_data.append({
            "date": r.date,
            "income": float(r.income) if r.income else 0,
            "expense": float(r.expense) if r.expense else 0,
            "net": float((r.income or 0) - (r.expense or 0))
        })
    
    return {
        "data": daily_data,
        "start_date": start_date,
        "end_date": end_date
    }


@router.get("/by-project", summary="按项目统计")
async def get_by_project(
    start_date: Optional[str] = Query(None, description="开始日期"),
    end_date: Optional[str] = Query(None, description="结束日期"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    按项目统计
    - 返回项目消费汇总
    """
    # 查询有项目关联的记录
    query = db.query(
        Record.project_id,
        func.sum(Record.amount).label('total')
    ).filter(
        Record.user_id == current_user.id,
        Record.project_id.isnot(None)
    )
    
    # 日期筛选
    if start_date:
        start = parse_date(start_date)
        if start:
            query = query.filter(Record.date >= start)
    
    if end_date:
        end = parse_date(end_date)
        if end:
            end = end + timedelta(days=1)
            query = query.filter(Record.date < end)
    
    query = query.group_by(Record.project_id)
    results = query.all()
    
    # 获取项目信息
    project_data = []
    for r in results:
        from ..models import Project
        project = db.query(Project).filter(Project.id == r.project_id).first()
        if project:
            project_data.append({
                "project_id": r.project_id,
                "project_title": project.title,
                "total": float(r.total),
                "status": project.status
            })
    
    return {
        "projects": project_data,
        "total": sum(p['total'] for p in project_data)
    }


@router.get("/trend", summary="趋势分析")
async def get_trend(
    period: str = Query("month", description="周期: day/week/month"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    趋势分析
    - 按周期聚合数据
    - 用于对比分析
    """
    # 获取最近的数据
    from datetime import datetime, timedelta
    
    if period == "day":
        days = 30
        date_format = "%Y-%m-%d"
    elif period == "week":
        days = 90
        date_format = "%Y-W%V"
    else:  # month
        days = 365
        date_format = "%Y-%m"
    
    start_date = datetime.utcnow() - timedelta(days=days)
    
    # 按周期分组查询
    if period == "day":
        date_trunc = func.date(Record.date)
    elif period == "week":
        date_trunc = func.strftime("%Y-W%W", Record.date)
    else:  # month
        date_trunc = func.strftime("%Y-%m", Record.date)
    
    query = db.query(
        date_trunc.label('period'),
        func.sum(case((Record.type == 'income', Record.amount), else_=0)).label('income'),
        func.sum(case((Record.type == 'expense', Record.amount), else_=0)).label('expense')
    ).filter(
        Record.user_id == current_user.id,
        Record.date >= start_date
    ).group_by(date_trunc).order_by(date_trunc)
    
    results = query.all()
    
    trend_data = []
    for r in results:
        trend_data.append({
            "period": r.period,
            "income": float(r.income) if r.income else 0,
            "expense": float(r.expense) if r.expense else 0,
            "net": float((r.income or 0) - (r.expense or 0))
        })
    
    return {
        "data": trend_data,
        "period": period
    }
