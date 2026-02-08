"""
分类路由
分类和二级分类的 CRUD API
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from ..models import Category, CategoryItem, PaymentMethod
from ..schemas.category import (
    CategoryCreate, CategoryUpdate, CategoryResponse,
    CategoryItemCreate, CategoryItemUpdate, CategoryItemResponse,
    PaymentMethodCreate, PaymentMethodUpdate, PaymentMethodResponse,
    CategoryWithItemsResponse, CategoriesListResponse, MessageResponse
)

router = APIRouter(prefix="/api/v1/categories", tags=["分类"])


# ============ 一级分类 API ============

@router.get("", response_model=CategoriesListResponse, summary="获取所有分类")
async def get_categories(db: Session = Depends(get_db)):
    """
    获取所有分类（支出+收入）
    包含二级分类
    """
    # 获取支出分类
    expense_categories = db.query(Category).filter(
        Category.type == 'expense'
    ).order_by(Category.sort_order).all()
    
    # 获取收入分类
    income_categories = db.query(Category).filter(
        Category.type == 'income'
    ).order_by(Category.sort_order).all()
    
    return {
        "expense": expense_categories,
        "income": income_categories
    }


@router.get("/list", response_model=List[CategoryResponse], summary="获取分类列表")
async def get_category_list(
    type: str = None,
    db: Session = Depends(get_db)
):
    """
    获取分类列表
    - type: 筛选类型 (expense/income)
    """
    query = db.query(Category)
    if type:
        query = query.filter(Category.type == type)
    return query.order_by(Category.sort_order).all()


@router.get("/{category_id}", response_model=CategoryWithItemsResponse, summary="获取分类详情")
async def get_category(category_id: int, db: Session = Depends(get_db)):
    """获取分类详情（包含所有二级分类）"""
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="分类不存在"
        )
    return category


@router.post("", response_model=CategoryResponse, summary="创建分类")
async def create_category(
    category: CategoryCreate,
    db: Session = Depends(get_db)
):
    """创建新分类"""
    # 检查名称是否已存在
    existing = db.query(Category).filter(
        Category.name == category.name,
        Category.type == category.type
    ).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="分类名称已存在"
        )
    
    db_category = Category(
        name=category.name,
        type=category.type,
        icon=category.icon,
        sort_order=category.sort_order
    )
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    
    return db_category


@router.put("/{category_id}", response_model=CategoryResponse, summary="更新分类")
async def update_category(
    category_id: int,
    category_update: CategoryUpdate,
    db: Session = Depends(get_db)
):
    """更新分类"""
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="分类不存在"
        )
    
    # 更新字段
    update_data = category_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(category, field, value)
    
    db.commit()
    db.refresh(category)
    
    return category


@router.delete("/{category_id}", response_model=MessageResponse, summary="删除分类")
async def delete_category(category_id: int, db: Session = Depends(get_db)):
    """删除分类（级联删除二级分类）"""
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="分类不存在"
        )
    
    db.delete(category)
    db.commit()
    
    return MessageResponse(message="删除成功")


# ============ 二级分类 API ============

@router.get("/items", response_model=List[CategoryItemResponse], summary="获取所有二级分类")
async def get_all_items(
    category_id: int = None,
    db: Session = Depends(get_db)
):
    """
    获取二级分类列表
    - category_id: 筛选一级分类
    """
    query = db.query(CategoryItem)
    if category_id:
        query = query.filter(CategoryItem.category_id == category_id)
    return query.order_by(CategoryItem.sort_order).all()


@router.get("/items/{item_id}", response_model=CategoryItemResponse, summary="获取二级分类详情")
async def get_item(item_id: int, db: Session = Depends(get_db)):
    """获取二级分类详情"""
    item = db.query(CategoryItem).filter(CategoryItem.id == item_id).first()
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="二级分类不存在"
        )
    return item


@router.post("/items", response_model=CategoryItemResponse, summary="创建二级分类")
async def create_item(
    item: CategoryItemCreate,
    db: Session = Depends(get_db)
):
    """创建二级分类"""
    # 检查分类是否存在
    category = db.query(Category).filter(Category.id == item.category_id).first()
    if not category:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="一级分类不存在"
        )
    
    db_item = CategoryItem(
        category_id=item.category_id,
        name=item.name,
        icon=item.icon,
        sort_order=item.sort_order
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    
    return db_item


@router.put("/items/{item_id}", response_model=CategoryItemResponse, summary="更新二级分类")
async def update_item(
    item_id: int,
    item_update: CategoryItemUpdate,
    db: Session = Depends(get_db)
):
    """更新二级分类"""
    item = db.query(CategoryItem).filter(CategoryItem.id == item_id).first()
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="二级分类不存在"
        )
    
    update_data = item_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(item, field, value)
    
    db.commit()
    db.refresh(item)
    
    return item


@router.delete("/items/{item_id}", response_model=MessageResponse, summary="删除二级分类")
async def delete_item(item_id: int, db: Session = Depends(get_db)):
    """删除二级分类"""
    item = db.query(CategoryItem).filter(CategoryItem.id == item_id).first()
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="二级分类不存在"
        )
    
    db.delete(item)
    db.commit()
    
    return MessageResponse(message="删除成功")


# ============ 支付方式 API ============

@router.get("/payment-methods", response_model=List[PaymentMethodResponse], summary="获取支付方式")
async def get_payment_methods(db: Session = Depends(get_db)):
    """获取所有支付方式"""
    return db.query(PaymentMethod).order_by(PaymentMethod.sort_order).all()


@router.post("/payment-methods", response_model=PaymentMethodResponse, summary="创建支付方式")
async def create_payment_method(
    pm: PaymentMethodCreate,
    db: Session = Depends(get_db)
):
    """创建支付方式"""
    existing = db.query(PaymentMethod).filter(PaymentMethod.name == pm.name).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="支付方式已存在"
        )
    
    db_pm = PaymentMethod(
        name=pm.name,
        icon=pm.icon,
        sort_order=pm.sort_order
    )
    db.add(db_pm)
    db.commit()
    db.refresh(db_pm)
    
    return db_pm


@router.put("/payment-methods/{pm_id}", response_model=PaymentMethodResponse, summary="更新支付方式")
async def update_payment_method(
    pm_id: int,
    pm_update: PaymentMethodUpdate,
    db: Session = Depends(get_db)
):
    """更新支付方式"""
    pm = db.query(PaymentMethod).filter(PaymentMethod.id == pm_id).first()
    if not pm:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="支付方式不存在"
        )
    
    update_data = pm_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(pm, field, value)
    
    db.commit()
    db.refresh(pm)
    
    return pm


@router.delete("/payment-methods/{pm_id}", response_model=MessageResponse, summary="删除支付方式")
async def delete_payment_method(pm_id: int, db: Session = Depends(get_db)):
    """删除支付方式"""
    pm = db.query(PaymentMethod).filter(PaymentMethod.id == pm_id).first()
    if not pm:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="支付方式不存在"
        )
    
    db.delete(pm)
    db.commit()
    
    return MessageResponse(message="删除成功")
