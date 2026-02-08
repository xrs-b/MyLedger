"""
管理路由
管理员功能 API
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from ..database import get_db
from ..models import User, Record, Category, CategoryItem, PaymentMethod, Project
from ..schemas.user import UserResponse, UserUpdate
from ..schemas.record import RecordResponse, RecordListResponse
from ..schemas.category import CategoryResponse, CategoryItemResponse, PaymentMethodResponse
from ..schemas.project import ProjectResponse
from .auth import get_current_user, get_current_admin

router = APIRouter(prefix="/api/v1/admin", tags=["管理"])


# ============ 用户管理 ============

@router.get("/users", response_model=List[UserResponse], summary="用户列表")
async def get_users(
    page: int = 1,
    page_size: int = 20,
    current_admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """获取所有用户列表"""
    users = db.query(User).order_by(User.created_at.desc()).offset((page-1)*page_size).limit(page_size).all()
    return users


@router.get("/users/count", summary="用户数量")
async def get_user_count(
    current_admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """获取用户总数"""
    return {"count": db.query(User).count()}


@router.put("/users/{user_id}", response_model=UserResponse, summary="更新用户")
async def update_user(
    user_id: int,
    user_update: UserUpdate,
    current_admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """更新用户信息"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    update_data = user_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(user, field, value)
    
    db.commit()
    db.refresh(user)
    return user


@router.delete("/users/{user_id}", summary="删除用户")
async def delete_user(
    user_id: int,
    current_admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """删除用户"""
    if user_id == current_admin.id:
        raise HTTPException(status_code=400, detail="不能删除自己")
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    db.delete(user)
    db.commit()
    return {"message": "删除成功"}


# ============ 记录管理 ============

@router.get("/records", response_model=RecordListResponse, summary="记录列表")
async def get_all_records(
    page: int = 1,
    page_size: int = 20,
    current_admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """获取所有用户的记录"""
    query = db.query(Record).order_by(Record.created_at.desc())
    total = query.count()
    records = query.offset((page-1)*page_size).limit(page_size).all()
    
    return {
        "records": records,
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": (total + page_size - 1) // page_size
    }


@router.delete("/records/{record_id}", summary="删除记录")
async def delete_record(
    record_id: int,
    current_admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """删除记录"""
    record = db.query(Record).filter(Record.id == record_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="记录不存在")
    
    db.delete(record)
    db.commit()
    return {"message": "删除成功"}


# ============ 分类管理 ============

@router.get("/categories", response_model=List[CategoryResponse], summary="分类列表")
async def get_all_categories(
    type: Optional[str] = None,
    current_admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """获取所有分类"""
    query = db.query(Category)
    if type:
        query = query.filter(Category.type == type)
    return query.order_by(Category.sort_order).all()


@router.post("/categories", response_model=CategoryResponse, summary="创建分类")
async def create_category(
    name: str,
    type: str,
    icon: Optional[str] = None,
    current_admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """创建新分类"""
    if db.query(Category).filter(Category.name == name, Category.type == type).first():
        raise HTTPException(status_code=400, detail="分类已存在")
    
    category = Category(name=name, type=type, icon=icon)
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


@router.put("/categories/{category_id}", response_model=CategoryResponse, summary="更新分类")
async def update_category(
    category_id: int,
    name: Optional[str] = None,
    icon: Optional[str] = None,
    current_admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """更新分类"""
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="分类不存在")
    
    if name:
        category.name = name
    if icon is not None:
        category.icon = icon
    
    db.commit()
    db.refresh(category)
    return category


@router.delete("/categories/{category_id}", summary="删除分类")
async def delete_category(
    category_id: int,
    current_admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """删除分类（级联删除二级分类）"""
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="分类不存在")
    
    db.delete(category)
    db.commit()
    return {"message": "删除成功"}


# ============ 二级分类管理 ============

@router.get("/category-items", response_model=List[CategoryItemResponse], summary="二级分类列表")
async def get_all_items(
    category_id: Optional[int] = None,
    current_admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """获取所有二级分类"""
    query = db.query(CategoryItem)
    if category_id:
        query = query.filter(CategoryItem.category_id == category_id)
    return query.order_by(CategoryItem.sort_order).all()


@router.post("/category-items", response_model=CategoryItemResponse, summary="创建二级分类")
async def create_category_item(
    category_id: int,
    name: str,
    current_admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """创建二级分类"""
    if not db.query(Category).filter(Category.id == category_id).first():
        raise HTTPException(status_code=400, detail="一级分类不存在")
    
    item = CategoryItem(category_id=category_id, name=name)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@router.delete("/category-items/{item_id}", summary="删除二级分类")
async def delete_category_item(
    item_id: int,
    current_admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """删除二级分类"""
    item = db.query(CategoryItem).filter(CategoryItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="二级分类不存在")
    
    db.delete(item)
    db.commit()
    return {"message": "删除成功"}


# ============ 支付方式管理 ============

@router.get("/payment-methods", response_model=List[PaymentMethodResponse], summary="支付方式列表")
async def get_all_payment_methods(
    current_admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """获取所有支付方式"""
    return db.query(PaymentMethod).order_by(PaymentMethod.sort_order).all()


@router.post("/payment-methods", response_model=PaymentMethodResponse, summary="创建支付方式")
async def create_payment_method(
    name: str,
    icon: Optional[str] = None,
    current_admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """创建支付方式"""
    if db.query(PaymentMethod).filter(PaymentMethod.name == name).first():
        raise HTTPException(status_code=400, detail="支付方式已存在")
    
    pm = PaymentMethod(name=name, icon=icon)
    db.add(pm)
    db.commit()
    db.refresh(pm)
    return pm


@router.delete("/payment-methods/{pm_id}", summary="删除支付方式")
async def delete_payment_method(
    pm_id: int,
    current_admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """删除支付方式"""
    pm = db.query(PaymentMethod).filter(PaymentMethod.id == pm_id).first()
    if not pm:
        raise HTTPException(status_code=404, detail="支付方式不存在")
    
    db.delete(pm)
    db.commit()
    return {"message": "删除成功"}


# ============ 项目管理 ============

@router.get("/projects", response_model=List[ProjectResponse], summary="项目列表")
async def get_all_projects(
    status: Optional[str] = None,
    page: int = 1,
    page_size: int = 20,
    current_admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """获取所有项目"""
    query = db.query(Project)
    if status:
        query = query.filter(Project.status == status)
    return query.order_by(Project.created_at.desc()).offset((page-1)*page_size).limit(page_size).all()


@router.delete("/projects/{project_id}", summary="删除项目")
async def delete_project(
    project_id: int,
    current_admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """删除项目"""
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="项目不存在")
    
    db.delete(project)
    db.commit()
    return {"message": "删除成功"}


# ============ 统计数据 ============

@router.get("/stats", summary="管理统计数据")
async def get_admin_stats(
    current_admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """获取管理统计数据"""
    return {
        "user_count": db.query(User).count(),
        "record_count": db.query(Record).count(),
        "project_count": db.query(Project).count(),
        "category_count": db.query(Category).count()
    }
